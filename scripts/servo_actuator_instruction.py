
def move_x(location_x):
    
    
    # center x pixel
    center_x = 424

    # find difference between center and object, postive number means to the right
    diff_x = location_x - center_x

    #if object is to the right
    if (diff_x > 300):
        return 1

    elif (diff_x > 200):
        return 2

    elif (diff_x > 100):
        return 3

    elif (diff_x > 10):
        return 4

    #if object is to the left 
    elif (diff_x < -300):
        return -1
    
    elif (diff_x < -200):
        return -2
    
    elif (diff_x < -100):
        return -3
    
    elif (diff_x < -10):
        return -4

    #if object is in neither then do nothing so return 200
    else:
        return 200

# find direction to turn motor
def find_direction(data):
    direction = 0
    if (data > 0):
        direction = -1
    else:
        direction = 1
    return direction
    
# calculate angle to send to motors
def calc_angle(data):
    angle = 0
    diff = abs(data)

    if diff == 1:
        angle = 30
    elif diff == 2:
        angle = 20
    elif diff == 3:
        angle = 10
    elif diff == 4:
        angle = 3
    else:
        angle = 0

    return angle





def move_y(location_y):
    
    # center x pixel
    bottom_y = 480

    # find difference between center and object, postive number means to the right
    diff_y = bottom_y - location_y

    # starting from top of camera frame
    if (diff_y > 450):
        return 10
    elif (diff_y > 400):
        return 9
    elif (diff_y > 350):
        return 8
    elif (diff_y > 300):
        return 7
    elif (diff_y > 250):
        return 6
    elif (diff_y > 200):
        return 5
    elif (diff_y > 150):
        return 4
    elif (diff_y > 100):
        return 3
    elif (diff_y > 50):
        return 2
    else:
        return 1

def smooth_move_y(location_y):
    BOTTOM_Y = float(480)
    ACTUATOR_HEIGHT = float(10)
    ACTUATOR_OFFSET = float(1)

    # find y ratio  by y_location divided by total frame height
    pixel_ratio = (float(location_y))/BOTTOM_Y
    pixel_ratio = 1 - pixel_ratio
    print(pixel_ratio)

    #find actuator extension length based on ratio. actuator height is 10in
    extend_actuator = pixel_ratio * ACTUATOR_HEIGHT
    extend_actuator = extend_actuator + ACTUATOR_OFFSET
    print (extend_actuator)




if __name__ == '__main__':
    smooth_move_y(420)



