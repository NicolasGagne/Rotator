"""
Rotator Class
"""
import time
from HR8825 import HR8825

class Rotator():
    def __init__(self):
        self.actual_az = 0
        self.actual_el = 0
        self.target_az = 0
        self.target_el = 0
        """
        # 1.8 degree: nema23, nema14
        # softward Control :
        # 'fullstep': A cycle = 200 steps
        # 'halfstep': A cycle = 200 * 2 steps
        # '1/4step': A cycle = 200 * 4 steps
        # '1/8step': A cycle = 200 * 8 steps
        # '1/16step': A cycle = 200 * 16 steps
        # '1/32step': A cycle = 200 * 32 steps
        """
        self.stepAngleName = 'fullstep'
        self.motorStepPerTurn = 200
        self.precisionLimite = 360 / (self.motorStepPerTurn * 16)  # '1/16step': A cycle = 200 * 16 steps
        print('Precision Limit: ', self.precisionLimite, " degrees")
        self.Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))


    def readServerData(self, data):

        match(data[0:2]):

            case "p\n": #Get position.
                return self.actualPosition()

            case "P ": #Set position
                # create format exemple: ['P', '136.61', '12.37\n']
                values = data.split(" ")

                self.target_az = float(values[1])
                self.target_el = float(values[2])
                return "RPRT 0" #required to avoid errori

            case "S ": #Stop the rotator.
                #self.Motor1.Stop()
                #self.Motor2.Stop()
                return

            case "M ":  # Move the rotator in a specific direction at the given rate.
                return

            case "K ":  # Park the rotator
                self.target_az = 0
                self.target_el = 0
                return

            case "R ":  # Reset the rotator.
                return

            case _:
                print('Unknown request form client: ', data)
                return

    def actualPosition(self):
        response = "{}\n{}\n".format(self.actual_az, self.actual_el)
        return response

    def moveRotator(self, stop_event):
        """
        this function run on a separate thread in main file.
        :return: none (It should never stop)
        """
        while not stop_event.is_set():

            time.sleep(.5)  # Slowing the code for the motors
            self.resetRotatorPosition()  # Reset to zero if rotator is back to 0.0
            # Calculate delta both
            """
            More work needed in the math side to reach via the quickest way
            Need reserche on calculating shortest path on sphère. 
            az -
                - negative = Counter clock wise
                - positive = clockwise              
            el -
                -
            """
            #calculate Azimuth delta
            if self.target_az - self.actual_az < 180:
                d_az = self.target_az - self.actual_az
            else:
                d_az = -360 + self.target_az - self.actual_az

            #calculate Elevation delta
            d_el = self.target_el - self.actual_el



            if abs(d_az) > abs(d_el):
                #Azimut
                self.adjustRotatorSpeed(abs(d_az))
                # Motor1.SetMicroStep('softward', self.stepAngleName)
                # Motor2.SetMicroStep('softward', self.stepAngleName)
                """
                Bellow TEST move
                """
                if d_az > 0 and abs(d_az) > self.precisionLimite:
                    self.actual_az = self.actual_az + (360 / self.stepPerTurn())

                    #Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.005)
                    #Motor2.TurnStep(Dir='forward', steps=1, stepdelay=0.005)
                elif  d_az < 0 and abs(d_az) > self.precisionLimite:
                    self.actual_az = self.actual_az - (360 / self.stepPerTurn())
                    #Motor1.TurnStep(Dir='backward', steps=1, stepdelay=0.005)
                    #Motor2.TurnStep(Dir='backward', steps=1, stepdelay=0.005)

            else:
                #Elevation
                self.adjustRotatorSpeed(abs(d_el))
                # Motor1.SetMicroStep('softward', self.stepAngleName)
                # Motor2.SetMicroStep('softward', self.stepAngleName)

                if d_el > 0 and abs(d_el) > self.precisionLimite:
                    self.actual_el = self.actual_el + (360 / self.stepPerTurn())
                    # Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.005)
                    # Motor2.TurnStep(Dir='backward', steps=1, stepdelay=0.005)
                elif d_el < 0 and abs(d_el) > self.precisionLimite:
                    self.actual_el = self.actual_el - (360 / self.stepPerTurn())
                    # Motor1.TurnStep(Dir='backward', steps=1, stepdelay=0.005)
                    # Motor2.TurnStep(Dir='forward', steps=1, stepdelay=0.005)



    def resetRotatorPosition(self):
        """
        Check if the Rotator expect to be at 0.0 and if switch match and reset.

        :return: none
        """
        # add switches to IF
        if (self.target_az == 0 and
                self.target_el == 0 and
                abs(self.actual_az) < self.precisionLimite and
                abs(self.actual_el) < self.precisionLimite):
            #print('Rotator Position reset to AZ 0 and EL 0')
            self.actual_az = 0
            self.actual_el = 0

        """
        
        elif (self.target_az == 0 and 
            self.target_el == 0 and 
            abs(self.actual_az) < self.precisionLimite and 
            abs(self.actual_el) < self.precisionLimite):
            self.adjustRotatorSpeed(1)
            Motor1.SetMicroStep('softward', self.stepAngleName)
            Motor2.SetMicroStep('softward', self.stepAngleName)
            print('Reseting AZ position')
            while not self.on_switch():
                #Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.005)
                Motor2.TurnStep(Dir='forward', steps=1, stepdelay=0.005)
            self.actual_az = 0 
            print('Reseting AZ position')
            while not self.on_switch():
                # Motor1.TurnStep(Dir='backward', steps=1, stepdelay=0.005)
                # Motor2.TurnStep(Dir='forward', steps=1, stepdelay=0.005)
            self.actual_el = 0 
        else: Do nothing
        """



    def adjustRotatorSpeed(self, delta):
        if delta > 45:
            self.stepAngleName = 'fullstep'
            return
        elif delta > 20:
            self.stepAngleName = 'halfstep'
            return

        elif delta > 5:
            self.stepAngleName = '1/4step'
            return

        elif delta > 1:
            self.stepAngleName = '1/8step'
            return
        else:
            self.stepAngleName = '1/16step'
            return



    def stepPerTurn(self):
        """

        :return: the number of step in 360 degree depending on the microstep setting
        """
        """
               # Exemple 1.8 degree: nema23, nema14
               # softward Control :
               # 'fullstep': A cycle = 200 steps
               # 'halfstep': A cycle = 200 * 2 steps
               # '1/4step': A cycle = 200 * 4 steps
               # '1/8step': A cycle = 200 * 8 steps
               # '1/16step': A cycle = 200 * 16 steps
               # '1/32step': A cycle = 200 * 32 steps
               """
        match (self.stepAngleName):

            case 'fullstep':
                return self.motorStepPerTurn

            case 'halfstep':
                return self.motorStepPerTurn * 2

            case '1/4step':
                return self.motorStepPerTurn * 4

            case '1/8step':
                return self.motorStepPerTurn * 8

            case '1/16step':
                return self.motorStepPerTurn * 16

            case '1/32step':
                return self.motorStepPerTurn * 32
            case _:
                print("error", self.stepAngleName)
                return "Step Type not good"
