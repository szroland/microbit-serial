from serial import *
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque

s = Serial('COM6', baudrate=115200)

# Initialize the figure and axis for plotting
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()
x_data = []  # List to hold the x-axis data (e.g., time or index)
gyalogos_data = []  # List to hold the x-axis data (e.g., time or index)
y_data = []  # List to hold the y-axis data (values received from the serial port)
window_size = 10  # Size of the moving window for average calculation
window = deque(maxlen=window_size)  # Deque to store last `window_size` values

x_data.append(0)
gyalogos_data.append(0)
y_data.append(0)


# Function to calculate the moving average
def moving_average(values, window_size):
    return np.mean(values) if len(values) == window_size else np.nan


index = 1  # Counter for x-axis (could be time or index)
try:
    while True:
        # Read a line of data from the serial port (blocking)
        line = s.readline()
        if line:
            # Decode the byte data to string and strip any trailing newline/space
            decoded_line = line.decode('utf-8').strip()
            print(f"Line: {decoded_line}")

            try:
                # Convert the received data to a float (you can change this if the data is of different type)
                n = list(map(int, decoded_line.split(",")))
            except ValueError as e:
#                //print(e)
                continue  # Skip if the data is not a valid number

            if len(n) == 2:
                if (n[0] == 0 and n[1]==0) or (n[0] >= y_data[index-1] and n[1] >= gyalogos_data[index-1]):
                    print(f"Jo adat: {n}")
                    x_data.append(index)
                    y_data.append(n[0])
                    gyalogos_data.append(n[1])

                    index += 1

                    x_data = x_data[-100:]
                    y_data = y_data[-100:]
                else:
                    print(f"Rossz adat: {n}")

            # Update the plot
            ax.clear()  # Clear the previous plot
            ax.plot(x_data, y_data, label="Forgalom", color='blue')
            ax.plot(x_data, gyalogos_data, label="Gyalogos", color='red', linestyle='--')
            ax.set_xlabel('Idő (s)')
            ax.set_ylabel('Darab')
            ax.set_title('Forgalom számláló rendszer')
            ax.legend()
            plt.draw()  # Redraw the plot
            plt.pause(0.1)  # Pause to update the plot and allow interaction

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    s.close()  # Close the serial connection
    plt.ioff()  # Turn off interactive mode
    plt.show()  # Display the final plot