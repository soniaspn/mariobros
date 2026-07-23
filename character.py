import pyxel
class Character:
    """ This class contains the code needed for Mario/Luigi in the final project """
    def __init__(self, side: str, up,down):
        """ This magic method is used to create the attributes of the objects. """
        if side.lower() == "left" or side.lower() == "right":
            self.__side = side
        else:
            raise ValueError("Level must be left or right")
        # We decide that Mario will always be created at the lower __level, so no
        # parameter for __level, we assign directly the value of 0 (lower __level)
        self.__level = 0
        # It will start with no package, so no parameter for this either
        self.__has_package = [False,0]
        self.__up = up
        self.__down = down
        self.__cooldown = 0 # prevents moving too fast
        self.__hold_cooldown = 0

    @property
    def side(self):        
        return self.__side

    @property
    def level(self):        
        return self.__level

    @property
    def has_package(self):        
        return self.__has_package

    @property
    def up(self):        
        return self.__up

    @property
    def down(self):        
        return self.__down
    
    @property
    def cooldown(self):        
        return self.__cooldown

    @property
    def hold_cooldown(self):        
        return self.__hold_cooldown
    
    @property
    def can_drop(self):
        return self.__hold_cooldown == 0

    # movement between floors
    def move_up(self):
        if self.__level < 2:
            self.__level += 1

    def move_down(self):
        if self.__level > 0:
            self.__level -= 1


    # pick up / drop package methods:
    def pick_package(self,height):
        self.__has_package[0] = True
        self.__has_package[1] = height
        self.__hold_cooldown = 1
        self.__cooldown += 15

    def drop_package(self):       
        self.__has_package[0] = False
        self.__has_package[1] = 0

    def restart(self):
        """ This method resets the character for new round. """
        self.__level= 0
        self.__has_package[0] = False
        self.__has_package[1] = 0
        self.__cooldown = 0
        self.__hold_cooldown = 0

    def update(self):
        
        if pyxel.btnp(self.__up) and self.__cooldown ==0:  # player pressed the UP key this frame
            self.move_up()
            self.__cooldown += 5
        if pyxel.btnp(self.__down) and self.__cooldown ==0:  # player pressed the DOWN key this frame
            self.move_down()
            self.__cooldown += 5
        if self.__cooldown > 0:  # decrease cooldown every frame, once it reaches 0, the player can move again
            self.__cooldown -=1
        if self.__hold_cooldown > 0: 
            self.__hold_cooldown -=1

    def prepare_draw(self):
        """This method calculates where the character and sprite appear. It
        is based on game art."""
        if self.__side == "left":
           x = 40
           v = 33
           y = 77-(32 * self.__level)  # levels are evenly spaces by 32 pyxels
        
        else:
           x = 152 
           v = 1
           if self.__level !=2:  # special case for top floor
                y = 89-(28 * self.__level)
           else:
               y = 29

        if self.__has_package[0] == True:  # this changes sprite tile
            u = 16
        else:
            u = 1

        return (x,y,0,u,v,11,15,0)  # (x, y, flip_x, sprite_u, sprite_v, width, height, layer)
