import pygame   as pg
import os
import random
import json
import time

from .constants import *
from .scenery   import Scenery
from .player    import Player
from .enemy     import Enemy
from .treasure_chest    import Treasure_Chest
from .move_room import Move_Room
from .going_tile import Going_Tile
from .sounds    import *
from .debug     import debug
from .prompt    import Prompt
from .treasure_winner   import Treasure_Winner

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
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(25).render("Instructions", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(255, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(255, 400), 
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
                        pg.quit()
                        sys.exit()
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
font2 = pg.font.SysFont('comicsans', 20, True)
font3 = pg.font.SysFont('comicsans', 100, True)
font4 = pg.font.SysFont('comicsans', 50, True)
def get_high_score():
    high_score_file = open("high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score

class Level():
    """
    - LOADS THE MAP DATA
    - PLACES ALL SPRITES
    - CALLS UPDATE METHOD
    """    
    def __init__(self):
        #SET UP SPRITE GROUPS
        self.visible_sprites  = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        self.prompts          = pg.sprite.Group()
        self.display_surface = pg.display.get_surface()
        self.data_files = ["player.json"]
        self.room_list = ['1', '2', '3', '4', '5', '6', '7', '8']
        [self.data_files.append(f"rooms/{room}/status.json") for room in self.room_list]
        [self.data_files.append(f"rooms/{room}/layout.txt") for room in self.room_list]
        
        self.going_dict = {"n":"North","e":"East","s":"South","w":"West"}
        self.direction_list = ['n', 'e', 's', 'w']
        
        self.current_room = self.room_list[0]
        
        pg.mixer.music.play(-1)
        
        self.complete = False
        self.reset_game()
        self.create_map(self.current_room)
    
    def create_map(self, level='1'):
        self.current_room = level
        
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        
        #LOAD THE LEVEL FILE PASSED AS PARAMETER
        with open(resource_path(os.path.join(f"DungeonGame/data/live/rooms/{level}", "layout.txt")), 'r') as level_file:
            world_map = level_file.readlines()
        
        #GENERATE TERRAIN AND PLAYER BASED ON MAP FILE
        for row_index, row in enumerate(world_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                
                #BLOCKADES
                if col.lower() == 'x':
                    Scenery(
                        name     = "stump",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites, self.obstacle_sprites]
                    )
                
                #FOLIAGE
                elif col.lower() == 'f':
                    Scenery(
                        name     = f"foliage/{random.randrange(0,7)+1}",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites]
                    )
                
                #TREES
                elif col.lower() == 't':
                    Scenery(
                        name     = f"tree/{random.randrange(0,3)+1}",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites, self.obstacle_sprites],
                        size     = (64,64)
                    )
                
                #ROOM MOVING TILES
                elif col.lower() in self.room_list:
                    Move_Room(
                        name     = col.lower(),
                        position = (x, y),
                        sprite_groups = [self.visible_sprites],
                        level = self
                    )
                
                #WINNER TREASURE
                elif col.lower() == "m":
                    Treasure_Winner(
                        name     = col.lower(),
                        position = (x, y),
                        sprite_groups = [self.visible_sprites],
                        level = self
                    )
                
                #GOING TILES
                elif col.lower() in self.direction_list:
                    Going_Tile(
                        name     = self.going_dict[col.lower()],
                        position = (x, y),
                        sprite_groups = [self.visible_sprites]
                    )
                
        player_data = self.load_json_data("player.json")
        room_sprite_data = self.load_json_data(f"rooms/{level}/status.json")
        
        self.player = Player(
            name             = "player",
            position         = (room_sprite_data["entries"][player_data["Going"]]["X"], room_sprite_data["entries"][player_data["Going"]]["Y"]),
            sprite_groups    = [self.visible_sprites], #MUST PASS 'visible_sprites' FIRST
            obstacle_sprites = self.obstacle_sprites,
            target           = "enemy",
            damage           = 100,
            health           = player_data["Health"],
            gold             = player_data["Gold"]
        )
        
        try:
            for chest in room_sprite_data["chests"]:
                Treasure_Chest(
                    name     = "treasure_chest",
                    position = (room_sprite_data["chests"][chest]["Position X"], room_sprite_data["chests"][chest]["Position Y"]),
                    sprite_groups = [self.visible_sprites, self.obstacle_sprites],
                    health   = room_sprite_data["chests"][chest]["Health"]
                )
        except KeyError:
            print("No chests data provided this room.")
        
        try:
            for enemy in room_sprite_data["enemies"]:
                if room_sprite_data["enemies"][enemy]["Health"] > 0:
                    Enemy(
                        name             = "enemy",
                        position         = (room_sprite_data["enemies"][enemy]["Position X"], room_sprite_data["enemies"][enemy]["Position Y"]),
                        sprite_groups    = [self.visible_sprites], #MUST PASS 'visible_sprites' FIRST
                        obstacle_sprites = self.obstacle_sprites,
                        target           = self.player,
                        damage           = 40,
                        health   = room_sprite_data["enemies"][enemy]["Health"]
                    )
        except KeyError:
            print("No enemy data provided this room.")
    
    def reset_game(self):
        """
        LOADS ALL STANDARD DATA FROM CORE DATA DIRECTORIES
        PASSES THEM TO THE LIVE VERSIONS TO BE RESET
        """
        self.complete = False
        for path in self.data_files:
            if path.endswith('.json'):
                data = self.load_json_data(path, "core")
                self.write_json_data(path, data)
            elif path.endswith('.txt'):
                data = self.load_text_data(path, "core")
                self.write_text_data(path, data)
            print(f"Reset: {path}")
    
    def write_json_data(self, path, data):
        """
        WRITES GIVEN DATA TO THE LIVE VERSIONS OF THE PATH PROVIDED
        """
        path = resource_path(os.path.join("DungeonGame/data/live/", path))
        
        with open(path, 'w+', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def load_json_data(self, path, data_type="live"):
        """
        LOADS EITHER CORE OR LIVE DATA OF THE PATH GIVEN AS JSON
        """
        path = resource_path(os.path.join(f"DungeonGame/data/{data_type}/", path))
        print(f"Loading data from: {path}")
        with open(path, 'r') as status_file:
            status = json.load(status_file)
        return status
    
    def write_text_data(self, path, data):
        """
        WRITES GIVEN DATA TO THE LIVE VERSIONS OF THE PATH PROVIDED
        """
        path = resource_path(os.path.join("DungeonGame/data/live/", path))
        with open(path, 'w+') as file:
            file.writelines(data)
    
    def load_text_data(self, path, data_type="live"):
        """
        LOADS EITHER CORE OR LIVE DATA OF THE PATH GIVEN AS JSON
        """
        path = resource_path(os.path.join(f"DungeonGame/data/{data_type}/", path))
        print(f"Loading data from: {path}")
        with open(path, 'r') as layout_file:
            content = layout_file.read()
        return content
    
    def save_room_state(self, room):
        data = self.load_json_data(f"rooms/{room}/status.json")
        data["chests"] = {}
        data["enemies"] = {}
        count = 0
        for sprite in self.visible_sprites:
            if sprite.name == "treasure_chest":
                data["chests"][count] = {"Health": sprite.health, "Position X": sprite.rect.x, "Position Y": sprite.rect.y}
                count += 1
        count = 0
        for sprite in self.visible_sprites:
            if sprite.name == "enemy":
                data["enemies"][count] = {"Health": sprite.health, "Position X": sprite.rect.x, "Position Y": sprite.rect.y}
                count += 1
        self.write_json_data(f"rooms/{room}/status.json", data)
    
    def save_player_state(self):
        data = self.player.get_info()
        self.write_json_data("player.json", data)
    
    def run(self):
        #DRAW ALL VISIBLE SPRITES
        best = get_high_score()
        self.visible_sprites.custom_draw(self.player)
        text9 = font2.render('Press ESC to Close Program', 1, (0, 0, 0))
        self.display_surface.blit(text9, (10, SCREENHEIGHT-50))
        text8 = font2.render('High Score: '+ str(best), 1, (0, 0, 0))
        self.display_surface.blit(text8, (SCREENWIDTH-115, SCREENHEIGHT-50))
        self.visible_sprites.update()
        self.prompts.update()
        text1 = font3.render('You died!', 1, (255, 0, 0))
        text2 = font4.render('Adventure Complete!', 1, (0, 255, 0))
    
        
        if self.player.health <= 0:
            self.reset_game()
            self.create_map(1)
            self.display_surface.blit(text1, (100, SCREENHEIGHT-100))
            main_menu()
            
        
        if self.complete:
            self.reset_game()
            self.create_map(1)
            self.display_surface.blit(text2, (10, SCREENHEIGHT-110))
            main_menu()



class YSortCameraGroup(pg.sprite.Group):
    """
    CUSTOM SPRITE GROUP CLASS TO:
        - ORDER SPRITES BY THEIR Y COORDINATE SO OVERLAP IS CORRECT
        - CREATE A CAMERA BY OFFSETTING VISIBLE SPRITES BASED ON PLAYER POSITION
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width      = SCREENWIDTH//2
        self.half_height     = SCREENHEIGHT//2
        self.offset          = pg.math.Vector2()
    
    def custom_draw(self,player):
        #GETTING THE OFFSET
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #OFFSET SPRITE POSITIONS
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
