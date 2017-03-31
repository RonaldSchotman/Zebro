import math                             # mathematical functions library

class Blocking:
    def __init__(self):
        pass
    #Check if any of the x and y values are close to each other.
    #or if any of the x or y values are to close to the edge which is
    # if x == 0 or x == 1600 or y = 0 or y == 920 
    #So a gigantic multiple if statement. which becomes smaller and smaller
    def Block_1(self, Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y):
        Blocking = []   #Here will be the blocking in
        
        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)
        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)
        Blocking_x_3 = abs(Zebro_1_Middle_x - Zebro_3_Middle_x)
        Blocking_y_3 = abs(Zebro_1_Middle_y - Zebro_3_Middle_y)
        Blocking_x_4 = abs(Zebro_1_Middle_x - Zebro_4_Middle_x)
        Blocking_y_4 = abs(Zebro_1_Middle_y - Zebro_4_Middle_y)
        Blocking_x_5 = abs(Zebro_1_Middle_x - Zebro_5_Middle_x)
        Blocking_y_5 = abs(Zebro_1_Middle_y - Zebro_5_Middle_y)
        Blocking_x_6 = abs(Zebro_1_Middle_x - Zebro_6_Middle_x)
        Blocking_y_6 = abs(Zebro_1_Middle_y - Zebro_6_Middle_y)
        Blocking_x_7 = abs(Zebro_1_Middle_x - Zebro_7_Middle_x)
        Blocking_y_7 = abs(Zebro_1_Middle_y - Zebro_7_Middle_y)
        Blocking_x_8 = abs(Zebro_1_Middle_x - Zebro_8_Middle_x)
        Blocking_y_8 = abs(Zebro_1_Middle_y - Zebro_8_Middle_y)
        Blocking_x_9 = abs(Zebro_1_Middle_x - Zebro_9_Middle_x)
        Blocking_y_9 = abs(Zebro_1_Middle_y - Zebro_9_Middle_y)
        Blocking_x_10 = abs(Zebro_1_Middle_x - Zebro_10_Middle_x)
        Blocking_y_10 = abs(Zebro_1_Middle_y - Zebro_10_Middle_y)
        Blocking_x_11 = abs(Zebro_1_Middle_x - Zebro_11_Middle_x)
        Blocking_y_11 = abs(Zebro_1_Middle_y - Zebro_11_Middle_y)
        Blocking_x_12 = abs(Zebro_1_Middle_x - Zebro_12_Middle_x)
        Blocking_y_12 = abs(Zebro_1_Middle_y - Zebro_12_Middle_y)
        Blocking_x_13 = abs(Zebro_1_Middle_x - Zebro_13_Middle_x)
        Blocking_y_13 = abs(Zebro_1_Middle_y - Zebro_13_Middle_y)
        Blocking_x_14 = abs(Zebro_1_Middle_x - Zebro_14_Middle_x)
        Blocking_y_14 = abs(Zebro_1_Middle_y - Zebro_14_Middle_y)
        Blocking_x_15 = abs(Zebro_1_Middle_x - Zebro_15_Middle_x)
        Blocking_y_15 = abs(Zebro_1_Middle_y - Zebro_15_Middle_y)
        Blocking_x_16 = abs(Zebro_1_Middle_x - Zebro_16_Middle_x)
        Blocking_y_16 = abs(Zebro_1_Middle_y - Zebro_16_Middle_y)
        Blocking_x_17 = abs(Zebro_1_Middle_x - Zebro_17_Middle_x)
        Blocking_y_17 = abs(Zebro_1_Middle_y - Zebro_17_Middle_y)
        Blocking_x_18 = abs(Zebro_1_Middle_x - Zebro_18_Middle_x)
        Blocking_y_18 = abs(Zebro_1_Middle_y - Zebro_18_Middle_y)
        Blocking_x_19 = abs(Zebro_1_Middle_x - Zebro_19_Middle_x)
        Blocking_y_19 = abs(Zebro_1_Middle_y - Zebro_19_Middle_y)
        Blocking_x_20 = abs(Zebro_1_Middle_x - Zebro_20_Middle_x)
        Blocking_y_20 = abs(Zebro_1_Middle_y - Zebro_20_Middle_y)
            
        if (((0 < Blocking_x_2 < 80) and (0 < Blocking_y_2 < 80)) or ((0 < Blocking_x_3 < 80) and (0 < Blocking_y_3 < 80)) or ((0 < Blocking_x_4 < 80) and (0 < Blocking_y_4 < 80))
            or ((0 < Blocking_x_5 < 80) and (0 < Blocking_y_5 < 80)) or ((0 < Blocking_x_6 < 80) and (0 < Blocking_y_6 < 80)) or ((0 < Blocking_x_7 < 80) and (0 < Blocking_y_7 < 80))
            or ((0 < Blocking_x_8 < 80) and (0 < Blocking_y_8 < 80)) or ((0 < Blocking_x_9 < 80) and (0 < Blocking_y_9 < 80)) or ((0 < Blocking_x_10 < 80) and (0 < Blocking_y_10 < 80))
            or ((0 < Blocking_x_11 < 80) and (0 < Blocking_y_11 < 80)) or ((0 < Blocking_x_12 < 80) and (0 < Blocking_y_12 < 80)) or ((0 < Blocking_x_13 < 80) and (0 < Blocking_y_13 < 80))
            or ((0 < Blocking_x_14 < 80) and (0 < Blocking_y_14 < 80)) or ((0 < Blocking_x_15 < 80) and (0 < Blocking_y_15 < 80)) or ((0 < Blocking_x_16 < 80) and (0 < Blocking_y_16 < 80))
            or ((0 < Blocking_x_17 < 80) and (0 < Blocking_y_17 < 80)) or ((0 < Blocking_x_18 < 80) and (0 < Blocking_y_18 < 80)) or ((0 < Blocking_x_19 < 80) and (0 < Blocking_y_19 < 80))
            or ((0 < Blocking_x_20 < 80) and (0 < Blocking_y_20 < 80)) ):
                if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y)) or ((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y)) or ((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y)) or ((Zebro_1_Middle_x < Zebro_6_Middle_x) and (Zebro_1_Middle_y > Zebro_6_Middle_y)) or ((Zebro_1_Middle_x < Zebro_7_Middle_x) and (Zebro_1_Middle_y > Zebro_7_Middle_y)) 
                or ((Zebro_1_Middle_x < Zebro_8_Middle_x) and (Zebro_1_Middle_y > Zebro_8_Middle_y)) or ((Zebro_1_Middle_x < Zebro_9_Middle_x) and (Zebro_1_Middle_y > Zebro_9_Middle_y)) or ((Zebro_1_Middle_x < Zebro_10_Middle_x) and (Zebro_1_Middle_y > Zebro_10_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_11_Middle_x) and (Zebro_1_Middle_y > Zebro_11_Middle_y)) or ((Zebro_1_Middle_x < Zebro_12_Middle_x) and (Zebro_1_Middle_y > Zebro_12_Middle_y)) or ((Zebro_1_Middle_x < Zebro_13_Middle_x) and (Zebro_1_Middle_y > Zebro_13_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_14_Middle_x) and (Zebro_1_Middle_y > Zebro_14_Middle_y)) or ((Zebro_1_Middle_x < Zebro_15_Middle_x) and (Zebro_1_Middle_y > Zebro_15_Middle_y)) or ((Zebro_1_Middle_x < Zebro_16_Middle_x) and (Zebro_1_Middle_y > Zebro_16_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_17_Middle_x) and (Zebro_1_Middle_y > Zebro_17_Middle_y)) or ((Zebro_1_Middle_x < Zebro_18_Middle_x) and (Zebro_1_Middle_y > Zebro_18_Middle_y)) or ((Zebro_1_Middle_x < Zebro_19_Middle_x) and (Zebro_1_Middle_y > Zebro_19_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_20_Middle_x) and (Zebro_1_Middle_y > Zebro_20_Middle_y))):
                    Block = "East"
                    Blocking.append(Block)
                    Block = None
                if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y)) or ((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y)) or ((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y)) or ((Zebro_1_Middle_x < Zebro_6_Middle_x) and (Zebro_1_Middle_y > Zebro_6_Middle_y)) or ((Zebro_1_Middle_x < Zebro_7_Middle_x) and (Zebro_1_Middle_y > Zebro_7_Middle_y)) 
                or ((Zebro_1_Middle_x < Zebro_8_Middle_x) and (Zebro_1_Middle_y > Zebro_8_Middle_y)) or ((Zebro_1_Middle_x < Zebro_9_Middle_x) and (Zebro_1_Middle_y > Zebro_9_Middle_y)) or ((Zebro_1_Middle_x < Zebro_10_Middle_x) and (Zebro_1_Middle_y > Zebro_10_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_11_Middle_x) and (Zebro_1_Middle_y > Zebro_11_Middle_y)) or ((Zebro_1_Middle_x < Zebro_12_Middle_x) and (Zebro_1_Middle_y > Zebro_12_Middle_y)) or ((Zebro_1_Middle_x < Zebro_13_Middle_x) and (Zebro_1_Middle_y > Zebro_13_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_14_Middle_x) and (Zebro_1_Middle_y > Zebro_14_Middle_y)) or ((Zebro_1_Middle_x < Zebro_15_Middle_x) and (Zebro_1_Middle_y > Zebro_15_Middle_y)) or ((Zebro_1_Middle_x < Zebro_16_Middle_x) and (Zebro_1_Middle_y > Zebro_16_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_17_Middle_x) and (Zebro_1_Middle_y > Zebro_17_Middle_y)) or ((Zebro_1_Middle_x < Zebro_18_Middle_x) and (Zebro_1_Middle_y > Zebro_18_Middle_y)) or ((Zebro_1_Middle_x < Zebro_19_Middle_x) and (Zebro_1_Middle_y > Zebro_19_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_20_Middle_x) and (Zebro_1_Middle_y > Zebro_20_Middle_y))):
                    Block = "West"
                    Blocking.append(Block)
                    Block = None
                if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y)) or ((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y)) or ((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y)) or ((Zebro_1_Middle_x < Zebro_6_Middle_x) and (Zebro_1_Middle_y > Zebro_6_Middle_y)) or ((Zebro_1_Middle_x < Zebro_7_Middle_x) and (Zebro_1_Middle_y > Zebro_7_Middle_y)) 
                or ((Zebro_1_Middle_x < Zebro_8_Middle_x) and (Zebro_1_Middle_y > Zebro_8_Middle_y)) or ((Zebro_1_Middle_x < Zebro_9_Middle_x) and (Zebro_1_Middle_y > Zebro_9_Middle_y)) or ((Zebro_1_Middle_x < Zebro_10_Middle_x) and (Zebro_1_Middle_y > Zebro_10_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_11_Middle_x) and (Zebro_1_Middle_y > Zebro_11_Middle_y)) or ((Zebro_1_Middle_x < Zebro_12_Middle_x) and (Zebro_1_Middle_y > Zebro_12_Middle_y)) or ((Zebro_1_Middle_x < Zebro_13_Middle_x) and (Zebro_1_Middle_y > Zebro_13_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_14_Middle_x) and (Zebro_1_Middle_y > Zebro_14_Middle_y)) or ((Zebro_1_Middle_x < Zebro_15_Middle_x) and (Zebro_1_Middle_y > Zebro_15_Middle_y)) or ((Zebro_1_Middle_x < Zebro_16_Middle_x) and (Zebro_1_Middle_y > Zebro_16_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_17_Middle_x) and (Zebro_1_Middle_y > Zebro_17_Middle_y)) or ((Zebro_1_Middle_x < Zebro_18_Middle_x) and (Zebro_1_Middle_y > Zebro_18_Middle_y)) or ((Zebro_1_Middle_x < Zebro_19_Middle_x) and (Zebro_1_Middle_y > Zebro_19_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_20_Middle_x) and (Zebro_1_Middle_y > Zebro_20_Middle_y))):
                    Block = "South"
                    Blocking.append(Block)
                    Block = None
                if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y)) or ((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y)) or ((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y)) or ((Zebro_1_Middle_x < Zebro_6_Middle_x) and (Zebro_1_Middle_y > Zebro_6_Middle_y)) or ((Zebro_1_Middle_x < Zebro_7_Middle_x) and (Zebro_1_Middle_y > Zebro_7_Middle_y)) 
                or ((Zebro_1_Middle_x < Zebro_8_Middle_x) and (Zebro_1_Middle_y > Zebro_8_Middle_y)) or ((Zebro_1_Middle_x < Zebro_9_Middle_x) and (Zebro_1_Middle_y > Zebro_9_Middle_y)) or ((Zebro_1_Middle_x < Zebro_10_Middle_x) and (Zebro_1_Middle_y > Zebro_10_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_11_Middle_x) and (Zebro_1_Middle_y > Zebro_11_Middle_y)) or ((Zebro_1_Middle_x < Zebro_12_Middle_x) and (Zebro_1_Middle_y > Zebro_12_Middle_y)) or ((Zebro_1_Middle_x < Zebro_13_Middle_x) and (Zebro_1_Middle_y > Zebro_13_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_14_Middle_x) and (Zebro_1_Middle_y > Zebro_14_Middle_y)) or ((Zebro_1_Middle_x < Zebro_15_Middle_x) and (Zebro_1_Middle_y > Zebro_15_Middle_y)) or ((Zebro_1_Middle_x < Zebro_16_Middle_x) and (Zebro_1_Middle_y > Zebro_16_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_17_Middle_x) and (Zebro_1_Middle_y > Zebro_17_Middle_y)) or ((Zebro_1_Middle_x < Zebro_18_Middle_x) and (Zebro_1_Middle_y > Zebro_18_Middle_y)) or ((Zebro_1_Middle_x < Zebro_19_Middle_x) and (Zebro_1_Middle_y > Zebro_19_Middle_y))
                or ((Zebro_1_Middle_x < Zebro_20_Middle_x) and (Zebro_1_Middle_y > Zebro_20_Middle_y))):
                    Block = "North"
                    Blocking.append(Block)
                    Block = None
                    
        if ((Zebro_1_Middle_y < 80) or (Zebro_1_Middle_y > 850) or (Zebro_1_Middle_x > 1500) or (Zebro_1_Middle_x < 80)):
            if ((Zebro_1_Middle_x > 1500) or (Zebro_1_Middle_y < 80)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 80) or (Zebro_1_Middle_y > 850)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1500) or (Zebro_1_Middle_y > 850)):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 80) or (Zebro_1_Middle_y < 80)):
                Block = "North"
                Blocking.append(Block)
                Block = None
            
        return Blocking

    def Block_2(self, Zebro_1_Middle_x,Zebro_1_Middle_y):
        Blocking = []   #Here will be the blocking in
            
        if ((Zebro_1_Middle_y < 80) or (Zebro_1_Middle_y > 850) or (Zebro_1_Middle_x > 1500) or (Zebro_1_Middle_x < 80)):
                if ((Zebro_1_Middle_x > 1500) or (Zebro_1_Middle_y < 80)):
                    Block = "East"
                    Blocking.append(Block)
                    Block = None
                if ((Zebro_1_Middle_x < 80) or (Zebro_1_Middle_y > 850)):
                    Block = "West"
                    Blocking.append(Block)
                    Block = None
                if ((Zebro_1_Middle_x > 1500) or (Zebro_1_Middle_y > 850)):
                    Block = "South"
                    Blocking.append(Block)
                    Block = None
                if ((Zebro_1_Middle_x < 80) or (Zebro_1_Middle_y < 80)):
                    Block = "North"
                    Blocking.append(Block)
                    Block = None
                
        return Blocking
