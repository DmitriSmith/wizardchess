import RPi.GPIO as GPIO
import time
class MotorController:
    
    GPIO.setmode(GPIO.BCM)

    ResetPin = [3, 5]
    MotorPins = [
        [26, 19], #[Direction, Step]
        [35, 37]
    ]

    activeMotors = [0]
    
    global MAGNET
    MAGNET = 39

    STEP = 19#35
    DIR = 26#37
    CW = 1
    CCW = 0
    SPR = int(360/1.8)
    
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.output(DIR, CW)

    GPIO.setup(MAGNET, GPIO.OUT)
    
    delay = 0.2/SPR

    global position
    position = [0, 0]
    resetButton = [False, False]
    
    originPosition = [-99, -99]
    graveyardXPosition = float(13.5)


    for i in range(0,2):
        GPIO.setup(ResetPin[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #TODO: change to GPIO>PUD_DOWN IF CONNECTED TO 5V

    global TPI
    TPI = 20 #turns per inch of the threaded rod
    global SizeOfSquare
    SizeOfSquare = 1.5 #size of the square of the chess board in inches

    def distanceToTurns(self, distance): #changes distance in inches to turns
        return distance * TPI

    def TurnMotor(self, tempMotorPins, turns): #TODO update the position of the piece as you move the motor
        if isDoneTurning(turns) == False:
            if turns > 0:
                GPIO.output(tempMotorPins[0], CW)
            else:
                GPIO.output(tempMotorPins[0], CCW)
            GPIO.output(tempMotorPins[1], GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(tempMotorPins[1], GPIO.LOW)
            time.sleep(delay)
            turns -= 1/SPR
        return turns

    def TurnFor(self, myTurns):
        j=0
        while True:
            doneTurning = True;
            j = j + 1
            if j%10 == 0:
                print(myTurns[0])
            for motor in activeMotors:
                if j == 1:
                    print(motor)
                if(isPositionReset(motor) == False):
                    myTurns[motor] = TurnMotor(MotorPins[motor],myTurns[motor])
                    doneTurning = doneTurning and isDoneTurning(myTurns[motor]) == True
                else:
                    print("position reset for motor")
            if(doneTurning == True):
                print("finished turning")
                break;
        print(myTurns[0])

    def isPositionReset(self, resetIndex):
        input_state = GPIO.input(ResetPin[resetIndex])
        return input_state == resetButton[resetIndex] and input_state == True

    def resetPosition(self):
        global position
        turns = [distanceToTurns(originPosition[0] - position[0]), distanceToTurns(originPosition[1] - position[1])];
        while True:
            positionReset = True
            for motor in activeMotors:
                if isPositionReset(motor) == False:
                    turns[motor] = TurnMotor(MotorPins[motor], turns[motor])
                positionReset = positionReset and isPositionReset(motor) == True;
            if positionReset == True:
                break
        position = [0,0]

    def isDoneTurning(self, turns):
        return turns < 0.5/float(SPR) and turns > -0.5/float(SPR)

    def moveToPosition(self, tempPosition, isKnight):
        global position
        j = 0;
        if isKnight == False:
            targetPosition = [(tempPosition[0]+.5) * SizeOfSquare, (tempPosition[1]+.5) * SizeOfSquare]
            myTurns = [TPI*(targetPosition[0] - position[0]), TPI*(targetPosition[1] - position[1])]
            self.TurnFor(myTurns)
            position = targetPosition;
            print("target position =", tempPosition)

    #moveToPosition([0,4], False)

    def grab(self):
        GPIO.output(MAGNET, GPIO.HIGH)
    
    def release(self):
        GPIO.output(MAGNET, GPIO.LOW)
    
    print(position)


    print("----------------------END-----------------------")