import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "newman"
ylabel = "Edge Correctness"
plot_name = "newman_ec_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.991247, 0.989059, 0.987965, 0.989059, 0.989059, 0.99453, 0.993435, 0.995624, 0.989059, 0.985777, 0.950766, 0.950766, 0.93326, 0.950766]
y_seed = [1, 1, 0.997812, 0.998906, 1, 0.997812, 1, 0.998906, 0.995624, 0.99453, 0.982495, 0.974836, 0.958425, 0.971554 ]
y_netal = [0.991247, 0.947484, 0.983589, 0.972648, 0.66302, 0.630197, 0.710066, 0.574398, 0.583151, 0.780088, 0.68709, 0.612691, 0.592998, 0.605033 ]
y_isorank = [0.991247, 0.332604, 0.154267, 0.13895, 0.0765864, 0.0820569, 0.0656455, 0.0820569, 0.0612691, 0.071116, 0.0448578, 0.0448578, 0.0525164, 0.0426696]
y_hubalign = [0.771335, 0.69256, 0.675055, 0.588621, 0.567834, 0.646608, 0.564551, 0.538293, 0.575492, 0.625821, 0.521882, 0.595186, 0.554705, 0.586433]
y_modulealign = [0.77335, 0.68256, 0.655055, 0.5882231, 0.5767834, 0.636608, 0.579551, 0.518293, 0.525492, 0.615821, 0.5231882, 0.615186, 0.514705, 0.576433]
y_cgraal = [0.315098, 0.345733, 0.293217, 0.314004, 0.319475, 0.295405, 0.301969, 0.31291, 0.306346, 0.323851, 0.335886, 0.294311, 0.33151, 0.36105]
y_eigenalign = [1, 0.602845, 0.349015, 0.265864, 0.262582, 0.278993, 0.277899, 0.248359, 0.196937, 0.184902, 0.19256, 0.177243, 0.215536, 0.21116 ]
y_netalign = [0.425602, 0.415755, 0.356674, 0.345733, 0.296499, 0.293217, 0.222101, 0.258206, 0.195842, 0.175055, 0.213348, 0.206783, 0.169584, 0.165208]
y_klau = [0.425602, 0.415755, 0.363239, 0.349015, 0.310722, 0.30744, 0.249453, 0.263676, 0.226477, 0.231947, 0.236324, 0.237418, 0.170678, 0.200219]


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
