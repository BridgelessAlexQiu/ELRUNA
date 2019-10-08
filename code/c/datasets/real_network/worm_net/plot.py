import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

y_mine_naive = [0.995385, 0.998462, 0.996154, 0.996154, 0.996923, 0.988462, 0.990769, 0.979231, 0.981538, 0.978462, 0.948462, 0.960769, 0.907692, 0.930769]

y_mine_advanced = [1, 1, 0.997692, 0.999231, 0.999231, 0.997692, 0.991538, 0.991538, 0.989231, 0.989231, 0.974615, 0.976154, 0.963846, 0.960769]

y_netal = [1, 0.991538, 0.960769, 0.899231, 0.892308, 0.865385, 0.87, 0.815385, 0.808462, 0.763846, 0.753846,  0.730769, 0.733846, 0.682308]

y_hubalign = [1, 0.813846, 0.606154, 0.55, 0.548462, 0.481538, 0.506154, 0.470769, 0.479231, 0.485385, 0.474615, 0.480769, 0.508462, 0.519231]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))
plt.title("Gene functional associations networks")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.legend()
plt.show()