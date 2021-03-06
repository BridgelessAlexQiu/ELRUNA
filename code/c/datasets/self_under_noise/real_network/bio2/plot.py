import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

# [, , , , , , , , , , , , , ]

y_mine_naive = [1, 1, 0.999562, 0.99737, 0.996931, 0.993643, 0.99189, 0.973915, 0.964051, 0.971285, 0.952652, 0.945199, 0.922402, 0.878343]

y_mine_advanced = [1, 1, 1, 0.997808, 0.99737, 0.99715, 0.996274, 0.99167, 0.982025, 0.987944, 0.98071, 0.978299, 0.971723, 0.95594]

y_netal = [1, 0.954844, 0.872863, 0.86541, 0.814117, 0.723367, 0.70868, 0.673389, 0.638097, 0.613985, 0.651907, 0.604559, 0.592722, 0.595791]

y_hubalign = [1, 0.598203, 0.504822, 0.466243, 0.428321, 0.435774, 0.442131, 0.42021, 0.437308, 0.432924, 0.452652, 0.423937, 0.45331, 0.448049]

y_iso = [0.999562, 0.462723, 0.2839484, 0.1592834, 0.1592834, 0.138293, 0.1389328, 0.0934323, 0.079423, 0.0724923, 0.050923, 0.079238, 0.07237932, 0.0628483]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))

plt.title("Bio network")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plt.plot(x, y_iso, 'o--', label='IsoRank')
plt.legend()

plt.show()
