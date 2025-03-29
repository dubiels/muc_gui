import csv
import random

# File name for the generated data
FILENAME = "pressure_data.csv"

# Number of data points
NUM_SAMPLES = 100
TIME_STEP = 0.1  # Simulating 0.1s interval between samples

# Generate sample data
with open(FILENAME, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Pressure (units)"])  # CSV Header

    for i in range(NUM_SAMPLES):
        timestamp = round(i * TIME_STEP, 2)  # Incrementing time
        pressure = random.randint(300, 700)  # Simulated sensor values
        writer.writerow([timestamp, pressure])

print(f"Sample pressure data saved to {FILENAME}")