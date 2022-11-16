from polygon import Point, Polygon
from graph import ShortestPathFinder
from itertools import chain


def main():

    with open('input_data.txt', 'r') as f:
        lines = f.readlines(0)

    start_and_end_coordinates = []

    num_of_vertexes = int(lines[0])
    start_and_end_coordinates.append(lines[1].split())
    start_and_end_coordinates.append(lines[2].split())
    start_and_end_coordinates = list(map(int, list(chain.from_iterable(start_and_end_coordinates))))

    assert len(lines[3:]) == num_of_vertexes

    fig = Polygon()

    for line in lines[3:]:
        fig.addPoint(Point(float(line.split()[0]), float(line.split()[1])))

    if fig.isConvexPolygon():

        fig.addLines()

        start = Point(start_and_end_coordinates[0], start_and_end_coordinates[1])
        end = Point(start_and_end_coordinates[2], start_and_end_coordinates[3])
        path_finder = ShortestPathFinder(start, end, fig.lines)

        min_distances_from_beginning = path_finder.find_shortest_distance()
        print(min_distances_from_beginning)
        print("Minimum distance is ", list(min_distances_from_beginning.values())[-1])
    else:
        print('Полігон не опуклий')


main()
