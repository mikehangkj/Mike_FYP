from robomaster import robot
from time import sleep

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis
    x_val=0.5
    y_val=0.6
    z_val=90

    ep_chassis.move(x=-x_val,y=0,z=0,xy_speed=0.7).wait_for_completed()
    print("running")

    ep_robot.close()
