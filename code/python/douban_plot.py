import matplotlib.pyplot as plt

from matplotlib import rc
## use \showthe\font to check the font in Latex! https://tex.stackexchange.com/questions/109703/how-to-determine-the-font-being-used-by-a-latex-document
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

labels = ['Naive alignment', 'Seed alignment', 'NETAL', 'HubAlign', 'IsoRank', 'ModuleAlign', 'C-GRAAL', 'EigaenAlign', "NetAlign", "Klau"]
h_dblp = [0.290536, 0.555261, 0.423728, 0.356744, 0.079378, 0.336744, 0.228273, 0.17293, 0.09345, 0.0929372]
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

f, ax = plt.subplots(1)

ax.set_title(r"douban onlive vs offline - 1,118 vs 3,906")
ax.set_ylabel("Edge Correctness")
ax.bar(x,h_dblp,color=[style[l]['color'] for l in labels])
ax.set_ylim((0,0.7))

ax.set_xticks([])

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
plt.savefig('bar_plots/douban.pdf')
