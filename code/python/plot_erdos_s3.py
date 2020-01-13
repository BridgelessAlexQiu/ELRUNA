import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "erdos"
ylabel = "S3"
plot_name = "erdos_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 0.990136, 0.970723, 0.951929, 0.921395, 0.913001, 0.892417, 0.869653, 0.830372, 0.830551, 0.80624, 0.799496, 0.771361, 0.754093, ]
y_seed = [1, 0.990136, 0.970723, 0.951929, 0.923558, 0.913001, 0.897458, 0.872086, 0.843898, 0.834301, 0.81147, 0.81121, 0.781458, 0.765209, ]
y_netal = [1, 0.758747, 0.498956, 0.544007, 0.464007, 0.418365, 0.432633, 0.386955, 0.393421, 0.373849, 0.370083, 0.362128, 0.353932, 0.351747, ]
y_isorank = [1, 0.0905771, 0.0241119, 0.0143219, 0.0105159, 0.00910036, 0.00901307, 0.00841354, 0.0100563, 0.00838338, 0.00811849, 0.00699344, 0.00821718, 0.00674658, ]
y_hubalign = [1, 0.646631, 0.59488, 0.480794, 0.454451, 0.382984, 0.387605, 0.347845, 0.361815, 0.357991, 0.34761, 0.335639, 0.312624, 0.315777, ]
y_modulealign = [1, 0.66631, 0.65488, 0.580794, 0.494451, 0.432984, 0.427605, 0.397845, 0.401815, 0.397991, 0.40761, 0.455639, 0.352624, 0.395777, ]
y_cgraal = [0.423807, 0.499448, 0.474189, 0.468229, 0.472419, 0.394789, 0.41773, 0.165623, 0.219922, 0.290266, 0.37309, 0.397021, 0.396745, 0.15509, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.114729, 0.107978, 0.106399, 0.0962563, 0.0943839, 0.0880292, 0.0859895, 0.079858, 0.0717402, 0.0703234, 0.0692126, 0.0634232, 0.0579294, 0.056982, ]
y_klau = [0.116321, 0.111939, 0.108188, 0.0985499, 0.0959441, 0.090858, 0.0868932, 0.0797843, 0.0746249, 0.0721032, 0.07062, 0.064941, 0.0592825, 0.0594612, ]


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
