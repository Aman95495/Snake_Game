import pygame
import random
import os

# Music Setting
pygame.mixer.init()
pygame.init()

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))


# Images
welcome_image = pygame.image.load('welcome.jpg')
background_image = pygame.image.load('background.jpg')
gameover_image = pygame.image.load('gameover.png')
welcome_image = pygame.transform.scale(welcome_image, (screen_width, screen_height)).convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height)).convert_alpha()
gameover_image = pygame.transform.scale(gameover_image, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("King Snake")
pygame.display.update()
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock() # Clock



# Colors
white = (255,255,255)
red = (255, 0 , 0)
black = (0, 0, 0)
green = (0,255,0)
yellow = (255,255,0)


# length of snake adjustment
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])     



# Screen Display of Score
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x,y))


# Welcome Screen

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(green)
        gameWindow.blit(welcome_image, (0,0))
        text_screen(" Reptile  Rhythm ", black, screen_width/3.5, screen_height/2.3)
        text_screen("Press Enter To Begin", black, screen_width/3.6, screen_height/1.8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('background_music.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()

        pygame.display.update()
        clock.tick(30)
        
# Game Loop
def gameloop():

    # length of snake adjustment
    snake_list = []
    snake_length = 1
    
    # Game Specific Variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y =  0
    food_x = random.randint(20,800)
    food_y = random.randint(20,500)
    food_size = 10
    score = 0
    snake_size = 10

    fps = 30

    # Check if hiscore file exits
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")
        

    # HighScore
    with open("hiscore.txt","r") as f:
        hiscore = f.read()


    while(exit_game!=True):
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(green)
            gameWindow.blit(gameover_image, (0,0))
            text_screen("Press Enter To Start New Game", red, screen_width/5, screen_height/1.5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = 5
                        velocity_y =  0
                        
                    if event.key == pygame.K_DOWN or event.key == pygame.K_z:
                        velocity_y =  5
                        velocity_x = 0
                        
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = -5
                        velocity_y =  0
                        
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_y =  -5
                        velocity_x = 0
                    
                    # fun
                    if event.key == pygame.K_k:
                        score += 10

                        if score > int(hiscore):
                            hiscore = score
                        
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<6:
                score += 10
                pygame.mixer.music.pause()  # Pause the background music
                pygame.mixer.Sound('foodeaten_music.mp3').play()  # Play the score increased sound
                pygame.mixer.music.unpause()  # Resume the background music
                '''
                print("Score :: ",score)
                '''
                food_x = random.randint(20,800)
                food_y = random.randint(20,500)
                snake_length += 10

                if score > int(hiscore):
                    hiscore = score
                

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]
                
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover_music.mp3')
                pygame.mixer.music.play()

                
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover_music.mp3')
                pygame.mixer.music.play()

                
            
            gameWindow.fill(black)
            gameWindow.blit(background_image, (0,0))
            text_screen("Score : " + str(score) + "  HiScore : " + str(hiscore), black,   5,  5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            plot_snake(gameWindow, (0, 0, 128), snake_list, snake_size)

        pygame.display.update()

        clock.tick(fps)

        

    # Pygame Quit
    pygame.quit()
    quit()



welcome()

