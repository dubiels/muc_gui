import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from scipy.signal import savgol_filter

# ===== USER SETTINGS =====
SERIAL_PORT = '\dev\tty.Bluetooth-Incoming-Port-'        
BAUD_RATE = 9600
MAX_DATA_POINTS = 100       # Number of points on plot

# Filter toggles
USE_MOVING_AVG = True
USE_EXP_MOVING_AVG = False
USE_SAVGOL_FILTER = False

# Filter parameters
MOVING_AVG_WINDOW = 5
EXP_MOVING_AVG_ALPHA = 0.3
SAVGOL_WINDOW = 7            # Must be odd and <= MAX_DATA_POINTS
SAVGOL_POLYORDER = 2
# ==========================

# Initialize serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Buffers
time_data = []
pressure_data = []
start_time = time.time()

# Plot setup
plt.style.use('ggplot')
fig, ax = plt.subplots()
raw_line, = ax.plot([], [], 'r--', label='Raw Data', alpha=0.4)
filtered_line, = ax.plot([], [], 'b-', label='Filtered Data')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Pressure")
ax.set_title("Real-Time Pressure with Filters")
ax.legend()

def apply_filters(data):
    data_np = np.array(data)

    if USE_MOVING_AVG and len(data_np) >= MOVING_AVG_WINDOW:
        data_np = np.convolve(data_np, np.ones(MOVING_AVG_WINDOW)/MOVING_AVG_WINDOW, mode='same')

    if USE_EXP_MOVING_AVG:
        ema = np.zeros_like(data_np)
        ema[0] = data_np[0]
        for i in range(1, len(data_np)):
            ema[i] = EXP_MOVING_AVG_ALPHA * data_np[i] + (1 - EXP_MOVING_AVG_ALPHA) * ema[i-1]
        data_np = ema

    if USE_SAVGOL_FILTER and len(data_np) >= SAVGOL_WINDOW:
        try:
            data_np = savgol_filter(data_np, SAVGOL_WINDOW, SAVGOL_POLYORDER)
        except Exception as e:
            print(f"Savitzky-Golay filter error: {e}")

    return data_np

def update(frame):
    global start_time

    try:
        raw_line_str = ser.readline().decode('utf-8').strip()
        if raw_line_str:
            pressure = float(raw_line_str)
            current_time = round(time.time() - start_time, 2)

            time_data.append(current_time)
            pressure_data.append(pressure)

            if len(time_data) > MAX_DATA_POINTS:
                time_data.pop(0)
                pressure_data.pop(0)

            filtered_data = apply_filters(pressure_data)

            raw_line.set_data(time_data, pressure_data)
            filtered_line.set_data(time_data, filtered_data)

            ax.relim()
            ax.autoscale_view()
    except Exception as e:
        print(f"Data read error: {e}")

    return raw_line, filtered_line

ani = FuncAnimation(fig, update, interval=100)
plt.tight_layout()
plt.show()

ser.close()
