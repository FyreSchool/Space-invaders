import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title
pygame.display.set_caption("Space Invaders 2.0")

# Clock to control speed
clock = pygame.time.Clock()

# Player (Triangle)
player_x = 370
player_y = 480
player_x_change = 0

def draw_player(x, y):
    points = [(x, y), (x - 20, y + 40), (x + 20, y + 40)]
    pygame.draw.polygon(screen, (0, 255, 0), points)

# Grid parameters
grid_columns = 6
grid_cell_width = WIDTH // grid_columns
enemy_size = 35  # Size of the square enemy

# Function to initialize enemies
def initialize_enemies(num_of_enemies):
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_health = []  # New list to track health of each enemy
    
    for i in range(num_of_enemies):
        col = i % grid_columns
        row = i // grid_columns
        x_position = col * grid_cell_width + (grid_cell_width - enemy_size) // 2
        y_position = 50 + row * 50
        enemy_x.append(x_position)
        enemy_y.append(y_position)
        enemy_x_change.append(4)
        enemy_health.append(1)  # Initial health set to 1 (one bullet to destroy)
    
    return enemy_x, enemy_y, enemy_x_change, enemy_health

# Initial enemy setup
base_num_of_enemies = 6
current_num_of_enemies = base_num_of_enemies
enemy_x, enemy_y, enemy_x_change, enemy_health = initialize_enemies(current_num_of_enemies)

# Bullet (Oval)
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"  # "ready" means you can't see the bullet, "fire" means bullet is moving

def draw_bullet(x, y):
    pygame.draw.ellipse(screen, (0, 0, 255), (x, y, 10, 20))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Health system
player_health = 3
font = pygame.font.Font(None, 36)

def show_health(health):
    health_text = font.render(f'Health: {health}', True, (255, 255, 255))
    screen.blit(health_text, (10, 10))

# Score system
score = 0

def show_score(score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 150, 10))

# Threshold for increasing number of enemies
threshold_score = 2000

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # RGB - Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    player_x = max(0, min(player_x, WIDTH - 40))  # Keep player within screen bounds

   # Speed multiplier for enemies
    speed_multiplier = 0.8  # Initial speed multiplier

    # Check if score crosses the threshold to add more enemies and speed up
    if score >= threshold_score:
        current_num_of_enemies += 2  # Add 2 more enemies
        enemy_x, enemy_y, enemy_x_change, enemy_health = initialize_enemies(current_num_of_enemies)
    
        # Increase the speed of all enemies
        speed_multiplier += 0.2  # Adjust this value to change the speed increment
        enemy_x_change = [change * speed_multiplier for change in enemy_x_change]  # Scale existing speeds

        # Increase health of existing enemies
        enemy_health = [health + 1 for health in enemy_health]
    
        threshold_score += 2000  # Increment the threshold for next increase

    # Enemy movement and logic
    for i in range(current_num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= WIDTH - enemy_size:
            enemy_x_change[i] = -enemy_x_change[i]  # Change direction
            enemy_y[i] += 40  # Only this enemy drops when it hits the wall

        # Check if enemy goes past player
        if enemy_y[i] > player_y:
            player_health -= 1
            # Reset enemy position to its original grid cell
            col = i % grid_columns
            row = i // grid_columns
            enemy_x[i] = col * grid_cell_width + (grid_cell_width - enemy_size) // 2
            enemy_y[i] = 50 + row * 50

        # Collision detection
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            enemy_health[i] -= 1  # Reduce health by 1 on collision
    
            # If enemy's health reaches zero, reset its position and increment score
            if enemy_health[i] <= 0:
                score += 100  # Increment score by 100 for each enemy destroyed
                # Reset enemy position to its original grid cell
                col = i % grid_columns
                row = i // grid_columns
                enemy_x[i] = col * grid_cell_width + (grid_cell_width - enemy_size) // 2
                enemy_y[i] = 50 + row * 50
                enemy_health[i] = 1 + (score // 2000)  

        pygame.draw.rect(screen, (255, 0, 0), (enemy_x[i], enemy_y[i], enemy_size, enemy_size))

    # Bullet movement
    if bullet_state == "fire":
        draw_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    draw_player(player_x, player_y)
    show_health(player_health)
    show_score(score)  # Display the score
    pygame.display.update()

    # Control the frame rate
    clock.tick(40)

    # End game condition
    if player_health <= 0:
        running = False

def game_over_screen(score):
    game_over_font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 48)
    
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
    
    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height()))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
    
    pygame.display.update()
    
    # Keep displaying until user quits
    waiting = True 
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

game_over_screen(score)