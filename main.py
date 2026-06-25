import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event, log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize Pygame
    pygame.init()

    # Create GUI
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    # Create Groups
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    # Add Asteroid class to Group
    Asteroid.containers = (asteroids, updatable, drawable)

    # Add AsteroidField class to Group
    AsteroidField.containers = (updatable)

    asteroidfields = AsteroidField()

    # Add Shot class to Group
    Shot.containers = (shots, drawable, updatable)

    # Add Player class to Groups (before player object instantiated)
    Player.containers = (updatable, drawable)

    # Create Player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Begin Game Loop
    while True:   
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        screen.fill("black")     

        for sprite in drawable:
            sprite.draw(screen)   
         
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        # print(dt)                

if __name__ == "__main__":
    main()
