#!/usr/bin python3
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 85
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1650  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "m": ("Michael Test", self.square),
                "a": ("Stop at wall", self.stopatwall),
                "r": ("Go around the box", self.round),
                "b": ("Maze", self.maze),
                "p": ("Detect", self.detect)
                }
               
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''
    def square(self):
      self.fwd()
      time.sleep(2)
      self.stop()

      self.left(primary=30, counter=-40)
      time.sleep(2)
      self.stop()

      self.fwd()
      time.sleep(2)
      self.stop()


      self.left(primary=30, counter=-40)
      time.sleep(2)
      self.stop()

      self.fwd()
      time.sleep(2)
      self.stop()

      self.left(primary=30, counter=-40)
      time.sleep(2)
      self.stop()

      self.fwd()
      time.sleep(2)
      self.stop()
      
    def round(self):
        wall_stoping_distance = 200
        if (self.read_distance() < wall_stoping_distance):
          self.stop()
          self.servo(1200)
          time.sleep(0.5)
          right = self.read_distance()
          self.servo(2000)
          time.sleep(0.5)
          left = self.read_distance()
            
          if(left > right):
            self.left(primary=30, counter=-40)
            time.sleep(2)
            self.stop()
            self.fwd()
            time.sleep(2)
            self.stop()
            self.right(primary=30, counter=-40)
            time.sleep(2)
            self.stop()

          if(right > left):
            self.right(primary=30, counter=-40)
            time.sleep(2)
            self.stop()
            self.fwd()
            time.sleep(2)
            self.stop()
            self.left(primary=30, counter=-40)
            time.sleep(2)
            self.stop()
          
        else:
          self.servo(self.MIDPOINT)
          self.fwd()



    def dance(self):
        
        # lower-ordered example...
        self.right()
        time.sleep(2)
        self.stop()

        self.left()
        time.sleep(2)
        self.stop()

        self.fwd()
        time.sleep(2)
        self.stop()
        
        self.right()
        time.sleep(1)
        self.stop()

        self.left()
        time.sleep(1)
        self.stop()


    def stopatwall(self):
      wall_stoping_distance = 100
      while True:
        if self.read_distance() < 100:
          self.left(primary=30, counter=-40)
          time.sleep(2)
          self.stop()
          self.fwd()

        else:
          self.fwd()

    def maze(self):
      wall_stoping_distance = 150
      while True:
        if (self.read_distance() < wall_stoping_distance):
          self.stop()
          self.servo(900)
          time.sleep(0.5)
          right = self.read_distance()
          self.servo(2300)
          time.sleep(0.5)
          left = self.read_distance()
            
          if(left > right):
            self.left(primary=30, counter=-30)
            time.sleep(2)
            self.stop()
            self.fwd()

          if(right > left):
            self.right(primary=30, counter=-30)
            time.sleep(2)
            self.stop()
            self.fwd()

        else:
         self.servo(self.MIDPOINT)
         self.fwd()

    def detect(self):
      wall_stoping_distance = 300
      while True:
        self.fwd()
        self.servo(1200)
        time.sleep(0.5)
        right = self.read_distance()

        self.servo(2000)
        time.sleep(0.5)
        left = self.read_distance()
        if(left < wall_stoping_distance):
          self.stop()
          self.servo(self.MIDPOINT)
          time.sleep(.2)
          if(self.read_distance() > wall_stoping_distance):
            self.right(primary=50, counter=20)
            time.sleep(1)
            self.fwd()
            self.left(primary=20, counter=50)
            time.sleep(1)
            self.fwd()
          else:
            self.round()
            
            
        elif(right < wall_stoping_distance):
          self.stop()
          self.servo(self.MIDPOINT)
          time.sleep(.2)
          if(self.read_distance() > wall_stoping_distance):
            self.left(primary=50, counter=20)
            time.sleep(1)
            self.fwd()
            self.right(primary=20, counter=50)
            time.sleep(1)
            self.fwd()
          else:
            self.round()

          
            

         
         

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        pass

    def shake(self):
        """ Another example move """
        self.deg_fwd(720)
        self.stop()

    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        while self.read_distance() > 250:  # TODO: fix this magic number
            self.fwd()
            time.sleep(.01)
        self.stop()
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
