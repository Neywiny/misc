GRAVITY = 1.622
class Lander():
    def __init__(this):
        this.altitude = 400.0
        this.speed = 40.0
        this.fuel = 25.0
        this.strength = 4.0
        
def human_controller(lander):
    thrust = int(raw_input("enter thrust: "))
    while thrust < 0 or thrust > min(lander.strength,lander.fuel):
        print("invalid thrust")
        thrust = int(raw_input("enter thrust: "))
    return thrust

def smart_controller(lander):
    thrust = 0
    if ((lander.altitude - lander.speed) < lander.speed * lander.strength):
        thrust = min(lander.strength,lander.fuel)
    if lander.altitude <= (4 * lander.strength):
        if lander.strength * 4 > lander.speed:
            thrust = (lander.speed + lander.strength) / 4
        else:
            thrust = 4
    if (lander.speed + GRAVITY) - (4 * thrust) <= 0:
        thrust = lander.speed / 4
        if lander.altitude < lander.speed and lander.altitude < 10:
            thrust = (lander.speed + GRAVITY) / 4
    return int(thrust)

def main():
    print('Hello, welcome to the simulation.\nfor manual    control, enter "m"\nfor autimatic control, enter "a"')
    i = raw_input("enter choice: ").lower()
    while i != 'm' and i != 'a':
        i = raw_input("enter choice: ").lower()
    manual = i == 'm'
    lander = Lander()
    while lander.altitude > 0:
        print("Altitude\tSpeed\tFuel\tStrength")
        print(str(lander.altitude)+'\t\t'+str(lander.speed)+"\t"+str(lander.fuel)+"\t"+str(lander.strength))
        if manual:
            thrust = human_controller(lander)
        else:
            thrust = smart_controller(lander)
            #print "|Calculated Thrust: ",thrust
        lander.fuel -= thrust
        lander.speed -= 4 * thrust
        lander.speed += GRAVITY
        lander.altitude -= lander.speed
        if lander.altitude < 0:
            lander.altitude = 0
    if lander.speed <= lander.strength:
        print("the landing was a success")
    else:
        print("the lander has crashed")
        
if __name__ == "__main__":
    main()
