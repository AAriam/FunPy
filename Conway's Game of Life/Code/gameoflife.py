import numpy as np

def update_cell(cell, num_neighbors):
    """
    Decide whether a cell lives or dies in the next generation,
    based on the following rules:
        1. Any live cell with two or three live neighbours survives.
        2. Any dead cell with three live neighbours becomes a live cell.
        3. All other cells die/stay dead in the next generation.
    
    Parameters
    ----------
    cell : 0 or 1
        Current state of the cell (0 for dead; 1 for alive).
    num_neighbors : int
        Number of neighbors the cell has in the current state.
    
    Returns
    -------
        0 (the cell dies) or 1 (the cell lives)
    """
    if num_neighbors == 3:
        return 1
    elif num_neighbors == 2 and cell == 1:
        return 1
    else:
        return 0

    
def update_grid(grid, periodic_boundary=True):
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
    new_grid = np.zeros(grid.shape)
    
    # expand grid 
    if periodic_boundary:
        #for periodic boundary conditions
        grid = np.column_stack((grid[:,-1], grid, grid[:,0])) # add right column to left, and left column to right
        grid = np.vstack((grid[-1], grid, grid[0])) # add top row to bottom and bottom row to top
    else:
        temp_grid = np.zeros((shape[0]+2, shape[1]+2))
        temp_grid[1:-1,1:-1] = grid
        grid = temp_grid
    
    # iterate over grid 
    for i in range(shape[0]):
        for j in range(shape[1]):
            # create 3x3 sub-grids where the cell is in the middle surrounded by neighbors
            sub_grid = grid[i:i+3, j:j+3] 
            cell = sub_grid[1,1]
            # number of neighbors is sum of sub-grid minus value of cell
            num_neighbors = np.sum(sub_grid) - cell 
            # update the corresponding cell and fill the value in new grid
            new_grid[i,j] = update_cell(cell, num_neighbors) 
    
    return new_grid


def create_game(grid, periodic_boundary=True):
    """
    Create a generator object that returns the new generation of the grid in each call.
    
    Parameters
    ----------
    grid : numpy array (2-dimensional, binary)
        The initial state of the grid (world), where each element is a cell either dead (0) or alive (1).
    
    Returns
    -------
        generator object
        Infinite generator that returns the next generation grid (2-dim. binary numpy array) after each call.
        Note: The first call returns the initial grid.
    """
    # raise error if the grid contains non-binary values
    if not np.array_equal(grid, grid.astype(bool)):
        raise ValueError("Grid contains non-binary values.")
    grid = grid.astype(int)
    while True:
        yield grid
        grid = update_grid(grid, periodic_boundary)

        
