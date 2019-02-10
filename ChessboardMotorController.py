import RPi.GPIO as GPIO
import time
class MotorController:
    
    

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.ResetPin = [3, 5]
        self.MotorPins = [
            [26, 19], #[Direction, Step]
            [35, 37]
        ]

        self.activeMotors = [0]
        
        self.MAGNET = 39

        self.STEP = 19#35
        self.DIR = 26#37
        self.CW = 1
        self.CCW = 0
        self.SPR = int(360/1.8)
        
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.output(self.DIR, self.CW)

        GPIO.setup(self.MAGNET, GPIO.OUT)
        
        self.delay = 0.2/self.SPR

        
        self.position = [0, 0]
        self.resetButton = [False, False]
        
        self.originPosition = [-99, -99]
        
        self.graveyardXPosition= float(13.5)


        for i in range(0,2):
            GPIO.setup(self.ResetPin[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #TODO: change to GPIO>PUD_DOWN IF CONNECTED TO 5V

        
        self.TPI = 20 #turns per inch of the threaded rod
        
        self.SizeOfSquare = 1.5 #size of the square of the chess board in inches

    def distanceToTurns(self, distance): #changes distance in inches to turns
        return distance * self.TPI

    def TurnMotor(self, tempMotorPins, turns): #TODO update the position of the piece as you move the motor
        if self.isDoneTurning(turns) == False:
            if turns > 0:
                GPIO.output(tempMotorPins[0], self.CW)
            else:
                GPIO.output(tempMotorPins[0], self.CCW)
            GPIO.output(tempMotorPins[1], GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(tempMotorPins[1], GPIO.LOW)
            time.sleep(self.delay)
            turns -= 1/self.SPR
        return turns

    def TurnFor(self, myTurns):
        j=0
        while True:
            doneTurning = True;
            j = j + 1
            if j%10 == 0:
                print(myTurns[0])
            for motor in self.activeMotors:
                if j == 1:
                    print(motor)
                if(self.isPositionReset(motor) == False):
                    myTurns[motor] = self.TurnMotor(self.MotorPins[motor],myTurns[motor])
                    doneTurning = doneTurning and self.isDoneTurning(myTurns[motor]) == True
                else:
                    print("position reset for motor")
            if(doneTurning == True):
                print("finished turning")
                break;
        print(myTurns[0])

    def isPositionReset(self, resetIndex):
        input_state = GPIO.input(self.ResetPin[resetIndex])
        return input_state == self.resetButton[resetIndex] and input_state == True

    def resetPosition(self):
        
        turns = [self.distanceToTurns(originPosition[0] - self.position[0]), self.distanceToTurns(originPosition[1] - self.position[1])];
        while True:
            positionReset = True
            for motor in self.activeMotors:
                if self.isPositionReset(motor) == False:
                    turns[motor] = self.TurnMotor(MotorPins[motor], turns[motor])
                positionReset = positionReset and self.isPositionReset(motor) == True;
            if positionReset == True:
                break
        self.position = [0,0]

    def isDoneTurning(self, turns):
        return turns < 0.5/float(self.SPR) and turns > -0.5/float(self.SPR)

    def moveToPosition(self, tempPosition, isKnight):
        
        j = 0;
        if isKnight == False or isKnight == True:
            targetPosition = [(tempPosition[0]+.5) * self.SizeOfSquare, (tempPosition[1]+.5) * self.SizeOfSquare]
            myTurns = [self.TPI*(targetPosition[0] - self.position[0]), self.TPI*(targetPosition[1] - self.position[1])]
            self.TurnFor(myTurns)
            self.position = targetPosition;
            print("target position =", tempPosition)

    #moveToPosition([0,4], False)
    def moveToGraveyard(self):
        targetPosition = [0,0]
        
        if self.position[1] > .5 * self.SizeOfSquare:
            targetPosition = [self.position[0], self.position[1]-.5 * self.SizeOfSquare]
        else:
            targetPosition = [self.position[0], self.position[1]+.5 * self.SizeOfSquare]
        myTurns = [self.TPI*(targetPosition[0] - self.position[0]), self.TPI*(targetPosition[1] - self.position[1])]
        self.TurnFor(myTurns)
        self.position = targetPosition;
        
        targetPosition = [self.graveyardXPosition * self.SizeOfSquare, self.position[1]]
        myTurns = [self.TPI*(targetPosition[0] - self.position[0]), self.TPI*(targetPosition[1] - self.position[1])]
        self.TurnFor(myTurns)
        self.position = targetPosition;

    def grab(self):
        GPIO.output(MAGNET, GPIO.HIGH)
    
    def release(self):
        GPIO.output(MAGNET, GPIO.LOW)
    


    print("----------------------END-----------------------")
test = MotorController()
test.moveToPosition([1,1], False)