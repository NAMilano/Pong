import pygame

SCR_WID, SCR_HEI = 640, 480
class Player():
        def __init__(self, side):
                # side has two valid answers - 1 is left side - 2 is right side
                if (side == 1):
                        self.x, self.y = 16, SCR_HEI/2
                if (side == 2):
                        self.x, self.y = SCR_WID-16, SCR_HEI/2
                self.side = side
                self.speed = 3
                self.padWid, self.padHei = 8, 64
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font.ttf", 64)
       
        def scoring(self, screen):
                victory = pygame.mixer.Sound("victory.wav")
                # load font style and size for victory message
                vicFont = pygame.font.Font("imagine_font.ttf", 32)
                scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
                # checks side of current object uses proper screen.blit parameters 
                if (self.side == 1):
                        screen.blit(scoreBlit, (32, 16))
                if (self.side == 2):
                        screen.blit(scoreBlit, (SCR_HEI+92, 16))

                # checks side of current object and score to display who won
                if self.score == 10 and self.side == 1:
                        # play victory sound
                        pygame.mixer.Channel(3).play(victory)
                        ## create the background rectangles
                        outerRect = pygame.draw.rect(screen, (60, 130, 160), pygame.Rect(0,0,640,480))
                        innerRect = pygame.draw.rect(screen, (255,255,255), pygame.Rect(70,70,500,340))
                        middleBar = pygame.draw.rect(screen, (60, 130, 160), pygame.Rect(0,140,640,200))
                        # create the message
                        vic = vicFont.render("Player one wins!", True, (255,255,255))
                        # diplay the message
                        screen.blit(vic, (165, 230))
                        # update screen with victory screen
                        pygame.display.flip()
                        # pauses program so victory sound can play all the way through
                        pygame.time.wait(700)
                        print ("player 1 wins!")
                        exit()
                if self.score == 10 and self.side == 2:
                        # play victory sound
                        pygame.mixer.Channel(3).play(victory)
                        # create the background rectangles
                        outerRect = pygame.draw.rect(screen, (60, 130, 160), pygame.Rect(0,0,640,480))
                        innerRect = pygame.draw.rect(screen, (255,255,255), pygame.Rect(70,70,500,340))
                        middleBar = pygame.draw.rect(screen, (60, 130, 160), pygame.Rect(0,140,640,200))
                        # create the message
                        vic = vicFont.render("Player two wins!", True, (255,255,255))
                        # diplay the message
                        screen.blit(vic, (165, 230))
                        # update screen with victory screen
                        pygame.display.flip()
                        # pauses program so victory sound can play all the way through
                        pygame.time.wait(700)
                        print ("player 2 wins!")
                        exit()
       
        def movement(self):
                keys = pygame.key.get_pressed()
                # checks side of current object to use the correct keybinds
                if (self.side == 1):
                        if keys[pygame.K_w]:
                                self.y -= self.speed
                        elif keys[pygame.K_s]:
                                self.y += self.speed
                if (self.side == 2):
                        if keys[pygame.K_UP]:
                                self.y -= self.speed
                        elif keys[pygame.K_DOWN]:
                                self.y += self.speed
                if self.y <= 0:
                        self.y = 0
                elif self.y >= SCR_HEI-64:
                        self.y = SCR_HEI-64
       
        def draw(self, screen):
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))

class Ball():
        def __init__(self):
                self.x, self.y = SCR_WID/2, SCR_HEI/2
                self.speed_x = -3
                self.speed_y = 3
                self.size = 8
       
        def movement(self, player, enemy):
                # load paddlehit sound 
                ballCollision = pygame.mixer.Sound("ballcollision.wav")
                ballScore = pygame.mixer.Sound("ballscore.wav")
                self.x += self.speed_x
                self.y += self.speed_y
 
                #wall col
                if self.y <= 0:
                        # plays sound when the ball collides with a border wall
                        pygame.mixer.Channel(3).play(ballCollision)
                        self.speed_y *= -1
                elif self.y >= SCR_HEI-self.size:
                        # plays sound when the ball collides with a border wall
                        pygame.mixer.Channel(3).play(ballCollision)
                        self.speed_y *= -1
                if self.x <= 0:
                        self.__init__()
                        # plays sound when a goal is scored
                        pygame.mixer.Channel(3).play(ballScore)
                        enemy.score += 1
                elif self.x >= SCR_WID-self.size:
                        self.__init__()
                        # plays sound when a goal is scored
                        pygame.mixer.Channel(3).play(ballScore)
                        self.speed_x = 3
                        player.score += 1
                ##wall col
                #paddle col
                #player
                for n in range(-self.size, player.padHei):
                        if self.y == player.y + n:
                                if self.x <= player.x + player.padWid:
                                        # plays sound when the ball connects with a paddle
                                        pygame.mixer.Channel(3).play(ballCollision)
                                        self.speed_x *= -1
                                        break
                        n += 1
                #enemy
                for n in range(-self.size, enemy.padHei):
                        if self.y == enemy.y + n:
                                if self.x >= enemy.x - enemy.padWid:
                                        # plays sound when the ball connects with a paddle
                                        pygame.mixer.Channel(3).play(ballCollision)
                                        self.speed_x *= -1
        
                                        break
                        n += 1
                ##paddle col
 
        def draw(self, screen):
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 8, 8))

# plays the correct background song based on score
def getBackgroundSong(playerOne, playerTwo, winningOne, winningTwo, tiedGame):
        # if player one is winning play winningOne song - Only works if channel(0) is not already playing to avoid duplicate songs from playing
        if playerOne.score > playerTwo.score and (pygame.mixer.Channel(0).get_busy() == False):
                # stops other background song from playing
                pygame.mixer.Channel(1).stop()
                pygame.mixer.Channel(2).stop()
                # starts new background song
                pygame.mixer.Channel(0).play(winningOne)
        # if player two is winning play winningTwo song - Only works if channel(1) is not already playing to avoid duplicate songs from playing
        if playerTwo.score > playerOne.score and (pygame.mixer.Channel(1).get_busy() == False):
                # stops other background song from playing
                pygame.mixer.Channel(0).stop()
                pygame.mixer.Channel(2).stop()
                # starts new background song
                pygame.mixer.Channel(1).play(winningTwo)
        # if both player scores are equal play tiedGame song - Only works if channel(2) is not already playing to avoid duplicate songs from playing
        if playerOne.score == playerTwo.score and (pygame.mixer.Channel(2).get_busy() == False):
                # stops other background song from playing
                pygame.mixer.Channel(0).stop()
                pygame.mixer.Channel(1).stop()
                # starts new background song
                pygame.mixer.Channel(2).play(tiedGame)

# Main menu screen
def mainMenu(screen):
        # fill background of menu
        screen.fill((60, 130, 160))
        # create fonts
        largeFont = pygame.font.Font("imagine_font.ttf", 72)
        mediumFont = pygame.font.Font("imagine_font.ttf", 28)
        smallFont = pygame.font.Font("imagine_font.ttf", 18)
         # create messages
        pongTitle = largeFont.render("Pong", True, (255,255,255))
        menuTitle = largeFont.render("Main Menu", True, (255,255,255))
        version = smallFont.render("Version 1.5", True, (255,255,255))
        enterButton = mediumFont.render("{ENTER}",True,(0,0,0))
        startMessage = mediumFont.render("Start Game", True,(255,255,255))
        escapeButton = mediumFont.render("{ESCAPE}", True,(0,0,0))
        endMessage = mediumFont.render("Exit Game", True, (255,255,255))
        # diplay messages
        screen.blit(pongTitle, (210, 20))
        screen.blit(menuTitle, (120, 85))
        screen.blit(version, (260,460))
        # create and display button background
        outerRect = pygame.draw.rect(screen, (0,0,0), pygame.Rect(122.5,200,400,75))
        innerRect = pygame.draw.rect(screen, (255,255,255), pygame.Rect(135,212,143,50))
        # display button text
        screen.blit(enterButton, (140,227.5))
        screen.blit(startMessage, (300, 227.5))
        # create and display button background
        outerRect = pygame.draw.rect(screen, (0,0,0), pygame.Rect(122.5,325,400,75))
        innerRect = pygame.draw.rect(screen, (255,255,255), pygame.Rect(135,337,163,50))
        # display button text
        screen.blit(escapeButton, (140,353))
        screen.blit(endMessage, (330, 353))
        # update screen
        pygame.display.flip()
        # get users key input - enter or escape
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                        # when enter is pressed return to main and continue the program
                                        return
                                if event.key == pygame.K_ESCAPE:
                                        # when escape is pressed exit the entire program
                                        quit()



def main():
    # initialize pygame mixer
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    SCR_WID, SCR_HEI = 640, 480
    screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
    # load background image
    background = pygame.image.load("background.png")
    # scale to fit screen size
    background = pygame.transform.scale(background,(SCR_WID, SCR_HEI))

    pygame.display.set_caption("Pong")
    pygame.font.init()
    clock = pygame.time.Clock()
    FPS = 60

    # playerOne instance (1 - left side)
    playerOne = Player(1) 
    ball = Ball()
    #player = Player()
    # playerTwo instance (2 - right side)
    playerTwo = Player(2)
    
    # -- pygame.mixer.Channel reserved channels -- 
    # Channel(0) is for winningOne background song
    # Channel(1) is for winningTwo background song
    # Channel(2) is for tiedGame background song
    # Channel(3) is for extra sound effects (victory, ballCollision, ballScore)

    # loading background songs
    winningOne = pygame.mixer.Sound("player_one_winning_background_song.wav")
    winningTwo = pygame.mixer.Sound("player_two_winning_background_song.wav")
    tiedGame = pygame.mixer.Sound("tied_game_background_song.wav")
    # lower song volumes
    winningOne.set_volume(0.1)
    winningTwo.set_volume(0.1)
    tiedGame.set_volume(0.1)


    # launch the main menu
    mainMenu(screen)
 
    while True:
                #process
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                print ("Game exited by user")
                                exit()
                ##process
                #logic
                ball.movement(playerOne, playerTwo)
                playerOne.movement()
                playerTwo.movement()
                ##logic
                #draw
                screen.fill((0, 0, 0))
                # show background
                screen.blit(background,(0,0))
                ball.draw(screen)
                playerOne.draw(screen)
                playerOne.scoring(screen)
                playerTwo.draw(screen)
                playerTwo.scoring(screen)
                getBackgroundSong(playerOne, playerTwo, winningOne, winningTwo, tiedGame)
                ##draw
                #_______
                pygame.display.flip()
                clock.tick(FPS)











if __name__ == "__main__":
    main()