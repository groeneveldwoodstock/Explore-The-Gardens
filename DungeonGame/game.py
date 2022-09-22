import pygame   as pg
import sys

from .constants import *
from .level     import Level
from .debug     import debug


pg.init()
SCREEN = pg.display.set_mode((500, 480))
pg.display.set_caption("Menu")
BG = pg.image.load("assets/Background.png")

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("assets/font.ttf", size)

def get_high_score():
    high_score_file = open("high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score

# options or instructions screen    
def options():
    global button
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(25).render("Instructions", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(255, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        Navigate_TEXT = get_font(15).render("Navigate with Arrows or WASD", True, "Green")
        Navigate_RECT = Navigate_TEXT.get_rect(center=(255, 100))
        SCREEN.blit(Navigate_TEXT, Navigate_RECT)
        
        Attack_TEXT = get_font(15).render("Attack with Spacebar", True, "Red")
        Attack_RECT = Attack_TEXT.get_rect(center=(255, 130))
        SCREEN.blit(Attack_TEXT, Attack_RECT)
        
        Details1_TEXT = get_font(15).render("After you attack you must ", True, "Gray")
        Details1_RECT = Details1_TEXT.get_rect(center=(255, 160))
        SCREEN.blit(Details1_TEXT, Details1_RECT)
        
        Details2_TEXT = get_font(15).render("regain energy to attack again.", True, "Gray")
        Details2_RECT = Details2_TEXT.get_rect(center=(255, 180))
        SCREEN.blit(Details2_TEXT, Details2_RECT)
        
        Details3_TEXT = get_font(15).render("The ghosts may drop gold", True, "Purple")
        Details3_RECT = Details3_TEXT.get_rect(center=(255, 200))
        SCREEN.blit(Details3_TEXT, Details3_RECT)
        
        Details4_TEXT = get_font(15).render("or health bonuses when beaten.", True, "Purple")
        Details4_RECT = Details4_TEXT.get_rect(center=(255, 220))
        SCREEN.blit(Details4_TEXT, Details4_RECT)
        
        Details5_TEXT = get_font(15).render("Explore, collect gold,", True, "Black")
        Details5_RECT = Details5_TEXT.get_rect(center=(255, 250))
        SCREEN.blit(Details5_TEXT, Details5_RECT)
        
        Details6_TEXT = get_font(15).render("and make a new high score!", True, "Black")
        Details6_RECT = Details6_TEXT.get_rect(center=(255, 270))
        SCREEN.blit(Details6_TEXT, Details6_RECT)
        
        Details7_TEXT = get_font(15).render("Complete the mission by", True, "Black")
        Details7_RECT = Details7_TEXT.get_rect(center=(255, 300))
        SCREEN.blit(Details7_TEXT, Details7_RECT)
        
        Details8_TEXT = get_font(15).render("finding the Magic Gem!", True, "Black")
        Details8_RECT = Details8_TEXT.get_rect(center=(255, 320))
        SCREEN.blit(Details8_TEXT, Details8_RECT)
        
        OPTIONS_BACK = Button(image=None, pos=(255, 450), 
                            text_input="BACK", font=get_font(45), base_color="Red", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pg.display.update()

# main menu screen
def main_menu():
    best = get_high_score()
    global button
    class DungeonGame:
        """
        MAIN WINDOW HANDLER
            - CREATES WINDOW
            - HANDLES MAIN GAME LOOP
        """
        def __init__(self):
            pg.init()
            pg.mixer.init()
            self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
            pg.display.set_caption("Explore the Gardens")
            programIcon = pg.image.load(resource_path(os.path.join("assets/treasure", "winner_gem.png")))
            pg.display.set_icon(programIcon)
            self.clock = pg.time.Clock()
            
            """
            LEVEL CLASS GENERATES EVERYTHING AND HANDLES SPRITES
            """
            self.level = Level()
            
        
        def run(self):
            while True:
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    #pg.quit()
                    #sys.exit()
                    main_menu()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                
                self.screen.fill((126,200,80))
                self.level.run() #UPDATE GAME EACH FRAME
                #debug(round(self.clock.get_fps(), 2)) #DISPLAY FPS IN TOPLEFT CORNER
                pg.display.update()
                self.clock.tick(FPS)
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(20).render("Explore the Gardens", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(255, 50))
        text8 = get_font(20).render('High Score: '+ str(best), 1, (255, 255, 255))
        SCREEN.blit(text8, (120, 375))

        PLAY_BUTTON = Button(image=None, pos=(255, 150), text_input="PLAY", font=get_font(40), base_color="#d2f000", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(255, 225), text_input="INSTRUCTIONS", font=get_font(40), base_color="#ffbf00", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(255, 300), text_input="QUIT", font=get_font(40), base_color="#ff0000", hovering_color="White")
        
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        game = DungeonGame()
                        game.run()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        pg.display.update()

main_menu()
