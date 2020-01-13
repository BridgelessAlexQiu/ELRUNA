import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "bio"
ylabel = "S3"
plot_name = "bio_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.990812, 0.987072, 0.963542, 0.945255, 0.929032, 0.897346, 0.885223, 0.850936, 0.840026, 0.821175, 0.763941, 0.769089, 0.686446, 0.705539]
y_seed = [1, 0.990099, 0.966468, 0.950952, 0.93319, 0.910689, 0.88652, 0.863392, 0.85222, 0.837785, 0.800759, 0.786692, 0.758035, 0.748356]
y_netal = [1, 0.984055, 0.765217, 0.513345, 0.49417, 0.4584, 0.412461, 0.461985, 0.35548, 0.343973, 0.395588, 0.362257, 0.326167, 0.340513, ]
y_isorank = [0.993865, 0.261709, 0.103722, 0.0873113, 0.0499415, 0.0539178, 0.0343137, 0.0366904, 0.0279515, 0.0288111, 0.028169, 0.0177117, 0.0179073, 0.0188088, ]
y_hubalign = [1, 0.680386, 0.425716, 0.366667, 0.360465, 0.299378, 0.315588, 0.283727, 0.286832, 0.288128, 0.276682, 0.278025, 0.295353, 0.3, ]
y_modulealign = [1, 0.650386, 0.434716, 0.361667, 0.366465, 0.3149378, 0.312588, 0.293727, 0.306832, 0.298128, 0.286682, 0.238025, 0.305353, 0.312321, ]
y_cgraal = [0.908957, 0.838846, 0.199, 0.178682, 0.352941, 0.167096, 0.153976, 0.183333, 0.154482, 0.174927, 0.16776, 0.217889, 0.17226, 0.16256, ]
y_eigenalign = [0.983219, 0.173327, 0.0860082, 0.0763328, 0.0733945, 0.073913, 0.0719031, 0.0795322, 0.0647619, 0.0641267, 0, 0, 0, 0, ]
y_netalign = [0.0748243, 0.0806452, 0.0815574, 0.0642971, 0.0627962, 0.0596724, 0.0481467, 0.0532522, 0.0476012, 0.0557635, 0.0417124, 0.0432099, 0.0443084, 0.0339343, ]
y_klau = [0.0819809, 0.0869384, 0.0833333, 0.0664266, 0.0674336, 0.0596724, 0.0489484, 0.0556615, 0.0452506, 0.0545794, 0.0482327, 0.0401883, 0.0488423, 0.0450161, ]


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
