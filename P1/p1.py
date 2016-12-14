from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    queue = []
    heappush(queue, (0, initial_position))
    came_from = {}
    cost_so_far = {}
    came_from[initial_position] = None
    cost_so_far[initial_position] = 0
    
    while queue:
        current_cost, current_node = heappop(queue)

        if current_node == destination:
            path = []
            current_path = destination
            while current_path is not None:
                path.insert(0, current_path)
                current_path = came_from[current_path]
            return path

        for next_node, next_cost in navigation_edges(graph, current_node):
            new_cost = cost_so_far[current_node] + 1/2*(graph["spaces"][current_node] + next_cost)*sqrt((current_node[0] - next_node[0])**2 + (current_node[1] - next_node[1])**2)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                heappush(queue, (new_cost, next_node))
                came_from[next_node] = current_node

    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    queue = []
    heappush(queue, (0, initial_position))
    came_from = {}
    cost_so_far = {}
    came_from[initial_position] = None
    cost_so_far[initial_position] = 0
    
    while queue:
        current_cost, current_node = heappop(queue)

        for next_node, next_cost in navigation_edges(graph, current_node):
            new_cost = cost_so_far[current_node] + 1/2*(graph["spaces"][current_node] + next_cost)*sqrt((current_node[0] - next_node[0])**2 + (current_node[1] - next_node[1])**2)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                heappush(queue, (new_cost, next_node))
                came_from[next_node] = current_node

    return cost_so_far


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    if cell in level['walls']:
        return [];
    
    x = cell[0]
    y = cell[1]

    #list that hold adjacencies and costs
    adj = []

    #iterates in around cell
    for a in range(x-1, x+2, 1):
        for b in range(y-1,y+2, 1):
            if (a, b) in level['walls']:
                continue
            elif (a,b) == cell:
                continue
            else:
                adj.append( ( (a, b), level['spaces'][(a,b)] ) )

    return adj


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
     filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')
