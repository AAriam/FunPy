# Module contains the necessary functions to visualise a game using Jupyter Notebook.
# You only need to use the last function: visualize_game

from IPython import display
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["figure.dpi"] = 200  # for plots with higher resolution


def plot_grid(grid):
    """
    Plot a grid (i.e. state).
    
    Parameters
    ----------
    grid : numpy array (2-dimensional, binary)
        Array representing the state of the grid (a.k.a world)
        
    Returns
    -------
    	None
	The grid is visualised in the Jupyter notebook.
    """

    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    ax.axis("off")
    num_rows, num_cols = grid.shape

    # draw the grid
    for x in range(num_rows + 1):
        ax.axhline(x, lw=0.1, color="k", zorder=2)
    for y in range(num_cols + 1):
        ax.axvline(y, lw=0.1, color="k", zorder=2)

    # draw the cells
    ax.imshow(
        grid, interpolation="none", cmap="binary", extent=[0, num_rows, 0, num_cols], zorder=0
    )
    plt.show()


def visualize_game(game_results):
    """
    Take a game result and animate the game.
    
    Parameters
    ----------
    game_results : numpy array (3-dimensional, binary)
        Array of 2-dim. arrays, where each represent a generation.
        
    Returns
    -------
    	None
	The game is animated in the Jupyter notebook.
    """

    for generation in game_results:
        plot_grid(generation)
        display.clear_output(wait=True)
