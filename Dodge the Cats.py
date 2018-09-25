"""Author: Eric Wang

   Date: May 29, 2016
   
   Description: This program creats a 'Dodge the Cats' game.It is a single player game. The player controls the mouse to dodge the cats that drop from the top of screen. When the score hits the certain point, the speed of cats will increase. Also, the number of cats will be more and more and the game keeps going."""

# I - IMPORT AND INITIALIZE
import pygame, Sprites, random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640,480))

def main():
   '''This function defines the 'mainline logic' for our game.'''
    
   # Display
   pygame.display.set_caption("Dodge the Cats")
   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((255, 255, 255)) 
   screen.blit(background, (0, 0))
   
   # Sprites for: Player,EndZone,ScoreKeeper,Life,Background,PowerUp and group for cat sprite
   player = Sprites.Player(screen)
   endzone = Sprites.EndZone(screen)
   score = Sprites.ScoreKeeper(screen)
   life = Sprites.Life(screen)
   background_new = Sprites.Background(screen)
   catsgroup = pygame.sprite.Group(Sprites.Cats(screen))
   heart = Sprites.PowerUp(screen)
   
   highSprites = pygame.sprite.OrderedUpdates(player,score,life,heart)
   lowSprites = pygame.sprite.OrderedUpdates(endzone, background_new)
   allSprites = pygame.sprite.OrderedUpdates(lowSprites,highSprites,catsgroup)
   
   # Load image for "game over"
   game_over = pygame.image.load("game_over_by_don_amine-d4ef.gif")
   game_over = game_over.convert()
   
   # Load all the sound effects.
   game_over_sound = pygame.mixer.Sound("gameover.wav")
   game_over_sound.set_volume(1.0)
   life_sound = pygame.mixer.Sound("life.wav")
   life_sound.set_volume(1.0)
   hit_sound = pygame.mixer.Sound("hit.wav")
   hit_sound.set_volume(1.0)
   pygame.mixer.music.load("bgm.mp3")
   pygame.mixer.music.set_volume(0.5)
   pygame.mixer.music.play(-1)
   
   # ACTION
        
   # Assign 
   keepGoing = True
   clock = pygame.time.Clock()
      
   # Hide the mouse pointer
   pygame.mouse.set_visible(False)
   
       
   # Loop
   while keepGoing:
        
      # Time
      clock.tick(30)
        
      # Events
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            keepGoing = False
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               player.go_left()
            if event.key == pygame.K_RIGHT:
               player.go_right()
            if event.key == pygame.K_UP:
               player.go_up()
            if event.key == pygame.K_DOWN:
               player.go_down()            
         elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
               player.keep_going_x()
               player.gravity()
            if event.key == pygame.K_RIGHT:
               player.keep_going_x()
               player.gravity()
            if event.key == pygame.K_UP:
               player.gravity()
            if event.key == pygame.K_DOWN:
               player.gravity()
            
            # If it equals to 1, the catsgroup adds 1 more cat to the group
            if random.randrange(10) == 1:
               cats = Sprites.Cats(screen)
               catsgroup.add(cats)
               allSprites = pygame.sprite.OrderedUpdates(lowSprites,catsgroup,highSprites)
            
            # If it equals to 1, the powerup displays on the screen.
            if random.randrange(30) == 1:
               heart.show()      
      
      # If player collides with heart, then player gains 1 life and the heart displays and the sound effect is playing.
      if player.rect.colliderect(heart.rect):
         life.gain_life()
         heart.hide()
         life_sound.play()
      
      #collision detection  
      collide_cats = pygame.sprite.spritecollide(player, catsgroup, False)
      
      # If player collides with cats, the cats will be repositioned to the top of the screen and player loses 1 life and the sound effect is playing. 
      for cat in collide_cats:
         cat.reset()
         life.lose_life()
         hit_sound.play()
      
      #collision detection   
      collide_score = pygame.sprite.spritecollide(endzone, catsgroup, False)
      
      # If the cats reach the bottom of the screen, they will be reposisioned to the top of the screen and the sound effect is playing.
      for cat in collide_score:
         cat.reset()
         score.player_scored()
      
      # If the score hits the certain points, the speed of cats will increase.   
      for cat in catsgroup:
         if score.medium():
            cat.medium_dy()
         if score.hard():
            cat.hard_dy()
      
      # Check for game over (if a loses all lives)  
      if life.lose_game():
         keepGoing = False
         
      # Refresh screen
      allSprites.clear(screen, background)
      allSprites.update()
      allSprites.draw(screen)
                       
      pygame.display.flip()
                    
   # Unhide the mouse pointer
   pygame.mouse.set_visible(True)
   
   # Display the "game over" image and the sound effect is playing.
   screen.blit(game_over,(0,0))
   game_over_sound.play()
   pygame.display.flip()
   pygame.time.delay(4500)
   # Close the game window
   pygame.quit()     
                     
# Call the main function
main()     
