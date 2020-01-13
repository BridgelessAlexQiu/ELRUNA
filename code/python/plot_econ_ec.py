import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "econ"
ylabel = "Edge Correctness"
plot_name = "econ_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 1, 1, 1, 1, 0.999601, 1, 0.999468, 0.999068, 0.999468, 0.998669, 0.999601, 0.996806, 0.990417, ]
y_seed = [1, 1, 1, 1, 1, 0.999601, 1, 1, 1, 1, 1, 0.999867, 1, 0.999601, ]
y_netal = [1, 0.9614, 0.933981, 0.912685, 0.915746, 0.913217, 0.910289, 0.919606, 0.879409, 0.884201, 0.883003, 0.861307, 0.821776, 0.77692, ]
y_isorank = [1, 0.479303, 0.391189, 0.340077, 0.298682, 0.295488, 0.27672, 0.2883, 0.297751, 0.244643, 0.226008, 0.251298, 0.248902, 0.263277, ]
y_hubalign = [1, 0.941169, 0.906961, 0.900972, 0.857314, 0.864768, 0.816585, 0.868761, 0.702516, 0.705976, 0.639691, 0.814721, 0.823639, 0.731532, ]
y_modulealign = [1, 0.931169, 0.921961, 0.91272, 0.871314, 0.854768, 0.826585, 0.888761, 0.752516, 0.725976, 0.629691, 0.824721, 0.813639, 0.721532, ]
y_cgraal = [0, 0, 0.513909, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [1, 0.70358, 0.615333, 0.596965, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.467989, 0.459337, 0.408226, 0.408625, 0.37109, 0.349661, 0.304539, 0.318781, 0.249701, 0.247172, 0.266205, 0.233462, 0.214295, 0.221749, ]
y_klau = [0.472381, 0.465593, 0.419007, 0.416744, 0.390124, 0.350859, 0.333954, 0.325702, 0.285505, 0.25782, 0.274591, 0.252096, 0.240516, 0.228271, ]


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
