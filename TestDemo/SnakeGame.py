# import pygame
# import random

# # Initialize Pygame
# pygame.init()

# # Set up the display window
# WIDTH = 600
# HEIGHT = 400
# window = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Pac-Man Game")

# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)

# # Pac-Man properties
# pac_man_speed = 3
# current_speed = pac_man_speed

# # Ghosts properties
# num_ghosts = 4
# ghost_size = 15

# # Create maze layout
# maze_layout = [
#     ['O', 'O', 'O', 'O', 'O', 'O'],
#     ['O', 'P', '.', 'G', '.', 'O'],
#     ['O', '.', 'O', 'G', 'O', '.'],
#     ['O', '.', 'G', 'G', 'O', '.'],
#     ['O', '.', 'O', '.', 'O', '.'],
#     ['O', 'O', 'O', 'O', 'O', 'O']
# ]

# # Initialize Pac-Man
# x = 300
# y = 250

# # Initialize ghosts
# ghosts = []
# for i in range(num_ghosts):
#     row = random.randint(1, 4)
#     col = random.randint(1, 3)
#     while (row, col) == (y, x):
#         row = random.randint(1, 4)
#         col = random.randint(1, 3)
#     ghosts.append((row, col))

# # Power pellets
# power_pellets = []
# for i in range(5):
#     row = random.randint(0, 5)
#     col = random.randint(0, 5)
#     while (row, col) == (y, x):
#         row = random.randint(0, 5)
#         col = random.randint(0, 5)
#     power_pellets.append((row, col))

# # Game state
# game_over = False
# score = 0

# def draw_maze():
#     global game_over, score
    
#     # Clear the screen
#     window.fill(BLACK)
    
#     # Draw maze walls
#     for row in range(len(maze_layout)):
#         for col in range(len(maze_layout[row])):
#             if maze_layout[row][col] == 'O':
#                 pygame.draw.rect(window, WHITE, (col * 50 + 2, row * 50 + 2, 46, 46))
    
#     # Draw Pac-Man
#     if not game_over:
#         pygame.draw.circle(window, GREEN, (x, y), ghost_size)
    
#     # Draw power pellets
#     for pellet in power_pellets:
#         pygame.draw.circle(window, RED, (pellet[0], pellet[1]), 3)
    
#     # Draw score
#     font = pygame.font.Font(None, 74)
#     text = font.render(f"Score: {score}", True, WHITE)
#     window.blit(text, (50, 50))
    
#     pygame.display.flip()

# def move_pacman():
#     global x, y, current_speed
    
#     # Handle keyboard input
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             game_over = True
#             return
        
#         if event.type == pygame.KEYDOWN:
#             key_pressed = False
            
#             if event.key == pygame.K_LEFT and x > 250:
#                 x -= current_speed
#                 pressed = True
#             elif event.key == pygame.K_RIGHT and x < 350:
#                 x += current_speed
#                 pressed = True
#             elif event.key == pygame.K_UP and y > 250:
#                 y -= current_speed
#                 pressed = True
#             elif event.key == pygame.K_DOWN and y < 350:
#                 y += current_speed
#                 pressed = True
            
#             if pressed:
#                 move_pacman()
    
# def move_ghosts():
#     global ghosts, x, y
    
#     for ghost in ghosts:
#         row, col = ghost
        
#         # Check if ghost reached Pac-Man
#         if (row == x and col == y) or maze_layout[row][col] == 'G':
#             new_row = random.randint(0, 5)
#             new_col = random.randint(0, 5)
#             while (new_row, new_col) == (row, col):
#                 new_row = random.randint(0, 5)
#                 new_col = random.randint(0, 5)
#             ghost = (new_row, new_col)
        
#         # Move ghost
#         row, col = ghost
        
#         if maze_layout[row][col] == '.':
#             col += random.randint(-1, 1)
#             row += random.randint(-1, 1)
            
#         ghost = (row, col)

# def check_power_pellet():
#     global score, x, y
    
#     for pellet in power_pellets:
#         if (x, y) == (pellet[0], pellet[1]):
#             score += 1
#             font = pygame.font.Font(None, 74)
#             text = font.render(f"Score: {score}", True, WHITE)
#             window.blit(text, (50, 50))
    
#     power_pellets = []
#     for i in range(5):
#         row = random.randint(0, 5)
#         col = random.randint(0, 5)
#         while (row, col) == (y, x):
#             row = random.randint(0, 5)
#             col = random.randint(0, 5)
#         power_pellets.append((row, col))

# def game_over_check():
#     global game_over
    
#     for ghost in ghosts:
#         if maze_layout[ghost[0]][ghost[1]] == 'G' and (x, y) == (ghost[0], ghost[1]):
#             font = pygame.font.Font(None, 74)
#             text = font.render("Game Over!", True, RED)
#             window.blit(text, (WIDTH//2 - 100, HEIGHT//2))
#             game_over = True
#             return

# while not game_over:
#     draw_maze()
    
#     move_pacman()
#     move_ghosts()
#     check_power_pellet()
#     game_over_check()

# pygame.quit()



