#Here comes a calculation for determing new middle point. (for now only with forward because turning depends on how it turns.(On same position or with going forward.
                    #Also With these values will be done nothing untill it is determined this works (In theorie it does)
                    if Movement == "Forward" and DONT_Send == 0:
                        Max_x = 60 #(EXAMPLE NEEDS TO BE TESTED)
                        Max_y = 80 #(EXAMPLE NEEDS TO BE TESTED)
                        if Current_Direction == "North":
                            Angle_90 = Angle - 270
                            X_1 = (90 - Angle_90)
                            X = (X_1/ 90) * Max_x
                            Y = Angle_90 * Max_y
                            New_Middle_point_x = Middle_point_x + X
                            New_Middle_point_y = Middle_point_y + Y
                        elif Current_Direction == "South":
                            Angle_90 = Angle - 90
                            X_1 = (90 - Angle_90)
                            X = (X_1/ 90) * Max_x
                            Y = Angle_90 * Max_y
                            New_Middle_point_x = Middle_point_x - X
                            New_Middle_point_y = Middle_point_y - Y
                        elif Current_Direction == "East":
                            Angle_90 = Angle
                            Y_1 = (90 - Angle_90)
                            Y = (Y_1/ 90) * Max_y
                            X = Angle_90 * Max_x
                            New_Middle_point_x = Middle_point_x + X
                            New_Middle_point_y = Middle_point_y - Y
                        elif Current_Direction == "West":
                            Angle_90 = Angle - 180
                            Y_1 = (90 - Angle_90)
                            Y = (Y_1/ 90) * Max_x
                            X = Angle_90 * Max_y
                            New_Middle_point_x = Middle_point_x - X
                            New_Middle_point_y = Middle_point_y + Y
                        print(New_Middle_point_x, New_Middle_point_y)
#For Pico Zebro 1
                    if Zebros == 0:
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
            
                        if (0 < Blocking_x_2 < 80) or (0 < Blocking_x_3 < 80) or (0 < Blocking_x_4 < 80) or (0 < Blocking_x_5 < 80)
                        or (0 < Blocking_x_6 < 80) or (0 < Blocking_x_7 < 80) or (0 < Blocking_x_8 < 80) or (0 < Blocking_x_9 < 80)
                        or (0 < Blocking_x_10 < 80) or (0 < Blocking_x_11 < 80) or (0 < Blocking_x_12 < 80) or (0 < Blocking_x_13 < 80)
                        or (0 < Blocking_x_14 < 80) or (0 < Blocking_x_15 < 80) or (0 < Blocking_x_16 < 80) or (0 < Blocking_x_17 < 80)
                        or (0 < Blocking_x_18 < 80) or (0 < Blocking_x_19 < 80) or (0 < Blocking_x_20 < 80):
                            if (Zebro_1_Middle_x < Zebro_2_Middle_x) or (Zebro_1_Middle_x < Zebro_3_Middle_x) or (Zebro_1_Middle_x < Zebro_4_Middle_x) or (Zebro_1_Middle_x < Zebro_5_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_6_Middle_x) or (Zebro_1_Middle_x < Zebro_7_Middle_x) or (Zebro_1_Middle_x < Zebro_8_Middle_x) or (Zebro_1_Middle_x < Zebro_9_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_10_Middle_x) or (Zebro_1_Middle_x < Zebro_11_Middle_x) or (Zebro_1_Middle_x < Zebro_12_Middle_x) or (Zebro_1_Middle_x < Zebro_13_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_14_Middle_x) or (Zebro_1_Middle_x < Zebro_15_Middle_x) or (Zebro_1_Middle_x < Zebro_16_Middle_x) or (Zebro_1_Middle_x < Zebro_17_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_18_Middle_x) or (Zebro_1_Middle_x < Zebro_19_Middle_x) or (Zebro_1_Middle_x < Zebro_20_Middle_x) or (Zebro_1_Middle_x > 1550):
                                Block = "East"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_1_Middle_x > Zebro_2_Middle_x) or (Zebro_1_Middle_x > Zebro_3_Middle_x) or (Zebro_1_Middle_x > Zebro_4_Middle_x) or (Zebro_1_Middle_x > Zebro_5_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_6_Middle_x) or (Zebro_1_Middle_x > Zebro_7_Middle_x) or (Zebro_1_Middle_x > Zebro_8_Middle_x) or (Zebro_1_Middle_x > Zebro_9_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_10_Middle_x) or (Zebro_1_Middle_x > Zebro_11_Middle_x) or (Zebro_1_Middle_x > Zebro_12_Middle_x) or (Zebro_1_Middle_x > Zebro_13_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_14_Middle_x) or (Zebro_1_Middle_x > Zebro_15_Middle_x) or (Zebro_1_Middle_x > Zebro_16_Middle_x) or (Zebro_1_Middle_x > Zebro_17_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_18_Middle_x) or (Zebro_1_Middle_x > Zebro_19_Middle_x) or (Zebro_1_Middle_x > Zebro_20_Middle_x) or (Zebro_1_Middle_x < 50):
                                Block = "West"
                                Bloking.append(Block)
                                Block = None
                        if (0 < Blocking_y_2 < 80) or (0 < Blocking_y_3 < 80) or (0 < Blocking_y_4 < 80) or (0 < Blocking_y_5 < 80)
                        or (0 < Blocking_y_6 < 80) or (0 < Blocking_y_7 < 80) or (0 < Blocking_y_8 < 80) or (0 < Blocking_y_9 < 80)
                        or (0 < Blocking_y_10 < 80) or (0 < Blocking_y_11 < 80) or (0 < Blocking_y_12 < 80) or (0 < Blocking_y_13 < 80)
                        or (0 < Blocking_y_14 < 80) or (0 < Blocking_y_15 < 80) or (0 < Blocking_y_16 < 80) or (0 < Blocking_y _17 < 80)
                        or (0 < Blocking_y_18 < 80) or (0 < Blocking_y_19 < 80) or (0 < Blocking_y_20 < 80):
                            if (Zebro_1_Middle_y > Zebro_2_Middle_y) or (Zebro_1_Middle_y > Zebro_3_Middle_y) or (Zebro_1_Middle_y > Zebro_4_Middle_y) or (Zebro_1_Middle_y > Zebro_5_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_6_Middle_y) or (Zebro_1_Middle_y > Zebro_7_Middle_y) or (Zebro_1_Middle_y > Zebro_8_Middle_y) or (Zebro_1_Middle_y > Zebro_9_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_10_Middle_y) or (Zebro_1_Middle_y > Zebro_11_Middle_y) or (Zebro_1_Middle_y > Zebro_12_Middle_y) or (Zebro_1_Middle_y > Zebro_13_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_14_Middle_y) or (Zebro_1_Middle_y > Zebro_15_Middle_y) or (Zebro_1_Middle_y > Zebro_16_Middle_y) or (Zebro_1_Middle_y > Zebro_17_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_18_Middle_y) or (Zebro_1_Middle_y > Zebro_19_Middle_y) or (Zebro_1_Middle_y > Zebro_20_Middle_y) or (Zebro_1_Middle_y > 850):
                                Block = "South"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_1_Middle_y < Zebro_2_Middle_y) or (Zebro_1_Middle_y < Zebro_3_Middle_y) or (Zebro_1_Middle_y < Zebro_4_Middle_y) or (Zebro_1_Middle_y < Zebro_5_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_6_Middle_y) or (Zebro_1_Middle_y < Zebro_7_Middle_y) or (Zebro_1_Middle_y < Zebro_8_Middle_y) or (Zebro_1_Middle_y < Zebro_9_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_10_Middle_y) or (Zebro_1_Middle_y < Zebro_11_Middle_y) or (Zebro_1_Middle_y < Zebro_12_Middle_y) or (Zebro_1_Middle_y < Zebro_13_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_14_Middle_y) or (Zebro_1_Middle_y < Zebro_15_Middle_y) or (Zebro_1_Middle_y < Zebro_16_Middle_y) or (Zebro_1_Middle_y < Zebro_17_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_18_Middle_y) or (Zebro_1_Middle_y < Zebro_19_Middle_y) or (Zebro_1_Middle_y < Zebro_20_Middle_y) or (Zebro_1_Middle_y < 50):
                                Block = "North"
                                Bloking.append(Block)
                                Block = None

# For Pico Zebro 2 (Also here if know how to do this shorter plz do so)
                    if Zebros == 1:
                        Blocking_x_1 = abs(Zebro_2_Middle_x - Zebro_1_Middle_x)
                        Blocking_y_1 = abs(Zebro_2_Middle_y - Zebro_1_Middle_y)
                        Blocking_x_3 = abs(Zebro_2_Middle_x - Zebro_3_Middle_x)
                        Blocking_y_3 = abs(Zebro_2_Middle_y - Zebro_3_Middle_y)
                        Blocking_x_4 = abs(Zebro_2_Middle_x - Zebro_4_Middle_x)
                        Blocking_y_4 = abs(Zebro_2_Middle_y - Zebro_4_Middle_y)
                        Blocking_x_5 = abs(Zebro_2_Middle_x - Zebro_5_Middle_x)
                        Blocking_y_5 = abs(Zebro_2_Middle_y - Zebro_5_Middle_y)
                        Blocking_x_6 = abs(Zebro_2_Middle_x - Zebro_6_Middle_x)
                        Blocking_y_6 = abs(Zebro_2_Middle_y - Zebro_6_Middle_y)
                        Blocking_x_7 = abs(Zebro_2_Middle_x - Zebro_7_Middle_x)
                        Blocking_y_7 = abs(Zebro_2_Middle_y - Zebro_7_Middle_y)
                        Blocking_x_8 = abs(Zebro_2_Middle_x - Zebro_8_Middle_x)
                        Blocking_y_8 = abs(Zebro_2_Middle_y - Zebro_8_Middle_y)
                        Blocking_x_9 = abs(Zebro_2_Middle_x - Zebro_9_Middle_x)
                        Blocking_y_9 = abs(Zebro_2_Middle_y - Zebro_9_Middle_y)
                        Blocking_x_10 = abs(Zebro_2_Middle_x - Zebro_10_Middle_x)
                        Blocking_y_10 = abs(Zebro_2_Middle_y - Zebro_10_Middle_y)
                        Blocking_x_11 = abs(Zebro_2_Middle_x - Zebro_11_Middle_x)
                        Blocking_y_11 = abs(Zebro_2_Middle_y - Zebro_11_Middle_y)
                        Blocking_x_12 = abs(Zebro_2_Middle_x - Zebro_12_Middle_x)
                        Blocking_y_12 = abs(Zebro_2_Middle_y - Zebro_12_Middle_y)
                        Blocking_x_13 = abs(Zebro_2_Middle_x - Zebro_13_Middle_x)
                        Blocking_y_13 = abs(Zebro_2_Middle_y - Zebro_13_Middle_y)
                        Blocking_x_14 = abs(Zebro_2_Middle_x - Zebro_14_Middle_x)
                        Blocking_y_14 = abs(Zebro_2_Middle_y - Zebro_14_Middle_y)
                        Blocking_x_15 = abs(Zebro_2_Middle_x - Zebro_15_Middle_x)
                        Blocking_y_15 = abs(Zebro_2_Middle_y - Zebro_15_Middle_y)
                        Blocking_x_16 = abs(Zebro_2_Middle_x - Zebro_16_Middle_x)
                        Blocking_y_16 = abs(Zebro_2_Middle_y - Zebro_16_Middle_y)
                        Blocking_x_17 = abs(Zebro_2_Middle_x - Zebro_17_Middle_x)
                        Blocking_y_17 = abs(Zebro_2_Middle_y - Zebro_17_Middle_y)
                        Blocking_x_18 = abs(Zebro_2_Middle_x - Zebro_18_Middle_x)
                        Blocking_y_18 = abs(Zebro_2_Middle_y - Zebro_18_Middle_y)
                        Blocking_x_19 = abs(Zebro_2_Middle_x - Zebro_19_Middle_x)
                        Blocking_y_19 = abs(Zebro_2_Middle_y - Zebro_19_Middle_y)
                        Blocking_x_20 = abs(Zebro_2_Middle_x - Zebro_20_Middle_x)
                        Blocking_y_20 = abs(Zebro_2_Middle_y - Zebro_20_Middle_y)
            
                        if (0 < Blocking_x_1 < 80) or (0 < Blocking_x_3 < 80) or (0 < Blocking_x_4 < 80) or (0 < Blocking_x_5 < 80)
                        or (0 < Blocking_x_6 < 80) or (0 < Blocking_x_7 < 80) or (0 < Blocking_x_8 < 80) or (0 < Blocking_x_9 < 80)
                        or (0 < Blocking_x_10 < 80) or (0 < Blocking_x_11 < 80) or (0 < Blocking_x_12 < 80) or (0 < Blocking_x_13 < 80)
                        or (0 < Blocking_x_14 < 80) or (0 < Blocking_x_15 < 80) or (0 < Blocking_x_16 < 80) or (0 < Blocking_x_17 < 80)
                        or (0 < Blocking_x_18 < 80) or (0 < Blocking_x_19 < 80) or (0 < Blocking_x_20 < 80):
                            if (Zebro_2_Middle_x < Zebro_1_Middle_x) or (Zebro_2_Middle_x < Zebro_3_Middle_x) or (Zebro_2_Middle_x < Zebro_4_Middle_x) or (Zebro_2_Middle_x < Zebro_5_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_6_Middle_x) or (Zebro_2_Middle_x < Zebro_7_Middle_x) or (Zebro_2_Middle_x < Zebro_8_Middle_x) or (Zebro_2_Middle_x < Zebro_9_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_10_Middle_x) or (Zebro_2_Middle_x < Zebro_11_Middle_x) or (Zebro_2_Middle_x < Zebro_12_Middle_x) or (Zebro_2_Middle_x < Zebro_13_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_14_Middle_x) or (Zebro_2_Middle_x < Zebro_15_Middle_x) or (Zebro_2_Middle_x < Zebro_16_Middle_x) or (Zebro_2_Middle_x < Zebro_17_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_18_Middle_x) or (Zebro_2_Middle_x < Zebro_19_Middle_x) or (Zebro_2_Middle_x < Zebro_20_Middle_x) or (Zebro_2_Middle_x > 1550)::
                                Block = "East"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_2_Middle_x > Zebro_1_Middle_x) or (Zebro_2_Middle_x > Zebro_3_Middle_x) or (Zebro_2_Middle_x > Zebro_4_Middle_x) or (Zebro_2_Middle_x > Zebro_5_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_6_Middle_x) or (Zebro_2_Middle_x > Zebro_7_Middle_x) or (Zebro_2_Middle_x > Zebro_8_Middle_x) or (Zebro_2_Middle_x > Zebro_9_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_10_Middle_x) or (Zebro_2_Middle_x > Zebro_11_Middle_x) or (Zebro_2_Middle_x > Zebro_12_Middle_x) or (Zebro_2_Middle_x > Zebro_13_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_14_Middle_x) or (Zebro_2_Middle_x > Zebro_15_Middle_x) or (Zebro_2_Middle_x > Zebro_16_Middle_x) or (Zebro_2_Middle_x > Zebro_17_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_18_Middle_x) or (Zebro_2_Middle_x > Zebro_19_Middle_x) or (Zebro_2_Middle_x > Zebro_20_Middle_x) or (Zebro_2_Middle_x < 50):
                                Block = "West"
                                Bloking.append(Block)
                                Block = None
                        if (0 < Blocking_y_1 < 80) or (0 < Blocking_y_3 < 80) or (0 < Blocking_y_4 < 80) or (0 < Blocking_y_5 < 80)
                        or (0 < Blocking_y_6 < 80) or (0 < Blocking_y_7 < 80) or (0 < Blocking_y_8 < 80) or (0 < Blocking_y_9 < 80)
                        or (0 < Blocking_y_10 < 80) or (0 < Blocking_y_11 < 80) or (0 < Blocking_y_12 < 80) or (0 < Blocking_y_13 < 80)
                        or (0 < Blocking_y_14 < 80) or (0 < Blocking_y_15 < 80) or (0 < Blocking_y_16 < 80) or (0 < Blocking_y _17 < 80)
                        or (0 < Blocking_y_18 < 80) or (0 < Blocking_y_19 < 80) or (0 < Blocking_y_20 < 80):
                            if (Zebro_2_Middle_y > Zebro_1_Middle_y) or (Zebro_2_Middle_y > Zebro_3_Middle_y) or (Zebro_2_Middle_y > Zebro_4_Middle_y) or (Zebro_2_Middle_y > Zebro_5_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_6_Middle_y) or (Zebro_2_Middle_y > Zebro_7_Middle_y) or (Zebro_2_Middle_y > Zebro_8_Middle_y) or (Zebro_2_Middle_y > Zebro_9_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_10_Middle_y) or (Zebro_2_Middle_y > Zebro_11_Middle_y) or (Zebro_2_Middle_y > Zebro_12_Middle_y) or (Zebro_2_Middle_y > Zebro_13_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_14_Middle_y) or (Zebro_2_Middle_y > Zebro_15_Middle_y) or (Zebro_2_Middle_y > Zebro_16_Middle_y) or (Zebro_2_Middle_y > Zebro_17_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_18_Middle_y) or (Zebro_2_Middle_y > Zebro_19_Middle_y) or (Zebro_2_Middle_y > Zebro_20_Middle_y) or (Zebro_2_Middle_y > 850):
                                Block = "South"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_2_Middle_y < Zebro_1_Middle_y) or (Zebro_2_Middle_y < Zebro_3_Middle_y) or (Zebro_2_Middle_y < Zebro_4_Middle_y) or (Zebro_2_Middle_y < Zebro_5_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_6_Middle_y) or (Zebro_2_Middle_y < Zebro_7_Middle_y) or (Zebro_2_Middle_y < Zebro_8_Middle_y) or (Zebro_2_Middle_y < Zebro_9_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_10_Middle_y) or (Zebro_2_Middle_y < Zebro_11_Middle_y) or (Zebro_2_Middle_y < Zebro_12_Middle_y) or (Zebro_2_Middle_y < Zebro_13_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_14_Middle_y) or (Zebro_2_Middle_y < Zebro_15_Middle_y) or (Zebro_2_Middle_y < Zebro_16_Middle_y) or (Zebro_2_Middle_y < Zebro_17_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_18_Middle_y) or (Zebro_2_Middle_y < Zebro_19_Middle_y) or (Zebro_2_Middle_y < Zebro_20_Middle_y) or (Zebro_1_Middle_y < 50):
                                Block = "North"
                                Bloking.append(Block)
                                Block = None
                        # Grab condition zebro 2:
                        PicoZebro = []
                        PicoZebro_2 = Zebro_2_Middle_x , Zebro_2_Middle_y, Direction_Zebro_2, Blocking, Angle_Zebro_2
                        PicoZebro = PicoZebro_2




    CameraThread= Camera_Thread()
    CameraThread.setName("Camera_Thread")

class Camera_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.start()

    def run(self):
        global picture_test
        #Picture_number = 0
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the NumPy array representing the image, the initialize the timestamp
            # and occupied/unoccupied text
            start_time = time.time()
            image = frame.array

            Timetest = time.strftime("%d-%m-%Y")
            # Show the current view for debugging
            cv2.imshow("original %s" % Timetest,image)

            if (picture_test == 1) or (picture_test == 2) or (picture_test == 3):
                cv2.imwrite("Image%s.jpg"%picture_test, image)
                print(picture_test)
                    #self.condition2.acquire()
                    #print ('lock acquire by %s' % self.name)
                    #Picture_number = 0
                    #self.Picture_number = Picture_number
                    #self.condition2.notify()
                    #time.sleep(0.01)
                    #print ('lock released by %s' % self.name)
                    #self.condition2.release()

            # show the frame
            key = cv2.waitKey(1) & 0xFF

            #clear the stream in preparation of the next frame
            rawCapture.truncate(0)
                
            # if the 'q' key was pressed, break from the loop
            if key == ord("q"):
                # cleanup the camera and close any open windows
                cv2.destroyAllWindows()
                break

    cv2.imwrite("See_Difference.jpg",New_image)
    lowValY = 200
    highValY = 100
    array_np = np.asarray(New_image)
    low_values_indices = array_np > lowValY  # Where values are low
    high_values_indices = array_np < highValY
    array_np[low_values_indices] = 0  # All low values set to 0
    array_np[high_values_indices] = 0

    cv2.imshow("Testing 2 image", array_np)
    cv2.imwrite("new_image.jpg", array_np)

    Finding = cv2.imread("new_image_2.jpg")
    Finding_Canny = cv2.Canny(Finding, 15, 200)
    kernel = np.ones((8,8),np.uint8)
    Finding_Canny = cv2.morphologyEx(Finding_Canny, cv2.MORPH_CLOSE, kernel)
    Finding_Canny = cv2.Canny(Finding_Canny, 100, 200)
    cv2.imshow("Edge detection", Finding_Canny)
    Finding_Gray = cv2.cvtColor(Finding, cv2.COLOR_BGR2GRAY)

    (_, contours, _) = cv2.findContours(Finding_Canny.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_NONE)    
    for c in contours:
        try:
            [x,y,w,h] = cv2.boundingRect(c)
            #cv2.drawContours(Finding, [c], -1, (255, 0, 255), -1)
            cv2.rectangle(Finding,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(Finding,'Found led 1',(x+w+10,y+h),0,0.3,(0,255,0))
        except AttributeError:
            pass
    cv2.imshow("Found Objects", Finding)

#from wakeonlan import *


class Camera_Thread(threading.Thread):
    def __init__(self, Picture_number):
        ''' Constructor. of Control Thread '''
        threading.Thread.__init__(self)

        self.daemon = True

        self.Picture_number = Picture_number
        
        self.start()
 
    def run(self):
        while True:
            # capture frames from the camera
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the NumPy array representing the image, the initialize the timestamp
                # and occupied/unoccupied text
                image = frame.array
                
                Timetest = time.strftime("%d-%m-%Y")
                # Show the current view for debugging
                cv2.imshow("original %s" % Timetest,image)
                if (self.Picture_number == 1) or (self.Picture_number == 2) or (self.Picture_number == 3):
                    cv2.imwrite("image%s.jpg"%self.Picture_number, image)

                # show the frame
                key = cv2.waitKey(1) & 0xFF

                #clear the stream in preparation of the next frame
                rawCapture.truncate(0)

                self.Picture_number = 0

                # if the 'q' key was pressed, break from the loop
                if key == ord("q"):
                    # cleanup the camera and close any open windows
                    cv2.destroyAllWindows()
                    # Wait for the threads to finish...
                    print('Main Terminating...')
                    break
            time.sleep(15) 

#phone = "ff:ff:ff:ff:ff:ff"

#def search():         
#  devices = bluetooth.discover_devices(duration = 5, lookup_names = True)
#  return devices

#while True:
#    results = search()
#    print(results)


            hullArea = cv2.contourArea(cv2.convexHull(c))
            keepSolidity = solidity > 0.8
            try:
                solidity = area / float(hullArea)
            except ZeroDivisionError:
                solidity = 0
            #if len(approx) >= 2 and len(approx) <= 7:

"""
    # computes the bounding box for the contour, and draws it on the frame,
    for cnts, hier in zip(cnts, hierarchy):
        (x,y,w,h) = cv2.boundingRect(cnts)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)
        if w > 5 and h > 5:
            cv2.rectangle(Orientation_image, (x,y), (x+w,y+h), (255, 0, 0), 2)

    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(Orientation_image, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2) """

    mask_white = cv2.imread("Pico/White_MASK.jpg", 0)

    white_edges = cv2.Canny(mask_white, 100, 200, apertureSize = 3)

    cv2.imshow("TEs 2",white_edges)
    
    (_, cnts_white, hierarchy) = cv2.findContours(white_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts_white:
        cv2.drawContours(mask_white, cnts_white, -1, (255,255,255), 1)

    cv2.imshow("contours white",mask_white)
    
#    areaArray_white = []
    
 #   for i, c_white in enumerate(cnts_white):
  #      area_white = cv2.contourArea(c_white)
   #     areaArray_white.append(area_white)
        
    #sorteddata_white = sorted(zip(areaArray_white, cnts_white), key=lambda x: x[0], reverse=True)



        if np.all(white_pixel0 == ([[0],[255],[255]] or [[255],[0],[255]] or [[255],[255],[0]])):
            if Do_once ==1:
                print("Found White on pixel 0")
                print(white_pixel0)
                Do_once = 2
        elif np.all(white_pixel1 == ([[0],[255],[255]] or [[255],[0],[255]] or [[255],[255],[0]])):
            if Do_once ==1:
                print("Found White on pixel 1")
                print(white_pixel1)
                Do_once = 2
        elif np.all(white_pixel2 == ([[0],[255],[255]] or [[255],[0],[255]] or [[255],[255],[0]])):
            if Do_once ==1:
                print("Found White on pixel 2")
                print(white_pixel2)
                Do_once = 2
        elif np.all(white_pixel3 == ([[0],[255],[255]] or [[255],[0],[255]] or [[255],[255],[0]])):
            if Do_once ==1:
                print("Found White on pixel 3")
                print(white_pixel3)
                Do_once = 2    

    if Do_once == 1:
        sys.stdout = open("out.txt", "w")
        np.set_printoptions(threshold=np.nan)
        print(mask_QR_white)
        Do_once = 2

    for i2, c2 in enumerate(qrc):
        area2 = cv2.contourArea(c2)
        areaArray2.append(area2)
    sorteddata2 = sorted(zip(areaArray2, qrc), key=lambda x: x[0], reverse=True)

    try:
        largestcontour2 = sorteddata2[0][1]
        #rect = cv2.minAreaRect(largestcontour) # Colud be used for finding angle
        #draw it
        x1, y1, w1, h1 = cv2.boundingRect(largestcontour2)
        QR_CODE = Orientation_image[y:y+h, x:x+w]
        cv2.imshow("QR_CODE LargestContour", QR_CODE)
    except IndexError:
        pass

        with open('outpu_file.txt', 'w+') as f:
            f.write('B,G,R\n')
            for x in range(width):
                f.write('%d ' %x)
                f.write('\n')
                for y in range(height):
                    b = pix[x,y][0]
                    g = pix[x,y][1]
                    r = pix[x,y][2]
                    f.write(' %d' %y)
                    f.write('[{0}, {1}, {2}] '.format(r,g,b))

    cv2.imshow("Zebro_s", Zebro_edges)

    #Function for finding larges contour in image Zebro
    (_,contours2,hierarchy2) = cv2.findContours(Zebro_edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Find contours with hierarchy
    areaArray = []

    cv2.drawContours(Zebro_edges, contours2, -1, (255, 0,0 ), 1)
    cv2.imshow("Zebro_edges", Zebro_edges)
    
    for i, c in enumerate(contours2):
        area = cv2.contourArea(c)
        areaArray.append(area)
        [vx,vy,x,y] = cv2.fitLine(contours2[0], cv2.DIST_L2,0,1,1)
        lefty = int((-x*vy/vx)+y)
        righty = int(((200-x)*vy/vx)+y)
        cv2.line(Zebro_edges, (200-1,righty),(0,lefty),(0,255,255),2)

    cv2.imshow("Zebro_lines", Zebro_edges)

    minLineLength = 20
    lines = cv2.HoughLinesP(image = Zebro_edges, rho=0.5, theta = np.pi/180, threshold = 20,
                            lines=np.array([]),minLineLength=minLineLength,maxLineGap=100)

    a,b,c = lines.shape
    for i in range(a):
        cv2.line(Zebro_res, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
                 (0,0,255), 3, cv2.LINE_AA)

    cv2.imshow("Zebro_res ",Zebro_res)

    Zebro_template = cv2.imread("Pico/fourdots2.jpg", 1)

    Zebro_height, Zebro_width = Zebro_image.shape[:2]
    Zebro_template_height, Zebro_template_width = Zebro_template.shape[:2]
    result_size = [ s[0] - s[1] + 1 for s in zip([Zebro_height, Zebro_width], [Zebro_template_height, Zebro_template_width]) ]

    #result = cv2.createImage(result_size, cv.IPL_DEPTH_32F, 1)

    result = cv2.matchTemplate(image, Zebro_template, cv2.TM_CCORR)

    min_val, Max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    cv2.imshow("Zeres", result)

    ret, thresh = cv2.threshold(Zebro_gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(),255,0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    cv2.imshow("unknown", sure_bg)

black = [([0,0,0],[0,0,40])] #=black
white = [([0,0,0],[0,0,255])] #=white

    Zebro_image= cv2.imread("Pico/rect.jpg", 1)

    # color in cube is hsv values for easier detection of green.
    black_hsv = cv2.cvtColor(Zebro_image, cv2.COLOR_BGR2HSV)

    #green the important color
    for(black_lower,black_upper) in black:
            black_lower = np.array(black_lower,dtype=np.uint8)
            black_upper = np.array(black_upper,dtype=np.uint8) 
    # the mask 
    mask_black = cv2.inRange(black_hsv,black_lower,black_upper)

    #green the important color
    for(white_lower,white_upper) in white:
            white_lower = np.array(white_lower,dtype=np.uint8)
            white_upper = np.array(white_upper,dtype=np.uint8) 
    # the mask 
    mask_white = cv2.inRange(black_hsv,white_lower,white_upper)

    Black_white_out = cv2.bitwise_and(Zebro_image, Zebro_image, mask = mask_white)
    cv2.imshow("HSV white mask", mask_white)
    cv2.imshow("HSV white", Black_white_out)

    #Function for finding larges contour in image
    image_gray2 = cv2.cvtColor(qr2_image, cv2.COLOR_BGR2GRAY) # Convert Image captured from Image Input to GrayScale
    edges2 = cv2.Canny(image_gray2,100,200,3)      # Apply Canny edge detection on the gray image
    (_,contours2,hierarchy2) = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Find contours with hierarchy
    areaArray = []
    for i, c in enumerate(contours2):
        area = cv2.contourArea(c)
        areaArray.append(area)
    #first sort the array by area
 
    sorteddata = sorted(zip(areaArray, contours2), key=lambda x: x[0], reverse=True)

    #find the nth largest contour [n-1][1], in this case 1
    try:
        largestcontour = sorteddata[0][1]
        #draw it
        x, y, w, h = cv2.boundingRect(largestcontour)
        appelkoek = qr2_image[y:y+h, x:x+w]
        cv2.rectangle(qr2_image, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.imwrite("Pico/testing.jpg", appelkoek)

    except IndexError:
        pass


        while True:        
            i = 0
            for c in contours2:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                if i == 1:
                    break
     
                # if the shape has 4 vertices, it is either a square or
                # a rectangle
                if len(approx) == 4:
                # compute the bounding box of the contour and use the
                # bounding box to compute the aspect ratio
                    (x, y, w, h) = cv2.boundingRect(approx)
                    ar = w / float(h)
     
                    # a square will have an aspect ratio that is approximately
                    # equal to one, otherwise, the shape is a rectangle
                    if ar >= 0.95 and ar <= 1.05:
                        break
                i = i + 1


    g = sum(sum(mask_green))

    # blue
    for(lower,upper) in blue:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)
    # the mask    
    mask = cv2.inRange(hsv,lower,upper)
    b = sum(sum(mask))

    #red
    for(lower,upper) in red:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask = cv2.inRange(hsv,lower,upper)
    r = sum(sum(mask))

    #yellow	
    for(lower,upper) in yellow:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask = cv2.inRange(hsv,lower,upper)
    y = sum(sum(mask))

    if b < 1000 and r < 1000 and y < 1000 and g < 1000:
        pass 
    else:
        if b > r and b > g and b >y:
            pass 
        elif r > g and r > y:
            pass 
        elif y > g:
            pass 
        else:
            pass # print ("block green")

    # For Finding rectangles
    
    # make image gray for finding rectangles
    # convert the image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    # shape detector
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:    
        rect = cv2.boundingRect(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            if rect[2] < 100 or rect[3] < 100: continue
            x,y,w,h = rect
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(image,'Moth Detected',(x+w+10,y+h),0,0.3,(0,255,0))
        else:
            pass
        

    # convert the image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
 
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    
    # loop over conturs for finding rectangles.
    for c in cnts:
        M = cv2.moments(c)
        # shape using only the contour
        shape = functions_shape.detect(c)
        if shape == "rectangle":
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"]=1
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)


    

        # if no contours were found, return None
        if len(cnts) == 0:
            pass

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            
            if ar >= 0.95 and ar <= 1.05:
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

                    M = cv2.moments(c)
        # initialize the shape name and approximate the contour
        area = cv2.contourArea(c)
        if area < 10000:
           cnts.remove(c)
        else:
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
       
    approx = cv2.approxPolyDP(cn, 0.02 * cv2.arcLength(cn, True), True)

    def is_contour_bad(self, c):
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # the contour is 'bad' if it is not a rectangle
        return not len(approx) == 4

    # function from pyimagesearch for finding barcodes (works for qr codes.
    def detect(self, image):
        # convert the image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            # initialize the shape name and approximate the contour
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            # if no contours were found, return None
            if len(cnts) == 0:
                return None

            # if the shape has 4 vertices, it is either a square or
            # a rectangle
            elif len(approx) == 4:
                # compute the bounding box of the contour and use the
                # bounding box to compute the aspect ratio
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)

                box = c
 
                # a square will have an aspect ratio that is approximately
                # equal to one, otherwise, the shape is a rectangle
                shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # return the bounding box of the rectangle
        return box
            
    def detect_shape(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
 
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
 
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
                                          
        # if the shape is a hexagon, it will have 6 vertices
        elif len(approx) == 6:
            shape = "hexagon"                                    
 
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape
    
