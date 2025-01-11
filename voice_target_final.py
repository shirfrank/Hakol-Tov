import pygame
import pyaudio
import numpy as np
import math
import time

# Graphic settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Voice Target")
clock = pygame.time.Clock()

# Global variables
pull_distance = 0
running = True
is_stretching = False
current_target = 0
success_count = 0
hold_time = 0
required_hold_time = 2  # Initial hold time in seconds
start_time = None

# Thresholds
DB_THRESHOLD = 100  # Restored to original threshold for movement
START_THRESHOLD = 100  # Restored to original threshold to start each level

# Generate infinite targets
targets = [(100 + i * 100, SCREEN_HEIGHT // 2) for i in range(1000)]
slingshot_x, slingshot_y = 50, SCREEN_HEIGHT // 2
falling = False
fall_speed = 3  # Reduced fall speed

# New global variables
next_level_displaying = False
level_started = False  # Flag to check if the level has started

def save_score(score):
    """Save the score to a file for integration with the leaderboard."""
    with open("voice_target_leaderboard.json", "w") as score_file:
        json.dump({"score": score}, score_file)


def listen_for_ah():
    global pull_distance, is_stretching, current_target, running, success_count, hold_time, start_time, required_hold_time, falling, level_started
    is_stretching = False
    silent_start_time = None
    audio = pyaudio.PyAudio()

    # Open the microphone stream
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    try:
        while running:
            data = np.frombuffer(stream.read(1024), dtype=np.int16)
            volume = np.linalg.norm(data)
            db = 20 * math.log10(volume) if volume > 0 else 0

            if db > DB_THRESHOLD:
                print("Sound detected above threshold!")
                if not level_started:
                    start_time = time.time()
                    level_started = True  # Mark the level as started

                is_stretching = True
                silent_start_time = None

                # Update ball movement
                pull_distance += 1  # Simplified constant movement
                print(f"Updated pull_distance: {pull_distance}")

                target_x, _ = targets[current_target]

                # Calculate the position of the ball based on slingshot_x and pull_distance
                ball_x_position = slingshot_x + pull_distance

                print(
                    f"Slingshot position: {slingshot_x}, pull distance: {pull_distance}, target position: {target_x}, ball position: {ball_x_position}")

                # Ensure ball continues moving forward, even after passing the target
                if ball_x_position < slingshot_x:
                    print(f"Warning: ball is moving backwards! Correcting.")
                    pull_distance = max(pull_distance, 0)  # Ensure the ball does not move backward

                # Check if the ball has reached or passed the target
                if ball_x_position >= target_x:
                    print("Target reached!")
                    pull_distance = 0  # We can safely reset after passing the target
                    falling = False
                    current_target += 1
                    success_count += 1
                    required_hold_time += 1
                    next_level_screen()  # Show next level screen
                else:
                    # Prevent falling if the ball is near the target
                    if ball_x_position > target_x - 20 and ball_x_position < target_x + 20:
                        # Keep the ball in "stretching" state close to the target to avoid accidental fall
                        print("Ball is near target, not falling yet.")
                        falling = False

                    # Prevent pulling distance from going back or off-screen
                    if ball_x_position < slingshot_x:
                        print(f"Warning: ball is moving backwards! Correcting.")
                        pull_distance = 0  # Stop the ball from moving backwards
                        print(f"Corrected pull_distance: {pull_distance}")

            else:
                if silent_start_time is None:
                    silent_start_time = time.time()
                elif time.time() - silent_start_time > 2:  # Allow for 2 seconds of silence before falling
                    print("Sound stopped for too long. Ball is falling!")
                    reset_after_fail()
                    silent_start_time = None
                is_stretching = False

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def show_splash_screen():
    """Displays a splash screen with the game's title, logo (target), and start button."""
    font_title = pygame.font.Font(None, 74)
    font_button = pygame.font.Font(None, 48)

    # Title text
    title_text = font_title.render("Voice Target", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    # Start button text
    start_text = font_button.render("Start", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))  # הורדנו את כפתור ה-"Start" למטה

    # Draw the target logo (bullseye) as a circle with concentric circles
    target_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # מיקום המטרה
    target_radius = 100

    while True:
        screen.fill(WHITE)

        # Draw the target logo
        pygame.draw.circle(screen, RED, target_center, target_radius)  # Outer circle (Red)
        pygame.draw.circle(screen, WHITE, target_center, target_radius - 20)  # Inner circle (White)
        pygame.draw.circle(screen, RED, target_center, target_radius - 40)  # Inner circle (Red)

        # Display title and start button
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, RED, start_rect.inflate(20, 20))  # Draw button rectangle
        screen.blit(start_text, start_rect)  # Display start button text

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return  # Exit splash screen and start the game

def next_level_screen():
    """Displays a 'Next Level' screen for 3 seconds without blinking."""
    global next_level_displaying
    next_level_displaying = True  # Set the flag to indicate next level screen is showing
    font = pygame.font.Font(None, 74)
    text = font.render("Next Level!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    start_ticks = pygame.time.get_ticks()  # Start time for 3 seconds display

    # Display the message for 3 seconds
    while pygame.time.get_ticks() - start_ticks < 3000:  # 3000 ms = 3 seconds
        screen.fill(WHITE)  # Clear the screen
        screen.blit(text, text_rect)  # Draw the text
        pygame.display.update()
        clock.tick(30)  # Ensure the frame rate is consistent

    next_level_displaying = False  # Reset flag after 3 seconds

def draw_background():
    """Draws a gradient background."""
    for y in range(SCREEN_HEIGHT):
        color = (
            int(135 + (120 * y / SCREEN_HEIGHT)),
            int(206 + (49 * y / SCREEN_HEIGHT)),
            int(250 + (5 * y / SCREEN_HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

def draw_target():
    """Draws the current target as a bullseye."""
    if current_target < len(targets):
        target_x, target_y = targets[current_target]
        pygame.draw.circle(screen, RED, (target_x, target_y), 30)
        pygame.draw.circle(screen, WHITE, (target_x, target_y), 20)
        pygame.draw.circle(screen, RED, (target_x, target_y), 10)

def draw_slingshot():
    """Draws the slingshot stone based on pull_distance."""
    base_x = slingshot_x + pull_distance
    base_y = slingshot_y
    pygame.draw.circle(screen, RED, (base_x, base_y), 10)

def draw_success_count():
    """Draws the number of successes and required hold time on the screen."""
    font = pygame.font.Font(None, 36)
    success_text = font.render(f"Successes: {success_count}", True, BLACK)
    hold_text = font.render(f"Hold Time: {int(required_hold_time)} sec", True, BLACK)
    screen.blit(success_text, (10, 10))
    screen.blit(hold_text, (10, 50))

def update_falling():
    """Handles the falling animation if the player fails."""
    global slingshot_y, falling
    if falling:
        slingshot_y += fall_speed
        if slingshot_y > SCREEN_HEIGHT:
            falling = False
            game_over_screen()

def reset_after_fail():
    """Starts the falling animation and resets the game state."""
    global pull_distance, falling
    falling = True
    pull_distance = 0


import threading

# Define a global variable to check if there's an active thread
listen_thread = None


def reset_game():
    """Resets the game variables to their initial state and starts the game again."""
    global pull_distance, is_stretching, current_target, success_count, hold_time, required_hold_time, start_time, falling, level_started
    global slingshot_x, slingshot_y, targets  # Ensure slingshot and targets are reset

    # Reset game variables
    pull_distance = 0
    is_stretching = False
    current_target = 0
    success_count = 0
    hold_time = 0
    required_hold_time = 2  # Reset hold time to 2 seconds
    start_time = None
    falling = False
    level_started = False  # Reset the level flag
    next_level_displaying = False  # Ensure "Next Level" screen is not showing

    # Reset the slingshot position to the left and the target to the center
    slingshot_x, slingshot_y = 50, SCREEN_HEIGHT // 2  # Starting position of the slingshot
    targets = [(100 + i * 100, SCREEN_HEIGHT // 2) for i in range(1000)]  # Reset targets for new game

    # Stop the previous listening thread if it's active
    global listen_thread
    if listen_thread and listen_thread.is_alive():
        listen_thread.join()

    # Start a new listening thread for the sound
    listen_thread = threading.Thread(target=listen_for_ah, daemon=True)
    listen_thread.start()


def game_over_screen():
    """Displays a Game Over screen with 'Quit' and 'Try Again' buttons."""
    print("Game Over Screen Displayed")
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(text, text_rect)

    # Create the 'Quit' button
    quit_button = pygame.Rect(SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2, 200, 50)
    quit_text = font.render("Quit", True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)

    # Create the 'Try Again' button with larger width
    try_again_button = pygame.Rect(3 * SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2, 250, 50)  # Increased width
    try_again_text = font.render("Try Again", True, WHITE)
    try_again_text_rect = try_again_text.get_rect(center=try_again_button.center)

    pygame.draw.rect(screen, RED, quit_button)
    pygame.draw.rect(screen, RED, try_again_button)
    screen.blit(quit_text, quit_text_rect)
    screen.blit(try_again_text, try_again_text_rect)

    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                elif try_again_button.collidepoint(event.pos):
                    reset_game()  # Reset the game state
                    return  # Continue the game from the reset state


def main():
    global running, next_level_displaying, level_started

    show_splash_screen()  # Show the splash screen before the game starts

    threading.Thread(target=listen_for_ah, daemon=True).start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not next_level_displaying:  # Only draw game elements when "Next Level" screen isn't showing
            # Draw the screen
            draw_background()
            draw_target()
            draw_slingshot()
            draw_success_count()
            update_falling()

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    final_score = main()
    print(f"Final Score: {final_score}")
