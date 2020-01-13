import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

# rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

title = "social"
ylabel = "S3"
plot_name = "social_s3_plot.pdf"
network_type = "real_network"

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
y_naive = [0.985628, 0.977544, 0.951645, 0.927944, 0.896605, 0.874862, 0.84216, 0.811514, 0.782684, 0.752699, 0.729017, 0.708843, 0.676737, 0.649213, ]
y_seed = [1, 0.989295, 0.966652, 0.944793, 0.917559, 0.896269, 0.870025, 0.842839, 0.819413, 0.793203, 0.778386, 0.757407, 0.730019, 0.706625, ]
y_netal = [1, 0.963009, 0.759123, 0.761129, 0.316162, 0.348547, 0.505546, 0.436141, 0.298309, 0.300015, 0.301528, 0.331533, 0.343043, 0.359144, ]
y_isorank = [0.496784, 0.00625888, 0.00245735, 0.00259463, 0.00211038, 0.0017741, 0.00142486, 0.00145017, 0.00147504, 0.00102445, 0.00137272, 0.000931307, 0.000959905, 0.000658436, ]
y_hubalign = [1, 0.717202, 0.419276, 0.332344, 0.290119, 0.255373, 0.247138, 0.219635, 0.230847, 0.224047, 0.225198, 0.235981, 0.217395, 0.236016, ]
y_modulealign = [1, 0.737202, 0.459276, 0.352344, 0.310119, 0.295373, 0.267138, 0.249635, 0.260847, 0.254047, 0.25198, 0.25981, 0.247395, 0.26016, ]
y_cgraal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_eigenalign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
y_netalign = [0.138869, 0.135387, 0.127839, 0.123363, 0.110979, 0.107962, 0.104115, 0.0983099, 0.0900542, 0.0873104, 0.0859334, 0.0794231, 0.0744447, 0.076289, ]
y_klau = [0.13935, 0.136073, 0.128587, 0.124022, 0.112403, 0.109534, 0.10478, 0.1002, 0.0914424, 0.0893982, 0.0874635, 0.0804214, 0.0760011, 0.0773275, ]


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
