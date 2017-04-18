import math                             # mathematical functions library

class Blocking2:
    def __init__(self):
        pass
    #Check if any of the x and y values are close to each other.
    #or if any of the x or y values are to close to the edge which is
    # if x == 0 or x == 1600 or y = 0 or y == 920 

    #For 1 Pico
    def Block_4(self, Zebro_1_Middle_x,Zebro_1_Middle_y):
        Blocking = []   #Here will be the blocking in in ROI
        
        if ((Zebro_1_Middle_y < 150) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_x > 1200) or (Zebro_1_Middle_x < 400)):
            if ((Zebro_1_Middle_x > 1200) or (Zebro_1_Middle_y < 150) or (Zebro_1_Middle_y > 820)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 400) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_y < 150)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1200) or (Zebro_1_Middle_y > 820) ):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 400) or (Zebro_1_Middle_y < 150)):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 500) and (Zebro_1_Middle_y < 500) ):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 500) and (Zebro_1_Middle_y > 500) ):
                Block = "West"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1100) and (Zebro_1_Middle_y < 500)):
                Block = "East"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1100) and (Zebro_1_Middle_y > 500)):
                Block = "South"
                Blocking.append(Block)
                Block = None
        return Blocking
    
    #For 2 Pico
    def Block_5(self, Zebro_1_Middle_x, Zebro_2_Middle_x,
                Zebro_1_Middle_y, Zebro_2_Middle_y):
        Blocking = []   #Here will be the blocking in in ROI
        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)     # For determing the blocked Direction for the Pico Zebro it needs to be determined if any of the other Pico Zebro's are close by
        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)     # With its absolute value in distance this can be stermined.
        
        if ((0 < Blocking_x_2 < 300) and (0 < Blocking_y_2 < 300)):
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) or (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) or (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ((Zebro_1_Middle_y < 150) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_x > 1200) or (Zebro_1_Middle_x < 400)):
            if ((Zebro_1_Middle_x > 1200) or (Zebro_1_Middle_y < 150) or (Zebro_1_Middle_y > 820)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 400) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_y < 150)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1200) or (Zebro_1_Middle_y > 820) ):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 400) or (Zebro_1_Middle_y < 150)):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 500) and (Zebro_1_Middle_y < 500) ):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 500) and (Zebro_1_Middle_y > 500) ):
                Block = "West"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1100) and (Zebro_1_Middle_y < 500)):
                Block = "East"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1100) and (Zebro_1_Middle_y > 500)):
                Block = "South"
                Blocking.append(Block)
                Block = None
        return Blocking

    #For 3 Pico
    def Block_6(self, Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x,
                Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y):
        Blocking = []   #Here will be the blocking in in ROI
        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)     # For determing the blocked Direction for the Pico Zebro it needs to be determined if any of the other Pico Zebro's are close by
        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)     # With its absolute value in distance this can be stermined.
        Blocking_x_3 = abs(Zebro_1_Middle_x - Zebro_3_Middle_x)     # Then needs to be checked where the blocking is comming from onces that is determined the blocked Directions can be determined
        Blocking_y_3 = abs(Zebro_1_Middle_y - Zebro_3_Middle_y)     # Also no matter how many zebro's you have always check if the Zebro is reaching the edges.
        
        if ((0 < Blocking_x_2 < 400) and (0 < Blocking_y_2 < 400)):
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None
        if ((0 < Blocking_x_3 < 400) and (0 < Blocking_y_3 < 400)):
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ((Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_x < 450)):
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_y < 200)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y > 820) ):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y < 200)):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 550) and (Zebro_1_Middle_y < 400) ):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 510) and (Zebro_1_Middle_y > 500) ):
                Block = "West"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y < 400)):
                Block = "East"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y > 500)):
                Block = "South"
                Blocking.append(Block)
                Block = None
        return Blocking

    #For 4 Pico
    def Block_7(self, Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x,
                Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y):
        Blocking = []   #Here will be the blocking in in ROI
        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)     # For determing the blocked Direction for the Pico Zebro it needs to be determined if any of the other Pico Zebro's are close by
        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)     # With its absolute value in distance this can be stermined.
        Blocking_x_3 = abs(Zebro_1_Middle_x - Zebro_3_Middle_x)     # Then needs to be checked where the blocking is comming from onces that is determined the blocked Directions can be determined
        Blocking_y_3 = abs(Zebro_1_Middle_y - Zebro_3_Middle_y)     # Also no matter how many zebro's you have always check if the Zebro is reaching the edges.
        Blocking_x_4 = abs(Zebro_1_Middle_x - Zebro_4_Middle_x)
        Blocking_y_4 = abs(Zebro_1_Middle_y - Zebro_4_Middle_y)
        
        if ((0 < Blocking_x_2 < 400) and (0 < Blocking_y_2 < 400)):
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_3 < 400) and (0 < Blocking_y_3 < 400)):
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_4 < 400) and (0 < Blocking_y_4 < 400)):
            if (((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_4_Middle_x) and (Zebro_1_Middle_y < Zebro_4_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y < Zebro_4_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ((Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_x < 450)):
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_y < 200)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y > 820) ):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y < 200)):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 550) and (Zebro_1_Middle_y < 400) ):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 510) and (Zebro_1_Middle_y > 500) ):
                Block = "West"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y < 400)):
                Block = "East"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y > 500)):
                Block = "South"
                Blocking.append(Block)
                Block = None
        return Blocking
    #For 5 Pico
    def Block_8(self, Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x,
                Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y):
        Blocking = []   #Here will be the blocking in in ROI
        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)     # For determing the blocked Direction for the Pico Zebro it needs to be determined if any of the other Pico Zebro's are close by
        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)     # With its absolute value in distance this can be stermined.
        Blocking_x_3 = abs(Zebro_1_Middle_x - Zebro_3_Middle_x)     # Then needs to be checked where the blocking is comming from onces that is determined the blocked Directions can be determined
        Blocking_y_3 = abs(Zebro_1_Middle_y - Zebro_3_Middle_y)     # Also no matter how many zebro's you have always check if the Zebro is reaching the edges.
        Blocking_x_4 = abs(Zebro_1_Middle_x - Zebro_4_Middle_x)
        Blocking_y_4 = abs(Zebro_1_Middle_y - Zebro_4_Middle_y)
        Blocking_x_5 = abs(Zebro_1_Middle_x - Zebro_5_Middle_x)
        Blocking_y_5 = abs(Zebro_1_Middle_y - Zebro_5_Middle_y)
        
        if ((0 < Blocking_x_2 < 400) and (0 < Blocking_y_2 < 400)):
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_3 < 400) and (0 < Blocking_y_3 < 400)):
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_4 < 400) and (0 < Blocking_y_4 < 400)):
            if (((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_4_Middle_x) and (Zebro_1_Middle_y < Zebro_4_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y < Zebro_4_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_5 < 400) and (0 < Blocking_y_5 < 400)):
            if (((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_5_Middle_x) and (Zebro_1_Middle_y < Zebro_5_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y < Zebro_5_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ((Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_x < 450)):
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_y < 200)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y > 820) ):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y < 200)):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 550) and (Zebro_1_Middle_y < 400) ):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 510) and (Zebro_1_Middle_y > 500) ):
                Block = "West"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y < 400)):
                Block = "East"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y > 500)):
                Block = "South"
                Blocking.append(Block)
                Block = None
        return Blocking
    #For 6 Pico
    def Block_9(self, Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x,
                Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y):
        Blocking = []   #Here will be the blocking in in ROI
        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)     # For determing the blocked Direction for the Pico Zebro it needs to be determined if any of the other Pico Zebro's are close by
        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)     # With its absolute value in distance this can be stermined.
        Blocking_x_3 = abs(Zebro_1_Middle_x - Zebro_3_Middle_x)     # Then needs to be checked where the blocking is comming from onces that is determined the blocked Directions can be determined
        Blocking_y_3 = abs(Zebro_1_Middle_y - Zebro_3_Middle_y)     # Also no matter how many zebro's you have always check if the Zebro is reaching the edges.
        Blocking_x_4 = abs(Zebro_1_Middle_x - Zebro_4_Middle_x)
        Blocking_y_4 = abs(Zebro_1_Middle_y - Zebro_4_Middle_y)
        Blocking_x_5 = abs(Zebro_1_Middle_x - Zebro_5_Middle_x)
        Blocking_y_5 = abs(Zebro_1_Middle_y - Zebro_5_Middle_y)
        Blocking_x_6 = abs(Zebro_1_Middle_x - Zebro_6_Middle_x)
        Blocking_y_6 = abs(Zebro_1_Middle_y - Zebro_6_Middle_y)
        
        if (((0 < Blocking_x_2 < 400) and (0 < Blocking_y_2 < 400)) or ((0 < Blocking_x_3 < 400) and (0 < Blocking_y_3 < 400)) or ((0 < Blocking_x_4 < 400) and (0 < Blocking_y_4 < 400))
            or ((0 < Blocking_x_5 < 400) and (0 < Blocking_y_5 < 400)) or ((0 < Blocking_x_6 < 400) and (0 < Blocking_y_6 < 400))):
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_2_Middle_x) and (Zebro_1_Middle_y > Zebro_2_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_2_Middle_x) and (Zebro_1_Middle_y < Zebro_2_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_3 < 400) and (0 < Blocking_y_3 < 400)):
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_3_Middle_x) and (Zebro_1_Middle_y > Zebro_3_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_3_Middle_x) and (Zebro_1_Middle_y < Zebro_3_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_4 < 400) and (0 < Blocking_y_4 < 400)):
            if (((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_4_Middle_x) and (Zebro_1_Middle_y < Zebro_4_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_4_Middle_x) and (Zebro_1_Middle_y > Zebro_4_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_4_Middle_x) and (Zebro_1_Middle_y < Zebro_4_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_5 < 400) and (0 < Blocking_y_5 < 400)):
            if (((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_5_Middle_x) and (Zebro_1_Middle_y < Zebro_5_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_5_Middle_x) and (Zebro_1_Middle_y > Zebro_5_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_5_Middle_x) and (Zebro_1_Middle_y < Zebro_5_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None

        if ((0 < Blocking_x_6 < 400) and (0 < Blocking_y_6 < 400)):
            if (((Zebro_1_Middle_x < Zebro_6_Middle_x) and (Zebro_1_Middle_y > Zebro_6_Middle_y))):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_6_Middle_x) and (Zebro_1_Middle_y < Zebro_6_Middle_y))):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x > Zebro_6_Middle_x) and (Zebro_1_Middle_y > Zebro_6_Middle_y))):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if (((Zebro_1_Middle_x < Zebro_6_Middle_x) and (Zebro_1_Middle_y < Zebro_6_Middle_y))):
                Block = "North"
                Blocking.append(Block)
                Block = None
        
        if ((Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_x < 450)):
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y < 200) or (Zebro_1_Middle_y > 820)):
                Block = "East"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y > 820) or (Zebro_1_Middle_y < 200)):
                Block = "West"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x > 1350) or (Zebro_1_Middle_y > 820) ):
                Block = "South"
                Blocking.append(Block)
                Block = None
            if ((Zebro_1_Middle_x < 450) or (Zebro_1_Middle_y < 200)):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 550) and (Zebro_1_Middle_y < 400) ):
                Block = "North"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x < 510) and (Zebro_1_Middle_y > 500) ):
                Block = "West"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y < 400)):
                Block = "East"
                Blocking.append(Block)
                Block = None
                
        if ( (Zebro_1_Middle_x > 1200) and (Zebro_1_Middle_y > 500)):
                Block = "South"
                Blocking.append(Block)
                Block = None
        return Blocking
    
    
