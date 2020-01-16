import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "retweet"
ylabel = "S3"
plot_name = "retweet_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.992942, 0.979905, 0.960996, 0.938639, 0.924911, 0.902631, 0.883647, 0.863766, 0.848027, 0.82836, 0.81465, 0.790223, 0.769447, 0.756858, ]
y_seed = [1, 0.989623, 0.967999, 0.94751, 0.930251, 0.909526, 0.891061, 0.873754, 0.857073, 0.841548, 0.824717, 0.803468, 0.787328, 0.772149, ]
y_netal = [1, 0.71084, 0.462292, 0.43452, 0.499282, 0.338262, 0.325679, 0.327125, 0.325183, 0.292331, 0.279719, 0.272223, 0.272411, 0.276175, ]
y_isorank = [0.990133, 0.342417, 0.214219, 0.151795, 0.13166, 0.111002, 0.102769, 0.0874439, 0.0652815, 0.0702907, 0.0556542, 0.0507173, 0.0529097, 0.0490785, ]
y_hubalign = [1, 0.942497, 0.648717, 0.626208, 0.552156, 0.543039, 0.477726, 0.490976, 0.506751, 0.492546, 0.471025, 0.470172, 0.451051, 0.442245, ]
y_modulealign = [1, 0.952497, 0.658717, 0.676208, 0.592156, 0.593039, 0.497726, 0.530976, 0.56751, 0.512546, 0.491025, 0.490172, 0.481051, 0.502245, ]
y_cgraal = [0.468483, 0.137497, 0.185685, 0.155843, 0.16282, 0.155557, 0.158435, 0.241228, 0.134909, 0.182492, 0.131284, 0.146469, 0.126288, 0.139557, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.10271, 0.0961063, 0.0944016, 0.0882972, 0.0830924, 0.0824712, 0.0824128, 0.0758497, 0.0709951, 0.0667131, 0.0624742, 0.0660835, 0.0592867, 0.0634793, ]
y_klau = [0.109295, 0.107745, 0.102994, 0.0947193, 0.0936307, 0.0907142, 0.0883449, 0.0850895, 0.0822221, 0.0773667, 0.0762322, 0.0744542, 0.0724944, 0.0722387, ]
y_regal = [0.960289, 0.610077, 0.322962, 0.214436, 0.184981, 0.160831, 0.150382, 0.145698, 0.122651, 0.102252, 0.113921, 0.0962755, 0.0962463, 0.0976571, ]

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
