import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "retweet_2"
ylabel = "EC"
plot_name = "retweet2_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.995533, 0.995161, 0.994417, 0.993672, 0.983251, 0.984367, 0.973201, 0.945409, 0.899132, 0.93139, 0.820347, 0.854715, 0.92928, 0.895285, ]
y_seed = [1, 0.999628, 0.999007, 0.998015, 0.993797, 0.990074, 0.990323, 0.971464, 0.993176, 0.952481, 0.988958, 0.96464, 0.959926, 0.952481, ]
y_netal = [0.999504, 0.964764, 0.78995, 0.783995, 0.787345, 0.777295, 0.770844, 0.776799, 0.774318, 0.740695, 0.749007, 0.737717, 0.746774, 0.740943, ]
y_isorank = [0.987841, 0.797767, 0.696154, 0.549504, 0.438958, 0.212655, 0.365881, 0.344541, 0.294417, 0.23598, 0.196278, 0.23871, 0.18139, 0.256948, ]
y_hubalign = [1, 0.646631, 0.59488, 0.480794, 0.454451, 0.382984, 0.387605, 0.347845, 0.361815, 0.357991, 0.34761, 0.335639, 0.312624, 0.315777, ]
y_modulealign = [0.874814, 0.885112, 0.874194, 0.861166, 0.869727, 0.858437, 0.857692, 0.83871, 0.818114, 0.85794, 0.806948, 0.810298, 0.787841, 0.802357, ]
y_cgraal = [0.318362, 0.319107, 0.354963, 0.351985, 0.324442, 0.320471, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.0315136, 0.0305211, 0.0341191, 0.0269231, 0.0326303, 0.025062, 0.0294045, 0.0282878, 0.030273, 0.0280397, 0.0218362, 0.0235732, 0.0212159, 0.0245658, ]
y_klau = [0.0421836, 0.0408189, 0.0368486, 0.0362283, 0.0353598, 0.033871, 0.0334988, 0.030397, 0.0334988, 0.0308933, 0.0301489, 0.0276675, 0.0269231, 0.0282878, ]


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
