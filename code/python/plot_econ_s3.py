import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "econ"
ylabel = "S3"
plot_name = "econ_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 0.990116, 0.970923, 0.952459, 0.934685, 0.916748, 0.900947, 0.88414, 0.868147, 0.853878, 0.838324, 0.82591, 0.808398, 0.786326, ]
y_seed = [1, 0.990116, 0.970923, 0.952459, 0.934685, 0.916748, 0.900947, 0.885028, 0.869661, 0.854721, 0.84038, 0.826312, 0.813095, 0.799446, ]
y_netal = [1, 0.916857, 0.852198, 0.802552, 0.793449, 0.776043, 0.758793, 0.759815, 0.692195, 0.687681, 0.675629, 0.63867, 0.583609, 0.527424, ]
y_isorank = [1, 0.31313, 0.23871, 0.198895, 0.168633, 0.164664, 0.150948, 0.156548, 0.160762, 0.127065, 0.11508, 0.128304, 0.125647, 0.13252, ]
y_hubalign = [1, 0.880573, 0.807633, 0.784175, 0.707025, 0.705812, 0.631368, 0.688865, 0.485378, 0.482226, 0.412638, 0.583953, 0.585708, 0.481767, ]
y_modulealign = [1, 0.893573, 0.817633, 0.794175, 0.727025, 0.712812, 0.61368, 0.6908865, 0.495378, 0.491226, 0.42638, 0.591953, 0.590708, 0.491767, ]
y_cgraal = [0, 0, 0.338982, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [1, 0.538563, 0.434983, 0.410865, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.305474, 0.296223, 0.251724, 0.248966, 0.218444, 0.200918, 0.168682, 0.176012, 0.131409, 0.128548, 0.13838, 0.118122, 0.10632, 0.109332, ]
y_klau = [0.309227, 0.301474, 0.260101, 0.255175, 0.23225, 0.201745, 0.188039, 0.180524, 0.153138, 0.134832, 0.143363, 0.128765, 0.120902, 0.112911, ]


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
