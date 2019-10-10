import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

# [, , , , , , , , , , , , , ]

y_mine_naive = [0.50471, 0.44695, 0.426873, 0.421004, 0.40973, 0.384247, 0.392124, 0.375907, 0.410502, 0.364788, 0.380541, 0.382548, 0.366178, 0.388417]

y_mine_advanced = [1, 0.959846, 0.930347, 0.95861, 0.941776, 0.928803, 0.938976, 0.9461, 0.939923, 0.90749, 0.931274, 0.919537, 0.940232, 0.938996]

y_netal = [1, 0.999537, 0.998456, 0.986873, 0.993514, 0.901776, 0.988726, 0.982085, 0.981004, 0.95444, 0.977143, 0.972664, 0.956757, 0.963243]

y_hubalign = []

y_isorank = []

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))

plt.title("Web edu network")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.legend()

plt.show()
