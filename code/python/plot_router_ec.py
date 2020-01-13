import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "router"
ylabel = "Edge Correctness"
plot_name = "router_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.998945, 0.99804, 0.996984, 0.992913, 0.995024, 0.992159, 0.992612, 0.986882, 0.983414, 0.979343, 0.980097, 0.975724, 0.97301, 0.968034, ]
y_seed = [1, 1, 0.999246, 0.996984, 0.997286, 0.997286, 0.99427, 0.993366, 0.990651, 0.991255, 0.990048, 0.986128, 0.982811, 0.985223, ]
y_netal = [1, 0.998794, 0.83263, 0.737183, 0.624397, 0.725121, 0.802925, 0.916013, 0.411188, 0.935163, 0.96351, 0.903498, 0.897316, 0.817853, ]
y_isorank = [0.998945, 0.24035, 0.0921291, 0.0738842, 0.0491556, 0.050965, 0.0452352, 0.0428227, 0.0375452, 0.0370929, 0.0390531, 0.0348311, 0.0384499, 0.0372437, ]
y_hubalign = [1, 0.99608, 0.891586, 0.951297, 0.876659, 0.419029, 0.818758, 0.852232, 0.357961, 0.388571, 0.447829, 0.400633, 0.371381, 0.372738, ]
y_modulealign = [1, 0.97608, 0.897586, 0.956297, 0.870659, 0.439029, 0.813758, 0.842232, 0.367961, 0.398571, 0.457829, 0.410633, 0.391381, 0.342738, ]
y_cgraal = [0.463812, 0.485977, 0.481001, 0.477232, 0.43079, 0.368215, 0.41345, 0.319813, 0.308957, 0.471803, 0.38073, 0.384952, 0.464867, 0.336701, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.486128, 0.472256, 0.430187, 0.405609, 0.39038, 0.357811, 0.371984, 0.316948, 0.306996, 0.315591, 0.298251, 0.273221, 0.268094, 0.261007, ]
y_klau = [0.485977, 0.472256, 0.430187, 0.407117, 0.391888, 0.358715, 0.372286, 0.319059, 0.309409, 0.316647, 0.301568, 0.274427, 0.267642, 0.261158, ]


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
