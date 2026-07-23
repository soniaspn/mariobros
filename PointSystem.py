
class PointSystem:
    def __init__(self):
        self.__pts = 0  # the score the player has
        self.__fails = 0  # number of mistakes

    @property
    def pts(self):        
        return self.__pts
    
    @property
    def fails(self):        
        return self.__fails
    
    def add_pts(self,qty):
        """Method that adds points to the score."""
        self.__pts += qty

    def subst_pts(self,qty):
        """Method that subtracts points from the score."""
        self.__pts -= qty
        if self.__pts < 0:  # prevents points from going negative
            self.__pts = 0

    def restart_pts(self):
        """Method that resets the score."""
        self.__pts = 0

    def add_fail(self):
        """Method that adds one fail."""
        self.__fails +=1

    def subst_fails(self,qty):
        """Method that subtracts one fail."""
        self.__fails -= qty
        if self.__fails < 0:
            self.__fails = 0

    def restart_fails(self):
        """Method that resets the fails."""
        self.__fails = 0

    def restart(self):
        """Method that resets both score and fails."""
        self.restart_fails()
        self.restart_pts()
