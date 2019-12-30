import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

# [, , , , , , , , , , , , , ]

y_mine_naive = [1, 1, 1, 1, 1, 0.999601, 1, 0.999468, 0.999068, 0.999468, 0.998669, 0.999601, 0.996806, 0.990417]

y_mine_advanced = [1, 1, 1, 1, 1, 0.999601, 1, 1, 1, 1, 1, 0.999867, 1, 0.999601]

y_netal = [1, 0.964195, 0.931053, 0.911087, 0.929189, 0.921203, 0.921869, 0.927725, 0.87129, 0.899108, 0.900439, 0.869559, 0.860109, 0.882337]

y_hubalign = [1, 0.941169, 0.906961, 0.900972, 0.857314, 0.864768, 0.816585, 0.868761, 0.702516, 0.705976, 0.639691, 0.814721, 0.823639, 0.731532]

y_iso = [1, 0.664537, 0.503298, 0.358445, 0.363769, 0.335951, 0.316252, 0.31918, 0.321872, 0.3019283, 0.2938371, 0.30291823, 0.3192833, 0.3011283]

y_natalie = []

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))

plt.title("Economic network")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plt.plot(x, y_iso, 'o--', label='IsoRank')
plt.legend()

plt.show()
