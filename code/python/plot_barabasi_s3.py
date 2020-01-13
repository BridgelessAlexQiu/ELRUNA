import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "barabasi"
ylabel = "S3"
plot_name = "barabasi_s3_plot.pdf"
network_type = "random_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
y_naive = [1, 0.990281, 0.971055, 0.952562, 0.93476, 0.917612, 0.901081, 0.885135, 0.869744, 0.854879, 0.840513, 0.826623]
y_seed = [1, 0.990281, 0.971055, 0.952562, 0.93476, 0.917612, 0.901081, 0.885135, 0.869744, 0.854879, 0.840513, 0.826623]
y_netal = [1, 0.990281, 0.971055, 0.952562, 0.93476, 0.917612, 0.838454, 0.684589, 0.687304, 0.625164, 0.668236, 0.642973]
y_isorank = [1, 0.301614, 0.1563753, 0.0575769, 0.0560089, 0.0585528, 0.0541228, 0.0650791, 0.0532502, 0.0514356, 0.0472879, 0.0455796]
y_hubalign = [1, 0.33261, 0.256526, 0.499335, 0.210459, 0.489378, 0.231749, 0.387402, 0.211141, 0.202942, 0.203837, 0.207828]
y_modulealign = [1, 0.31261, 0.356526, 0.489335, 0.230459, 0.479378, 0.251749, 0.3972402, 0.19141, 0.232942, 0.213837, 0.217828]
y_cgraal = [0, 0.338417, 0.31574, 0.289504, 0.15873, 0.20071, 0.143645, 0.172034, 0.143244, 0.152984, 0.138968, 0.143744]
y_eigenalign = [1, 0.241077, 0.0985638, 0.126898, 0.0818925, 0.0666048, 0.0718375, 0.0734701, 0.0646265, 0.0636137, 0.0637471, 0.059613]
y_netalign = [0.364245, 0.322727, 0.267075, 0.202602, 0.199242, 0.166836, 0.159409, 0.106516, 0.12284, 0.099871, 0.0903167, 0.0795596]
y_klau = [0.364245, 0.322727, 0.267075, 0.22162, 0.195465, 0.0906849, 0.0901578, 0.0612208, 0.0579606, 0.0503255, 0.0476522, 0.0416381]

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
