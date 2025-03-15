import serial
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('TkAgg')

# Set up the serial connection
serial_port = 'COM4'  # Replace with your actual serial port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux/Mac)
baud_rate = 9600      # Set the baud rate as per your device
ser = serial.Serial(serial_port, baud_rate)

# Set up the plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(0, 1023)  # Adjust this based on your sensor's data range
plt.xlim(0, 100)

# Initial data
data = np.zeros(100)
line, = ax.plot(data, color='b')  # Ensure 'line' is the plot object, keep it a single line with a color

# Enable grid and put it on top of the plot
ax.grid(True, zorder=5)

ax.set_xlabel('Time')
ax.set_ylabel('Data')
ax.set_title('Real-time Data')
ax.legend(['Data'], loc='upper right')

# Variable to store the numerical value text (next to the title)
value_text = ax.text(0.7,1.09, 'Latest Value: 0', transform=ax.transAxes, 
                     fontsize=15, color='red', ha='left', va='top')

# Function to read and process serial data line by line
def read_serial_data():
    global data  # Declare data as global so we can modify it inside the function
    
    while True:
        if ser.in_waiting > 0:  # Check if there's data available to read
            line_data = ser.readline().decode('utf-8').strip()  # Read a line from serial, decode and strip newline
            try:
                # Convert the line to an integer
                number = int(line_data)
                
                # Append the new data point to the array
                data = np.append(data, number)

                # Keep only the last 100 data points
                if len(data) > 100:
                    data = data[-100:]

                # Update the plot with the new data
                line.set_ydata(data)
                line.set_xdata(np.arange(len(data)))

                # Update the numerical value next to the title
                value_text.set_text(f'Latest Value: {number}')  # Update the numerical value inside the plot

                # Redraw the plot
                plt.draw()
                plt.pause(0.05)  # Pause to allow the plot to update

            except ValueError:
                print(f"Received invalid data: {line_data}")  # Handle invalid data

# Start reading serial data
read_serial_data()
