import os 
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

#Initialise pygame module
pygame.init()

#Caption for display/Caption at the top of the window
pygame.display.set_caption("Cao Ni Ma Mikey")

#Define global variables

#Width and height of our screen
WIDTH, HEIGHT = 800, 600

#FPS
FPS = 60

#Player speed
PLAYER_VEL = 5

#Pygame windows
window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    """
    Flip the sprites in the list

    Args:
        sprites (_type_): take in a list of sprites

    Returns:
        _type_: _description_
    """
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Load all the different sprite sheets for our characters.

    Args:
        dir1 (_type_): load other images that aren't just my characters
        dir2 (_type_): load other images that aren't just my characters
        width: width of the image
        height: height of the image

    Returns:
        _type_: _description_
    """
    #Determine the path to the images that we're going to loading
    path = join("assets", dir1, dir2)
    #Get all the image in this directory
    #We are gonna list all the things inside path
    #Load every single file that is inside of this directory and
    #Split into the individual image that I want to get
    images = [f for f in listdir(path) if isfile(join(path, f))]

    #This dictionary is having key values pairs where
    #The key is the animation style and the values is the images of that animation
    all_sprites = {}
    #Loop through all the images
    for image in images:
        #I am loading the image which is the image from these path
        #and I just append the path to it an then it will be transparent background
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        #Get all the individual images from the spritesheet and load those
        sprites = []
        #width is gonna be wthe witdth of the animation inside of the spritesheet
        for i in range(sprite_sheet.get_width() // width):
            #We are going to create a surface that the size of our
            #Desired individual animation frame
            #grab that animation frame from our main image then draw it into the surface
            #Then export that surface 
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            #Create an rectangle where in this image,
            #An image being the spritesheet that I want
            #To take and individual image from and bullet it onto the surface
            #Only drawing the frame from the spritesheet that I want
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        #If I want a multidirectional direction, then we need to add 2 keys
        #To the dictionary, we look for the png file in the spritesheet
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites

def get_block(size):
    """
    Define the block that wanted in the folder

    Args:
        size (_type_): passing what size block gonna be

    Returns:
        _type_: _description_
    """
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    #Create an image that is of that size of 32
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    #96 is the pixel where the image from the image that i want start
    rect = pygame.Rect(96, 0, size, size)
    #Blit the image onto the surface
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
#Players
#.sprite to make pixel perfect collision
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    #Gravity
    GRAVITY = 1
    #Images
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    #Width and height will be determined by the image that
    #Valuable that in charge for the amount of delay between changing sprites
    ANIMATION_DELAY = 3
    #we will use for the player
    def __init__(self, x, y, width, height):
        super().__init__()
        #Put the value in rectangle, make it easier to move
        self.rect = pygame.Rect(x, y, width, height)
        #How fast we moving our player in single frame
        # in both direction
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        #Keep track of what direction my player's facing
        self.direction = "left"
        #Reset the count that we're using to change the animation frames
        self.animation_count = 0
        #Counting how long have been failing for gravity
        self.fall_count = 0
        #The player will be able to jump
        self.jump_count = 0
        #telling if being hit or not
        self.hit = False
        self.hit_count = 0
    
    def jump(self):
        """
        #This functio nwill help player to jump
        """
        #Negative gravity becasue jumping up to the air and 8 is how fast
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        #Check if double jump
        #As soon as jump, get rid of any gravity already obtain
        #Then landed and jump again
        if self.jump_count == 1:
            self.fall_count = 0



    def move(self, dx, dy):
        """
        Moving a player by the y axis and the x axis

        Args:
            dx (_type_): as the x axis go up, we move to the right
            dy (_type_): as the y axis go up, we move down

        Returns:
            _type_: _description_
        """
        #If we want to move up or down or left or right,
        #We will just changing the dx dy
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        """
        Moving a player to the left

        Args:
            vel (_type_): moving the player to the left, the reason why -vel is becasue pygame start from top left
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move_right(self, vel):
        """
        Moving a player to the right

        Args:
            vel (_type_): _description_
        """
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self,fps):
        """
        Loop function, being called once every frame

        Args:
            fps (_type_): _description_

        Returns:
            _type_: _description_
        """
        #Every single frame in loop, we're going to increase the Y velocity by our gravity
        #How large the gravity are varies on how long we failing for
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1 
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        #If we landed, the gravity need to be equal to 0
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        #Multiply velocity by -1 because when hit head, go backward
        self.y_vel *= -1

    def update_sprite(self):
        """
        Animating sprites
        """
        #This is the default spritesheet, 
        #if we are not doing anything, we using idle
        sprite_sheet = "idle"
        #if we doing something else, we use other sprite
        #Animation for jumping
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        #If i have some velocity in the x direction, then i'm running
        elif self.x_vel != 0:
            sprite_sheet = "run"

        

        #Change the main spritesheet name so it'll run, jump
        #adding direction to it show knowing what exact spritesheet
        #we're using
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        #Iterate through the sprites and every seconds chaneg
        #The sprite that we're showing so that it looks like we
        #are animating
        #Every 5 frames showing a different sprite in whatever animation using
        #Then we mod whatever the line of our sprites is
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        """_summary_
        """
        #Depending on what sprite have, is goona be adjust the rectangle
        #Specifically adjust the width and the height but using the same x
        #and y position that have 
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        #Aloud collision and make it overlap with another mask
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        """_summary_

        Args:
            window (_type_): _description_

        Returns:
            _type_: _description_
        """
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        #Define rectangle
        self.rect = pygame.Rect(x, y, width, height)
        #Define image
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, win, offset_x):
        """
        Drawing the image, so basically modify the image
        When we change the image, the draw function will 
        automatically draw it accurately on the screen

        Args:
            win (_type_): _description_

        Returns:
            _type_: _description_
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        #Get the image what need then blits the image to pygame surface
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        #Specify image
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        """

        """
        #Change the main spritesheet name so it'll run, jump
        #adding direction to it show knowing what exact spritesheet
        #we're using

        sprites = self.fire[self.animation_name]
        #Iterate through the sprites and every seconds chaneg
        #The sprite that we're showing so that it looks like we
        #are animating
        #Every 5 frames showing a different sprite in whatever animation using
        #Then we mod whatever the line of our sprites is
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        #Depending on what sprite have, is goona be adjust the rectangle
        #Specifically adjust the width and the height but using the same x
        #and y position that have 
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        #Aloud collision and make it overlap with another mask
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
#Background
def get_background(name):
    """
    This function is return a list that contains all of the background tiles

    Args:
        name: Colors of the background tiles
    """
    #Get the path of the background
    image = pygame.image.load(join("assets", "Background", name))
    #Get the width and height of the background
    _, _, width, height = image.get_rect()
    tiles = []

    #Loops through how many tiles need to create in X and Y direction
    #Get the width of the screen to divide by the 
    #Width of the tiles to get approximately how many tiles need
    #To make sure there are no gaps, I add 1
    #Same things happen with height 
    for i in range(WIDTH // width + 1):
        for j in range (HEIGHT // height + 1):
            #Denote the position of the top left hand
            pos = (i * width, j * height)
            tiles.append(pos)
    
    #Also return the image to know what image to use 
    return tiles, image
    
def draw(window, background, bg_image, player, objects, offset_x):
    """
    This function is to draw
    """
    #Draw background,
    #and the position want to draw it at
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)
 
    player.draw(window, offset_x)

    #Update the display so every single frame we clear the screen
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    #All objects be colliding with
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            #If moving down on the screen, that would mean colliding with top
            #of this object, taking player bottom and make it equal to the top of the object
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)
    
    return collided_objects

def collide(player, objects, dx):
    """_summary_

    Args:
        player (_type_): _description_
        objects (_type_): _description_
        dx (_type_): _description_
    """
    player.move(dx, 0)
    player.update()
    collided_objects = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_objects = obj
            break
    
    player.move(-dx, 0)
    player.update()
    return collided_objects

def handle_move(player, objects):
    """
    This function is to handle the movement of the player
    """
    #Get the key pressed
    #Tell if the keyboard get pressed
    keys = pygame.key.get_pressed()


    #Set player velocity to 0
    player.x_vel = 0

    #Check if collide
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    #This is the left arrow key
    if keys[pygame.K_LEFT] and not collide_left:
        #How want to move the player
        player.move_left(PLAYER_VEL)
    
    #This is the right arrow key
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    verticle_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *verticle_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
#Main function
#Event loop
def main(window):
    """
    _summary_

    Args:
        window (_type_): _description_
    """
    clock = pygame.time.Clock() 
    background, bg_image = get_background("Blue.png")

    block_size = 96
    player = Player(100, 100, 50, 50)
    fire = Fire(100 ,HEIGHT - block_size - 64, 16, 32)
    fire.on()
    #Making a floor
    #Create blcoks that go to the left and to the right of the screen
    #-WIDTH // block_size which is how many block i want in the left of the screen
    #WIDTH * 2 // block_size which is how many block i want in the right of the screen
    #i is telling me the x coordinate position that i want my block to be on
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range (-WIDTH // block_size, WIDTH *3 // block_size)]
    
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size), fire]
    #While loop that's continually loop and event loop

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        #Ensuring that our while loop is run at 60 frames per second
        clock.tick(FPS)

        for event in pygame.event.get():
            #Check if the user quit the game
            if event.type == pygame.QUIT:
                run = False
                break
            
            #Allow for jumping
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
        
        #Called loop function because loop is actualy what moving player
        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        #Passing background and bg image
        draw(window, background, bg_image, player, objects, offset_x)

        #Checking if moving to the right and checking if the character is right on the screen
        #Crossed a specific boundary (200px)
        #Take whatever position of the character on the screen the minus the offset 
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel >0)) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit() 

if __name__ == "__main__":
    #Have this function to run the file directly
    main(window)