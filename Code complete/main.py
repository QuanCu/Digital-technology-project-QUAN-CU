from settings import *
from level import Level

# This class is going to run the basic logic
class Game:
    def __init__(self):
        pygame.init()
        # Passing through the width and height of the window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        #Name of the game
        pygame.display.set_caption("Adventure 1")

        self.current_stage = Level()
    
    def run(self):
        """
        Creating the game loop
        """
        run = True
        while run:
            for event in pygame.event.get():
                #Check if the user quit the game
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.current_stage.run()
            pygame.display.update()

# Make sure that don't run anything accidentally 
if __name__ == '__main__':
    game = Game()
    game.run()