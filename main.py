from conveyorbelt import ConveyorBelt
from SpecialConveyorBelt import SpecialConveyorBelt
from character import Character
from truck import Truck
from Bowser import Bowser
from PointSystem import PointSystem
import pyxel
FPS = 30

# create game objects
belt1 = SpecialConveyorBelt(level=1,range=3)
belt2 = ConveyorBelt(level=2)
belt3 = ConveyorBelt(level=3)
belt4 = ConveyorBelt(level=4)
belt5 = ConveyorBelt(level=5)
belt6 = ConveyorBelt(level=6)
belt7 = SpecialConveyorBelt(level=7,range=1)

belt_list = [belt2,belt3,belt4,belt5,belt6]
special_belt_list = [belt1,belt7]

Capataz = Bowser()
Luigi = Character("left",up =pyxel.KEY_W,down = pyxel.KEY_S)
Mario = Character("right",up=pyxel.KEY_UP,down=pyxel.KEY_DOWN,)
Main_score = PointSystem()
FedEx = Truck()


class App:
    def __init__(self):
        self.__paused = False       # True when game is paused
        self.__lost = False         # True when the player loses (3 fails)
        self.__upd_break = False    # freeze updates when Bowser appears
        self.__delivering = False   # True when truck is out for delivery
        
        # New Menu and Speed attributes
        self.__in_menu = True          # Shows the speed selection menu
        self.__belt_speed = 15         # Default Normal (Medium)
        self.__special_belt_speed = 30 # Default Special (Medium)

        # initialize Pyxel window and load resources
        pyxel.init(208,112, "Mario Bros", fps=FPS)
        pyxel.load("./assets/sprites.pyxres")

        # start the game loop
        pyxel.run(self.update, self.draw)
    
    @property
    def paused(self):        
        return self.__paused
    
    @property
    def lost(self):        
        return self.__lost
    
    @property
    def upd_break(self):        
        return self.__upd_break
    
    @property
    def delivering(self):        
        return self.__delivering
    
    @property
    def in_menu(self):        
        return self.__in_menu
    
    @property
    def belt_speed(self):        
        return self.__belt_speed
    
    @property
    def special_belt_speed(self):        
        return self.__special_belt_speed

    
    def update(self):
        
        if self.__in_menu:
            if pyxel.btnp(pyxel.KEY_1): # Slow
                self.__belt_speed = 30
                self.__special_belt_speed = 40
                self.__in_menu = False
            elif pyxel.btnp(pyxel.KEY_2): # Normal
                self.__belt_speed = 25
                self.__special_belt_speed = 35
                self.__in_menu = False
            elif pyxel.btnp(pyxel.KEY_3): # Fast
                self.__belt_speed = 20
                self.__special_belt_speed = 25
                self.__in_menu = False
            return # Stop here, do not run game logic

        
        Capataz.update()  # update Bowser
        FedEx.update(Main_score)  # update truck logic

        #pause
        if pyxel.btnp(pyxel.KEY_P):
            self.__paused = not self.__paused

        # restart after losing
        if pyxel.btnp(pyxel.KEY_R) and self.__lost == True:
            Mario.restart()
            Luigi.restart()
            for i in belt_list:
                i.restart()
            Capataz.restart()
            for i in special_belt_list:
                i.restart()
            Main_score.restart()
            FedEx.restart()

        self.__delivering = FedEx.is_out_for_delivery
        self.__lost = (Main_score.fails == 3)
        self.__upd_break = not Capataz.hidden  # freeze if Bowser appears

        # if paused, lost, delivering or Bowser blocks updates, stop updates
        if self.__paused or self.__lost or self.__upd_break or self.__delivering:
            if self.__delivering == True:
                for i in belt_list:
                    i.clean_while_delivering()
                belt1.clean_while_delivering()
            return

        # update characters
        Mario.update()
        Luigi.update()
        
        # NORMAL BELT UPDATE (timer controlled)
        if pyxel.frame_count % self.__belt_speed == 0:
            for s in belt_list:
                s.update(Mario,Luigi,Capataz,Main_score)

        # SPECIAL BELT UPDATE
        if pyxel.frame_count % self.__special_belt_speed == 0:    
            for i in special_belt_list:
                i.update(Mario,Luigi,Capataz,Main_score,FedEx)
        


    def draw(self):
        pyxel.cls(0)
        
        # draw menu if active
        if self.__in_menu:
            pyxel.text(75, 40, "SELECT SPEED:", 7)
            pyxel.text(75, 55, "1. SLOW", 11)
            pyxel.text(75, 65, "2. NORMAL", 10)
            pyxel.text(75, 75, "3. FAST", 8)
            return

        # draw background tilemap
        pyxel.bltm(0, 0, 0, 0, 0, 208, 112)
        # draw characters and truck
        pyxel.blt(*Mario.prepare_draw())
        pyxel.blt(*Luigi.prepare_draw())
        pyxel.blt(*FedEx.prepare_draw_truck_body())
        pyxel.blt(*FedEx.prepare_draw_loaded_packages())
        # score and fails
        pyxel.text(30,5,"Score:"+str(Main_score.pts),9)
        pyxel.text(160,5,"Fails:"+str(Main_score.fails),2)

        # draw normal belt packages
        for i in belt_list:
            for args in i.prepare_draw_packages():
                if args[2] != 0:  # only draw visible sprites
                    pyxel.blt(*args)
            for args2 in i.prepare_draw_packages_fallen():
                pyxel.blt(*args2)

        # draw center wall
        for i in range(0, 96, 16):
            pyxel.blt(96, i, 0, 0, 192, 16, 16, 0)

        # draw special belts
        for i in special_belt_list:
            for args in i.prepare_draw():
                pyxel.blt(*args)
        # draw Bowser
        pyxel.blt(*Capataz.prepare_draw())

        # status messages
        if self.__paused == True:
            pyxel.text(60,40,"PAUSED", 7)
        if self.__delivering == True:
            pyxel.text(75,50,"DELIVERING", 7)

        # Game Over screen
        if Main_score.fails == 3:
            pyxel.cls(0)
            pyxel.text(90,50,"YOU LOSE", 8)


App()