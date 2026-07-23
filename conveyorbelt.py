from character import Character
from Bowser import Bowser
from PointSystem import PointSystem

class ConveyorBelt:
    """Represents a single conveyor belt. Each belt can contain 7 package positions.
    Packages move left or right depending on the belt level (odd/even)."""

    def __init__(self, level: int):
        if level >= 0:
            self.__level = level
        else:
            raise ValueError("Level must be higher than 0")
        #7 positions for package on belt → 0 means empty, 1 means there is a package
        self.__packages = [0,0,0,0,0,0,0]
        self.__fallen = [0] # tracks if a package has fallen off the belt

    @property
    def level(self):        
        return self.__level

    @property
    def packages(self):        
        return self.__packages
    
    @property
    def fallen(self):        
        return self.__fallen
    

    def add_package(self, character:Character, score:PointSystem):
        """Character can drop a package onto the belt only if:
        - they are on the correct belt (level check)
        - they have a package in hand
        - the first position on the belt is empty"""

        # odd belts, the package enters on the left side (index 0)
        if self.__level % 2 != 0 and self.__packages[0]==0 and (character.level*2) +3 == self.__level and character.has_package[0] == True and character.can_drop == True and character.has_package[1]+1 == self.__level:            
            self.__packages[0] = 1
            character.drop_package()
            score.add_pts(1)

        # even belts, the package enters on the right side (index 6)
        elif self.__level % 2 == 0 and self.__packages[6]==0 and (character.level*2) + 2 == self.__level and character.has_package[0] == True and character.can_drop == True and character.has_package[1]+1 == self.__level:
            self.__packages[6] = 1
            character.drop_package()
            score.add_pts(1)


    def remove_package(self, character:Character):
        """This method removes package from belt as the character picks it
        up."""

        # odd belts, pickup happens on the right end (index 6)
        if self.__level % 2 != 0 and self.__packages[6]==1 and (character.level*2) +1== self.__level and character.has_package[0] == False: 
            self.__packages[6] = 0
            character.pick_package(self.__level)

        # even belts, pick up happens on the left end (index 0)
        elif self.__level % 2 == 0 and self.__packages[0]==1 and (character.level*2) +2 == self.__level and character.has_package[0] == False:
            self.__packages[0] = 0
            character.pick_package(self.__level)


    def move_packages(self, character:Character, enemy:Bowser, score:PointSystem):
        """This method moves all packages along the belt according to
        direction and speed.
        - odd belts: move right (0-6)
        - even belts: move left (6-0)
         Also checks if a package reaches the end and falls.
        """

        # odd belts (move right)
        if self.__level % 2 != 0: 
            for x in range(6,-1,-1):
                # if package reaches index 6 and player is not there, it falls
                if x == 6 and self.__packages[6] == 1 and ((character.level*2)+1 != self.__level or character.has_package):
                    self.fall_packages(character,enemy,score)

                # move packages right
                if  ((x== 6 and self.__packages[6] == 0 and self.__packages[5]==1)  # special condition for the last position (index 6)
                    or ((self.__packages[x]==0 and self.__packages[x-1] == 1) and (x!=0))):  # general case for all other indices
                    self.__packages[x] = 1  # place package in the new position
                    self.__packages[x-1] = 0  # empty the old position
                
        # even belts (move left)
        else:
            for x in range(0,6):
                # if package reached index 0 and character is not there → it falls
                if x == 0 and self.__packages[0] == 1 and ((character.level*2)+2 != self.__level or character.has_package):
                    self.fall_packages(character,enemy,score)

                # move package from x+1 -> x, left
                if (x== 0 and self.__packages[0] == 0 and self.__packages[1]==1)or (self.__packages[x] == 0 and self.__packages[x+1] ==1):
                    self.__packages[x+1] = 0
                    self.__packages[x] = 1
                

    def fall_packages(self, character:Character, enemy:Bowser, score:PointSystem):
        """This method handles the package falling animation + penalty."""

        # even -> falls off left side (index 0)
        if self.__level %2 == 0:
            self.__packages[0] = 0

        # odd -> falls off right side (index 6)
        else:
            self.__packages[6] = 0

        self.__fallen[0] = 1
        enemy.caerle_al_punto(character)
        score.add_fail()
            
    def clean_while_delivering(self):
        if self.__level %2 == 0:
            if self.__packages[0] == 1:
                self.__packages[0] = 0
        elif self.__level %2 != 0:
            if self.__packages[6] == 1:
                self.__packages[6] = 0
    
    def update(self, character:Character, character2:Character,
               enemy:Bowser, score:PointSystem):
        """Each belt gets 2 characters:
        - one interacts with the belt entry
        - one interacts with the belt exit
        Depends on belt parity (odd/even)."""
        
        if self.__level %2 == 0:
            # even belts use character2 for movement and pickup
            self.move_packages(character2,enemy,score)
            self.add_package(character,score)
            self.remove_package(character2)

        else:
            # odd belts use character1 for movement and pickup
            self.move_packages(character,enemy,score)
            self.add_package(character2,score)
            self.remove_package(character)

        if self.__fallen[0] == 1 and enemy.hidden == True:
            self.__fallen[0] = 0
            
        
    def restart(self):
        """This method resets the conveyor belt to its initial state."""
        self.__packages = [0,0,0,0,0,0,0]  # all package positions are empty
        self.__fallen = [0]  # no package has fallen


    def prepare_draw_packages(self):

        # prepare a list of sprite positions for drawing packages on the belt
        draw_list =[]
        packageSide = 0
        for i,e in enumerate(self.__packages):
            if e == 1:
                # if there is a package at this position, add its drawing info
                # x = 64+11*i -> horizontal position
                # y = 102-(16*(self.__level-1)) -> vertical position depends on belt level
                # the rest of the numbers define sprite sheet coordinates and size
                if i < 3:
                    packageSide = 1
                else:
                    packageSide = 0

                # choose which sprite to draw depending on belt level,
                # packageSide (left/right)
                #   (x, y, image_bank, u, v, w, h, colkey)
                if self.__level == 2:
                    if packageSide == 0:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,0,0,16,16,0))
                    else:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,16,0,16,16,0))
                elif self.__level == 3:
                    if packageSide == 1:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,16,0,16,16,0))
                    else:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,32,0,16,16,0))
                elif self.__level == 4:
                    if packageSide == 0:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,32,0,16,16,0))
                    else:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,48,0,16,16,0))
                elif self.__level == 5:
                    if packageSide == 1:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,48,0,16,16,0))
                    else:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,0,16,16,16,0))
                elif self.__level == 6:
                    if packageSide == 0:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,0,16,16,16,0))
                    else:
                        draw_list.append((64+11*i,92-(16*(self.__level-1)),1,16,16,16,16,0))
            else:
                # if no package, place it off-screen so it is not drawn
                draw_list.append((-100,-100,0,0,0,0,0,0))

        return draw_list  # return the full list of drawing instructions
    

    def prepare_draw_packages_fallen(self):
        """Prepare a list of sprite drawing instructions for packages currently on the belt.
        Each element in the returned list is a tuple:
        (x, y, img, u, v, w, h, colkey)

        Meaning of each value:
        x, y    - screen coordinates
        img     - image bank index
        u, v    - top-left corner of the sprite in the image bank
        w, h    - width and height of the sprite
        colkey  - optional color treated as transparent

        Packages that are not present are placed off-screen with coordinates (-100, -100)
        so they are not drawn."""

        # prepare the sprite drawing info for packages that have fallen
        fallen_draw_list = []

        if self.__fallen[0] == 1:
            # if a package has fallen, choose sprite position based on belt side
            if self.__level %2 != 0:
                # odd belts -> package falls on the right side
                fallen_draw_list.append((147,100-(15*(self.__level-2)),1,0,82,6,6,0))
            if self.__level %2 == 0:
                # even belts -> package falls on the left side
                fallen_draw_list.append((53,100-(15*(self.__level-2)),1,7,82,6,6,0))
        else:
            # if no package has fallen, hide the sprite off-screen
            fallen_draw_list.append((-100,-100,0,0,0,0,1,1,0))

        return fallen_draw_list  # return the list of drawing instructions for fallen packages
