import matplotlib.pyplot as plt

# Noise levels
noise_levels = [0, 5, 10, 25, 50, 65, 80]

# Accuracy values (%)
accuracy_bus1 = [71.43, 71.43, 71.43, 57.14, 57.14, 42.86, 28.57]
accuracy_bus2 = [75.0, 75.0, 75.0, 87.5, 62.5, 37.5, 12.5]
accuracy_bus3 = [75.0, 75.0, 66.67, 58.33, 33.33, 8.33, 0.0]

plt.figure(figsize=(8,5))

# Plot each bus
plt.plot(noise_levels, accuracy_bus1, marker='o', label="Bus 1")
plt.plot(noise_levels, accuracy_bus2, marker='s', label="Bus 2")
plt.plot(noise_levels, accuracy_bus3, marker='^', label="Bus 3")

plt.xlabel("Noise Level")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy vs Noise Level for All Buses")
plt.ylim(0, 100)
plt.legend()
plt.grid(True)

plt.savefig("noise_accuracy_all_buses.png")
plt.show()