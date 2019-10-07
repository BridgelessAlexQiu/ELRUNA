import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

y_mine_naive = [0.996458, 0.994758, 0.994758, 0.992492, 0.994617, 0.9915, 0.9898, 0.987109, 0.986542, 0.983142, 0.983142, 0.975492, 0.969684, 0.969259]

y_mine_advanced = [1, 0.999575, 0.998583, 0.997025, 0.997592, 0.995467, 0.994333, 0.993625, 0.992917, 0.991642, 0.990084, 0.984842, 0.982717, 0.9813]

y_netal = [, , , , , , , , , , , , , ]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))
plt.title("Retweet networks")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.legend()
plt.show()