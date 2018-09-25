"""Author: Eric Wang

   Date: May 29, 2016
   
   Description: This is the module for "Dodge the Cats" game."""

import pygame, random
class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for Player'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter. It loads the appropriate image and positions it on the bottom of the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Define the image attributes for the player.
        self.__pikachuleft = pygame.image.load("1pikachu-left.gif")
        self.__pikachuleft = self.__pikachuleft.convert()
        self.__pikachuright = pygame.image.load("1pikachu-right.gif")
        self.__pikachuright = self.__pikachuright.convert()
        
        self.image = self.__pikachuleft
        self.rect = self.image.get_rect()
        self.rect.bottom = 470
        
        # Instance variables to keep track of the screen surface
        # Center the player horizontally in the window.
        self.rect.left = screen.get_width()/2-50        
        self.__screen = screen
        self.__dx = 0
        self.__dy = 3
      
    def go_right(self):
        '''This method changes the x direction.'''
        self.image = self.__pikachuright
        self.__dx = 10
        
    def go_left(self):
        '''This method reverses the x direction.'''
        self.image = self.__pikachuleft
        self.__dx = -10

    def go_up(self):
        '''This method changes the y direction.'''
        self.__dy = -7      
        
    def go_down(self):
        '''This method reverses the y direction.'''
        self.__dy = 13          
        
    def keep_going_x(self):
        '''This method sets the x direction to 0'''
        self.__dx = 0
    
    def keep_going_y(self):
        '''This method sets the y direction to 0'''
        self.__dy = 0
    
    def gravity(self):
        '''This method sets the y direction to 3'''
        self.__dy = 3
        
    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        # Check if we have reached the left or right or top or bottom of the screen.
        # If yes, then we don't change the x or y position of the player at all.
        if self.rect.left < 0: 
            self.rect.left = 0
        self.rect.right += self.__dx
        if self.rect.right > self.__screen.get_width():
            self.rect.right = 640
        if self.rect.top < 0:
            self.rect.top = 0
        self.rect.bottom +=self.__dy
        if self.rect.bottom > self.__screen.get_height():
            self.rect.bottom = 480
                        
class Cats(pygame.sprite.Sprite):
    '''This class defines the sprite for our cats.'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the cats.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
    
        # Set the image and rect attributes for the Cats
        self.image = pygame.image.load("1nyan-cat.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        # Instance variables to keep track of the screen surface
        self.__screen = screen
        self.reset()
        
    def medium_dy(self):
        '''This method sets the y direction randomly from 10 to 13'''
        self.__dy = random.randrange(10,13)
        
    def hard_dy(self):
        '''This method sets the y direction randomly from 13 to 16'''
        self.__dy = random.randrange(13,16)
        
    def update(self):
        '''This method will be called automatically to reposition the
        cats sprite on the screen.'''
        # Check if we have reached the bottom of the screen.
        # If yes, then call the reset() method.
        self.rect.top += self.__dy
        if self.rect.top > self.__screen.get_height():
            self.reset()

    def reset(self):
        '''This method will reposition the cats to the top of the screen'''
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, self.__screen.get_width())
        self.__dy = random.randrange(7,10)
                    
class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for our endzone on bottom of the window'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Our endzone sprite will be a 1 pixel wide black line.
        self.image = pygame.Surface((screen.get_width(),1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
        
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = screen.get_height()
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self, screen):
        '''This initializer loads the system font "Arial", and
        sets the starting score to 0:0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.SysFont("Arial", 30)
        self.__player_score = 0
         
    def player_scored(self):
        '''This method adds one to the score for player'''
        self.__player_score += 1
        
    def medium(self):
        '''This method returns True when the score is greater or equal to 50 and less than 100.'''
        if self.__player_score >= 50 and self.__player_score < 100:
            return True
        
    def hard(self):
        '''This method returns True when the score is greater or equal to 100.'''
        if self.__player_score >= 100:
            return True    
        
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        message = "Score: %d " %(self.__player_score)
        self.image = self.__font.render(message, 1, (255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (250, 15)
        
class Life(pygame.sprite.Sprite):
    '''This class defines a label sprite displays the player's lives remaining'''
    def __init__(self, screen):
        '''This method defines the amount of lives the player initially has'''
        pygame.sprite.Sprite.__init__(self)
        self.__life = 10 
        
    def lose_life(self):
        '''This method will be called when the player loses 1 life'''
        self.__life -= 1
        
    def gain_life(self):
        '''This method will be called when the player gains 1 life'''
        self.__life += 1
        
    def lose_game(self):
        '''This method will be called when the player has no life remaining '''
        if self.__life == 0 :
            return True 
        
    def update(self):
        '''This method will be called automatically to display 
        the current lives at the top of the game window.'''
        count_label = "lives: %d" %(self.__life)
        self.__font = pygame.font.SysFont("Arial", 30)
        self.image = self.__font.render(count_label, 1, (255, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.center = (390, 15)
        
class PowerUp(pygame.sprite.Sprite):
    '''This class defines the sprite for the powerup'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter. It loads the appropriate image and positions it out of the screen.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the powerup.
        self.image = pygame.image.load("heart_edited-1.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.top = screen.get_height()+ 10
        
        # Instance variables to keep track of the screen surface
        self.__screen = screen
        
    def show(self):
        '''This method positions the powerup sprite randomly on the top of the screen.'''
        self.rect.centerx = random.randrange(self.__screen.get_width())
        self.rect.bottom = 0
        
    def hide(self):
        '''This method hides the powerup sprite out of the screen.'''
        self.rect.top = self.__screen.get_height()+10
        
    def update(self):
        '''This method will be called automatically to reposition the
        powerup sprite on the screen.'''
        self.rect.centery +=5
         
class Background(pygame.sprite.Sprite):
    '''This class defines the sprite for the background'''
    def __init__(self,screen):
        '''This initializer loads the appropriate image and positions it on the screen.'''
         # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the background.
        self.image = pygame.image.load("nyan-cat-background.jpg")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = screen.get_height()
        

        
        

        
        
    