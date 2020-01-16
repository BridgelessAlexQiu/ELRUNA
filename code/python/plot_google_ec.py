import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "google"
ylabel = "EC"
plot_name = "google_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 0.999974, 0.999923, 0.986422, 0.999592, 0.971824, 0.960875, 0.895054, 0.91981, 0.906615, 0.922618, 0.884386, 0.855495, 0.868486, ]
y_seed = [1, 0.999974, 0.999949, 0.988719, 0.999796, 0.999515, 0.997678, 0.942576, 0.987367, 0.979072, 0.968072, 0.963861, 0.957634, 0.965903, ]
y_netal = [1, 0.771247, 0.717881, 0.681308, 0.675106, 0.662575, 0.658185, 0.651881, 0.609464, 0.611174, 0.615487, 0.612041, 0.601909, 0.608417, ]
y_isorank = [0.993594, 0.150809, 0.0858558, 0.0655403, 0.0568628, 0.054132, 0.0601041, 0.0429789, 0.0408096, 0.0378745, 0.0399929, 0.0327446, 0.0370578, 0.0323618, ]
y_hubalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_modulealign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_cgraal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.0598234, 0.0657445, 0.0498188, 0.0535195, 0.0541065, 0.053596, 0.0529835, 0.0505334, 0.0536471, 0.0536498, 0.0536483, 0.05371, 0.05641, 0.053627, ]
y_klau = [0.0881017, 0.0872084, 0.0848859, 0.0828186, 0.0813894, 0.0787862, 0.0772038, 0.0741922, 0.0752386, 0.075238, 0.07586, 0.0752311, 0.0752345, 0.0752309 ]
y_regal = [1, 0.785105, 0.517585, 0.334899, 0.228574, 0.216605, 0.153489, 0.132153, 0.175055, 0.0820275, 0.0885356, 0.0624777, 0.0668674, 0.0778419, ]

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
