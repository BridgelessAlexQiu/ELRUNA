import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

y_mine_naive = [0.991247, 0.989059, 0.991247, 0.986871, 0.989059, 0.996718, 0.989059, 0.991247, 0.992341, 0.980306, 0.947484, 0.960613, 0.937637, 0.945295]

y_mine_advanced = [1, 1, 0.997812, 0.998906, 0.997812, 0.997812, 0.998906, 0.998906, 0.996718, 0.995624, 0.982495, 0.987965, 0.973742, 0.961707]

y_netal = [1, 0.967177, 0.992341, 0.982495, 0.99453, 0.962801, 0.921225, 0.835886, 0.954048, 0.868709, 0.859956, 0.917943, 0.88512, 0.81291]

y_hubalign = [0.771335, 0.69256, 0.675055, 0.588621, 0.567834, 0.646608, 0.564551, 0.538293, 0.575492, 0.625821, 0.521882, 0.595186, 0.554705, 0.586433]

y_isorank = [1, 0.2374937, 0.13982384, 0.123706, 0.130098, 0.132798, 0.112937, 0.10839475, 0.1087364, 0.102934, 0.1209836, 0.1293846, 0.11929384, 0.0928273]

y_natali = [0.6751859956, 0.6021881838, 0.5070021882, 0.3971553611, 0.306345733, 0.2636761488]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))
plt.title("Newman coauthor networks")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.plot(x, y_hubalign, 'o--', label='HubAlign')
plt.plot(x, y_isorank, 'o--', label='IsoRank')
plt.legend()
plt.show()
