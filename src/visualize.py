import matplotlib.pyplot as plt # Plotting
import numpy as np # Flipping matrices vertically
import time # Timing plot generation
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pca import *

board_yellow = (1,0.823,0.302) # Roughly the color of a Go board
board_gray = (0.5,0.5,0.5)

board_color = board_yellow

colors = [(1,1,1), board_color, (0,0,0)]

"""
visualize
---------
Visualize a Go board

Parameters:
    - board: A 19x19 matrix with entries of -1, 0, and 1
"""
def visualize(board):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.pcolormesh(np.flipud(board), cmap=LinearSegmentedColormap.from_list("go", [(1,1,1), board_color, (0,0,0)], N=3))
    plt.show()

cmap = LinearSegmentedColormap.from_list("visibility", [(1, 1, 0), (0, 0, 0), (1, 0, 1)], N=1000) # Color scheme for all plots

"""
visualize_principals
--------------------
Visualize the principal components of a covariance matrix, arranged in a grid by size of eigenvalue.

Parameters:
    - cov: The 361x361 covariance matrix
    - K: The number of principal components to visualize
    - ncols: The number of columns to arrange the plots in
    - save: Whether to save an image of the plot in the PCA folder
"""
def visualize_principals(cov, K, ncols, save):
    fig, plots = plt.subplots(K//ncols,ncols)
    fig.set_size_inches(10,10)
    principals = principal_components(cov)
    for i in range(K//ncols): # Rows
        for j in range(ncols): # Columns
            plots[i,j].axis('off')
            plots[i,j].pcolormesh(np.flipud(principals[:, ncols*i+j].reshape(19, 19)), cmap=cmap, vmin=-0.5, vmax=0.5) # Make plot in row i, column j the correct reshaped principal component
    plt.tight_layout()
    if save:
        plt.savefig("../plots/PCA/%f.png" % (time.time()))
    plt.show()

"""
correlation_plot
----------------
Generate the correlation plot from Figure 2
"""
def correlation_plot():
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=False)
    ticks = [i for i in range(0,362,19)]
    axins = inset_axes(ax2,
                       width="5%",  # width = 5% of parent_bbox width
                       height="100%",  # height : 50%
                       loc='lower left',
                       bbox_to_anchor=(1.1, 0., 1, 1),
                       bbox_transform=ax2.transAxes,
                       borderpad=0,
                       )
    fig.colorbar(ScalarMappable(cmap=cmap, norm=Normalize(-1.,1.)), cax=axins)
    ax1.set_xticks(ticks)
    ax1.set_yticks(ticks)
    ax1.set_title("18k Correlations")
    ax1.pcolormesh(cor_18k, cmap=cmap, vmin=-1., vmax=1.)
    ax1.set_aspect("equal")
    ax2.pcolormesh(cor_9d, cmap=cmap, vmin=-1., vmax=1.)
    ax2.set_xticks(ticks)
    ax2.set_yticks(ticks)
    ax2.set_aspect("equal")
    ax2.set_title("9d Correlations")
    plt.show()

"""
save_board_correlations
-----------------------
Save all 361 board correlation plots, as in Figure 3

Parameters:
    - save: A boolean dictating whether to save all the images or view them
"""
def save_board_correlations(save):
    for i in range(361):
        fig, (ax1,ax2) = plt.subplots(1,2)

        ax1.set_aspect('equal')
        ax1.set_xticks([4, 9.5, 15])
        ax1.set_yticks([4, 9.5, 15])
        ax1.pcolormesh(np.flipud(cor_18k[:,i].reshape(19, 19)),
            cmap=cmap, vmin=-1., vmax=1.)
        ax1.set_title("18k")
        ax2.set_aspect('equal')
        ax2.set_xticks([4, 9.5, 15])
        ax2.set_yticks([4, 9.5, 15])
        ax2.pcolormesh(np.flipud(cor_9d[:,i].reshape(19, 19)),
            cmap=cmap, vmin=-1., vmax=1.)
        ax2.set_title("9d")
        fig.suptitle("Coordinate: (%d,%d), Row: %d" % (i//19+1, i%19+1, i+1), size=24)
        fig.tight_layout()
        if save:
            plt.savefig("../plots/%d.png" % (i))
        else:
            plt.show()
        plt.close()

"""
save_PC
-----------------------
Save all 361 principal component visualizations

Parameters:
    - save: A boolean dictating whether to save all the images or view them
"""
def save_PC(save):
    for cov in [(cov_18k, "18k"), (cov_9d, "9d")]:
        principals = principal_components(cov[0])
        for i in range(361):
            fig = plt.figure()
            fig.set_size_inches(10, 10)

            plt.axis('off')
            plt.title("%s: PC %d" % (cov[1], i+1), size=24)
            plt.pcolormesh(np.flipud(principals[:, i].reshape(19, 19)), cmap=cmap, vmin=-0.5,
                                   vmax=0.5)
            fig.tight_layout()
            if save:
                plt.savefig("../plots/PCA/%s/%d.png" % (cov[1], i + 1))
            else:
                plt.show()
            plt.close()
