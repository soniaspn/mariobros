from character import Character
from Bowser import Bowser
from PointSystem import PointSystem
from conveyorbelt import ConveyorBelt
from truck import Truck

class SpecialConveyorBelt(ConveyorBelt):

    def __init__(self, level, range):
       super().__init__(level)  # call the parent class (ConveyorBelt) constructor to initialize its attributes
       self.__level = level
       self.__range = range
       self.__packages = [0] * self.__range
       self.__countdown = 0
       self.__fallen=[0]
       self.__picked=[0]


    @property
    def range(self):        
        return self.__range
    
    @property
    def packages(self):        
        return self.__packages
    
    @property
    def countdown(self):        
        return self.__countdown
    
    @property
    def fallen(self):        
        return self.__fallen
    
    @property
    def picked(self):        
        return self.__picked
    

    def add_package(self, character:Character, score:PointSystem):

        # if this is the level 1 special belt and countdown reaches 7,
        # automatically place a package in slot 2
        if self.level == 1 and self.__countdown==7:
            self.__packages[2] = 1
            self.__countdown = 0   # reset countdown for next automatic package

        elif self.level != 1 and self.level == (character.level*3) + 1 and character.has_package[0] == True and character.side == "left" and character.has_package[1] == 6:
            self.__packages[0] = 1      # place package in slot 0
            character.drop_package()  # remove package from character
            score.add_pts(1)          # add a point to the score

        else:
            self.__countdown +=1
    

    def move_packages(self, character:Character, enemy:Bowser,
                      score:PointSystem, truck:Truck):
        """Moves packages along the special conveyor belt.
           Level 1 belt: moves packages from right to left (slots 2 -> 1 -> 0).
           If a package reaches slot 0, it falls if not collected."""

        # for level 1 special belt
        if self.level == 1:
            # move package from slot 2 to slot 1 if slot 1 is empty
            if self.__packages[2] == 1 and self.__packages[1] == 0:
                self.__packages[2] = 0  # remove from slot 2
                self.__packages[1] = 1  # place in slot 1

            # move package from slot 1 to slot 0 if slot 0 is empty
            elif self.__packages[1] == 1 and self.__packages[0] == 0:
                self.__packages[1] = 0  # remove from slot 1
                self.__packages[0] = 1  # place in slot 0

            # if a package is in slot 0 and can't move further, it falls
            elif self.__packages[0] == 1:   
                self.fall_packages(character,enemy,score)

        # for other special belts (level != 1)
        else:
            # any package in slot 0 is stored in the truck
            if self.__packages[0] == 1:                
                self.store_package(score,truck)  # move package into truck


    def remove_package(self, character):
        """This method allows the character to pick up a package from the belt.
        Conditions:
        - Only works on level 1 special belt
        - Character must be on the bottom level (level 0)
        - Character must not already be holding a package
        - There must be a package in slot 0
        """
        # check conditions for picking up the package
        if self.level == 1 and character.level == 0 and character.has_package[0] == False and self.__packages[0] == 1:
            self.__packages[0] = 0  # remove the package from the belt
            character.pick_package(height=self.__level)  # give the package to the character


    def fall_packages(self, character:Character, enemy:Bowser,
                      score:PointSystem):
        """
        This method handles a package falling off the special conveyor belt.
        Only applies to level 1 special belt.
        Removes the package from slot 0.
        Marks the package as fallen.
        Triggers Bowser event (caerle_al_punto).
        Adds a fail to the score.
        """
        if self.level == 1:
            self.__packages[0] = 0  # remove the package from slot 0
            self.__fallen[0] = 1    # mark that a package has fallen
            enemy.caerle_al_punto(character=character)  # trigger Bowser event
            score.add_fail()      # +fail
    

    def store_package(self,score:PointSystem,truck:Truck):
        """This method moves a package from the belt into the truck."""
        self.__packages[0] =0  # remove the package from slot 0
        self.__picked[0] +=1   # count that this package has been collected
        truck.load_package()  # add the package to the truck's storage
        
    def clean_while_delivering(self):  
        if self.__level %2 ==1:
            if self.__packages[0] == 1:
                self.__packages[0] = 0

    def update(self, character: Character, character2: Character,
               enemy:Bowser, score: PointSystem, truck: Truck):
        """Updates the state of the special conveyor belt for one game tick."""

        # move packages according to belt rules
        self.move_packages(character,enemy,score,truck)

        if self.level == 1:
            # add packages (automatic or from character)
            self.add_package(character,score)
            # let character pick up a package if possible
            self.remove_package(character)
        else:
            # for other belts, only add packages from character2
            self.add_package(character2,score)

        if self.__fallen[0] == 1 and enemy.hidden == True:
            self.__fallen[0] = 0
    

    def restart(self):
        """This method resets the special conveyor belt to its initial
        state."""
        self.__packages = [0,0,0]  # remove all packages from the belt
        self.__fallen = [0]        # reset fallen package indicator
        self.__picked = [0]        # reset count of picked packages


    def prepare_draw(self):
        """This method prepares the drawing instructions for the special
        conveyor belt."""
        draw_list =[]

        # go through all package slots
        for i,e in enumerate(self.__packages):
            if e == 1:  # if a package exists in this slot
                if self.level == 1:
                    # calculate x position based on slot index, y is fixed for level 1
                    draw_list.append((184-8*(2-i),76,1,0,0,16,16,0))
                else:
                    # for other levels, hide packages off-screen
                    draw_list.append((-100,-100,1,0,58,6,4,0))
            else:
                # no package, hide it off-screen
                draw_list.append((-100,-100,1,0,58,6,4,0))

        # draw fallen packages if any
        if self.__fallen[0] == 1:
            draw_list.append((160,100-(15*(self.level-1)),1,0,82,6,6,0))
        
        return draw_list
        