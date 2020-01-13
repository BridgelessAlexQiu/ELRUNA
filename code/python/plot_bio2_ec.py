import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "bio2"
ylabel = "Edge Correctness"
plot_name = "bio2_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 1, 0.999562, 0.99737, 0.996931, 0.993643, 0.99189, 0.973915, 0.964051, 0.971285, 0.952652, 0.945199, 0.922402, 0.878343, ]
y_seed = [1, 1, 1, 0.99737, 0.99737, 0.99715, 0.996274, 0.98904, 0.976765, 0.986409, 0.975011, 0.975888, 0.967996, 0.947172, ]
y_netal = [1, 0.997808, 0.940596, 0.864533, 0.62911, 0.750548, 0.635905, 0.629329, 0.531127, 0.556116, 0.506795, 0.572337, 0.55217, 0.512056, ]
y_isorank = [1, 0.261727, 0.0955721, 0.0528277, 0.0326611, 0.0311267, 0.018413, 0.021701, 0.0210434, 0.0177554, 0.0111793, 0.0142481, 0.0124945, 0.00832968, ]
y_hubalign = [1, 0.598203, 0.504822, 0.466243, 0.428321, 0.435774, 0.442131, 0.42021, 0.437308, 0.432924, 0.452652, 0.423937, 0.45331, 0.448049, ]
y_modulealign = [1, 0.618203, 0.524822, 0.456243, 0.438321, 0.4774, 0.452131, 0.44021, 0.417308, 0.452924, 0.462652, 0.413937, 0.44331, 0.438049, ]
y_cgraal = [0.800526, 0.451995, 0.358395, 0.544936, 0.405743, 0.390618, 0.448049, 0.37352, 0.418457, 0.440158, 0.352258, 0.377466, 0.362999, 0.363218, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.0800088, 0.0721175, 0.0795704, 0.0786936, 0.0806664, 0.0580886, 0.0587462, 0.0604998, 0.0604998, 0.0469093, 0.0464708, 0.0370452, 0.0488821, 0.0403332, ]
y_klau = [0.0962297, 0.0859272, 0.0918457, 0.0938185, 0.0946953, 0.0694871, 0.0723367, 0.0749671, 0.0747479, 0.0591846, 0.0537045, 0.0506357, 0.0561157, 0.0530469, ]


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
