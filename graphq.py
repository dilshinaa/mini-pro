import matplotlib.pyplot as plt

# Quality levels
quality_levels = ["Q100", "Q80", "Q60", "Q40", "Q20"]

# Test values for each bus
bus1 = [5, 4, 4, 4, 2]
bus2 = [6, 5, 4, 5, 4]
bus3 = [9, 8, 8, 7, 4]

plt.figure(figsize=(8,5))

# Plot each bus
plt.plot(quality_levels, bus1, marker='o', label="Bus 1")
plt.plot(quality_levels, bus2, marker='s', label="Bus 2")
plt.plot(quality_levels, bus3, marker='^', label="Bus 3")

plt.xlabel("Quality Level")
plt.ylabel("Accuracy")
plt.title("Accuracyvs Video Quality for All Buses")
plt.legend()
plt.grid(True)

plt.savefig("quality_test_all_buses.png")
plt.show()