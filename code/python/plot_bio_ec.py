import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "bio"
ylabel = "Edge Correctness"
plot_name = "bio_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.995385, 0.998462, 0.996154, 0.996154, 0.996923, 0.988462, 0.990769, 0.979231, 0.981538, 0.978462, 0.948462, 0.960769, 0.907692, 0.930769]
y_seed = [1, 1, 0.997692, 0.999231, 0.999231, 0.996154, 0.991538, 0.986923, 0.989231, 0.989231, 0.973846, 0.973077, 0.961538, 0.963077]
y_netal = [1, 0.996923, 0.88, 0.695385, 0.684615, 0.656923, 0.616154, 0.673077, 0.563846, 0.555385, 0.620769, 0.587692, 0.548462, 0.571538]
y_isorank = [0.996923, 0.416923, 0.190769, 0.164615, 0.0984615, 0.106923, 0.07, 0.0753846, 0.0584615, 0.0607692, 0.06, 0.0384615, 0.0392308, 0.0415385, ]
y_hubalign = [1, 0.813846, 0.606154, 0.55, 0.548462, 0.481538, 0.506154, 0.470769, 0.479231, 0.485385, 0.474615, 0.480769, 0.508462, 0.519231]
y_modulealign = [1, 0.803846, 0.636154, 0.5576, 0.538462, 0.491538, 0.516154, 0.480769, 0.499231, 0.495385, 0.454615, 0.476769, 0.524462, 0.509231]
y_cgraal = [0.952308, 0.916923, 0.336923, 0.310769, 0.54, 0.299231, 0.281538, 0.33, 0.287692, 0.323077, 0.314615, 0.395385, 0.327692, 0.314615]
y_eigenalign = [0.991538, 0.296923, 0.160769, 0.145385, 0.141538, 0.143846, 0.141538, 0.156923, 0.130769, 0.130769, 0, 0, 0, 0]
y_netalign = [0.139231, 0.15, 0.153077, 0.123846, 0.122308, 0.117692, 0.0969231, 0.107692, 0.0976923, 0.114615, 0.0876923, 0.0915385, 0.0946154, 0.0738462]
y_klau = [0.151538, 0.160769, 0.156154, 0.127692, 0.130769, 0.117692, 0.0984615, 0.112308, 0.0930769, 0.112308, 0.100769, 0.0853846, 0.103846, 0.0969231]


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
