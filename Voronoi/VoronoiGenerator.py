from DCEL.BST import BeachLine
import math
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola
from Voronoi.VoronoiEvent import (SiteEvent, CircleEvent, EventType)
from DCEL.DCEL import (HalfEdge, DCEL)
import Settings

class Arc(Parabola):
    def __init__(self, _site):
        super().__init__(_site)
        self.left_half_edge = None
        self.right_half_edge = None

    def __eq__(self, _other):
        return id(self) == id(_other)

class VoronoiGenerator:
    """The class used to generate the Voronoi diagram.

    Attributes
    ----------
    sweep_line: float
        The object used to advance the algorithm
    beach_line: [Arc]:
        The list of sites making up the parabolas
    queue: [VoronoiEvent]
        The priority queue used to contain the events
    sitesToConsider: [Vector]
        The list of sites yet to be handled
    vertices: [Vector]
        The vertices to be returned
    """
    def __init__(self, _points):
        self.sweep_line = 0.0
        self.beach_line = BeachLine()
        self.points = _points
        self.queue = self.init_sites(_points)
        self.edges = []
        self.vertices = []
        self.circles = []

    def generate_voronoi(self):
        while len(self.queue) > 0:
            self.handle_next_event()

        #self.complete_all_edges()
        return DCEL(self.vertices, self.edges, None)

    def handle_next_event(self):
        if not self.have_events():
            return

        event = self.queue.pop(0)
        self.sweep_line = event.position.y

        if event.type is EventType.SITE_EVENT:
            new_site = event.position
            new_arc = Arc(new_site)
            self.beach_line.append(new_arc, self.sweep_line)

            self.beach_line.display()
            print("***************")

            adjacent_arcs = self.beach_line.get_adjacent_arcs(new_arc)

            self.check_for_circle_events(new_arc, self.sweep_line)
            for a in adjacent_arcs:
                self.check_for_circle_events(a, self.sweep_line)

            #self.insert_new_site(new_site)
        elif event.type is EventType.VERTEX_EVENT:
            associated_arc = event.arc

            self.beach_line.remove_leaf_node(associated_arc)

            self.check_for_circle_events(associated_arc.prev, self.sweep_line)
            self.check_for_circle_events(associated_arc.next, self.sweep_line)

            self.vertices.append(event.mid_point)

        self.queue.sort(key=lambda e: e.position.y)

    def init_sites(self, _points):
        events = []
        for point in _points:
            events.append(SiteEvent(point))

        return events

    def insert_new_site(self, _new_site):
        while curr_arc is not None:
            intersection_point = self.get_lowest_intersection_point(_new_site, self.sweep_line)

            if intersection_point is not None:
                curr_arc.append(
                    Arc(_new_site, curr_arc, curr_arc.next),
                    intersection_point,
                    self.edges)

                curr_arc = curr_arc.next # Advance the linked list

                if curr_arc.next is not None:
                    curr_arc.append(
                        Arc(curr_arc.prev.focus, curr_arc, curr_arc.next),
                        intersection_point,
                        self.edges)

                self.check_for_circle_events(curr_arc, self.sweep_line)
                self.check_for_circle_events(curr_arc.prev, self.sweep_line)
                self.check_for_circle_events(curr_arc.next, self.sweep_line)

                self.vertices.append(intersection_point)

                return

            curr_arc = curr_arc.next

        last_arc = Arc.get_last(self.root_arc)
        new_arc = Arc(_new_site, last_arc, None)
        last_arc.Append(new_arc,
            Parabola.GetBreakpoint(last_arc, new_arc, self.sweep_line),
            self.edges)

    def get_lowest_intersection_point(self, _point, _sweep_line):
        intersection_point = None
        curr_arc = self.root_arc

        while curr_arc is not None:
            new_intersection_point = self.get_intersection_point(_point, curr_arc, self.sweep_line)

            if new_intersection_point is not None:
                if intersection_point is None:
                    intersection_point = new_intersection_point
                elif new_intersection_point.y > intersection_point.y:
                    intersection_point = new_intersection_point

            curr_arc = curr_arc.next

        return intersection_point

    def get_intersection_point(self, _point, _arc, _sweep_line):
        """ Checks if a parabola created with focus at _point intersects with _arc

        Parameters
        ----------
        _point : Vector
            The point to check
        _arc: Arc
            The arc on the beachline
        _sweep_line : float
            The sweep_line
        """
        if _arc is None:
            return None
        if _point == _arc.focus:
            return None

        left_intersection = Vector(0.0, 0.0)
        right_intersection = Vector(0.0, 0.0)

        if _arc.prev is not None:
            left_intersection = Parabola.GetBreakpoint(_arc.prev, _arc, _point.y)
        if _arc.next is not None:
            right_intersection = Parabola.GetBreakpoint(_arc, _arc.next, _point.y)
        if (_arc.prev is None or _point.x >= left_intersection.x) and \
           (_arc.next is None or _point.x <= right_intersection.x):
            return Vector(_point.x, _arc.GetValue(_point.x, _sweep_line))

        return None

    def check_for_circle_events(self, _arc, _sweep_line):
        if _arc is None:
            return False
        if _arc.prev is None or _arc.next is None:
            return False

        lowest_point, mid_point = self.lowest_point_on_circumcircle(
            _arc.prev.focus,
            _arc.focus,
            _arc.next.focus)

        if lowest_point is None:
            return False
        if lowest_point.y > _sweep_line:
            self.queue.append(CircleEvent(lowest_point, mid_point, _arc))
            return True

        return False

    def lowest_point_on_circumcircle(self, _vector_A, _vector_B, _vector_C):
        a = _vector_A
        b = _vector_B
        c = _vector_C

        #if (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0: return None

        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

        if G == 0:
            return None, None

        mid_point = Vector((D * E - B * F) / G, (A * F - C * E) / G)
        radius = math.sqrt((a.x - mid_point.x) ** 2 + (a.y - mid_point.y) ** 2)
        lowest_point = Vector(mid_point.x, mid_point.y + radius)

        return lowest_point, mid_point

    def complete_all_edges(self):
        self.sweep_line = Settings.SCREEN_HEIGHT * 3

        curr_arc = self.root_arc
        while curr_arc is not None:
            if curr_arc.left_half_edge is not None:
                if curr_arc.left_half_edge.next is None:
                    left_end_vertex = Parabola.GetBreakpoint(
                        curr_arc.prev,
                        curr_arc,
                        self.sweep_line)
                    if left_end_vertex is not None:
                        next_edge = HalfEdge(left_end_vertex, self.edges)
                        curr_arc.left_half_edge.next = next_edge

            if curr_arc.right_half_edge is not None:
                if curr_arc.right_half_edge.next is None:
                    right_end_vertex = Parabola.GetBreakpoint(
                        curr_arc,
                        curr_arc.next,
                        self.sweep_line)
                    if right_end_vertex is not None:
                        next_edge = HalfEdge(right_end_vertex, self.edges)
                        curr_arc.right_half_edge.next = next_edge

            curr_arc = curr_arc.next

    def have_events(self):
        return len(self.queue) > 0
