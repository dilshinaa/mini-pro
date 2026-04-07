import matplotlib.pyplot as plt

# Brightness levels
brightness_levels = ["Dark", "Normal", "Bright"]

# Accuracy values (%)
accuracy_bus1 = [42.86, 71.43, 57.14]
accuracy_bus2 = [75.0, 75.0, 87.5]
accuracy_bus3 = [50.0, 75.0, 75.0]

plt.figure(figsize=(8,5))

# Plot each bus
plt.plot(brightness_levels, accuracy_bus1, marker='o', label="Bus 1")
plt.plot(brightness_levels, accuracy_bus2, marker='s', label="Bus 2")
plt.plot(brightness_levels, accuracy_bus3, marker='^', label="Bus 3")

plt.xlabel("Brightness Level")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy vs Brightness Level for All Buses")
plt.ylim(0, 100)  # optional: to show full % range
plt.legend()
plt.grid(True)

plt.savefig("brightness_accuracy_all_buses.png")
plt.show()