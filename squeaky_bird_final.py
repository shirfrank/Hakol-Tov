import pygame
import sys
import random
import pyaudio
import numpy as np
import math
import json

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game constants
GRAVITY = 0.5
FLAP_STRENGTH = -8  # Slightly decreased flap strength
COLUMN_SPEED = 4
COLUMN_GAP = 200  # Increased gap to make the game easier

# Load assets (replace with your file paths)
BACKGROUND_IMAGE = r"C:\Users\97254\OneDrive - mail.tau.ac.il\שולחן העבודה\לימודים\שנה ד\hackathon\bg2.png"
BIRD_IMAGE = r"C:\Users\97254\OneDrive - mail.tau.ac.il\שולחן העבודה\לימודים\שנה ד\hackathon\bird2.png"
COLUMN_IMAGE = r"C:\Users\97254\OneDrive - mail.tau.ac.il\שולחן העבודה\לימודים\שנה ד\hackathon\column.png"

# Load images
background = pygame.image.load(BACKGROUND_IMAGE)
bird_image = pygame.image.load(BIRD_IMAGE)
column_image = pygame.image.load(COLUMN_IMAGE)

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_image = pygame.transform.scale(bird_image, (30, 20))  # Adjust size as needed
column_image = pygame.transform.scale(column_image, (80, 500))  # Adjust size as needed


# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Squeaky Bird")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Constants for microphone input
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Format of the audio stream
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (samples per second)

# Setup PyAudio to capture audio from the microphone
p = pyaudio.PyAudio()

# Function to calculate the dB level from audio data
def get_decibel_level(data):
    audio_data = np.frombuffer(data, dtype=np.int16)

    if len(audio_data) == 0:
        return 0

    audio_data = audio_data / 32768.0
    rms = np.sqrt(np.mean(np.square(audio_data)))

    return 20 * math.log10(rms) + 64 if rms > 0 else 0

# Bird class
class Bird:
    def __init__(self):
        self.x = 100  # Keep the same position
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = bird_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect)

# Column class
class Column:
    def __init__(self, x):
        self.x = x
        self.gap_height = random.randint(200, 250)
        self.top_height = random.randint(100, SCREEN_HEIGHT - self.gap_height - 100)
        self.passed = False  # To track if the bird has passed the column

        self.top_rect = column_image.get_rect(midbottom=(self.x, self.top_height))
        self.bottom_rect = column_image.get_rect(midtop=(self.x, self.top_height + self.gap_height))

    def update(self):
        self.x -= COLUMN_SPEED
        self.top_rect.midbottom = (self.x, self.top_height)
        self.bottom_rect.midtop = (self.x, self.top_height + self.gap_height)

    def draw(self):
        screen.blit(column_image, self.top_rect)
        screen.blit(pygame.transform.flip(column_image, False, True), self.bottom_rect)

    def is_off_screen(self):
        return self.x < -column_image.get_width()

    def collides_with(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

    def pass_column(self, bird, score):
        # Check if the bird has passed the column
        if not self.passed and bird.x > self.x + column_image.get_width():
            self.passed = True
            return score + 1
        return score

def track_max_decibels(db_level, max_db_list):
    """Track maximum decibels on each flap."""
    if db_level > THRESHOLD_DB:
        max_db_list.append(db_level)  # Store the decibel value if it's a jump

def calculate_average_decibels(max_db_list):
    """Calculate the average of the maximum decibels."""
    if len(max_db_list) > 0:
        return sum(max_db_list) / len(max_db_list)
    return 0  # Avoid division by zero if there are no jumps

def game_over_screen(score, columns, background, average_db):
    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, 400, 100, 50)  # Left button
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, 400, 100, 50)  # Right button

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    avg_db_text = small_font.render(f"Average jump dB: {int(average_db)}", True, WHITE)

    while True:
        screen.blit(background, (0, 0))

        # Draw the columns in their last positions
        for column in columns:
            column.draw()

        # Draw "Game Over" and score text
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        screen.blit(avg_db_text, (SCREEN_WIDTH // 2 - avg_db_text.get_width() // 2, 350))  # Display avg dB

        # Draw retry and quit buttons
        pygame.draw.rect(screen, BLACK, retry_button)
        pygame.draw.rect(screen, BLACK, quit_button)
        retry_text = small_font.render("Retry", True, WHITE)
        quit_text = small_font.render("Quit", True, WHITE)
        screen.blit(retry_text, (retry_button.centerx - retry_text.get_width() // 2, retry_button.centery - retry_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return True  # Retry the game
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        clock.tick(30)


def save_score(score):
    """Save the score to a file for integration with the leaderboard."""
    with open("squeaky_bird_leaderboard.json", "w") as score_file:
        json.dump({"score": score}, score_file)

def show_start_screen():
    bird = Bird()  # Create the bird instance for the start screen
    bird.image = pygame.transform.scale(bird_image, (60, 40))  # Make the bird bigger for the start screen
    bird.x = SCREEN_WIDTH // 2 - 10  # Move the bird 10 pixels to the left
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 150, 100, 50)  # Adjust start button position

    # Load the logo
    logo = pygame.image.load(r"C:\Users\97254\OneDrive - mail.tau.ac.il\שולחן העבודה\לימודים\שנה ד\hackathon\logo2.png")

    running = True
    start_time = pygame.time.get_ticks()

    while running:
        screen.fill((0, 0, 0))  # Fill screen with black
        screen.blit(background, (0, 0))

        # Draw the logo at the top
        screen.blit(logo, (SCREEN_WIDTH // 2 - logo.get_width() // 2, 20))

        # Calculate delta time (time passed since the start screen began)
        delta_time = pygame.time.get_ticks() - start_time

        # Make the bird float up and down slowly using sine wave
        bird.y = SCREEN_HEIGHT // 2 + 30 * math.sin(0.005 * delta_time)  # Floating behavior
        bird.rect.center = (bird.x, bird.y)

        # Draw the bird with the floating effect
        bird.draw()

        # Draw start button
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Start", True, (255, 255, 255))
        screen.blit(text, (start_button.centerx - text.get_width() // 2, start_button.centery - text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  # Start the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start
                    return

        clock.tick(30)  # Limit frame rate to 30 FPS

# Function to draw the decibel meter (Speedometer-style)

def draw_decibel_meter(db_level, center, radius):
    # Draw the arc (half-circle) mirrored to the top
    start_angle = math.radians(0)  # Start at the left (top of the arc)
    end_angle = math.radians(180)  # End at the right (top of the arc)
    arc_width = 20
    pygame.draw.arc(screen, BLACK, [center[0] - radius, center[1] - radius, 2 * radius, 2 * radius],
                    start_angle, end_angle, arc_width)

    # Draw the mirrored needle (pointing downwards from the top of the arc)
    needle_angle = math.radians(180 + (db_level / 100 * 180))  # Inverted angle so needle points down
    needle_length = radius - 10
    needle_x = center[0] + needle_length * math.cos(needle_angle)
    needle_y = center[1] + needle_length * math.sin(needle_angle)  # Needle moves down as db increases
    pygame.draw.line(screen, RED, center, (needle_x, needle_y), 4)

    # Optionally, label the decibel value
    font = pygame.font.Font(None, 24)
    db_text = font.render(f"dB: {int(db_level)}", True, BLACK)
    screen.blit(db_text, (center[0] - db_text.get_width() // 2, center[1] - radius - 20))


# Main game loop
def main(threshold_db=40):
    show_start_screen()

    while True:
        global THRESHOLD_DB
        THRESHOLD_DB = threshold_db

        # New position for the meter (center coordinates)
        meter_center = (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 10)  # Move to center of screen
        meter_radius = 42  # Set the size of the meter

        bird = Bird()
        columns = [Column(SCREEN_WIDTH + i * 200) for i in range(3)]
        score = 0

        # List to store the maximum decibels on each jump
        max_db_list = []

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        running = True

        while running:
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            data = stream.read(CHUNK)
            db_level = get_decibel_level(data)

            # Track maximum decibels on each flap (jump)
            track_max_decibels(db_level, max_db_list)

            if db_level > THRESHOLD_DB:
                bird.flap()

            bird.update()
            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                running = False

            for column in columns:
                column.update()
                if column.is_off_screen():
                    columns.remove(column)
                    new_column_x = columns[-1].x + random.randint(150, 250)
                    columns.append(Column(new_column_x))
                # Check if the bird passes the column and update score
                score = column.pass_column(bird, score)
                if column.collides_with(bird):
                    running = False

            bird.draw()
            for column in columns:
                column.draw()

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Draw the decibel meter at the new position
            draw_decibel_meter(db_level, meter_center, meter_radius)

            pygame.display.flip()
            clock.tick(30)

        stream.stop_stream()
        stream.close()

        # Calculate the average of the maximum decibels
        average_db = calculate_average_decibels(max_db_list)

        # Save the score
        save_score(score)

        # Show the game over screen with the average decibel level
        if not game_over_screen(score, columns, background, average_db):
            break

if __name__ == "__main__":
    main(threshold_db=40)
