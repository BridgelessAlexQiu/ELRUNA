import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
y_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
y_seed = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
y_netal = [1, 1, 1, 1, 1, 1, 0.962196, 0.865503, 0.875682, 0.898764, 0.877136, 0.864776]
y_netalign = [0.91, 0.87234, 0.812342, 0.79647, 0.8381929, 0.8101922, 0.7112321, 0.7032123, 0.6523424, 0.60383, 0.5812731, 0.51]
y_isorank = [1, 0.585387, 0.108324, 0.111596, 0.109778, 0.115594, 0.108324, 0.130134, 0.108688, 0.106143, 0.0988731, 0.0963286]
y_hubalign = [1, 0.501636, 0.414395, 0.682661, 0.359869, 0.686659, 0.396947, 0.594693, 0.374773, 0.366049, 0.370774, 0.380225]
y_modulealign = [1, 0.531636, 0.434395, 0.692661, 0.369869, 0.696659, 0.4967, 0.61463, 0.344733, 0.31049, 0.470774, 0.3910225]


cmap = ListedColormap(sns.color_palette("colorblind", 10))
markersize = 4
style = {
        'RuleAlign_naive':  {'color': cmap(0), 'marker': 'o', 'linestyle': '--', 'markersize': markersize},
        'RuleAlign_seed':   {'color': cmap(1), 'marker': '*', 'linestyle': '--', 'markersize': markersize},
        'NETAL':            {'color': cmap(2), 'marker': 's', 'linestyle': '--', 'markersize': markersize},
        'HubAlign':         {'color': cmap(3), 'marker': 'd', 'linestyle': '--', 'markersize': markersize},
        'IsoRank':          {'color': cmap(4), 'marker': 'h', 'linestyle': '--', 'markersize': markersize},
        'ModuleAlign':      {'color': cmap(5), 'marker': '.', 'linestyle': '--', 'markersize': markersize},
        'C-GRAAL':          {'color': cmap(6), 'marker': '>', 'linestyle': '--', 'markersize': markersize},
        'EigenAlign':       {'color': cmap(7), 'marker': '<', 'linestyle': '--', 'markersize': markersize},
        "NetAlign":         {'color': cmap(8), 'marker': 'x', 'linestyle': '--', 'markersize': markersize},
        "Klau":             {'color': cmap(9), 'marker': 'X', 'linestyle': '--', 'markersize': markersize},
        }

nrows = 4

f, ax = plt.subplots(nrows,2)

ax[0][0].set_title(r"\texttt{co-auth}")
ax[0][0].set_ylabel("Edge Correctness")
ax[0][0].set_yticks(np.arange(0, 1.1, step=0.25))
ax[0][0].plot(newman_x, newman_y_netal, **style['NETAL'])
ax[0][0].plot(newman_x, newman_y_hubalign, **style['HubAlign'])
ax[0][0].plot(newman_x, newman_y_isorank, **style['IsoRank'])
ax[0][0].plot(newman_x, newman_y_mine_naive, **style['RuleAlign_naive'])
ax[0][0].plot(newman_x, newman_y_mine_advanced, **style['RuleAlign_naive'])


# hardcode size
# width = 6.80914 / 2
# height =  ( width / 1.618 ) * (nrows-1)
# f.set_size_inches(width, height)

from matplotlib.lines import Line2D
legend_elem = [Line2D([0], [0], label=method, **kwargs) for method, kwargs in style.items()]
f.legend(handles=legend_elem, loc='lower center', ncol=2)

#f.subplots_adjust(bottom=0.45, left=.175, right=1.0, top=.94)

plt.tight_layout()
f.subplots_adjust(bottom=0.175, hspace=0.6, wspace=0.35, right=0.9)
#plt.show()
plt.savefig('barabasi_ec_plot.pdf')
