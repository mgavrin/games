import math

def check(position,base_x,base_y,box,dim):
        if position[0]<base_x or position[1]<base_y:
            print False
            return False
        elif position[0]>base_x+box*dim:
            print False
            return False
        elif position[1]>base_y+box*dim:
            print False
            return False
        else:
            x_box=int(math.floor((position[0]-base_x)/box))
            y_box=int(math.floor((position[1]-base_y)/box))
            print(x_box,y_box)
            return(x_box,y_box)

check((17,14.9),0,0,5,4)


