import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "retweet_2"
ylabel = "S3"
plot_name = "retweet2_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.991107, 0.980682, 0.96034, 0.940686, 0.904784, 0.89036, 0.856145, 0.798156, 0.718806, 0.751978, 0.598967, 0.630688, 0.71449, 0.660866, ]
y_seed = [1, 0.989439, 0.96907, 0.948697, 0.923449, 0.900169, 0.88453, 0.838599, 0.858537, 0.78233, 0.82345, 0.774634, 0.755862, 0.734079, ]
y_netal = [0.999008, 0.923077, 0.637082, 0.619267, 0.613852, 0.592155, 0.575651, 0.574088, 0.562861, 0.518229, 0.519804, 0.501096, 0.503513, 0.490997, ]
y_isorank = [0.975975, 0.658137, 0.521953, 0.366215, 0.269131, 0.113277, 0.209789, 0.192981, 0.158665, 0.122017, 0.0984504, 0.121098, 0.088547, 0.128922, ]
y_hubalign = [0.777484, 0.786896, 0.756414, 0.724379, 0.724623, 0.697058, 0.68493, 0.649563, 0.614252, 0.653901, 0.583475, 0.578938, 0.546331, 0.554251, ]
y_modulealign = [0.787484, 0.796896, 0.796414, 0.764379, 0.764623, 0.737058, 0.71493, 0.689563, 0.654252, 0.663901, 0.593475, 0.598938, 0.56331, 0.54251, ]
y_cgraal = [0.318362, 0.319107, 0.354963, 0.351985, 0.324442, 0.320471, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.0160091, 0.0154193, 0.0170956, 0.013308, 0.0160161, 0.0121372, 0.0141332, 0.0134601, 0.0142815, 0.0130908, 0.0100715, 0.010782, 0.00960566, 0.0110386, ]
y_klau = [0.0215463, 0.0207296, 0.0184885, 0.0179903, 0.0173791, 0.0164736, 0.0161329, 0.0144782, 0.0158274, 0.0144423, 0.0139591, 0.0126784, 0.0122212, 0.0127325, ]
y_regal = [0.96322, 0.461303, 0.161013, 0.18768, 0.140163, 0.115711, 0.158368, 0.109266, 0.107143, 0.10354, 0.0824186, 0.0688269, 0.0224131, 0.0152838, ]

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
