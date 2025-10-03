import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Microjuego Plataformero")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Estados del juego
START_SCREEN = 0
GAME_SCREEN = 1
game_state = START_SCREEN

# Jugador
player = pygame.Rect(400, 1100, 50, 50)
player_vel_y = 0
jump_power = 0
charging_jump = False
on_ground = False

# Plataformas
platforms = [
    pygame.Rect(300, 1150, 200, 20),
    pygame.Rect(100, 950, 200, 20),
    pygame.Rect(500, 750, 200, 20),
    pygame.Rect(300, 550, 200, 20),
    pygame.Rect(100, 350, 200, 20),
    pygame.Rect(500, 150, 200, 20)  # Plataforma final
]

# Plataforma movediza
moving_platform = pygame.Rect(100, 1050, 200, 20)
moving_direction = 1

def draw_start_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 60)
    text = font.render("Presiona ESPACIO para comenzar", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

def draw_game_screen():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
    pygame.draw.rect(screen, RED, moving_platform)
    if charging_jump:
        pygame.draw.rect(screen, BLACK, (player.x, player.y - 20, jump_power, 10))

def handle_player_movement():
    global player_vel_y, on_ground
    player.y += player_vel_y
    player_vel_y += 1  # gravedad

    on_ground = False
    for plat in platforms + [moving_platform]:
        if player.colliderect(plat) and player_vel_y >= 0:
            player.bottom = plat.top
            player_vel_y = 0
            on_ground = True

def update_moving_platform():
    global moving_direction
    moving_platform.x += moving_direction * 2
    if moving_platform.left <= 0 or moving_platform.right >= WIDTH:
        moving_direction *= -1

def check_win_condition():
    return player.colliderect(platforms[-1])

# Bucle principal
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START_SCREEN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = GAME_SCREEN

        elif game_state == GAME_SCREEN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    charging_jump = True
                    jump_power = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and charging_jump:
                    player_vel_y = -jump_power // 5
                    charging_jump = False

    if game_state == GAME_SCREEN:
        if charging_jump and jump_power < 100:
            jump_power += 2
        handle_player_movement()
        update_moving_platform()
        if check_win_condition():
            print("¡Has ganado!")
            running = False
        draw_game_screen()
    else:
        draw_start_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()