import pygame
import random
import time
import sys

# Pygame Init
pygame.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Initialise the window display
win_width = 500
win_height = 500
win_size = win_width, win_height
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Cute Snake")

# Snake attributes
position_x = 50
position_y = 50
width = 10
height = 10
vel = 5

# FPS
fps = pygame.time.Clock()

# Game settings
game_settings = {
    "delta": 10,
    "snakePos": [100, 50],
    "snakeBody": [[100, 50], [90, 50], [80, 50]],
    "foodPos": [400, 50],
    "foodSpawn": True,
    "direction": 'RIGHT',
    "changeTo": '',
    "score": 0,
}

# Define font
font = pygame.font.SysFont('Comic Sans MS', 30)

# Define menu items
menu_items = ["Start", "Options", "Quit"]
menu_rects = []

# Render menu items
for i, item in enumerate(menu_items):
    text = font.render(item, True, white)
    text_rect = text.get_rect()
    text_rect.center = (win_width // 2, 200 + i * 50)
    menu_rects.append(text_rect)

# Load the background image
background_image = pygame.image.load("background.png")
transparent_surface = pygame.Surface(background_image.get_size(), pygame.SRCALPHA) 
alpha_value = 0 
transparent_surface.fill((0, 0, 0, alpha_value))
background_image.blit(transparent_surface, (0, 0))

# Function to handle mouse clicks
def handle_click(pos):
    for i, rect in enumerate(menu_rects):
        if rect.collidepoint(pos):
            if menu_items[i] == "Start":
                return "game"  # Transition to game screen
            elif menu_items[i] == "Options":
                print("Opening options menu...")
            elif menu_items[i] == "Quit":
                pygame.quit()
                sys.exit()

# Game Over
def gameOver(game_settings):

    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (250, 50)
    win.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(2)
    
    # Reset game settings
    game_settings["delta"] = 10
    game_settings["snakePos"] = [100, 50]
    game_settings["snakeBody"] = [[100, 50], [90, 50], [80, 50]]
    game_settings["foodPos"] = [400, 50]
    game_settings["foodSpawn"] = True
    game_settings["direction"] = 'RIGHT'
    game_settings["changeTo"] = ''
    game_settings["score"] = 0

# Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('monaco', 32)
    Ssurf = SFont.render("Score  :  {0}".format(game_settings["score"]), True, white)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (70, 10)
    else:
        Srect.midtop = (70, 10)
    win.blit(Ssurf, Srect)

# Game screen function
def game_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game_settings["changeTo"] = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game_settings["changeTo"] = 'LEFT'
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                game_settings["changeTo"] = 'UP'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                game_settings["changeTo"] = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                # Transition to menu screen
                menu_screen()

    # Validate direction
    if game_settings["changeTo"] == 'RIGHT' and game_settings["direction"] != 'LEFT':
        game_settings["direction"] = game_settings["changeTo"]
    if game_settings["changeTo"] == 'LEFT' and game_settings["direction"] != 'RIGHT':
        game_settings["direction"] = game_settings["changeTo"]
    if game_settings["changeTo"] == 'UP' and game_settings["direction"] != 'DOWN':
        game_settings["direction"] = game_settings["changeTo"]
    if game_settings["changeTo"] == 'DOWN' and game_settings["direction"] != 'UP':
        game_settings["direction"] = game_settings["changeTo"]

    # Update snake position
    if game_settings["direction"] == 'RIGHT':
        game_settings["snakePos"][0] += game_settings["delta"]
    if game_settings["direction"] == 'LEFT':
        game_settings["snakePos"][0] -= game_settings["delta"]
    if game_settings["direction"] == 'DOWN':
        game_settings["snakePos"][1] += game_settings["delta"]
    if game_settings["direction"] == 'UP':
        game_settings["snakePos"][1] -= game_settings["delta"]

    # Snake body mechanism
    game_settings["snakeBody"].insert(0, list(game_settings["snakePos"]))
    if game_settings["snakePos"] == game_settings["foodPos"]:
        game_settings["foodSpawn"] = False
        game_settings["score"] += 10
    else:
        game_settings["snakeBody"].pop()
    if game_settings["foodSpawn"] == False:
        game_settings["foodPos"] = [random.randrange(1, win_width // 10) * game_settings["delta"], 
                                    random.randrange(1, win_height // 10) * game_settings["delta"]]
        game_settings["foodSpawn"] = True
    
    win.fill(black)
    for pos in game_settings["snakeBody"]:
        pygame.draw.rect(win, white, pygame.Rect(pos[0], pos[1], game_settings["delta"], game_settings["delta"]))
    pygame.draw.rect(win, green, pygame.Rect(game_settings["foodPos"][0], game_settings["foodPos"][1], game_settings["delta"], game_settings["delta"]))

    # Boundaries
    if game_settings["snakePos"][0] >= win_width or game_settings["snakePos"][0] < 0:
        print("1")
        gameOver(game_settings)
        menu_screen()
    if game_settings["snakePos"][1] >= win_height or game_settings["snakePos"][1] < 0:
        print("2")
        gameOver(game_settings)
        menu_screen()
        
    # Self hit
    for block in game_settings["snakeBody"][1:]:
        if game_settings["snakePos"] == block:
            gameOver(game_settings)
            menu_screen()

    showScore()
    pygame.display.flip()
    fps.tick(10)

# Menu screen function
def menu_screen():
    while True:
        # FIXME: The background color is supposed to be transparent
        win.blit(background_image, (0, 0))
        # win.fill(black)
        mouse_coordinates = pygame.mouse.get_pos()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                action = handle_click(pygame.mouse.get_pos())
                if action == "game":
                    return "game"  # Transition to game screen
                # TODO: add the options menu
                
        # Check for hover
        for i, rect in enumerate(menu_rects):
            if rect.collidepoint(mouse_coordinates):
                text_color = (16, 180, 155)  # Set text color to white when highlighted
            else:
                pygame.draw.rect(win, (254, 251, 146), rect)  # Regular background color
                text_color = black  # Set text color to black when not highlighted

            # Render text with appropriate color
            text_surface = font.render(menu_items[i], True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            win.blit(text_surface, text_rect)


        pygame.display.flip()


# Main loop
current_screen = "menu"
while True:
    if current_screen == "menu":
        current_screen = menu_screen()
    elif current_screen == "game":
        game_screen()
