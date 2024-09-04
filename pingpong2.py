import pygame, sys, random

# Function to reset the ball in the center and randomize the direction
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

# Function to update score when a point is won
def point_won(winner):
    global cpu_points, player_points

    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1

    reset_ball()

# Function to animate the ball
def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top or bottom screen boundaries
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    # CPU scores a point
    if ball.right >= screen_width:
        point_won("cpu")

    # Player scores a point
    if ball.left <= 0:
        point_won("player")

    # Ball collision with player or CPU paddles
    if ball.colliderect(player) or ball.colliderect(cpu):
        paddle_sound.play()  # Play paddle sound effect
        ball_speed_x *= -1
        # Optional: Add some randomness to ball speed when hit
        ball_speed_y += random.choice([-1, 1])

# Function to animate the player's paddle
def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

# Function to animate the CPU's paddle
def animate_cpu():
    global cpu_speed
    if ball.centery < cpu.centery:
        cpu_speed = -6
    elif ball.centery > cpu.centery:
        cpu_speed = 6
    else:
        cpu_speed = 0
    cpu.y += cpu_speed

    # Ensure CPU paddle stays within screen bounds
    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height

# Function to display the winning message
def display_winner(winner_text):
    winner_surface = winner_font.render(winner_text, True, "yellow")
    winner_rect = winner_surface.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(winner_surface, winner_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # Pause for 3 seconds before restarting the game

# Initialize pygame
pygame.init()

# Set up screen dimensions
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Pong Game!")

# Game clock
clock = pygame.time.Clock()

# Define the ball and paddles
ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)

cpu = pygame.Rect(0, 0, 20, 100)
cpu.centery = screen_height / 2

player = pygame.Rect(0, 0, 20, 100)
player.midright = (screen_width, screen_height / 2)

# Initial game variables
ball_speed_x = 10
ball_speed_y = 10
player_speed = 0
cpu_speed = 6

cpu_points, player_points = 0, 0
winning_score = 5

# Font for displaying scores and winner message
score_font = pygame.font.Font(None, 100)
winner_font = pygame.font.Font(None, 150)

# Initialize sound
pygame.mixer.init()

# Load background music and play it in a loop
pygame.mixer.music.load("8-bit-retro-game-music-233964.mp3")  # Replace with your own music file path
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load the paddle sound effect
paddle_sound = pygame.mixer.Sound("putting-coffee-mug-to-table-40507.mp3")  # Replace with your own sound file path

# Main game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed = 0

    # Update game objects
    animate_ball()
    animate_player()
    animate_cpu()

    # Check for a winner
    if cpu_points >= winning_score:
        display_winner("CPU Wins!")
        cpu_points, player_points = 0, 0  # Reset scores
        reset_ball()  # Reset the ball for a new game

    if player_points >= winning_score:
        display_winner("Player Wins!")
        cpu_points, player_points = 0, 0  # Reset scores
        reset_ball()  # Reset the ball for a new game

    # Clear the screen
    screen.fill('black')

    # Draw the score
    cpu_score_surface = score_font.render(str(cpu_points), True, "yellow")
    player_score_surface = score_font.render(str(player_points), True, "yellow")
    screen.blit(cpu_score_surface, (screen_width / 4, 20))
    screen.blit(player_score_surface, (3 * screen_width / 4, 20))

    # Draw the ball, paddles, and middle line
    pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.ellipse(screen, 'white', ball)
    pygame.draw.rect(screen, 'white', cpu)
    pygame.draw.rect(screen, 'cyan', player)

    # Update the display
    pygame.display.update()
    clock.tick(60)
