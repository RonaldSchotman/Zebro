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
Sheet 2 6
Title "Motor Driver"
Date "2017-01-19"
Rev "0"
Comp "Zebro"
Comment1 "Lisanne Kesselaar"
Comment2 "Concept Version 0.1"
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L DRV8871 U1
U 1 1 5886681D
P 6375 3775
F 0 "U1" H 6375 4225 60  0000 C CNN
F 1 "DRV8871" H 6425 3325 60  0000 C CNN
F 2 "Housings_SOIC:SOIC-8-1EP_3.9x4.9mm_Pitch1.27mm" H 6375 3875 60  0001 C CNN
F 3 "" H 6375 3875 60  0001 C CNN
	1    6375 3775
	1    0    0    -1  
$EndComp
Text HLabel 5825 3675 0    60   Input ~ 0
PWM1
Text HLabel 5825 3775 0    60   Input ~ 0
PWM2
$Comp
L C-EUC0603 C?
U 1 1 58866C8E
P 5450 3950
AR Path="/58866C8E" Ref="C?"  Part="1" 
AR Path="/58813887/58866C8E" Ref="C2"  Part="1" 
F 0 "C2" H 5510 3965 45  0000 L BNN
F 1 "1u" H 5510 3765 45  0000 L BNN
F 2 "Capacitors_SMD:C_0603" H 5480 4100 20  0001 C CNN
F 3 "" H 5450 3950 60  0001 C CNN
	1    5450 3950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 58866DBA
P 5825 4375
F 0 "#PWR01" H 5825 4125 50  0001 C CNN
F 1 "GND" H 5825 4225 50  0000 C CNN
F 2 "" H 5825 4375 50  0000 C CNN
F 3 "" H 5825 4375 50  0000 C CNN
	1    5825 4375
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 58866E99
P 5450 4375
F 0 "#PWR02" H 5450 4125 50  0001 C CNN
F 1 "GND" H 5450 4225 50  0000 C CNN
F 2 "" H 5450 4375 50  0000 C CNN
F 3 "" H 5450 4375 50  0000 C CNN
	1    5450 4375
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 58866F11
P 5250 4375
F 0 "#PWR03" H 5250 4125 50  0001 C CNN
F 1 "GND" H 5250 4225 50  0000 C CNN
F 2 "" H 5250 4375 50  0000 C CNN
F 3 "" H 5250 4375 50  0000 C CNN
	1    5250 4375
	1    0    0    -1  
$EndComp
$Comp
L CPOL-US C1
U 1 1 58866F32
P 5250 3950
F 0 "C1" H 5075 4000 45  0000 L BNN
F 1 "22u" H 4900 3775 45  0000 L BNN
F 2 "Capacitors_SMD:CP_Elec_5x5.3" H 5280 4100 20  0001 C CNN
F 3 "" H 5250 3950 60  0001 C CNN
	1    5250 3950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 58867435
P 6925 4375
F 0 "#PWR04" H 6925 4125 50  0001 C CNN
F 1 "GND" H 6925 4225 50  0000 C CNN
F 2 "" H 6925 4375 50  0000 C CNN
F 3 "" H 6925 4375 50  0000 C CNN
	1    6925 4375
	1    0    0    -1  
$EndComp
$Comp
L R-EU_R0603 R1
U 1 1 5886750D
P 6925 4125
F 0 "R1" H 6825 4175 45  0000 L BNN
F 1 "16.9k" H 6825 4025 45  0000 L BNN
F 2 "Resistors_SMD:R_0603_HandSoldering" H 6955 4275 20  0001 C CNN
F 3 "" H 6925 4125 60  0001 C CNN
	1    6925 4125
	0    1    -1   0   
$EndComp
Text HLabel 6975 3625 2    60   Output ~ 0
M1
Text HLabel 6975 3725 2    60   Output ~ 0
M2_S
Wire Wire Line
	5925 3925 5825 3925
Wire Wire Line
	5825 3925 5825 4375
Wire Wire Line
	5925 4025 5825 4025
Connection ~ 5825 4025
Wire Wire Line
	5925 3775 5825 3775
Wire Wire Line
	5925 3675 5825 3675
Wire Wire Line
	5250 3525 5925 3525
Wire Wire Line
	5250 3375 5250 3850
Connection ~ 5250 3525
Wire Wire Line
	5450 3525 5450 3850
Connection ~ 5450 3525
Wire Wire Line
	5450 4375 5450 4150
Wire Wire Line
	5250 4150 5250 4375
Wire Wire Line
	6825 3625 6975 3625
Wire Wire Line
	6825 3875 6925 3875
Wire Wire Line
	6925 3875 6925 3925
Wire Wire Line
	6925 4375 6925 4325
Wire Notes Line
	8375 2150 8375 5050
Wire Notes Line
	8375 5050 4175 5050
Wire Notes Line
	4175 5050 4175 2150
Text Notes 5700 2375 0    60   ~ 0
Motor Driver V1
Text Notes 4275 5300 0    60   ~ 0
Imax (A) = Vilm(kV)/Rilm(kOhm) --> Rilm(kOhm)=64(kV)/3.8(A)=16.8(kOhm)\nClosest realisic value is 16.9 --> Imax 3.79A
Wire Notes Line
	4175 2150 8375 2150
$Comp
L VPP #PWR05
U 1 1 589175ED
P 5250 3375
F 0 "#PWR05" H 5250 3225 50  0001 C CNN
F 1 "VPP" H 5250 3525 50  0000 C CNN
F 2 "" H 5250 3375 50  0000 C CNN
F 3 "" H 5250 3375 50  0000 C CNN
	1    5250 3375
	1    0    0    -1  
$EndComp
Wire Wire Line
	6975 3725 6825 3725
Wire Notes Line
	8375 2550 4175 2550
Wire Wire Line
	5925 4125 5825 4125
Connection ~ 5825 4125
$EndSCHEMATC
