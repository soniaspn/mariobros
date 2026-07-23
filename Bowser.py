from character import Character

class Bowser:
    def __init__(self):
        self.hidden = True  # Bowser starts hidden
        self.side = None
        self.level = None
        self.lose = False
        self.countdown = 0
       

    def frenar_el_operativo(self):
        """The player has lost because Bowser caught them."""
        self.lose = True

    def caerle_al_punto(self,character:Character):
        self.hidden = False  # Bowser becomes visible
        self.side = character.side  # he appears on the character's side
        self.level = character.level # appears on the same level as the character
        self.countdown = 0  # resets the timer
        self.frenar_el_operativo()  # triggers lose condition

    def restart(self):
        """This method resets Bowser back to his initial state."""
        self.hidden = True  # hide Bowser again
        self.lose = False   # clear lose condition
        self.countdown = 0  # prepare for next appearance
        
    def update(self):
        if not self.hidden:  # if Bowser is visible
            self.countdown += 1  # counts how long he has been visible for
            if self.countdown >= 60:  # if visible for 60 frames
                self.restart()

    def prepare_draw(self):
        
        if self.hidden:
            return (-100,-100,1,0,58,6,4)  # drawing him off-screen so he is invisible
        else:
            if self.side == "left":
                return(4,80,0,1,80,16,17,0)  # Bowser visible on left side
            # (x, y, flip_x, sprite_u, sprite_v, width, height, layer)
            else:
                return(192,56,0,1,64,16,17,0)  # Bowser visible on right side
