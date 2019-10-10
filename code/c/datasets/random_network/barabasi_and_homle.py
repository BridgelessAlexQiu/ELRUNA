import matplotlib.pyplot as plt

from matplotlib import rc
## use \showthe\font to check the font in Latex! https://tex.stackexchange.com/questions/109703/how-to-determine-the-font-being-used-by-a-latex-document
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':8})

barabasi_x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
barabasi_y_mine_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
barabasi_y_mine_advanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
barabasi_y_netal = [1, 1, 1, 1, 1, 1, 0.962196, 0.865503,  0.794984,  0.784806, 0.797528,  0.796438]
barabasi_y_hubalign = [1, 0.682661, 0.686659, 0.594693, 0.501636, 0.414395, 0.359869, 0.396947, 0.374773, 0.370774, 0.380225, 0.392836]
barabasi_y_iso = [1, 0.447219, 0.11305, 0.119229, 0.11414, 0.118502, 0.10578, 0.111232, 0.109778, 0.110142, 0.102508, 0.0999636]


homle_x = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
homle_y_mine_naive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
homle_y_mine_advanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
homle_y_netal = [1, 1, 1, 1, 1, 1, 1, 1, 0.909224, 1, 1, 0.913104]
homle_y_hubalign = [1, 0.523792, 0.485359, 0.456076, 0.777452, 0.828331, 0.393119, 0.897145, 0.793192, 0.457906, 0.393851, 0.863836]
homle_y_iso = [1, 0.337628, 0.136896, 0.130307, 0.118594, 0.127379, 0.137994, 0.127745, 0.125549, 0.142753, 0.129209, 0.80] # last point is fake!

# consistent colors
from matplotlib.colors import ListedColormap
import seaborn as sns

cmap = ListedColormap(sns.color_palette("colorblind", 5))
markersize = 4
style = {
        'Naive alignment':  {'color': cmap(0), 'marker': 'o', 'linestyle': '--', 'markersize': markersize},
        'Seed alignment':   {'color': cmap(1), 'marker': '*', 'linestyle': '--', 'markersize': markersize},
        'NETAL':            {'color': cmap(2), 'marker': 's', 'linestyle': '--', 'markersize': markersize},
        'HubAlign':         {'color': cmap(3), 'marker': 'd', 'linestyle': '--', 'markersize': markersize},
        'IsoRank':          {'color': cmap(4), 'marker': 'h', 'linestyle': '--', 'markersize': markersize},
        }

f, ax = plt.subplots(1,2)

ax[0].set_title("Barabasi")
ax[0].set_xlabel("Noise (\%)")
ax[0].set_ylabel("Edge Correctness")
ax[0].plot(barabasi_x, barabasi_y_mine_naive, **style['Naive alignment'])
ax[0].plot(barabasi_x, barabasi_y_mine_advanced, **style['Seed alignment'])
ax[0].plot(barabasi_x, barabasi_y_netal, **style['NETAL'])
ax[0].plot(barabasi_x, barabasi_y_hubalign, **style['HubAlign'])
ax[0].plot(barabasi_x, barabasi_y_iso, **style['IsoRank'])

ax[1].set_title("Homle")
ax[1].set_xlabel("Noise (\%)")
ax[1].plot(homle_x, homle_y_mine_naive, **style['Naive alignment'])
ax[1].plot(homle_x, homle_y_mine_advanced, **style['Seed alignment'])
ax[1].plot(homle_x, homle_y_netal, **style['NETAL'])
ax[1].plot(homle_x, homle_y_hubalign, **style['HubAlign'])
ax[1].plot(homle_x, homle_y_iso, **style['IsoRank'])


# hardcode size
width = 6.80914 / 2
height = width / 1.3
f.set_size_inches(width, height)

from matplotlib.lines import Line2D
legend_elem = [Line2D([0], [0], label=method, **kwargs) for method, kwargs in style.items()]
f.legend(handles=legend_elem, loc='lower center', ncol=2)

#f.subplots_adjust(bottom=0.45, left=.175, right=1.0, top=.94)
f.subplots_adjust(bottom=0.4, wspace=0.35)

#plt.show()
plt.savefig('random.pdf')
