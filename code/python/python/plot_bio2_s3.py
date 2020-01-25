import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "bio2"
ylabel = "S3"
plot_name = "bio2_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [1, 0.990232, 0.970213, 0.947522, 0.929111, 0.906419, 0.887255, 0.842435, 0.812939, 0.810351, 0.770021, 0.747314, 0.705448, 0.640403, ]
y_seed = [1, 0.990232, 0.971052, 0.947522, 0.9299, 0.912538, 0.894685, 0.866859, 0.832586, 0.833488, 0.802598, 0.790764, 0.767066, 0.727074, ]
y_netal = [1, 0.985922, 0.863554, 0.72929, 0.436635, 0.560393, 0.43144, 0.419369, 0.328097, 0.344607, 0.30112, 0.349485, 0.329109, 0.294652, ]
y_isorank = [1, 0.149718, 0.0494107, 0.0264515, 0.0160318, 0.0151193, 0.00880411, 0.0102932, 0.00988468, 0.00825015, 0.0051313, 0.00648897, 0.00563464, 0.00371602, ]
y_hubalign = [1, 0.423758, 0.331033, 0.294394, 0.260916, 0.263451, 0.265116, 0.245769, 0.255344, 0.249243, 0.260568, 0.237359, 0.255151, 0.248662, ]
y_modulealign = [1, 0.413758, 0.351033, 0.244394, 0.27916, 0.263451, 0.275116, 0.235769, 0.265344, 0.269243, 0.2568, 0.247359, 0.265151, 0.258662, ]
y_cgraal = [0.667398, 0.290136, 0.214426, 0.362074, 0.243809, 0.229876, 0.269621, 0.212654, 0.241676, 0.254467, 0.191697, 0.205981, 0.194435, 0.192518, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.0416714, 0.0372172, 0.0408003, 0.0399199, 0.040551, 0.0285899, 0.0286417, 0.0292342, 0.0289551, 0.022096, 0.0216813, 0.0170483, 0.0224121, 0.018254, ]
y_klau = [0.0505469, 0.0446622, 0.0473928, 0.0479606, 0.0479414, 0.034393, 0.035503, 0.03648, 0.0360199, 0.0280403, 0.0251411, 0.0234494, 0.0258143, 0.0241469, ]
y_regal = [0.792534, 0.441893, 0.253723, 0.173695, 0.152569, 0.0813202, 0.0631835, 0.0715704, 0.0699247, 0.0523015, 0.043342, 0.0390601, 0.0276796, 0.025682, ]

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
