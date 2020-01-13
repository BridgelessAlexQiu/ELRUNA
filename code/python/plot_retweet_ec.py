import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "retweet"
ylabel = "Edge Correctness"
plot_name = "retweet_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.996458, 0.994758, 0.994758, 0.992492, 0.994617, 0.9915, 0.9898, 0.987109, 0.986542, 0.983142, 0.983142, 0.975492, 0.969684, 0.969259, ]
y_seed = [1, 0.999717, 0.998442, 0.997308, 0.997592, 0.995467, 0.994192, 0.9932, 0.992209, 0.991642, 0.9898, 0.984559, 0.982292, 0.980309, ]
y_netal = [1, 0.835104, 0.641734, 0.620909, 0.689333, 0.528262, 0.518345, 0.525004, 0.527553, 0.490863, 0.47868, 0.472872, 0.477405, 0.486896, ]
y_isorank = [0.995042, 0.512679, 0.358124, 0.270152, 0.240827, 0.208811, 0.196628, 0.171271, 0.131747, 0.142513, 0.115455, 0.106672, 0.112056, 0.105256, ]
y_hubalign = [1, 0.975209, 0.798697, 0.789347, 0.736365, 0.735515, 0.682108, 0.701374, 0.723049, 0.716107, 0.701232, 0.706757, 0.693158, 0.689899, ]
y_modulealign = [1, 0.985209, 0.818697, 0.809347, 0.756365, 0.75515, 0.692108, 0.71374, 0.73049, 0.706107, 0.71232, 0.726757, 0.703158, 0.69899, ]
y_cgraal = [0.638051, 0.242952, 0.317892, 0.276385, 0.289843, 0.281343, 0.288568, 0.41394, 0.25556, 0.334892, 0.254144, 0.282335, 0.250035, 0.275535, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.186287, 0.176229, 0.175096, 0.166313, 0.158804, 0.159229, 0.160646, 0.150163, 0.142513, 0.135713, 0.128772, 0.136988, 0.124805, 0.134297, ]
y_klau = [0.197053, 0.195495, 0.189545, 0.177362, 0.177221, 0.173821, 0.171271, 0.167021, 0.163338, 0.155829, 0.155121, 0.153138, 0.15073, 0.15158, ]


cmap = ListedColormap(sns.color_palette("colorblind", 10))
markersize = 4
style = {
        'RuleAlign_naive':  {'color': cmap(0), 'marker': 'o', 'linestyle': '--', 'markersize': markersize},
        'RuleAlign_seed':   {'color': cmap(1), 'marker': '*', 'linestyle': '--', 'markersize': markersize},
        'NETAL':            {'color': cmap(2), 'marker': 's', 'linestyle': '--', 'markersize': markersize},
        'IsoRank':          {'color': cmap(4), 'marker': 'h', 'linestyle': '--', 'markersize': markersize},
        'HubAlign':         {'color': cmap(3), 'marker': 'd', 'linestyle': '--', 'markersize': markersize},
        'ModuleAlign':      {'color': cmap(5), 'marker': '.', 'linestyle': '--', 'markersize': markersize},
        'C-GRAAL':          {'color': cmap(6), 'marker': '>', 'linestyle': '--', 'markersize': markersize},
        'EigaenAlign':       {'color': cmap(7), 'marker': '<', 'linestyle': '--', 'markersize': markersize},
        "NetAlign":         {'color': cmap(8), 'marker': 'x', 'linestyle': '--', 'markersize': markersize},
        "Klau":             {'color': cmap(9), 'marker': 'X', 'linestyle': '--', 'markersize': markersize},
        }

nrows = 1
f, ax = plt.subplots(nrows, 1)

ax.set_title(title)
ax.set_ylabel(ylabel)
ax.set_yticks(np.arange(0, 1.1, step=0.25))
ax.plot(x, y_naive, **style['RuleAlign_naive'])
ax.plot(x, y_seed, **style['RuleAlign_seed'])
ax.plot(x, y_netal, **style['NETAL'])
ax.plot(x, y_isorank, **style['IsoRank'])
ax.plot(x, y_hubalign, **style['HubAlign'])
ax.plot(x, y_modulealign, **style['ModuleAlign'])
ax.plot(x, y_cgraal, **style['C-GRAAL'])
ax.plot(x, y_eigenalign, **style['EigaenAlign'])
ax.plot(x, y_netalign, **style['NetAlign'])
ax.plot(x, y_klau, **style['Klau'])

from matplotlib.lines import Line2D
legend_elem = [Line2D([0], [0], label=method, **kwargs) for method, kwargs in style.items()]
f.legend(handles=legend_elem, loc='lower center', ncol=2)

f.subplots_adjust(bottom=0.90, left=.175, right=1.0, top=.94)

plt.tight_layout()
f.subplots_adjust(bottom=0.24, hspace=0.6, wspace=0.35, right=0.9)
plt.show()
plt.savefig('plots/' + network_type + "/" + plot_name)
