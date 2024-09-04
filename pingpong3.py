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

    # Ball collision with left or right screen boundaries
    if ball.right >= screen_width or ball.left <= 0:
        ball_speed_x *= -1

    # CPU scores a point
    if ball.bottom >= screen_height:
        point_won("cpu")

    # Player scores a point
    if ball.top <= 0:
        point_won("player")

    # Ball collision with player or CPU paddles
    if ball.colliderect(player) or ball.colliderect(cpu):
        paddle_sound.play()  # Play paddle sound effect
        ball_speed_y *= -1
        # Optional: Add some randomness to ball speed when hit
        ball_speed_x += random.choice([-1, 1])

# Function to animate the player's paddle
def animate_player():
    player.x += player_speed

    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

# Function to animate the CPU's paddle
def animate_cpu():
    global cpu_speed
    if ball.centerx < cpu.centerx:
        cpu_speed = -6
    elif ball.centerx > cpu.centerx:
        cpu_speed = 6
    else:
        cpu_speed = 0
    cpu.x += cpu_speed

    # Ensure CPU paddle stays within screen bounds
    if cpu.left <= 0:
        cpu.left = 0
    if cpu.right >= screen_width:
        cpu.right = screen_width

# Function to display the winning message
def display_winner(winner_text):
    winner_surface = winner_font.render(winner_text, True, "yellow")
    winner_rect = winner_surface.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(winner_surface, winner_rect)
    pygame.display.update()
    pygame.time.delay(5000)  # Pause for 3 seconds before restarting the game

# Initialize pygame
pygame.init()

# Set up screen dimensions (swapped for vertical orientation)
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vertical Pong Game!")

# Game clock
clock = pygame.time.Clock()

# Define the ball
ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)

# Create rectangles for paddles
player = pygame.Rect(screen_width / 2 - 50, 10, 50, 20)  # Player paddle at the top
cpu = pygame.Rect(screen_width / 2 - 50, screen_height - 30, 50, 20)  # CPU paddle at the bottom

# Initial game variables
ball_speed_x = 10
ball_speed_y = 10
player_speed = 0
cpu_speed = 6

cpu_points, player_points = 0, 0
winning_score = 15

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
            if event.key == pygame.K_LEFT:
                player_speed = -6
            if event.key == pygame.K_RIGHT:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_speed = 0

    # Update game objects
    animate_ball()
    animate_player()
    animate_cpu()

    # Check for a winner
    if cpu_points >= winning_score:
        display_winner("")
        cpu_points, player_points = 0, 0  # Reset scores
        reset_ball()  # Reset the ball for a new game

    if player_points >= winning_score:
        display_winner("")
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
    pygame.draw.aaline(screen, 'white', (0, screen_height / 2), (screen_width, screen_height / 2))
    pygame.draw.ellipse(screen, 'white', ball)
    pygame.draw.rect(screen, 'cyan', player)
    pygame.draw.rect(screen, 'white', cpu)

    # Update the display
    pygame.display.update()
    clock.tick(60)
