"""
Module contains all the necessary functions to run the Game of Life.
Each function builds upon its previous function.
In general, in order to create and run a game, only the last function, 'run_game' needs to be used.
"""


import numpy as np


def update_cell(cell: np.bool_, num_neighbors: np.int_) -> np.bool_:
    """
    Decide whether a cell lives or dies in the next generation,
    based on the following rules:
        1. Any live cell with two or three live neighbours survives.
        2. Any dead cell with three live neighbours becomes a live cell.
        3. All other cells die/stay dead in the next generation.
    
    Parameters
    ----------
    cell : numpy.bool_
        Current state of the cell (0 for dead; 1 for alive).
    num_neighbors : numpy.int_
        Number of neighbors the cell has in the current state.
    
    Returns
    -------
    numpy.bool_
        0 (the cell becomes/remains dead) or 1 (the cell becomes/remains alive)
    """
    if num_neighbors == 3:
        return 1
    elif num_neighbors == 2 and cell == 1:
        return 1
    else:
        return 0


def update_grid(grid: np.ndarray, periodic_boundary: bool = True) -> np.ndarray:
    """
    Update the state of the grid (world) for the next generation.
    
    Parameters
    ----------
    grid : numpy array (2-dimensional, binary)
        The current state of the grid (world), where each element is a cell either dead (0) or alive (1).
    
    Returns
    -------
        numpy array (2-dimensional, binary)
        The next state of the grid (world), where each element is a cell either dead (0) or alive (1).
    """
    shape = grid.shape

    # create new grid to store the updated grid
    new_grid = np.zeros(shape=grid.shape, dtype=np.bool_)

    # expand grid
    if periodic_boundary:
        # for periodic boundary conditions
        grid = np.column_stack(
            (grid[:, -1], grid, grid[:, 0])
        )  # add right column to left, and left column to right
        grid = np.vstack((grid[-1], grid, grid[0]))  # add top row to bottom and bottom row to top
    else:
        # for non-periodic (i.e. absolute) boundaries
        temp_grid = np.zeros((shape[0] + 2, shape[1] + 2))
        temp_grid[1:-1, 1:-1] = grid
        grid = temp_grid

    # iterate over grid
    for i in range(shape[0]):
        for j in range(shape[1]):
            # create 3x3 sub-grids where the cell is in the middle surrounded by neighbors
            sub_grid = grid[i:i + 3, j:j + 3]
            cell = sub_grid[1, 1]
            # number of neighbors is sum of sub-grid minus value of cell
            num_neighbors = np.sum(sub_grid) - cell
            # update the corresponding cell and fill the value in new grid
            new_grid[i, j] = update_cell(cell, num_neighbors)
    return new_grid


def create_game(grid: np.ndarray, periodic_boundary: bool = True):
    """
    Create a generator object that returns the new generation of the grid in each call.
    Note: The first call returns the initial grid.
    
    Parameters
    ----------
    grid : numpy array (2-dimensional, binary)
        The initial state of the grid (world), where each element is a cell either dead (0) or alive (1).
    periodic_boundary

    Returns
    -------
        generator object
        Infinite generator that returns the next generation grid (2-dim. binary numpy array) after each call.
    """
    # raise error if the grid contains non-binary values
    if not np.array_equal(grid, grid.astype(bool)):
        raise ValueError("Grid contains non-binary values.")
    grid = grid.astype(int)
    while True:
        yield grid
        grid = update_grid(grid, periodic_boundary)


def run_game(
        grid: np.ndarray, num_generations: int = 200, periodic_boundary: bool = True
) -> np.ndarray:
    """
    Run a game for a given numbers of generations and return all the generations.
    
    Parameters
    ----------
    grid : numpy.ndarray(shape=(w, h), dtype=numpy.bool_)
        A 2-dimensional binary array representing the initial state of the grid (world),
        where each element is a cell, either dead (0) or alive (1).
    
    num_generations : int
        The number of generations to simulate in the game.
    
    periodic_boundary : bool
        Whether to use periodic boundary conditions or absolute boundaries for the grid.
    
    Returns
    -------
        numpy.ndarray(shape=(num_generations, w, h), dtype=numpy.bool_)
        The progression of the initial grid for the given number of generations.
        Each element of the array is itself a 2-dim. array corresponding to the state of the grid.
        The index corresponds to the generation number, e.g. the first element (index 0) is the
        initial input grid.
    """
    game = create_game(grid, periodic_boundary)
    results = np.zeros((num_generations, grid.shape[0], grid.shape[1]))
    for i in range(num_generations):
        results[i] = game.send(None)
    return results
