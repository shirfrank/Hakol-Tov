import pygame
import random
import sounddevice as sd
import numpy as np
from scipy.fft import fft
import time

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pitch Perfect!")

# Colors
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Add this
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
HIGHLIGHT_COLORS = [(255, 128, 128), (128, 255, 128), (128, 128, 255), (255, 255, 128), (255, 128, 255), (128, 255, 255)]

# Frequencies for the segments
FREQUENCIES = [200, 300, 400, 500, 600, 700]

# Game Variables
sequence = []
player_sequence = []
level = 1
in_game = True
in_game_over = False
recording_started = False

# Audio Functions
def record_audio(duration=2, sample_rate=44100):
    """Record audio from the microphone."""
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")
    return audio.flatten()

def analyze_frequency(signal, sample_rate):
    """Analyze the dominant frequency in the signal using FFT."""
    fft_values = np.abs(fft(signal))[:len(signal) // 2]
    frequencies = np.linspace(0, sample_rate / 2, len(fft_values))
    dominant_frequency = frequencies[np.argmax(fft_values)]
    return dominant_frequency

def play_audio_for_segment(segment_index):
    """Play a tone for the specified segment."""
    duration = 0.5
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * FREQUENCIES[segment_index] * t)
    sd.play(tone, samplerate=sample_rate)
    sd.wait()

def replay_sequence():
    """Replay the current sequence with highlights and sounds."""
    for index in sequence:
        play_audio_for_segment(index)
        draw_circle(highlight_index=index)
        pygame.time.wait(1000)
        draw_circle(highlight_index=None)
        pygame.time.wait(300)

# Drawing Functions
def draw_circle(highlight_index=None, detected_frequency=None):
    """Draw the main circle divided into six segments."""
    screen.fill(WHITE)
    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    radius = 300
    border_radius = 310  # Slightly larger radius for the white border
    font = pygame.font.Font(None, 36)

    # Draw the segments
    for i in range(6):
        start_angle = i * 60
        end_angle = start_angle + 60
        color = HIGHLIGHT_COLORS[i] if highlight_index == i else COLORS[i]

        points = [
            center,
            (
                center[0] + radius * np.cos(np.radians(start_angle)),
                center[1] - radius * np.sin(np.radians(start_angle)),
            ),
            (
                center[0] + radius * np.cos(np.radians(end_angle)),
                center[1] - radius * np.sin(np.radians(end_angle)),
            ),
        ]

        border_points = [
            center,
            (
                center[0] + border_radius * np.cos(np.radians(start_angle)),
                center[1] - border_radius * np.sin(np.radians(start_angle)),
            ),
            (
                center[0] + border_radius * np.cos(np.radians(end_angle)),
                center[1] - border_radius * np.sin(np.radians(end_angle)),
            ),
        ]

        # Draw the segment border if highlighted
        if highlight_index == i:
            pygame.draw.polygon(screen, WHITE, border_points)

        # Draw the segment
        pygame.draw.polygon(screen, color, points)

        # Add the label
        angle = np.radians(start_angle + 30)
        label_x = center[0] + radius * 0.6 * np.cos(angle)
        label_y = center[1] - radius * 0.6 * np.sin(angle)
        label = font.render(str(i + 1), True, BLACK)
        screen.blit(label, (label_x - label.get_width() // 2, label_y - label.get_height() // 2))

    # Draw the current level
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (10, 10))



    # Draw Record Button
    record_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 67, 140, 50)
    pygame.draw.rect(screen, (154, 45, 181) if not recording_started else (209, 64, 245), record_button_rect)
    record_text = font.render("RECORD" if not recording_started else "RECORDING", True, WHITE)
    screen.blit(record_text, (record_button_rect.x + 20, record_button_rect.y + 10))

    # Draw Replay Button
    replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 123, 140, 50)
    pygame.draw.rect(screen, (163, 10, 148), replay_button_rect)
    replay_text = font.render("REPLAY", True, WHITE)
    screen.blit(replay_text, (replay_button_rect.x + 25, replay_button_rect.y + 10))

    # Display the detected frequency
    if detected_frequency is not None:
        freq_text = font.render(f"Detected Frequency: {detected_frequency:.2f} Hz", True, BLACK)
        screen.blit(freq_text, (SCREEN_WIDTH // 2 - freq_text.get_width() // 2, SCREEN_HEIGHT - 40))

    pygame.display.flip()
    return record_button_rect, replay_button_rect

def draw_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 64)
    title_text = font.render("Pitch Perfect!", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, GREEN, play_button_rect)
    play_text = font.render("PLAY", True, WHITE)
    screen.blit(play_text, (play_button_rect.x + 50, play_button_rect.y + 5))

    pygame.display.flip()
    return play_button_rect

def draw_game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 64)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, (163, 10, 148), replay_button_rect)
    replay_text = font.render("REPLAY", True, WHITE)
    screen.blit(replay_text, (replay_button_rect.x + 10, replay_button_rect.y + 5))

    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
    pygame.draw.rect(screen, (240, 62, 222), quit_button_rect)
    quit_text = font.render("QUIT", True, WHITE)
    screen.blit(quit_text, (quit_button_rect.x + 45, quit_button_rect.y + 5))

    pygame.display.flip()
    return replay_button_rect, quit_button_rect

def next_level():
    global sequence, current_index, recording_started, level
    if level > 1:  # Increment level only after the first level
        level += 1
    print(f"New sequence: {sequence}")
    sequence.append(random.randint(0, 5))  # Add a random segment (0-5)
    replay_sequence()  # Replay the full sequence
    current_index = 0  # Reset player's index
    recording_started = False


def map_frequency_to_bar(frequency):
    for i, (low, high) in enumerate([(150, 250), (250, 350), (350, 450), (450, 550), (550, 650), (650, 750)]):
        if low <= frequency < high:
            return i
    return None  # No match


def display_message(text, color, duration=2):
    """Display a message on the screen for a short duration."""
    font = pygame.font.Font(None, 64)
    message = font.render(text, True, color)

    # Position the message slightly above the center to overlap the shape
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    message_x = center_x - message.get_width() // 2
    message_y = center_y - 310  # Adjust to position the message above the shape

    screen.blit(message, (message_x, message_y))
    pygame.display.flip()
    pygame.time.wait(int(duration * 1000))


# Initialize Variables
running = True  # Main game loop control
in_start_screen = True
in_game = False
in_game_over = False
current_index = 0  # Index of the sequence the player is currently repeating
level = 1  # Reset level to 1
detected_frequency = None  # To store detected frequency for display

while running:
    if in_start_screen:
        play_button_rect = draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    # Reset the game variables for a new game
                    sequence = []
                    current_index = 0
                    level = 1  # Reset level to 1
                    detected_frequency = None  # Clear detected frequency
                    in_start_screen = False
                    in_game = True
                    next_level()  # Start the first level

    elif in_game:
        record_button_rect, replay_button_rect = draw_circle(highlight_index=None, detected_frequency=detected_frequency)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if record_button_rect.collidepoint(event.pos) and not recording_started:
                    recording_started = True
                    print("Recording started!")
                    recorded_signal = record_audio(duration=2)
                    detected_frequency = analyze_frequency(recorded_signal, 44100)
                    print(f"Detected Frequency: {detected_frequency:.2f} Hz")

                    detected_index = map_frequency_to_bar(detected_frequency)

                    if detected_index is not None:
                        print(f"Detected Segment: {detected_index + 1}")
                        draw_circle(highlight_index=detected_index, detected_frequency=detected_frequency)  # Highlight matched segment
                        pygame.time.wait(1000)  # Pause to show the highlight
                        draw_circle(highlight_index=None, detected_frequency=detected_frequency)  # Reset highlights

                        if detected_index == sequence[current_index]:
                            display_message(f"Correct Match! Segment {current_index + 1}", GREEN)
                            current_index += 1
                            if current_index == len(sequence):
                                print ("Sequence complete! Proceeding to the next level.")
                                next_level()
                        else:
                            print(f"Wrong match for segment {current_index + 1}.")
                            detected_frequency = None  # Clear detected frequency
                            in_game = False
                            in_game_over = True
                    else:
                        print("No matching segment detected!")
                        detected_frequency = None  # Clear detected frequency
                        in_game = False
                        in_game_over = True

                    recording_started = False  # Allow for the next interaction
                elif replay_button_rect.collidepoint(event.pos):
                    print("Replaying sequence!")
                    replay_sequence()

    elif in_game_over:
        replay_button_rect, quit_button_rect = draw_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if replay_button_rect.collidepoint(event.pos):
                    # Reset the game variables
                    sequence = []
                    current_index = 0
                    level = 1  # Reset level to 1
                    detected_frequency = None  # Clear detected frequency
                    in_game_over = False
                    in_game = True
                    next_level()  # Restart the game
                elif quit_button_rect.collidepoint(event.pos):
                    running = False

pygame.quit()
