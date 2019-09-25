import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_mine = [0.995385, 1, 0.995385, 0.996923, 0.996923, 0.986923, 0.975385, 0.981538, 0.979231, 0.970769, 0.956923, 0.940769, 0.919231, 0.934615]
y_netal = [1, 0.991538, 0.960769, 0.899231, 0.892308, 0.865385, 0.87, 0.815385, 0.808462, 0.763846, 0.753846,  0.730769, 0.733846, 0.682308]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))
plt.title("Gene functional associations networks, n = 1.4k, m = 1.6k")

plt.plot(x, y_mine, 'o--', label='Our')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.legend()
plt.show()