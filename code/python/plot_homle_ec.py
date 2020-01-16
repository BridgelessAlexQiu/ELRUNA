import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "homle"
ylabel = "Edge Correctness"
plot_name = "homle_ec_plot.pdf"
network_type = "random_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
y_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
y_seed = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
y_netal = [1, 1, 1, 1, 1, 1, 1, 1, 0.909224, 1, 1, 0.905198]
y_isorank = [1, 0.211567, 0.160322, 0.14019, 0.148609, 0.140556, 0.131772, 0.133968, 0.128477, 0.132504, 0.139458, 0.13104]
y_hubalign = [1, 0.523792, 0.485359, 0.456076, 0.777452, 0.828331, 0.393119, 0.897145, 0.793192, 0.457906, 0.393851, 0.863836]
y_modulealign = [1, 0.623792, 0.435359, 0.476076, 0.767452, 0.808331, 0.593119, 0.857145, 0.813192, 0.457123, 0.353851, 0.853836]
y_cgraal = [0.603587, 0.587848, 0.605051, 0.572108, 0.582723, 0.482064, 0.323206, 0.258785, 0.256955, 0.330161, 0.367496, 0.251098]
y_eigenalign = [1, 0.791362, 0.419839, 0.336384, 0.282577, 0.201318, 0.231332, 0.15959, 0.213397, 0.187042, 0.208272, 0.166545]
y_netalign = [0.465959, 0.415447, 0.324305, 0.267936, 0.314056, 0.276354, 0.189971, 0.216325, 0.183382, 0.161786, 0.156662, 0.173133]
y_klau = [0.503294, 0.478038, 0.398243, 0.359078, 0.328697, 0.183382, 0.146413, 0.133968, 0.126281, 0.126647, 0.101391, 0.102855]
y_regal = [1, 0.558199, 0.214861, 0.144583, 0.14019, 0.124817, 0.130307, 0.113104, 0.132138, 0.115666, 0.11896, 0.0933382, ]

cmap = ListedColormap(sns.color_palette("colorblind", 11))
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
        "REGAL":            {'color': cmap(10), 'marker': 'd', 'linestyle': '--', 'markersize': markersize},
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
ax.plot(x, y_regal, **style['REGAL'])

from matplotlib.lines import Line2D
legend_elem = [Line2D([0], [0], label=method, **kwargs) for method, kwargs in style.items()]
f.legend(handles=legend_elem, loc='lower center', ncol=2)

f.subplots_adjust(bottom=0.90, left=.175, right=1.0, top=.94)

plt.tight_layout()
f.subplots_adjust(bottom=0.24, hspace=0.6, wspace=0.35, right=0.9)
plt.show()
plt.savefig('plots/' + network_type + "/" + plot_name)
