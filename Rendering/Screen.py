import sys
import math
import copy
import pygame.display
import Settings

class Screen:
    """Renderer

    Attributes
    ----------
    complete: Boolean
        Whether the renderer should stop updating
    clock: Clock
        The clock used to update
    """
    def __init__(self, _voronoi_generator):
        """Constructor"""
        pygame.display.init()
        self.voronoi_painter = VoronoiPainter(_voronoi_generator)
        self.complete = False
        self.clock = pygame.time.Clock()

    def display(self, _width, _height, _caption = "Renderer"):
        """Display Function

        Parameters
        ----------
        _width: float
            The horizontal length of the screen
        _height: float
            The vertical length of the screen
        _caption: String
            The window title
        """
        pygame.display.set_mode((_width, _height))
        pygame.display.set_caption(_caption)

    def update(self):
        """Update Function"""
        #self.voronoi_painter.draw_voronoi()

        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                        self.voronoi_painter.next()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                        self.voronoi_painter.prev()
            
            pygame.display.update()
            self.clock.tick(60)

class VoronoiPainter:
    def __init__(self, _voronoi_generator):
        self.voronoi_generator = _voronoi_generator
        self.states = []
        self.count = 0

    def progress(self):
        self.voronoi_generator.handle_next_event()
        self.states.append([
            copy.copy(self.voronoi_generator.beach_line),
            copy.copy(self.voronoi_generator.edges),
            copy.copy(self.voronoi_generator.vertices),
            self.voronoi_generator.sweep_line + Settings.SWEEP_LINE_OFFSET])

    def complete(self):
        #self.voronoi_generator.complete_all_edges()
        self.states.append([
            copy.copy(self.voronoi_generator.beach_line),
            copy.copy(self.voronoi_generator.edges),
            copy.copy(self.voronoi_generator.vertices),
            self.voronoi_generator.sweep_line + Settings.SWEEP_LINE_OFFSET])

    def run(self):
        while self.voronoi_generator.have_events():
            self.progress()
        self.complete()

    def next(self):
        if self.count < len(self.states) - 1:
            self.count += 1
            self.draw_voronoi()

    def prev(self):
        if self.count > 0:
            self.count -= 1
            self.draw_voronoi()

    def draw_voronoi(self):
        surface = pygame.display.get_surface()
        curr_state = self.states[self.count]

        surface.fill(pygame.Color(0, 0, 0))

        curr_arc = curr_state[0]
        while curr_arc is not None:
            self.draw_parabola(curr_arc, surface, 1000, 1, curr_state[3])
            curr_arc = curr_arc.next

        for edge in curr_state[1]:
            if edge.next is not None:
                pygame.draw.line(
                    surface,
                    pygame.Color(0, 255, 0),
                    edge.origin.ToTuple(),
                    edge.next.origin.ToTuple(),
                    1)

        for vertex in curr_state[2]:
            pygame.draw.ellipse(
                surface,
                pygame.Color(255, 125, 125),
                pygame.Rect(vertex.x, vertex.y, 4.0, 4.0))

        pygame.draw.line(surface,
            pygame.Color(100, 100, 100),
            (0, curr_state[3]),
            (Settings.SCREEN_WIDTH, curr_state[3])
            )

        for point in self.voronoi_generator.points:
            pygame.draw.ellipse(
                surface,
                pygame.Color(255, 0, 0),
                pygame.Rect(point.x, point.y, 4.0, 4.0))

    def draw_parabola(self, _parabola, _surface, _resolution, _increment, _directrix):
        '''Draws the parabola onto a pygame surface

        Parameters
        ----------
        _parabola: Parabola
            The parabola to draw
        _surface: Surface
            The surface to draw on
        _resolution: int
            The number of points to draw
        _increment: float
            The horizontal difference between each drawn coordinate
        _directrix: float
            The current height of the directrix
        '''
        xPos = _parabola.focus.x - (math.floor(_resolution / 2) * _increment)
        for i in range(_resolution):
            pygame.draw.line(
                _surface,
                pygame.Color(125, 125, 0),
                (xPos, _parabola.GetValue(xPos, _directrix)),
                (xPos + _increment, _parabola.GetValue(xPos + _increment, _directrix)))
            xPos += _increment