import step as motor
import sys
def moveTo(pos):
    step.step(pos,29,31)

if __name__ == '__main__':
    from sys import argv
    motor.setpins()
    motor.step(int(argv[1]),29,31) 
    motor.GPIO.cleanup()
