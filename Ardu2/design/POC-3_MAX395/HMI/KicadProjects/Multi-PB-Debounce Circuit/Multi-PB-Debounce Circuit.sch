EESchema Schematic File Version 2
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
LIBS:Multi-PB-Debounce Circuit-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L GND #PWR01
U 1 1 566DB239
P 7790 5100
F 0 "#PWR01" H 7790 4850 50  0001 C CNN
F 1 "GND" H 7790 4950 50  0000 C CNN
F 2 "" H 7790 5100 50  0000 C CNN
F 3 "" H 7790 5100 50  0000 C CNN
	1    7790 5100
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR02
U 1 1 566DB25A
P 7770 3920
F 0 "#PWR02" H 7770 3770 50  0001 C CNN
F 1 "VCC" H 7770 4070 50  0000 C CNN
F 2 "" H 7770 3920 50  0000 C CNN
F 3 "" H 7770 3920 50  0000 C CNN
	1    7770 3920
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 566DB317
P 7100 4370
F 0 "R2" V 6990 4380 50  0000 C CNN
F 1 "1K" V 7100 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7030 4370 50  0001 C CNN
F 3 "" H 7100 4370 50  0000 C CNN
	1    7100 4370
	0    1    1    0   
$EndComp
$Comp
L CP1 C1
U 1 1 5675BF29
P 7330 4780
F 0 "C1" H 7390 4650 50  0000 L CNN
F 1 "1uF" H 7445 4780 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 7330 4780 50  0001 C CNN
F 3 "" H 7330 4780 50  0000 C CNN
	1    7330 4780
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 56929606
P 7330 4150
F 0 "R3" H 7400 4196 50  0000 L CNN
F 1 "47k" V 7330 4100 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM15mm" V 7260 4150 50  0001 C CNN
F 3 "" H 7330 4150 50  0000 C CNN
	1    7330 4150
	1    0    0    -1  
$EndComp
Text Label 7430 4370 0    60   ~ 0
Pin5
$Comp
L R R11
U 1 1 56A5EECE
P 6210 4370
F 0 "R11" V 6100 4380 50  0000 C CNN
F 1 "1K" V 6210 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 6140 4370 50  0001 C CNN
F 3 "" H 6210 4370 50  0000 C CNN
	1    6210 4370
	0    1    1    0   
$EndComp
$Comp
L CP1 C6
U 1 1 56A5EEDC
P 6440 4780
F 0 "C6" H 6500 4650 50  0000 L CNN
F 1 "1uF" H 6555 4780 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 6440 4780 50  0001 C CNN
F 3 "" H 6440 4780 50  0000 C CNN
	1    6440 4780
	1    0    0    -1  
$EndComp
$Comp
L R R12
U 1 1 56A5EEE4
P 6440 4150
F 0 "R12" H 6510 4196 50  0000 L CNN
F 1 "47k" V 6440 4100 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM15mm" V 6370 4150 50  0001 C CNN
F 3 "" H 6440 4150 50  0000 C CNN
	1    6440 4150
	1    0    0    -1  
$EndComp
Text Label 6540 4370 0    60   ~ 0
Pin4
$Comp
L R R9
U 1 1 56A60210
P 5290 4370
F 0 "R9" V 5180 4380 50  0000 C CNN
F 1 "1K" V 5290 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 5220 4370 50  0001 C CNN
F 3 "" H 5290 4370 50  0000 C CNN
	1    5290 4370
	0    1    1    0   
$EndComp
$Comp
L CP1 C5
U 1 1 56A6021E
P 5520 4780
F 0 "C5" H 5580 4650 50  0000 L CNN
F 1 "1uF" H 5635 4780 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 5520 4780 50  0001 C CNN
F 3 "" H 5520 4780 50  0000 C CNN
	1    5520 4780
	1    0    0    -1  
$EndComp
$Comp
L R R10
U 1 1 56A60226
P 5520 4150
F 0 "R10" H 5590 4196 50  0000 L CNN
F 1 "47k" V 5520 4100 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM15mm" V 5450 4150 50  0001 C CNN
F 3 "" H 5520 4150 50  0000 C CNN
	1    5520 4150
	1    0    0    -1  
$EndComp
Text Label 5620 4370 0    60   ~ 0
Pin3
$Comp
L R R7
U 1 1 56A60232
P 4400 4370
F 0 "R7" V 4290 4380 50  0000 C CNN
F 1 "1K" V 4400 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 4330 4370 50  0001 C CNN
F 3 "" H 4400 4370 50  0000 C CNN
	1    4400 4370
	0    1    1    0   
$EndComp
$Comp
L CP1 C4
U 1 1 56A60240
P 4630 4780
F 0 "C4" H 4690 4650 50  0000 L CNN
F 1 "1uF" H 4745 4780 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 4630 4780 50  0001 C CNN
F 3 "" H 4630 4780 50  0000 C CNN
	1    4630 4780
	1    0    0    -1  
$EndComp
$Comp
L R R8
U 1 1 56A60248
P 4630 4150
F 0 "R8" H 4700 4196 50  0000 L CNN
F 1 "47k" V 4630 4100 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM15mm" V 4560 4150 50  0001 C CNN
F 3 "" H 4630 4150 50  0000 C CNN
	1    4630 4150
	1    0    0    -1  
$EndComp
Text Label 4730 4370 0    60   ~ 0
Pin2
$Comp
L R R5
U 1 1 56A60E6E
P 3470 4370
F 0 "R5" V 3360 4380 50  0000 C CNN
F 1 "1K" V 3470 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3400 4370 50  0001 C CNN
F 3 "" H 3470 4370 50  0000 C CNN
	1    3470 4370
	0    1    1    0   
$EndComp
$Comp
L CP1 C3
U 1 1 56A60E7C
P 3700 4780
F 0 "C3" H 3760 4650 50  0000 L CNN
F 1 "1uF" H 3815 4780 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 3700 4780 50  0001 C CNN
F 3 "" H 3700 4780 50  0000 C CNN
	1    3700 4780
	1    0    0    -1  
$EndComp
$Comp
L R R6
U 1 1 56A60E84
P 3700 4150
F 0 "R6" H 3770 4196 50  0000 L CNN
F 1 "47k" V 3700 4100 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM15mm" V 3630 4150 50  0001 C CNN
F 3 "" H 3700 4150 50  0000 C CNN
	1    3700 4150
	1    0    0    -1  
$EndComp
Text Label 3800 4370 0    60   ~ 0
Pin1
$Comp
L R R1
U 1 1 56A60E90
P 2580 4370
F 0 "R1" V 2470 4380 50  0000 C CNN
F 1 "1K" V 2580 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 2510 4370 50  0001 C CNN
F 3 "" H 2580 4370 50  0000 C CNN
	1    2580 4370
	0    1    1    0   
$EndComp
$Comp
L CP1 C2
U 1 1 56A60E9E
P 2810 4780
F 0 "C2" H 2870 4650 50  0000 L CNN
F 1 "1uF" H 2925 4780 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 2810 4780 50  0001 C CNN
F 3 "" H 2810 4780 50  0000 C CNN
	1    2810 4780
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 56A60EA6
P 2810 4150
F 0 "R4" H 2880 4196 50  0000 L CNN
F 1 "47k" V 2810 4100 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM15mm" V 2740 4150 50  0001 C CNN
F 3 "" H 2810 4150 50  0000 C CNN
	1    2810 4150
	1    0    0    -1  
$EndComp
Text Label 2910 4370 0    60   ~ 0
Pin0
Wire Wire Line
	6880 4370 6950 4370
Wire Wire Line
	7330 4300 7330 4630
Connection ~ 7330 4370
Wire Wire Line
	6880 4370 6880 4500
Wire Wire Line
	7330 5100 7330 4930
Wire Wire Line
	7330 3920 7330 4000
Wire Wire Line
	7250 4370 7430 4370
Connection ~ 7330 5100
Connection ~ 7770 3920
Wire Wire Line
	5990 4370 6060 4370
Wire Wire Line
	2810 5100 7790 5100
Wire Wire Line
	6440 4300 6440 4630
Connection ~ 6440 4370
Wire Wire Line
	5990 4370 5990 4500
Wire Wire Line
	6440 5100 6440 4930
Wire Wire Line
	6440 4000 6440 3920
Wire Wire Line
	2810 3920 7770 3920
Wire Wire Line
	6360 4370 6540 4370
Connection ~ 6440 5100
Wire Wire Line
	5070 4370 5140 4370
Wire Wire Line
	5520 4300 5520 4630
Connection ~ 5520 4370
Wire Wire Line
	5070 4370 5070 4500
Wire Wire Line
	5520 4930 5520 5100
Wire Wire Line
	5520 4000 5520 3920
Wire Wire Line
	5440 4370 5620 4370
Connection ~ 5520 5100
Wire Wire Line
	4180 4370 4250 4370
Wire Wire Line
	4630 4300 4630 4630
Connection ~ 4630 4370
Wire Wire Line
	4180 4370 4180 4500
Wire Wire Line
	4630 5100 4630 4930
Wire Wire Line
	4630 4000 4630 3920
Wire Wire Line
	4550 4370 4730 4370
Connection ~ 4630 5100
Wire Wire Line
	3250 4370 3320 4370
Wire Wire Line
	3700 4300 3700 4630
Connection ~ 3700 4370
Wire Wire Line
	3250 4370 3250 4500
Wire Wire Line
	3700 4000 3700 3920
Wire Wire Line
	3620 4370 3800 4370
Wire Wire Line
	2360 4370 2430 4370
Wire Wire Line
	2810 4300 2810 4630
Connection ~ 2810 4370
Wire Wire Line
	2360 4370 2360 4500
Wire Wire Line
	2810 5100 2810 4930
Wire Wire Line
	2810 4000 2810 3920
Wire Wire Line
	2730 4370 2910 4370
Connection ~ 7330 3920
Connection ~ 6440 3920
Connection ~ 5520 3920
Connection ~ 4630 3920
Connection ~ 3700 3920
Text Label 2360 4500 2    60   ~ 0
SW0
Text Label 3250 4500 2    60   ~ 0
SW1
Text Label 4180 4500 2    60   ~ 0
SW2
Text Label 5070 4500 2    60   ~ 0
SW3
Text Label 5990 4500 2    60   ~ 0
SW4
Text Label 6880 4500 2    60   ~ 0
SW5
Wire Wire Line
	3700 4930 3700 5100
Connection ~ 3700 5100
$Comp
L CONN_01X08 P1
U 1 1 56A64475
P 3310 3080
F 0 "P1" H 3387 3118 50  0000 L CNN
F 1 "CONN_01X08" H 3387 3026 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x08" H 3310 3080 50  0001 C CNN
F 3 "" H 3310 3080 50  0000 C CNN
	1    3310 3080
	1    0    0    -1  
$EndComp
Text Label 3110 2730 2    60   ~ 0
GND
Text Label 3110 3430 2    60   ~ 0
VCC
Text Label 3110 2830 2    60   ~ 0
Pin0
Text Label 3110 2930 2    60   ~ 0
Pin1
Text Label 3110 3030 2    60   ~ 0
Pin2
Text Label 3110 3130 2    60   ~ 0
Pin3
Text Label 3110 3230 2    60   ~ 0
Pin4
Text Label 3110 3330 2    60   ~ 0
Pin5
Text Notes 3580 2520 2    60   ~ 0
Inputs from Pyboard
$Comp
L CONN_01X06 P2
U 1 1 56A64C07
P 4760 3040
F 0 "P2" H 4837 3078 50  0000 L CNN
F 1 "CONN_01X06" H 4837 2986 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x06" H 4760 3040 50  0001 C CNN
F 3 "" H 4760 3040 50  0000 C CNN
	1    4760 3040
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X06 P3
U 1 1 56A64C9B
P 5600 3040
F 0 "P3" H 5677 3078 50  0000 L CNN
F 1 "CONN_01X06" H 5677 2986 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x06" H 5600 3040 50  0001 C CNN
F 3 "" H 5600 3040 50  0000 C CNN
	1    5600 3040
	1    0    0    -1  
$EndComp
Text Label 4560 2790 2    60   ~ 0
SW0
Text Label 4560 2890 2    60   ~ 0
SW1
Text Label 4560 2990 2    60   ~ 0
SW2
Text Label 4560 3090 2    60   ~ 0
SW3
Text Label 4560 3190 2    60   ~ 0
SW4
Text Label 4560 3290 2    60   ~ 0
SW5
Text Label 5400 2790 2    60   ~ 0
GND
Text Label 5400 2890 2    60   ~ 0
GND
Text Label 5400 2990 2    60   ~ 0
GND
Text Label 5400 3090 2    60   ~ 0
GND
Text Label 5400 3190 2    60   ~ 0
GND
Text Label 5400 3290 2    60   ~ 0
GND
$EndSCHEMATC
