import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "barabasi"
ylabel = "Edge Correctness"
plot_name = "barabasi_ec_plot.pdf"
network_type = "random_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
y_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
y_seed = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
y_netal = [1, 1, 1, 1, 1, 1, 0.962196, 0.865503, 0.875682, 0.898764, 0.877136, 0.864776]
y_isorank = [1, 0.585387, 0.108324, 0.111596, 0.109778, 0.115594, 0.108324, 0.130134, 0.108688, 0.106143, 0.0988731, 0.0963286]
y_hubalign = [1, 0.501636, 0.414395, 0.682661, 0.359869, 0.686659, 0.396947, 0.594693, 0.374773, 0.366049, 0.370774, 0.380225]
y_modulealign = [1, 0.531636, 0.434395, 0.692661, 0.369869, 0.696659, 0.4967, 0.61463, 0.344733, 0.31049, 0.470774, 0.3910225]
y_cgraal = [0.6012, 0.508179, 0.487096, 0.460196, 0.283533, 0.349328, 0.264995, 0.312614, 0.269357, 0.287895, 0.267176, 0.277717]
y_eigenalign = [1, 0.390403, 0.182116, 0.230825, 0.15667, 0.130498, 0.141403, 0.145765, 0.130498, 0.129771, 0.131225, 0.124318]
y_netalign = [0.533988, 0.490367, 0.427844, 0.345329, 0.343875, 0.2988, 0.290076, 0.205016, 0.235187, 0.197019, 0.181389, 0.16285]
y_klau = [0.51388, 0.450367, 0.417844, 0.371865, 0.338422, 0.173755, 0.174482, 0.122864, 0.117775, 0.103962, 0.0996001, 0.0883315]
y_regal = [1, 0.461287, 0.255907, 0.155216, 0.121047, 0.119229, 0.109051, 0.0999636, 0.102145, 0.0977826, 0.0992366, 0.0876045, ]


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

plt.savefig('plots/' + network_type + "/" + plot_name)
