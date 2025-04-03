import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
START_BUTTON_COLOR = (135, 171, 105)
PILLAR_COLOR = (34, 139, 34)  # Green color for pillars

# Load Assets
background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

game_over_img = pygame.image.load("game_over.png")
game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (50, 35))

welcome_img = pygame.image.load("welcome.png")
welcome_img = pygame.transform.scale(welcome_img, (WIDTH, HEIGHT))

coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (20, 20))

# Fonts
font = pygame.font.Font(None, 50)

# Button Properties
button_width, button_height = 250, 100
button_x, button_y = WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50
play_again_x, play_again_y = WIDTH - 300, HEIGHT // 2 + 100

# High Score
high_score = 0

def game_loop():
    bird_x, bird_y = 50, HEIGHT // 2
    gravity = 0.5
    velocity = 0
    pipe_width = 70
    pipe_gap = 200
    pipe_x = WIDTH
    pipe_height = random.randint(150, HEIGHT - 300)
    score = 0
    level = 1
    pipe_speed = 5
    coin_x = pipe_x + pipe_width // 2 - 10
    coin_y = pipe_height + pipe_gap // 2 - 10
    coin_collected = False
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.blit(background_img, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                velocity = -8

        velocity += gravity
        bird_y += velocity
        pipe_x -= pipe_speed
        coin_x -= pipe_speed

        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(150, HEIGHT - 300)
            score += 1
            coin_x = pipe_x + pipe_width // 2 - 10
            coin_y = pipe_height + pipe_gap // 2 - 10
            coin_collected = False
            
            if score % 5 == 0:
                level += 1
                pipe_speed += 1
                if pipe_gap > 130:
                    pipe_gap -= 10
        
        pygame.draw.rect(screen, PILLAR_COLOR, (pipe_x, 0, pipe_width, pipe_height))
        pygame.draw.rect(screen, PILLAR_COLOR, (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT))
        screen.blit(bird_img, (bird_x, bird_y))
        
        if not coin_collected:
            screen.blit(coin_img, (coin_x, coin_y))
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        
        if bird_y <= 0 or bird_y >= HEIGHT or (
            pipe_x < bird_x + 50 < pipe_x + pipe_width and (bird_y < pipe_height or bird_y > pipe_height + pipe_gap)
        ):
            running = False
        
        bird_rect = pygame.Rect(bird_x, bird_y, 50, 35)
        coin_rect = pygame.Rect(coin_x, coin_y, 20, 20)
        
        if bird_rect.colliderect(coin_rect) and not coin_collected:
            score += 5
            coin_collected = True

        pygame.display.update()
        clock.tick(30)

game_loop()
