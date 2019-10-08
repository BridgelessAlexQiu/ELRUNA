import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

# [, , , , , , , , , , , , , ]

y_mine_naive = [0.50471, 0.44695, 0.426873, 0.421004, 0.40973, 0.384247, 0.392124]

y_mine_advanced = [1, 0.959846, 0.930347, 0.95861, 0.941776, 0.928803, 0.392124]

y_netal = []

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
