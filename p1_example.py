#bwichers@ucsc.edu & majwang@ucsc.edu
#Brian Wichers and Matthew Wang
from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(start, dst, graph, adj):
    dist = {}
    prev = {}
    pq = []
    dist[start] = 0
    prev[start] = None

    for vertex in graph['waypoints']:
        vertex = graph['waypoints'][vertex]
        if vertex is not start:
            dist[vertex] = float("+inf")
            prev[vertex] = None
        heappush(pq, (dist[vertex], vertex))

    for vertex in graph['spaces']:
        dist[vertex] = float("+inf")
        prev[vertex] = None
        heappush(pq, (dist[vertex], vertex))

    while pq:
        priority, current = heappop(pq)
        neighbors = adj(graph, current)
        for neighbor in neighbors:
            neighbor, weight = neighbor
            better_distance = priority + weight
            if better_distance < dist[neighbor]:
                dist[neighbor] = better_distance
                prev[neighbor] = current
                if neighbor == dst:
                    break
                heappush(pq, (dist[neighbor], neighbor))

    if prev[dst] is None:
        return []
    path = []
    past = prev[dst]
    path.append(dst)
    while past is not start:
        path.append(past)
        past = prev[past]
    path.append(start)

    return path

def navigation_edges(graph, current):
    neighbors = []
    x, y = current
    right = x+1, y
    left = x-1, y
    above = x, y-1
    below = x, y+1
    bright = x+1, y+1
    aright = x+1, y-1
    aleft = x-1, y-1
    bleft = x-1, y+1
    temp = [right, left, above, below]
    temp2 = [aright, bright, aleft, bleft]
    walls = graph['walls'].keys()
    for neighbor in temp:
        if neighbor not in walls:
            neighbors.append((neighbor, 1))
    for neighbor in temp2:
        if neighbor not in walls:
            neighbors.append((neighbor, sqrt(2)))
    return neighbors

def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)

	show_level(level)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)
	else:
		print ("No path possible!")

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
