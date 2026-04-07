import matplotlib.pyplot as plt

# FPS test values for each bus
bus1 = [0.73, 1.41, 1.66, 1.83, 1.19, 1.38, 0.99]
bus2 = [0.95, 1.00, 0.99, 0.93, 0.97, 0.89, 1.01]
bus3 = [0.94, 1.64, 1.39, 1.96, 1.35, 1.43, 1.38, 0.98]

# X-axis: test instance number
x_bus1 = list(range(1, len(bus1)+1))
x_bus2 = list(range(1, len(bus2)+1))
x_bus3 = list(range(1, len(bus3)+1))

plt.figure(figsize=(8,5))

# Plot each bus
plt.plot(x_bus1, bus1, marker='o', label="Bus 1")
plt.plot(x_bus2, bus2, marker='s', label="Bus 2")
plt.plot(x_bus3, bus3, marker='^', label="Bus 3")

plt.xlabel("Test Instance")
plt.ylabel("FPS / Speed Value")
plt.title("FPS/Speed Test Values for All Buses")
plt.legend()
plt.grid(True)

plt.savefig("fps_speed_all_buses.png")
plt.show()