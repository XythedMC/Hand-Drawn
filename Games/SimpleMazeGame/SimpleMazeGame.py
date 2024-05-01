import pygame
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.handTrackerWrapper import HandTrackerWrapper
from Games.SimpleMazeGame.maze_levels import LEVEL_1, LEVEL_2, LEVEL_3

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAZE_GRID_SIZE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
END = (255, 0, 0)

def run_maze_game():
    # Initialize Pygame with hardware acceleration
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize the hand tracker
    hand_tracker = HandTrackerWrapper()

    # Set the starting position for the player
    player_radius = MAZE_GRID_SIZE // 4
    player = pygame.Rect(0, 0, player_radius * 2, player_radius * 2)

    # Initialize the cursor
    cursor_radius = 10
    player_cursor_color = GREEN
    hand_cursor_color = BLUE
    hand_cursor = pygame.Rect(0, 0, cursor_radius * 2, cursor_radius * 2)

    # Initialize the last valid hand position
    last_valid_hand_position = hand_cursor.topleft

    # Flag to indicate if the player cursor is connected to the hand cursor
    player_connected = True

    # Flag to indicate if the player reached the end
    reached_end = False

    # Game loop
    clock = pygame.time.Clock()
    running = True

    def load_level(level):
        maze_grid = [list(row) for row in level]
        for row in range(len(maze_grid)):
            for col in range(len(maze_grid[row])):
                if maze_grid[row][col] == 2:
                    start_row, start_col = row, col
                    player.x = col * MAZE_GRID_SIZE
                    player.y = row * MAZE_GRID_SIZE
                    hand_cursor.topleft = (start_col * MAZE_GRID_SIZE, start_row * MAZE_GRID_SIZE)  # Reset hand cursor position to the start
                    maze_grid[row][col] = 0  # Set the starting position to an open path
        return maze_grid, start_row, start_col

    maze_levels = [LEVEL_1, LEVEL_2, LEVEL_3, ]
    current_level = 0

    maze_grid, start_row, start_col = load_level(maze_levels[current_level])

    while running:
        # Only update the screen if necessary
        dirty_rects = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update hand information
        hand_tracker.update_hands_list()

        # Move player_grid_x and player_grid_y calculations outside the loop
        player_grid_x = int(player.centerx / MAZE_GRID_SIZE)
        player_grid_y = int(player.centery / MAZE_GRID_SIZE)

        # Reset player position if the level is completed
        if reached_end:
            player.center = (start_col * MAZE_GRID_SIZE + MAZE_GRID_SIZE // 2, start_row * MAZE_GRID_SIZE + MAZE_GRID_SIZE // 2)
            reached_end = False
            player_connected = False  # Disconnect player cursor from hand cursor

        # Iterate over detected hands
        for hand in hand_tracker.hands_list:
            if hand:
                hand_x = hand.getLandmarkX(HandLM.INDEX_FINGER_TIP)
                hand_y = hand.getLandmarkY(HandLM.INDEX_FINGER_TIP)

                # Update cursor position to match hand landmark
                hand_cursor.center = (hand_x, hand_y)

                # Translate hand cursor position to maze grid resolution
                hand_grid_x = int(hand_cursor.centerx / MAZE_GRID_SIZE)
                hand_grid_y = int(hand_cursor.centery / MAZE_GRID_SIZE)

                # Check if the hand cursor is inside the maze grid boundaries
                if 0 <= hand_grid_y < len(maze_grid) and 0 <= hand_grid_x < len(maze_grid[0]):
                    # Check if the hand cursor is inside a wall
                    if maze_grid[hand_grid_y][hand_grid_x] == 1:
                        # Reset hand cursor position to the last valid position
                        hand_cursor.topleft = last_valid_hand_position
                        player_connected = False
                    else:
                        # Update the last valid hand position
                        last_valid_hand_position = hand_cursor.topleft

                        # Check for overlap and reconnect
                        player_rect = pygame.Rect(player.centerx - player_radius, player.centery - player_radius,
                                                   player_radius * 2, player_radius * 2)
                        if player_rect.colliderect(hand_cursor):
                            player_connected = True

                        # Set the position of the player cursor to the hand cursor position if connected
                        if player_connected:
                            player.center = hand_cursor.center

        # Check if the player cursor is inside a wall
        if 0 <= player_grid_y < len(maze_grid) and 0 <= player_grid_x < len(maze_grid[0]):
            if maze_grid[player_grid_y][player_grid_x] == 1:
                # Stop the player cursor when it hits a wall
                player_connected = False

            # Check if the player reached the end
            if maze_grid[player_grid_y][player_grid_x] == 3:
                reached_end = True

        # Draw the entire maze, player, and cursors
        screen.fill(WHITE)
        for row in range(len(maze_grid)):
            for col in range(len(maze_grid[0])):
                if maze_grid[row][col] == 1:
                    pygame.draw.rect(screen, RED, (col * MAZE_GRID_SIZE, row * MAZE_GRID_SIZE, MAZE_GRID_SIZE, MAZE_GRID_SIZE))
                elif maze_grid[row][col] == 3:
                    pygame.draw.circle(screen, END, (col * MAZE_GRID_SIZE + MAZE_GRID_SIZE // 2, row * MAZE_GRID_SIZE + MAZE_GRID_SIZE // 2), player_radius)

        pygame.draw.circle(screen, player_cursor_color, player.center, player_radius)
        pygame.draw.circle(screen, hand_cursor_color, hand_cursor.center, cursor_radius)

        # Display "Well done" message if the player reached the end
        if reached_end:
            font = pygame.font.Font(None, 36)
            text = font.render("Well done!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

        # Load the next level if the player reached the end
        if reached_end:
            pygame.time.delay(2000)  # Delay for 2 seconds to show the "Well done!" message
            current_level += 1
            if current_level < len(maze_levels):
                maze_grid, start_row, start_col = load_level(maze_levels[current_level])
            else:
                # If there are no more levels, end the game
                running = False

    # Quit Pygame
    pygame.quit()

run_maze_game()
