import matplotlib.pyplot as plt
from matplotlib import rc


font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 10}

plt.rc('font', **font)

x = [2814, 4911, 15926, 19148, 19420, 24224, 26695, 30898]
y_naive = [1.04, 3.242, 33.322, 34.538, 46.429, 48.664, 66.32, 52.644]
y_seed = [1.96, 5.32, 69.42, 70.91, 91.17, 100.87, 130.78, 137.741]

plt.ylabel("Running time (s)", **font)
plt.ylim((0, 150))

plt.title("")

plt.plot(x, y_naive, 'o--', label='Naive alignment')
plt.plot(x, y_seed, '*--', label='Seed alignment')

plt.legend()

plt.show()
