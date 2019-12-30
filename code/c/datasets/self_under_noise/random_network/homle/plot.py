import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]

y_mine_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

y_mine_advanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

y_netal = [1, 1, 1, 1, 1, 1, 1, 1, 0.909224, 1, 1, 0.913104]

y_hubalign = [1, 0.523792, 0.485359, 0.456076, 0.777452, 0.828331, 0.393119, 0.897145, 0.793192, 0.457906, 0.393851, 0.863836]

y_iso = [1, 0.337628, 0.136896, 0.130307, 0.118594, 0.127379, 0.137994, 0.127745, 0.125549, 0.142753, 0.129209]

y_natali = [0.7829374, 0.6328374, 0.3829374, 0.3029384, 0.1503949]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))
plt.title("Holme and Kim powerlaw degree network")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plt.plot(x, y_iso, 'o--', label='IsoRank')
plt.legend()

plt.show()
