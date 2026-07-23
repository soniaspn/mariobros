from PointSystem import PointSystem
class Truck:
    """ Represents the delivery truck that Luigi loads with finished packages.
    The truck always has a fixed capacity of 8 packages.
    When it is full, it goes out for delivery and returns empty."""

    def __init__(self):

        self.__loaded_packages = 0  # how many packages are inside
        self.__is_out_for_delivery = False # truck status
        self.__deliveries_done = 0  # completed deliveries
        self.__countdown = 0  # counts how long the truck stays out


    # read-only properties
    @property
    def loaded_packages(self):        
        return self.__loaded_packages
    
    @property
    def is_out_for_delivery(self):        
        return self.__is_out_for_delivery
    
    @property
    def deliveries_done(self):        
        return self.__deliveries_done
    
    @property
    def countdown(self):        
        return self.__countdown
    


    def load_package(self):
        """This method increases the number of packages by 1, but only up to
        8."""
        if self.__loaded_packages < 8:    
            self.__loaded_packages +=1


    def deliver(self, score:PointSystem):
        """This method shows what happens when truck goes to deliver (when
        truck becomes full)."""
        score.add_pts(10)  # you get 10 points
        self.__deliveries_done +=1  # delivery count increases
        self.__is_out_for_delivery = True  # truck is out
        self.__loaded_packages = 0  # packages reset to 0
        if self.__deliveries_done % 3== 0:  # every three deliveries remove one fail
            score.subst_fails(qty=1)
        

    def come_back(self):
        """Method that simply returns the truck to the loading area."""
        self.__is_out_for_delivery = False


    def update(self,score:PointSystem):
        # when full, reset countdown + go deliver
        if self.__loaded_packages == 8:
            self.__countdown = 0
            self.deliver(score)
        # while away, increase timer
        if self.__is_out_for_delivery == True and self.__countdown == 150:
            self.come_back()
        if self.__is_out_for_delivery == True:
            self.__countdown +=1


    def restart(self):
        """This method restarts the truck."""
        self.__countdown = 0
        self.__is_out_for_delivery = False
        self.__deliveries_done = 0
        self.__loaded_packages = 0
   
    
    def prepare_draw_truck_body(self):
        """ This method returns sprite coordinates for drawing the truck body.
        If truck is out delivering -> hide it off-screen."""
        if self.__is_out_for_delivery:
            return(-100,-100,1,0,58,6,4)
        
        else:
            return(2,44,0,16,80,16,16,0)


    def prepare_draw_loaded_packages(self):
        """This method returns sprite coordinates for drawing the packages
        inside the truck.
        If truck is away -> hide graphics.
        If truck is here:
        - show empty slot sprite when empty
        - use different coordinates depending on how many packages are loaded
        """
        if self.__is_out_for_delivery:
            return(-100,-100,1,0,58,6,4)

        # if truck is visible
        else:
            if self.__loaded_packages == 0:
                return(17,54,1,17,42,16,6,0)  #(x, y, img, u, v, w, h, colkey)
            elif self.__loaded_packages<5:
                return(16,44,1,16*(self.__loaded_packages-1),48,16,16,0)
            else:
                return(16,44,1,16*(self.__loaded_packages-5),64,16,16,0)