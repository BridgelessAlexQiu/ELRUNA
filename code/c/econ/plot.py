import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_mine = [1, 1, 1, 1, 1, 0.999601, 0.999734, 0.999468,  0.999068, 0.999468, 0.998403, 0.999601, 0.996406, 0.989751]
y_netal = [1, 0.964195, 0.931053, 0.911087, 0.929189, 0.921203, 0.921869, 0.927725, 0.87129, 0.899108, 0.900439, 0.869559, 0.860109, 0.882337]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))

plt.title(" Economic network, n = 1.3k, m = 7.6k")

plt.plot(x, y_mine, 'o--', label='Our')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.legend()

plt.show()