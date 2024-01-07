import time 
import pygame
import random
import sys

def generate_meteor(meteor_image):
    return {
        "mask": pygame.mask.from_surface(meteor_image),
        "x": random.choice(range(10, 440, 20)),
        "y": random.choice(range(-10, -500, -20))
    }

def place_laser(laser_img, x, y):
    return {
        "mask": pygame.mask.from_surface(laser_img),
        "x": x+15,
        "y": y-50
    }

def check_collision(mask1, mask2, mask1_coords, mask2_coords):
    x_off = mask2_coords[0] - mask1_coords[0]
    y_off = mask2_coords[1] - mask1_coords[1]
    if mask1.overlap(mask2, (x_off, y_off)):
        return True
    else: 
        return False

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/pozadie.jpg")
    ship = pygame.image.load("assets/vesmírna_loď.png")
    meteor_img = pygame.image.load("assets/meteorit.png")
    laser_img = pygame.image.load("assets/laser.png")
    game_font = pygame.font.SysFont("dejavuserif", 50)
    explosion = pygame.image.load("assets/vybuch.png")

    ship_mask = pygame.mask.from_surface(ship)
    laser_mask = pygame.mask.from_surface(laser_img)


    window = pygame.display.set_mode((500, 800))
    
    ship_coordinates_x=250
    ship_coordinates_y=700

    laser_reload_time = 1
    last_laser_shot_time = 0

    score=0
    meteors = []
    lasers = []
    laser_speed = 15
    meteor_speed=0
    meteor_increment=4
    meteor_count=0
    end = False



    while True:
        score_text = game_font.render(f"Score {score}", True, (255, 255, 255))

        if len(meteors) == 0: 
            meteor_speed += 1
            meteor_count += meteor_increment
            for i in range(meteor_count):
                meteors.append(generate_meteor(meteor_img))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if ship_coordinates_x > 2:
                ship_coordinates_x -= 5
        if keys[pygame.K_RIGHT]:
            if ship_coordinates_x < 440:
                ship_coordinates_x += 5

        if keys[pygame.K_UP]:
            # Speed up meteors
            for meteor in meteors[:]:
                meteor["y"] += 10

        if keys[pygame.K_SPACE]:
            # Shot laser
            current_seconds = time.time()

            if current_seconds > (last_laser_shot_time + laser_reload_time):
                lasers.append(place_laser(laser_img, ship_coordinates_x, ship_coordinates_y))
                last_laser_shot_time = current_seconds

        
        window.blit(bg, (0, 0))
        window.blit(ship, (ship_coordinates_x, ship_coordinates_y))

        if not end:
            for meteor in meteors[:]:
                # Add meteors on new positions
                window.blit(meteor_img, (meteor['x'], meteor['y']))
                meteor["y"] += meteor_speed
                if meteor["y"] > 800:
                    score += 1
                    meteors.remove(meteor)
                if check_collision(ship_mask, meteor['mask'], (ship_coordinates_x, ship_coordinates_y), (meteor['x'], meteor['y'])):
                    end=True


                # For each meteor and each laser check collision
                for laser in lasers[:]:
                    if check_collision(laser_mask, meteor['mask'], (laser['x'],laser["y"] ), (meteor['x'], meteor['y'])):
                        score += 2
                        window.blit(score_text, (150, 10))
                        window.blit(explosion, (meteor['x'], meteor['y']))
                        pygame.display.update()
                        time.sleep(0.05)
                        if meteor in meteors:
                            meteors.remove(meteor)
                        lasers.remove(laser)


            for laser in lasers[:]:
                window.blit(laser_img, (laser['x'], laser['y']))
                laser["y"] -= laser_speed
                if laser["y"] < 0:
                    lasers.remove(laser)
        
        if end:
            end_text = game_font.render(f"GAME OVER", True, (255, 255, 255))
            window.blit(end_text, (100, 400))

        window.blit(score_text, (150, 10))

        pygame.display.update()
        clock.tick(60)