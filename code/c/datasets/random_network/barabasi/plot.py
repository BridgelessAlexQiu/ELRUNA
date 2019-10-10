import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
y_mine_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

y_mine_advanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

y_netal = [1, 1, 1, 1, 1, 1, 0.962196, 0.865503,  0.794984,  0.784806, 0.797528,  0.796438]

y_hubalign = [1, 0.501636, 0.414395, 0.682661, 0.359869, 0.686659, 0.396947, 0.594693, 0.374773, 0.370774, 0.380225]

y_iso = [1, 0.447219, 0.11305, 0.119229, 0.11414, 0.118502, 0.10578, 0.111232, 0.109778, 0.110142, 0.102508, 0.0999636]

y_natali = [0.615673, 0.39549255, 0.28102508,  0.18395493, 0.12395493]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))
plt.title("Barabasi-Albert preferential attachment network")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plot.plot(x, y_iso, 'o--', label='IsoRank')
plt.legend()
plt.show()
