
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "router"
ylabel = "S3"
plot_name = "router_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.997891, 0.986291, 0.965255, 0.939372, 0.925656, 0.903846, 0.888394, 0.863343, 0.843071, 0.822568, 0.81007, 0.790593, 0.774112, 0.755116, ]
y_seed = [1, 0.990146, 0.969568, 0.946871, 0.929716, 0.912779, 0.891202, 0.873972, 0.854579, 0.840988, 0.825082, 0.805816, 0.788055, 0.77897, ]
y_netal = [1, 0.987772, 0.695466, 0.561567, 0.431939, 0.531322, 0.614329, 0.754565, 0.236493, 0.757357, 0.785591, 0.691597, 0.673342, 0.571068, ]
y_isorank = [0.997891, 0.135821, 0.0475449, 0.0373903, 0.0243247, 0.0249963, 0.021909, 0.0205173, 0.0177743, 0.0173913, 0.0181563, 0.0160139, 0.0175451, 0.0168313, ]
y_hubalign = [1, 0.982451, 0.783283, 0.865907, 0.734647, 0.25079, 0.634124, 0.666981, 0.199764, 0.218131, 0.257054, 0.221435, 0.199822, 0.198554, ]
y_modulealign = [1, 0.992451, 0.793283, 0.8697, 0.729647, 0.26079, 0.644124, 0.686981, 0.20764, 0.238131, 0.267054, 0.2435, 0.19999822, 0.20554, ]
y_cgraal = [0.301924, 0.318888, 0.310553, 0.303452, 0.262809, 0.213873, 0.243712, 0.176676, 0.167827, 0.277837, 0.210434, 0.210939, 0.263369, 0.175979, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.321116, 0.307119, 0.268923, 0.246676, 0.232427, 0.206581, 0.214038, 0.174817, 0.166585, 0.17019, 0.15766, 0.141078, 0.136654, 0.131226, ]
y_klau = [0.320984, 0.307119, 0.268923, 0.24782, 0.233534, 0.207212, 0.214249, 0.176187, 0.168114, 0.170857, 0.159693, 0.141789, 0.136392, 0.131312, ]


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
