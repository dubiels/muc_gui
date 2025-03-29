import csv
import matplotlib.pyplot as plt

# Prompt user for CSV file name
filename = input("Enter the CSV filename (including .csv): ")

# Lists to store time and pressure data
time_values = []
pressure_values = []

# Read the CSV file
try:
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            time_values.append(float(row[0]))  # Time in seconds
            pressure_values.append(float(row[1]))  # Pressure values
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    exit()

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(time_values, pressure_values, marker="o", linestyle="-", color="b", label="Pressure Data")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (units)")
plt.title("Pressure vs. Time")
plt.legend()
plt.grid(True)
plt.show()
