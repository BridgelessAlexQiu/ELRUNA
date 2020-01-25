import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "newman"
ylabel = "S3"
plot_name = "newman_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.982646, 0.968917, 0.948529, 0.932921, 0.915907, 0.908092, 0.890196, 0.878378, 0.852026, 0.832717, 0.767668, 0.755652, 0.719831, 0.732098]
y_seed = [1, 0.990249, 0.967126, 0.951042, 0.935517, 0.913828, 0.901381, 0.883833, 0.862559, 0.846369, 0.814143, 0.789894, 0.753873, 0.760274 ]
y_netal = [0.982646, 0.891864, 0.940377, 0.903455, 0.471595, 0.431784, 0.507428, 0.369458, 0.372207, 0.561417, 0.457393, 0.383825, 0.362299, 0.367931 ]
y_isorank = [0.982646, 0.198304, 0.0822637, 0.0727377, 0.0384404, 0.0408719, 0.0321199, 0.0400855, 0.0293347, 0.0338895, 0.0209184, 0.020728, 0.0241206, 0.0193356]
y_hubalign = [0.627783, 0.525748, 0.498385, 0.402996, 0.37828, 0.448067, 0.365439, 0.338377, 0.365532, 0.405386, 0.312992, 0.368814, 0.331156, 0.352632]
y_modulealign = [0.627783, 0.515748, 0.51885, 0.422996, 0.33828, 0.458067, 0.375439, 0.358377, 0.364532, 0.407386, 0.332992, 0.378814, 0.321156, 0.322632]
y_cgraal = [0.187013, 0.207758, 0.168872, 0.180958, 0.182614, 0.164634, 0.16707, 0.172289, 0.166172, 0.175459, 0.181228, 0.153714, 0.17464, 0.191194 ]
y_eigenalign = [1, 0.42846, 0.207682, 0.14908, 0.145366, 0.154079, 0.151732, 0.132054, 0.10084, 0.0931643, 0.0964384, 0.0872375, 0.107007, 0.103596 ]
y_netalign = [0.270327, 0.26081, 0.213211, 0.202954, 0.167284, 0.163216, 0.117681, 0.138012, 0.100224, 0.0877674, 0.107973, 0.103279, 0.0823155, 0.0792651]
y_klau = [0.270327, 0.26081, 0.217991, 0.205277, 0.176727, 0.172498, 0.134118, 0.141349, 0.117747, 0.119706, 0.121008, 0.120422, 0.0828905, 0.0977042]
y_regal = [0.944681, 0.628546, 0.309104, 0.165526, 0.160123, 0.134204, 0.113164, 0.1082, 0.0743576, 0.066129, 0.0587302, 0.0626316, 0.0559585, 0.0452466, ]

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
