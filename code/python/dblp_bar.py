import matplotlib.pyplot as plt

from matplotlib import rc
## use \showthe\font to check the font in Latex! https://tex.stackexchange.com/questions/109703/how-to-determine-the-font-being-used-by-a-latex-document
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

labels = ['Naive alignment', 'Seed alignment', 'NETAL', 'HubAlign', 'IsoRank', 'ModuleAlign', 'C-GRAAL', 'EigaenAlign', "NetAlign", "Klau"]
h_dblp = [0.996296, 0.999234, 0.964619, 0.806744, 0.029378, 0.836744, 0.628273, 0.57293, 0.32345, 0.3329372]
h_elegan = [0.313616, 0.566964, 0.495536, 0.539062, 0.0478274, 0.530322, 0.213820, 0.24810383, 0.0928374, 0.0998374]
x=[1,2,3,4,5,6,7,8,9,10]

# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

cmap = ListedColormap(sns.color_palette("colorblind", 10))
markersize = 4
style = {
        'Naive alignment':  {'color': cmap(0), 'marker': 'o', 'linestyle': '--', 'markersize': markersize},
        'Seed alignment':   {'color': cmap(1), 'marker': '*', 'linestyle': '--', 'markersize': markersize},
        'NETAL':            {'color': cmap(2), 'marker': 's', 'linestyle': '--', 'markersize': markersize},
        'HubAlign':         {'color': cmap(3), 'marker': 'd', 'linestyle': '--', 'markersize': markersize},
        'IsoRank':          {'color': cmap(4), 'marker': 'h', 'linestyle': '--', 'markersize': markersize},
        'ModuleAlign':      {'color': cmap(5), 'marker': '.', 'linestyle': '--', 'markersize': markersize},
        'C-GRAAL':          {'color': cmap(6), 'marker': '>', 'linestyle': '--', 'markersize': markersize},
        'EigaenAlign':       {'color': cmap(7), 'marker': '<', 'linestyle': '--', 'markersize': markersize},
        "NetAlign":         {'color': cmap(8), 'marker': 'x', 'linestyle': '--', 'markersize': markersize},
        "Klau":             {'color': cmap(9), 'marker': 'X', 'linestyle': '--', 'markersize': markersize},
        }

f, ax = plt.subplots(1,2)

ax[0].set_title(r"dblp - 3,134 vs 3,875")
ax[0].set_ylabel("Edge Correctness")
ax[0].bar(x,h_dblp,color=[style[l]['color'] for l in labels])
ax[0].set_ylim((0,1.1))

ax[1].set_title(r"elegan - 2,194 vs 2,831")
ax[1].bar(x,h_elegan,color=[style[l]['color'] for l in labels])
ax[1].set_ylim((0,0.6))

for a in ax:
    a.set_xticks([])

# hardcode size
# width = 6.80914 / 2
# height = width / 1.618
# f.set_size_inches(width, height)

from matplotlib.lines import Line2D
legend_elem = [Line2D([0], [0], label=method, **kwargs) for method, kwargs in style.items()]
f.legend(handles=legend_elem, loc='lower center', ncol=2)

#f.subplots_adjust(bottom=0.45, left=.175, right=1.0, top=.94)

plt.tight_layout()
f.subplots_adjust(bottom=0.35, wspace=0.35, top = 0.9, right=0.9)
plt.show()
plt.savefig('bar_plots/dblp_elegan.pdf')
