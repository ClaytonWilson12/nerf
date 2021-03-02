
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

    #if object is in neither then do nothing so return 0
    else:
        return 200

# find direction to turn motor
def find_direction(data):
    direction = 0
    if (data > 0):
        direction = 0
    else:
        direction = 1
    direction = "setDirection:" + str(direction)
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

    angle = "moveMotor:" + str(angle)
    return angle





def move_y(location_y):
    
    # center x pixel
    center_y = 240

    # find difference between center and object, postive number means to the right
    diff_y = location_y - center_y

    #if object is to the below
    if (diff_y > -200):
        return 1

    elif (diff_y > -100):
        return 2

    #if object is to the above 
    elif (diff_y < 200):
        return -1
    
    elif (diff_y < 100):
        return -2

    #if object is in neither then do nothing so return 0
    else:
        return 200