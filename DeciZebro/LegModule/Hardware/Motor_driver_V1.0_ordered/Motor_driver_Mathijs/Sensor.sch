EESchema Schematic File Version 2
LIBS:Motor_driver-rescue
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:Basic
LIBS:extended
LIBS:IC
LIBS:MOTOR
LIBS:SmartPrj
LIBS:Motor_driver-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 4 6
Title "Sensors"
Date "2017-01-19"
Rev "0"
Comp "Zebro"
Comment1 "Lisanne Kesselaar"
Comment2 "Concept Version 0.1"
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L GND #PWR012
U 1 1 5881398C
P 2475 3275
F 0 "#PWR012" H 2475 3025 50  0001 C CNN
F 1 "GND" H 2475 3125 50  0000 C CNN
F 2 "" H 2475 3275 50  0000 C CNN
F 3 "" H 2475 3275 50  0000 C CNN
	1    2475 3275
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 58813995
P 1875 3275
F 0 "#PWR013" H 1875 3025 50  0001 C CNN
F 1 "GND" H 1875 3125 50  0000 C CNN
F 2 "" H 1875 3275 50  0000 C CNN
F 3 "" H 1875 3275 50  0000 C CNN
	1    1875 3275
	1    0    0    -1  
$EndComp
$Comp
L C-EUC0603 C?
U 1 1 5881399D
P 1875 2925
AR Path="/5881399D" Ref="C?"  Part="1" 
AR Path="/58813872/5881399D" Ref="C5"  Part="1" 
F 0 "C5" H 1935 2940 45  0000 L BNN
F 1 "100n" H 1935 2740 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 1905 3075 20  0001 C CNN
F 3 "" H 1875 2925 60  0001 C CNN
	1    1875 2925
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR014
U 1 1 58813C02
P 1875 2675
F 0 "#PWR014" H 1875 2525 50  0001 C CNN
F 1 "+3.3V" H 1875 2815 50  0000 C CNN
F 2 "" H 1875 2675 50  0000 C CNN
F 3 "" H 1875 2675 50  0000 C CNN
	1    1875 2675
	1    0    0    -1  
$EndComp
Text HLabel 2975 2775 2    60   Output ~ 0
HALL
Text Notes 2190 2000 0    60   ~ 0
Hall sensor
Connection ~ 1875 2775
Wire Wire Line
	2475 3225 2475 3275
Wire Wire Line
	2975 2775 2925 2775
Wire Wire Line
	1875 3125 1875 3275
Wire Wire Line
	1875 2675 1875 2825
Wire Wire Line
	1875 2775 2025 2775
Wire Notes Line
	10400 1800 1200 1800
Wire Notes Line
	1200 1800 1200 6100
Wire Notes Line
	1200 6100 10400 6100
Wire Notes Line
	10400 6100 10400 1800
Wire Notes Line
	3900 1800 3900 6100
$Comp
L SM451 U4
U 1 1 58844CE0
P 2475 2775
F 0 "U4" H 2475 3175 60  0000 C CNN
F 1 "SM451" H 2525 3075 60  0000 C CNN
F 2 "TO_SOT_Packages_THT:TO-92_Horizontal2_Inline_Narrow_Oval" H 2475 2775 60  0001 C CNN
F 3 "" H 2475 2775 60  0001 C CNN
	1    2475 2775
	1    0    0    -1  
$EndComp
$Comp
L ACS710 U5
U 1 1 5891271E
P 5575 3925
F 0 "U5" H 5575 4675 60  0000 C CNN
F 1 "ACS710" H 5575 3025 60  0000 C CNN
F 2 "Housings_SOIC:SOIC-16W_7.5x10.3mm_Pitch1.27mm" H 5575 3925 60  0001 C CNN
F 3 "" H 5575 3925 60  0001 C CNN
	1    5575 3925
	1    0    0    -1  
$EndComp
Wire Wire Line
	4975 3375 4200 3375
Wire Wire Line
	4200 2950 4200 4050
$Comp
L +3.3V #PWR015
U 1 1 58912BCE
P 4200 2950
F 0 "#PWR015" H 4200 2800 50  0001 C CNN
F 1 "+3.3V" H 4200 3090 50  0000 C CNN
F 2 "" H 4200 2950 50  0000 C CNN
F 3 "" H 4200 2950 50  0000 C CNN
	1    4200 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 3925 4975 3925
Wire Wire Line
	4850 3700 4850 4125
Wire Wire Line
	4850 4025 4975 4025
Connection ~ 4850 3925
Wire Wire Line
	4850 4125 4975 4125
Connection ~ 4850 4025
Wire Wire Line
	4775 4175 4775 4525
Wire Wire Line
	4775 4225 4975 4225
Wire Wire Line
	4975 4425 4775 4425
Connection ~ 4775 4425
Wire Wire Line
	4975 4325 4775 4325
Connection ~ 4775 4325
Wire Wire Line
	4975 4625 4775 4625
Wire Wire Line
	4775 4625 4775 4825
$Comp
L GND #PWR016
U 1 1 5891337D
P 4775 4825
F 0 "#PWR016" H 4775 4575 50  0001 C CNN
F 1 "GND" H 4775 4675 50  0000 C CNN
F 2 "" H 4775 4825 50  0000 C CNN
F 3 "" H 4775 4825 50  0000 C CNN
	1    4775 4825
	1    0    0    -1  
$EndComp
Wire Wire Line
	4625 3575 4975 3575
Wire Wire Line
	6175 3475 6375 3475
Wire Wire Line
	6175 3575 6375 3575
Wire Wire Line
	6175 3825 6600 3825
Wire Wire Line
	4850 3825 4975 3825
$Comp
L C-EUC0603 C?
U 1 1 58913F20
P 6500 4325
AR Path="/58913F20" Ref="C?"  Part="1" 
AR Path="/58813872/58913F20" Ref="C8"  Part="1" 
F 0 "C8" H 6560 4340 45  0000 L BNN
F 1 "1n" H 6560 4140 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 6530 4475 20  0001 C CNN
F 3 "" H 6500 4325 60  0001 C CNN
	1    6500 4325
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 3825 6500 4225
$Comp
L C-EUC0603 C?
U 1 1 5891407B
P 6225 4325
AR Path="/5891407B" Ref="C?"  Part="1" 
AR Path="/58813872/5891407B" Ref="C7"  Part="1" 
F 0 "C7" H 6285 4340 45  0000 L BNN
F 1 "1n" H 6285 4140 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 6255 4475 20  0001 C CNN
F 3 "" H 6225 4325 60  0001 C CNN
	1    6225 4325
	1    0    0    -1  
$EndComp
Wire Wire Line
	6225 4225 6225 4175
Wire Wire Line
	6225 4175 6175 4175
Wire Wire Line
	6225 4525 6225 4825
$Comp
L GND #PWR017
U 1 1 58914388
P 6225 4825
F 0 "#PWR017" H 6225 4575 50  0001 C CNN
F 1 "GND" H 6225 4675 50  0000 C CNN
F 2 "" H 6225 4825 50  0000 C CNN
F 3 "" H 6225 4825 50  0000 C CNN
	1    6225 4825
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 4525 6500 4825
$Comp
L GND #PWR018
U 1 1 589143D7
P 6500 4825
F 0 "#PWR018" H 6500 4575 50  0001 C CNN
F 1 "GND" H 6500 4675 50  0000 C CNN
F 2 "" H 6500 4825 50  0000 C CNN
F 3 "" H 6500 4825 50  0000 C CNN
	1    6500 4825
	1    0    0    -1  
$EndComp
Text HLabel 6375 3475 2    60   Output ~ 0
~FAULT_CURRENT
Text HLabel 6375 3575 2    60   Output ~ 0
V_Imotor
$Comp
L C-EUC0603 C?
U 1 1 58914B15
P 4200 4150
AR Path="/58914B15" Ref="C?"  Part="1" 
AR Path="/58813872/58914B15" Ref="C6"  Part="1" 
F 0 "C6" H 4260 4165 45  0000 L BNN
F 1 "100n" H 4260 3965 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 4230 4300 20  0001 C CNN
F 3 "" H 4200 4150 60  0001 C CNN
	1    4200 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 4350 4200 4775
$Comp
L GND #PWR019
U 1 1 58914B69
P 4200 4775
F 0 "#PWR019" H 4200 4525 50  0001 C CNN
F 1 "GND" H 4200 4625 50  0000 C CNN
F 2 "" H 4200 4775 50  0000 C CNN
F 3 "" H 4200 4775 50  0000 C CNN
	1    4200 4775
	1    0    0    -1  
$EndComp
Connection ~ 4200 3375
Text HLabel 4875 3100 2    60   Input ~ 0
current_sense_fault_en
$Comp
L R R5
U 1 1 589151B8
P 6250 3175
F 0 "R5" V 6330 3175 50  0000 C CNN
F 1 "330k" V 6150 3175 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 6180 3175 50  0001 C CNN
F 3 "" H 6250 3175 50  0000 C CNN
	1    6250 3175
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 3325 6250 3475
Connection ~ 6250 3475
Wire Wire Line
	6250 3025 6250 2950
$Comp
L +3.3V #PWR020
U 1 1 5891541F
P 6250 2950
F 0 "#PWR020" H 6250 2800 50  0001 C CNN
F 1 "+3.3V" H 6250 3090 50  0000 C CNN
F 2 "" H 6250 2950 50  0000 C CNN
F 3 "" H 6250 2950 50  0000 C CNN
	1    6250 2950
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 589156B4
P 4475 3575
F 0 "R3" V 4300 3575 50  0000 C CNN
F 1 "10k" V 4375 3575 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 4405 3575 50  0001 C CNN
F 3 "" H 4475 3575 50  0000 C CNN
	1    4475 3575
	0    -1   -1   0   
$EndComp
$Comp
L R R4
U 1 1 589158FB
P 4675 3825
F 0 "R4" V 4755 3825 50  0000 C CNN
F 1 "22k" V 4575 3825 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 4605 3825 50  0001 C CNN
F 3 "" H 4675 3825 50  0000 C CNN
	1    4675 3825
	1    0    0    -1  
$EndComp
Connection ~ 4850 3825
Connection ~ 4775 4225
Wire Wire Line
	4775 4525 4975 4525
Wire Wire Line
	4675 3675 4675 3575
Connection ~ 4675 3575
Wire Wire Line
	4325 3575 4200 3575
Connection ~ 4200 3575
Wire Wire Line
	4675 3975 4675 4825
$Comp
L GND #PWR021
U 1 1 58916ADE
P 4675 4825
F 0 "#PWR021" H 4675 4575 50  0001 C CNN
F 1 "GND" H 4675 4675 50  0000 C CNN
F 2 "" H 4675 4825 50  0000 C CNN
F 3 "" H 4675 4825 50  0000 C CNN
	1    4675 4825
	1    0    0    -1  
$EndComp
Text Notes 5050 2040 0    60   ~ 0
Current Sensor
Text HLabel 4850 3700 2    60   Input ~ 0
M2_S
Text HLabel 4775 4175 1    60   Input ~ 0
M2
Wire Notes Line
	1200 3975 3900 3975
Text Notes 2090 4200 0    60   ~ 0
Photo Encoder
$Comp
L GND #PWR022
U 1 1 58834FFA
P 1650 5550
F 0 "#PWR022" H 1650 5300 50  0001 C CNN
F 1 "GND" H 1650 5400 50  0000 C CNN
F 2 "" H 1650 5550 50  0000 C CNN
F 3 "" H 1650 5550 50  0000 C CNN
	1    1650 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 4650 2600 4900
Wire Wire Line
	2600 4900 2550 4900
$Comp
L +3.3V #PWR023
U 1 1 58834FAE
P 2600 4650
F 0 "#PWR023" H 2600 4500 50  0001 C CNN
F 1 "+3.3V" H 2600 4790 50  0000 C CNN
F 2 "" H 2600 4650 50  0000 C CNN
F 3 "" H 2600 4650 50  0000 C CNN
	1    2600 4650
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR024
U 1 1 58834F93
P 1650 4675
F 0 "#PWR024" H 1650 4525 50  0001 C CNN
F 1 "+3.3V" H 1650 4815 50  0000 C CNN
F 2 "" H 1650 4675 50  0000 C CNN
F 3 "" H 1650 4675 50  0000 C CNN
	1    1650 4675
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 4675 1650 4900
Wire Wire Line
	1650 4900 1700 4900
NoConn ~ 1700 5000
Wire Wire Line
	1700 5100 1650 5100
$Comp
L TCUT1350 U3
U 1 1 5883457C
P 2100 5000
F 0 "U3" H 2090 5200 60  0000 C CNN
F 1 "TCUT1350" H 2100 4800 60  0000 C CNN
F 2 "test:TCUT1350" H 2774 4988 60  0001 C CNN
F 3 "" H 2774 4988 60  0001 C CNN
	1    2100 5000
	1    0    0    -1  
$EndComp
Text Notes 8600 2000 0    60   ~ 0
Temp Sensor
Text Notes 7750 5850 0    60   ~ 0
Choose NCT75MNR2G for SOIC package @ Mouser
$Comp
L NCT75 U6
U 1 1 5884529D
P 8770 4125
F 0 "U6" H 8770 4575 60  0000 C CNN
F 1 "NCT75" H 8820 3775 60  0000 C CNN
F 2 "Housings_SOIC:SOIC-8_3.9x4.9mm_Pitch1.27mm" H 8770 4125 60  0001 C CNN
F 3 "" H 8770 4125 60  0001 C CNN
	1    8770 4125
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR025
U 1 1 5883DA03
P 7995 4525
F 0 "#PWR025" H 7995 4275 50  0001 C CNN
F 1 "GND" H 7995 4375 50  0000 C CNN
F 2 "" H 7995 4525 50  0000 C CNN
F 3 "" H 7995 4525 50  0000 C CNN
	1    7995 4525
	1    0    0    -1  
$EndComp
Wire Wire Line
	7995 4300 7995 4525
Connection ~ 7995 3875
Wire Wire Line
	7995 3600 7995 4000
$Comp
L C-EUC0603 C?
U 1 1 5883D9FA
P 7995 4100
AR Path="/5883D9FA" Ref="C?"  Part="1" 
AR Path="/58813872/5883D9FA" Ref="C9"  Part="1" 
F 0 "C9" H 8055 4115 45  0000 L BNN
F 1 "100n" H 8055 3915 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 8025 4250 20  0001 C CNN
F 3 "" H 7995 4100 60  0001 C CNN
	1    7995 4100
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR026
U 1 1 5883D9F3
P 9420 3575
F 0 "#PWR026" H 9420 3425 50  0001 C CNN
F 1 "+3.3V" H 9420 3715 50  0000 C CNN
F 2 "" H 9420 3575 50  0000 C CNN
F 3 "" H 9420 3575 50  0000 C CNN
	1    9420 3575
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR027
U 1 1 5883D9ED
P 7995 3600
F 0 "#PWR027" H 7995 3450 50  0001 C CNN
F 1 "+3.3V" H 7995 3740 50  0000 C CNN
F 2 "" H 7995 3600 50  0000 C CNN
F 3 "" H 7995 3600 50  0000 C CNN
	1    7995 3600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR028
U 1 1 5883D9E7
P 8270 4525
F 0 "#PWR028" H 8270 4275 50  0001 C CNN
F 1 "GND" H 8270 4375 50  0000 C CNN
F 2 "" H 8270 4525 50  0000 C CNN
F 3 "" H 8270 4525 50  0000 C CNN
	1    8270 4525
	1    0    0    -1  
$EndComp
Text HLabel 9520 4175 2    60   Input ~ 0
SCL_SL
Text HLabel 9520 4075 2    60   BiDi ~ 0
SDA_SL
Text HLabel 9520 3975 2    60   Output ~ 0
~ALERT_TEMP
Wire Wire Line
	9320 4175 9520 4175
Wire Wire Line
	9320 4075 9520 4075
Connection ~ 8270 4275
Wire Wire Line
	8270 4275 8320 4275
Connection ~ 8270 4175
Wire Wire Line
	8270 4175 8320 4175
Wire Wire Line
	8270 4075 8270 4525
Wire Wire Line
	8270 4075 8320 4075
Wire Wire Line
	7995 3875 8320 3875
Wire Wire Line
	9420 3625 9420 3575
$Comp
L R R6
U 1 1 5883D9D1
P 9420 3775
F 0 "R6" V 9500 3775 50  0000 C CNN
F 1 "2k7" V 9320 3775 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 9350 3775 50  0001 C CNN
F 3 "" H 9420 3775 50  0000 C CNN
	1    9420 3775
	1    0    0    -1  
$EndComp
Connection ~ 9420 3975
Wire Wire Line
	9420 3975 9420 3925
Wire Wire Line
	9320 3975 9520 3975
Wire Notes Line
	1200 2200 10400 2200
Wire Notes Line
	1200 4000 3900 4000
Wire Notes Line
	3900 4300 1200 4300
Wire Notes Line
	7500 1800 7500 6100
Wire Wire Line
	4975 3475 4875 3475
Wire Wire Line
	4875 3475 4875 3100
Wire Wire Line
	8320 3975 8270 3975
Wire Wire Line
	8270 3975 8270 4080
Connection ~ 8270 4080
$Comp
L GND #PWR029
U 1 1 58937C95
P 1400 5550
F 0 "#PWR029" H 1400 5300 50  0001 C CNN
F 1 "GND" H 1400 5400 50  0000 C CNN
F 2 "" H 1400 5550 50  0000 C CNN
F 3 "" H 1400 5550 50  0000 C CNN
	1    1400 5550
	-1   0    0    -1  
$EndComp
$Comp
L C-EUC0603 C?
U 1 1 58937C9B
P 1400 4950
AR Path="/58937C9B" Ref="C?"  Part="1" 
AR Path="/58813872/58937C9B" Ref="C18"  Part="1" 
AR Path="/5881389D/58937C9B" Ref="C?"  Part="1" 
F 0 "C18" H 1460 4965 45  0000 L BNN
F 1 "100n" H 1175 4775 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 1430 5100 20  0001 C CNN
F 3 "" H 1400 4950 60  0001 C CNN
	1    1400 4950
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1400 5150 1400 5550
Wire Wire Line
	1400 4850 1400 4800
Wire Wire Line
	1400 4800 1650 4800
Connection ~ 1650 4800
$Comp
L GND #PWR030
U 1 1 58937D84
P 3725 5525
F 0 "#PWR030" H 3725 5275 50  0001 C CNN
F 1 "GND" H 3725 5375 50  0000 C CNN
F 2 "" H 3725 5525 50  0000 C CNN
F 3 "" H 3725 5525 50  0000 C CNN
	1    3725 5525
	-1   0    0    -1  
$EndComp
$Comp
L C-EUC0603 C?
U 1 1 58937D8A
P 3725 4925
AR Path="/58937D8A" Ref="C?"  Part="1" 
AR Path="/58813872/58937D8A" Ref="C19"  Part="1" 
AR Path="/5881389D/58937D8A" Ref="C?"  Part="1" 
F 0 "C19" H 3785 4940 45  0000 L BNN
F 1 "100n" H 3500 4750 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 3755 5075 20  0001 C CNN
F 3 "" H 3725 4925 60  0001 C CNN
	1    3725 4925
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3725 5125 3725 5525
Wire Wire Line
	3725 4825 3725 4775
Wire Wire Line
	3725 4775 2600 4775
Connection ~ 2600 4775
Connection ~ 6500 3825
Text HLabel 6600 3825 2    60   Output ~ 0
V_Imotor0V
Text Notes 4650 5350 0    60   ~ 0
Ioc = 3.8V; sens = 151 mV/A;\n--> VOC = 0.574V
$Comp
L R R19
U 1 1 5894806D
P 1650 5350
F 0 "R19" V 1730 5350 50  0000 C CNN
F 1 "150E" V 1550 5350 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 1580 5350 50  0001 C CNN
F 3 "" H 1650 5350 50  0000 C CNN
	1    1650 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 5500 1650 5550
Wire Wire Line
	1650 5100 1650 5200
Wire Wire Line
	2550 5000 3000 5000
Wire Wire Line
	2550 5100 3000 5100
Text HLabel 3000 5000 2    60   Output ~ 0
ENCODER_1
Text HLabel 3000 5100 2    60   Output ~ 0
ENCODER_2
$Comp
L GND #PWR031
U 1 1 5894875C
P 2600 5550
F 0 "#PWR031" H 2600 5300 50  0001 C CNN
F 1 "GND" H 2600 5400 50  0000 C CNN
F 2 "" H 2600 5550 50  0000 C CNN
F 3 "" H 2600 5550 50  0000 C CNN
	1    2600 5550
	1    0    0    -1  
$EndComp
$Comp
L R R20
U 1 1 58948762
P 2600 5350
F 0 "R20" V 2680 5350 50  0000 C CNN
F 1 "150E" V 2500 5350 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 2530 5350 50  0001 C CNN
F 3 "" H 2600 5350 50  0000 C CNN
	1    2600 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 5500 2600 5550
Wire Wire Line
	2600 5100 2600 5200
$Comp
L GND #PWR032
U 1 1 589487BA
P 2850 5550
F 0 "#PWR032" H 2850 5300 50  0001 C CNN
F 1 "GND" H 2850 5400 50  0000 C CNN
F 2 "" H 2850 5550 50  0000 C CNN
F 3 "" H 2850 5550 50  0000 C CNN
	1    2850 5550
	1    0    0    -1  
$EndComp
$Comp
L R R21
U 1 1 589487C0
P 2850 5350
F 0 "R21" V 2930 5350 50  0000 C CNN
F 1 "150E" V 2750 5350 50  0000 C CNN
F 2 "Resistors_SMD:R_0603_HandSoldering" V 2780 5350 50  0001 C CNN
F 3 "" H 2850 5350 50  0000 C CNN
	1    2850 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 5500 2850 5550
Wire Wire Line
	2850 5200 2850 5000
Connection ~ 2850 5000
Connection ~ 2600 5100
$EndSCHEMATC
