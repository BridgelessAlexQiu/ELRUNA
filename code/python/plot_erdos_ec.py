import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "erdos"
ylabel = "EC"
plot_name = "erdos_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 1, 0.999865, 0.999731, 0.992596, 0.997442, 0.995019, 0.990711, 0.975363, 0.984518, 0.977518, 0.981826, 0.971055, 0.967286, ]
y_seed = [1, 1, 0.999865, 0.999731, 0.993807, 0.997442, 0.997981, 0.992192, 0.98398, 0.986941, 0.981018, 0.989768, 0.978191, 0.975363, ]
y_netal = [1, 0.867124, 0.675687, 0.722267, 0.656031, 0.616451, 0.637184, 0.594238, 0.607027, 0.590469, 0.591546, 0.587507, 0.582929, 0.585487, ]
y_isorank = [1, 0.166936, 0.0477921, 0.0289445, 0.0215401, 0.0188476, 0.0188476, 0.0177706, 0.0214055, 0.0180398, 0.017636, 0.0153473, 0.0181745, 0.0150781, ]
y_hubalign = [1, 0.789311, 0.757135, 0.66559, 0.646742, 0.578756, 0.589391, 0.549677, 0.571217, 0.572025, 0.56489, 0.555331, 0.531099, 0.539984, ]
y_modulealign = [1, 0.79311, 0.787135, 0.67559, 0.656742, 0.598756, 0.619391, 0.569677, 0.581217, 0.592025, 0.56489, 0.575331, 0.551099, 0.569984, ]
y_cgraal = [0.595315, 0.669494, 0.652935, 0.653743, 0.664109, 0.591546, 0.621702, 0.302639, 0.387588, 0.488153, 0.595046, 0.628029, 0.633414, 0.3021, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.205843, 0.19588, 0.195207, 0.179995, 0.178514, 0.16909, 0.167071, 0.157512, 0.143915, 0.142569, 0.141761, 0.131799, 0.122106, 0.121298, ]
y_klau = [0.208401, 0.202342, 0.198169, 0.183899, 0.181206, 0.174071, 0.168686, 0.157377, 0.1493, 0.145934, 0.144453, 0.13476, 0.124798, 0.126279, ]
y_regal = [0.994346, 0.64405, 0.352316, 0.200458, 0.15482, 0.115644, 0.0907377, 0.0573506, 0.0480614, 0.0578891, 0.0578891, 0.0375606, 0.0236941, 0.0193861, ]

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
