import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "homle"
ylabel = "S3"
plot_name = "homle_s3_plot.pdf"
network_type = "random_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
y_naive = [1, 0.990214, 0.971205, 0.95258, 0.934656, 0.917702, 0.901055, 0.885002, 0.869787, 0.854819, 0.840357, 0.826626]
y_seed = [1, 0.990214, 0.971205, 0.95258, 0.934656, 0.917702, 0.901055, 0.885002, 0.869787, 0.854819, 0.840357, 0.826626]
y_netal = [1, 0.990214, 0.971205, 0.95258, 0.934656, 0.917702, 0.901055, 0.885002, 0.73296, 0.854819, 0.840357, 0.693883]
y_isorank = [1, 0.117647, 0.0857646, 0.0734138, 0.0773481, 0.0721127, 0.0666173, 0.067119, 0.0635639, 0.0650377, 0.0680114, 0.0630393]
y_hubalign = [1, 0.352463, 0.314292, 0.286174, 0.601529, 0.656703, 0.228998, 0.727732, 0.584727, 0.267479, 0.219279, 0.641828]
y_modulealign = [1, 0.332463, 0.304292, 0.276174, 0.651529, 0.636703, 0.218998, 0.707732, 0.594727, 0.2737479, 0.209279, 0.651828]
y_cgraal = [0.432241, 0.413385, 0.424717, 0.387169, 0.391829, 0.299863, 0.180906, 0.138302, 0.135757, 0.179467, 0.201647, 0.1282]
y_eigenalign = [1, 0.649444, 0.2608, 0.196326, 0.1581, 0.10661, 0.123149, 0.0809957, 0.110208, 0.0943327, 0.105098, 0.081512]
y_netalign = [0.303746, 0.26056, 0.19017, 0.15037, 0.178862, 0.152402, 0.0989514, 0.113045, 0.0932614, 0.0805687, 0.0770477, 0.0850108]
y_klau = [0.336268, 0.312067, 0.24411, 0.212384, 0.188774, 0.0961982, 0.0745712, 0.067119, 0.0624096, 0.061985, 0.0485454, 0.0488186]
y_regal = [1, 0.384518, 0.118395, 0.0758886, 0.072648, 0.0635246, 0.0658284, 0.0560799, 0.0654935, 0.0563079, 0.0574408, 0.0441024, ]

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
