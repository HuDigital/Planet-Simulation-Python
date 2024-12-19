import pygame
import math
pygame.init()

WIDTH = 800
HEIGHT = 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AUnit = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AUnit # scale it down, 1AU = 100 pixels
    TIMESTEP = 3600 * 24 # num sec in an hour * 24 = 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.x_vel = 0
        self.y_vel = 0

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

    def draw(self, win):
        # this x, y is the center of the circle
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # we need at least two points to draw
        if len(self.orbit) > 2:
            # get a list of updated points which are the x and y coordinates to scale
            updated_position = []
            for position in self.orbit:
                x, y = position
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + WIDTH / 2
                updated_position.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_position, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            # have to use FONT object to create a text object (render) to render on screen
            # round and divide by 1000 to km to not massive
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km", 1, WHITE)
            # shifts it so that the text is exactly in the middle of the planets
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    # calculate the force of attraction between one object and another
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance

        # this is force of attraction which is that equation G*M*m/r^2
        force = self.G * self.mass * other.mass / distance ** 2
        # arctan to find the angle y/x
        theta = math.atan2(distance_y, distance_x)
        # find the components of force using the found theta value
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        # We're getting the total forces exerted on the planet by other celestial bodies
        total_force_x = total_force_y = 0
        for i in planets:
            # dont want to calculate force with itself
            if self == i:
                continue

            fx, fy = self.attraction(i)
            total_force_x += fx
            total_force_y += fy
        # 46 explanation
        self.x_vel += total_force_x / self.mass * self.TIMESTEP
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        # update the x and y position using the velocity that we just calcualted
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        # This is to draw the orbit
        self.orbit.append((self.x, self.y))




def main():
    run = True
    # limit framerate
    clock = pygame.time.Clock()

    sun = Planet(0,0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True

    mercury = Planet(.387 * Planet.AUnit, 0, 8, DARK_GREY, 3.30 * 10 ** 23)
    venus = Planet(.723 * Planet.AUnit, 0, 14, WHITE, 4.8685 * 10**24)
    earth = Planet(-1 * Planet.AUnit , 0, 16, BLUE, 5.8742 * 10**24) #-1 AU to the left

    mars = Planet(-1.524 * Planet.AUnit, 0, 12, RED, 6.39 * 10 **23)
    #jupitar = Planet()
    #saturn = Planet()
    #uranus = Planet()
    #neptune = Planet()

    # notice how if AU is positive vel is negative so everything is moving in the same direction
    mercury.y_vel = 47.4 * 1000
    venus.y_vel = 35.02 * 1000
    earth.y_vel = -29.783 * 1000
    mars.y_vel = -24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]
    while run:

        #60 fps
        clock.tick(60)
        # 0,0,0 is the color black
        # fill window black before displaying new planets
        WINDOW.fill((0, 0,  0))

        # all the events that occur but we just wanna check if quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i in planets:
            i.update_position(planets)
            i.draw(WINDOW)

        pygame.display.update()

    pygame.quit()

main()
