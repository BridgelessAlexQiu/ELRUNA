import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "social"
ylabel = "EC"
plot_name = "social_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.992762, 0.993584, 0.989842, 0.986675, 0.978574, 0.975243, 0.964591, 0.954187, 0.943946, 0.931897, 0.923384, 0.916722, 0.900025, 0.885713, ]
y_seed = [1, 0.999589, 0.997779, 0.995887, 0.9905, 0.987827, 0.981658, 0.974173, 0.968292, 0.959862, 0.958546, 0.952459, 0.940985, 0.931609, ]
y_netal = [1, 0.986059, 0.876008, 0.88596, 0.497245, 0.540179, 0.708505, 0.646858, 0.493996, 0.500781, 0.507361, 0.550255, 0.569584, 0.594547, ]
y_isorank = [0.663802, 0.0125021, 0.00497615, 0.00530515, 0.00435927, 0.00370127, 0.00300214, 0.00308439, 0.00316664, 0.00222076, 0.00300214, 0.00205626, 0.00213851, 0.00148051, ]
y_hubalign = [1, 0.839488, 0.599687, 0.511351, 0.465496, 0.425152, 0.41812, 0.383575, 0.403232, 0.397187, 0.402533, 0.421944, 0.398215, 0.429635, ]
y_modulealign = [1, 0.859488, 0.619687, 0.521351, 0.495496, 0.45152, 0.43812, 0.393575, 0.43232, 0.377187, 0.42533, 0.431944, 0.408215, 0.419635, ]
y_cgraal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.243872, 0.239678, 0.230095, 0.225119, 0.206777, 0.203652, 0.198964, 0.190656, 0.17762, 0.174247, 0.173302, 0.162609, 0.154507, 0.159483, ]
y_klau = [0.244613, 0.240747, 0.231288, 0.226189, 0.209163, 0.206325, 0.200115, 0.193987, 0.180128, 0.178072, 0.176139, 0.164501, 0.157509, 0.161499, ]


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
