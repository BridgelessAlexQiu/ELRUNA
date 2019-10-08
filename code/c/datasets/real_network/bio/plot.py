import matplotlib.pyplot as plt

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]

# [, , , , , , , , , , , , , ]

y_mine_naive = [1, 1, 0.999562, 0.99737, 0.996931, 0.993643, 0.99189, 0.973915, 0.964051, 0.971285, 0.952652, 0.945199, 0.922402, 0.878343]

y_mine_advanced = [1, 1, 1, 0.997808, 0.99737, 0.99715, 0.996274, 0.99167, 0.982025, 0.987944, 0.98071, 0.978299, 0.971723, 0.95594]

y_netal = [, , , , , , , , , , , , , ]

y_hubalign = [, , , , , , , , , , , , , ]

plt.xlabel("Noise level")
plt.ylabel("EC")
plt.ylim((0, 1.1))

plt.title("Economic network")

plt.plot(x, y_mine_naive, 'o--', label='Naive_alignment')
plt.plot(x, y_mine_advanced, 'o--', label='Seed_alignment')
plt.plot(x, y_netal, 'o--', label='NETAL')
plt.legend()

plt.show()