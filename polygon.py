import math


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"x:{self.x} y:{self.y}"

    @staticmethod
    # Intersection count on end points too.
    def lineIntersection(p1, p2, p3, p4) -> bool:
        denom = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)
        if denom == 0:  # parallel
            return False
        ua = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) / denom
        if ua < 0 or ua > 1:  # out of range
            return False
        ub = ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) / denom
        if ub < 0 or ub > 1:  # out of range
            return False
        return True

    @staticmethod
    def isOnTheSameLine(a, b, c):
        if b != c and b != a:
            if abs(Line(a, b).length() + Line(b, c).length() - Line(a, c).length()) < 0.00001:
                return True
            else:
                return False
        else:
            return False


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.a_x = end.x - start.x
        self.a_y = end.y - start.y

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        elif self.start == other.end and self.end == other.start:
            return True
        else:
            return False

    def length(self):
        return math.sqrt(self.a_x**2+self.a_y**2)

    def is_point_left_or_right(self, point: Point):
        s = self.a_x * (point.y - self.start.y) - self.a_y * (point.x - self.start.x)
        if s > 0:
            return 1
        elif s < 0:
            return 0
        else:
            return None

    # Intersection on end points not count
    def is_intersect_with(self, line):
        start = line.start
        end = line.end
        start_loc = self.is_point_left_or_right(start)
        end_loc = self.is_point_left_or_right(end)
        if (start_loc == end_loc) and start_loc is not None:
            return 0
        elif start_loc is None or end_loc is None:
            return 0
        else:
            return 1


class Polygon:
    points = []
    lines = []

    def __init__(self, *points):
        for i in range(len(points)):
            if isinstance(points[i], Point):
                self.points.append(points[i])

    def addPoint(self, point):
        if isinstance(point, Point):
            self.points.append(point)

    def addLines(self):
        for i in range(len(self.points) - 1):
            self.lines.append(Line(self.points[i], self.points[i+1]))
        self.lines.append(Line(self.points[-1], self.points[0]))

    def hasLeastFourPoints(self) -> bool:
        return len(self.points) >= 4

    def isPolygon(self) -> bool:
        for i in range(len(self.points) - 1):
            if Point.lineIntersection(
                    self.points[i % len(self.points)],
                    self.points[(i + 1) % len(self.points)],
                    self.points[(i + 2) % len(self.points)],
                    self.points[(i + 3) % len(self.points)]):
                return False

        return True

    def _crossProduct(self, A) -> int:
        X1 = (A[1].x - A[0].x)
        Y1 = (A[1].y - A[0].y)
        X2 = (A[2].x - A[0].x)
        Y2 = (A[2].y - A[0].y)
        return (X1 * Y2 - Y1 * X2)

    # опуклість
    def isConvex(self) -> bool:
        prev = 0
        curr = 0
        N = len(self.points)
        for i in range(N):
            temp = [self.points[i], self.points[(i + 1) % N],
                    self.points[(i + 2) % N]]
            curr = self._crossProduct(temp)

            if (curr != 0):
                if (curr * prev < 0):
                    return False
                else:
                    prev = curr
        return True

    def __repr__(self):
        return str(self)

    def isConvexPolygon(self):
        if not self.hasLeastFourPoints():
            raise RuntimeError('Введіть мінімум чотири точки')
        if self.isPolygon() and self.isConvex():
            return True
        else:
            return False


