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
L CONN_01X10 P1
U 1 1 574B54BE
P 2640 2510
F 0 "P1" H 2716 2549 50  0000 L CNN
F 1 "GND" H 2716 2463 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x10" H 2640 2510 50  0001 C CNN
F 3 "" H 2640 2510 50  0000 C CNN
	1    2640 2510
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X10 P2
U 1 1 574B5546
P 2640 3610
F 0 "P2" H 2716 3649 50  0000 L CNN
F 1 "GND" H 2716 3563 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x10" H 2640 3610 50  0001 C CNN
F 3 "" H 2640 3610 50  0000 C CNN
	1    2640 3610
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X10 P3
U 1 1 574B5696
P 4040 3110
F 0 "P3" H 4116 3149 50  0000 L CNN
F 1 "Wiper" H 4116 3063 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x10" H 4040 3110 50  0001 C CNN
F 3 "" H 4040 3110 50  0000 C CNN
	1    4040 3110
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X10 P4
U 1 1 574B5838
P 4410 3110
F 0 "P4" H 4486 3149 50  0000 L CNN
F 1 "Wiper" H 4486 3063 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x10" H 4410 3110 50  0001 C CNN
F 3 "" H 4410 3110 50  0000 C CNN
	1    4410 3110
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X10 P5
U 1 1 574B5892
P 5410 3120
F 0 "P5" H 5486 3159 50  0000 L CNN
F 1 "3.3v" H 5486 3073 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x10" H 5410 3120 50  0001 C CNN
F 3 "" H 5410 3120 50  0000 C CNN
	1    5410 3120
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X10 P6
U 1 1 574B5909
P 5970 3100
F 0 "P6" H 6046 3139 50  0000 L CNN
F 1 "5v" H 6046 3053 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x10" H 5970 3100 50  0001 C CNN
F 3 "" H 5970 3100 50  0000 C CNN
	1    5970 3100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 574B59A5
P 2980 4110
F 0 "#PWR01" H 2980 3860 50  0001 C CNN
F 1 "GND" H 2984 3942 50  0000 C CNN
F 2 "" H 2980 4110 50  0000 C CNN
F 3 "" H 2980 4110 50  0000 C CNN
	1    2980 4110
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 574B59D1
P 3570 2660
F 0 "R1" V 3371 2660 50  0000 C CNN
F 1 "10K" V 3457 2660 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 2660 50  0001 C CNN
F 3 "" H 3570 2660 50  0000 C CNN
	1    3570 2660
	0    1    1    0   
$EndComp
$Comp
L R R2
U 1 1 574B5BBD
P 3570 2760
F 0 "R2" V 3371 2760 50  0000 C CNN
F 1 "10K" V 3457 2760 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 2760 50  0001 C CNN
F 3 "" H 3570 2760 50  0000 C CNN
	1    3570 2760
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 574B5C0B
P 3570 2860
F 0 "R3" V 3371 2860 50  0000 C CNN
F 1 "10K" V 3457 2860 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 2860 50  0001 C CNN
F 3 "" H 3570 2860 50  0000 C CNN
	1    3570 2860
	0    1    1    0   
$EndComp
$Comp
L R R4
U 1 1 574B5E4B
P 3570 2960
F 0 "R4" V 3371 2960 50  0000 C CNN
F 1 "10K" V 3457 2960 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 2960 50  0001 C CNN
F 3 "" H 3570 2960 50  0000 C CNN
	1    3570 2960
	0    1    1    0   
$EndComp
$Comp
L R R5
U 1 1 574B5EAF
P 3570 3060
F 0 "R5" V 3371 3060 50  0000 C CNN
F 1 "10K" V 3457 3060 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 3060 50  0001 C CNN
F 3 "" H 3570 3060 50  0000 C CNN
	1    3570 3060
	0    1    1    0   
$EndComp
$Comp
L R R6
U 1 1 574B5F1A
P 3570 3160
F 0 "R6" V 3371 3160 50  0000 C CNN
F 1 "10K" V 3457 3160 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 3160 50  0001 C CNN
F 3 "" H 3570 3160 50  0000 C CNN
	1    3570 3160
	0    1    1    0   
$EndComp
$Comp
L R R7
U 1 1 574B5F6A
P 3570 3260
F 0 "R7" V 3371 3260 50  0000 C CNN
F 1 "10K" V 3457 3260 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 3260 50  0001 C CNN
F 3 "" H 3570 3260 50  0000 C CNN
	1    3570 3260
	0    1    1    0   
$EndComp
$Comp
L R R8
U 1 1 574B5FC3
P 3570 3360
F 0 "R8" V 3371 3360 50  0000 C CNN
F 1 "10K" V 3457 3360 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 3360 50  0001 C CNN
F 3 "" H 3570 3360 50  0000 C CNN
	1    3570 3360
	0    1    1    0   
$EndComp
$Comp
L R R9
U 1 1 574B6025
P 3570 3460
F 0 "R9" V 3371 3460 50  0000 C CNN
F 1 "10K" V 3457 3460 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 3460 50  0001 C CNN
F 3 "" H 3570 3460 50  0000 C CNN
	1    3570 3460
	0    1    1    0   
$EndComp
$Comp
L R R10
U 1 1 574B607E
P 3570 3560
F 0 "R10" V 3371 3560 50  0000 C CNN
F 1 "10K" V 3457 3560 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3500 3560 50  0001 C CNN
F 3 "" H 3570 3560 50  0000 C CNN
	1    3570 3560
	0    1    1    0   
$EndComp
$Comp
L +3.3V #PWR02
U 1 1 574B768C
P 5210 2400
F 0 "#PWR02" H 5210 2250 50  0001 C CNN
F 1 "+3.3V" H 5224 2569 50  0000 C CNN
F 2 "" H 5210 2400 50  0000 C CNN
F 3 "" H 5210 2400 50  0000 C CNN
	1    5210 2400
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR03
U 1 1 574B7975
P 5770 2400
F 0 "#PWR03" H 5770 2250 50  0001 C CNN
F 1 "+5V" H 5784 2569 50  0000 C CNN
F 2 "" H 5770 2400 50  0000 C CNN
F 3 "" H 5770 2400 50  0000 C CNN
	1    5770 2400
	1    0    0    -1  
$EndComp
Wire Wire Line
	2440 2060 2440 4110
Connection ~ 2440 2160
Connection ~ 2440 2260
Connection ~ 2440 2360
Connection ~ 2440 2460
Connection ~ 2440 2560
Connection ~ 2440 2660
Connection ~ 2440 2760
Connection ~ 2440 2860
Connection ~ 2440 2960
Connection ~ 2440 3160
Connection ~ 2440 3260
Connection ~ 2440 3360
Connection ~ 2440 3460
Connection ~ 2440 3560
Connection ~ 2440 3660
Connection ~ 2440 3760
Connection ~ 2440 3860
Connection ~ 2440 3960
Wire Wire Line
	2440 4110 3420 4110
Connection ~ 2440 4060
Wire Wire Line
	3420 4110 3420 2660
Connection ~ 3420 2760
Connection ~ 3420 2860
Connection ~ 3420 2960
Connection ~ 3420 3060
Connection ~ 3420 3160
Connection ~ 3420 3260
Connection ~ 3420 3360
Connection ~ 3420 3460
Connection ~ 2980 4110
Connection ~ 3420 3560
Wire Wire Line
	3720 2660 4210 2660
Wire Wire Line
	3720 2760 4210 2760
Wire Wire Line
	3720 2860 4210 2860
Wire Wire Line
	3720 2960 4210 2960
Wire Wire Line
	3720 3460 4210 3460
Wire Wire Line
	3720 3360 4210 3360
Wire Wire Line
	3720 3260 4210 3260
Wire Wire Line
	3720 3160 4210 3160
Wire Wire Line
	3720 3060 4210 3060
Wire Wire Line
	3720 3560 4210 3560
Connection ~ 3840 2660
Connection ~ 3840 2760
Connection ~ 3840 2860
Connection ~ 3840 2960
Connection ~ 3840 3060
Connection ~ 3840 3160
Connection ~ 3840 3260
Connection ~ 3840 3360
Connection ~ 3840 3460
Connection ~ 3840 3560
Wire Wire Line
	5770 2400 5770 3550
Connection ~ 5770 2650
Connection ~ 5770 2750
Connection ~ 5770 2850
Connection ~ 5770 2950
Connection ~ 5770 3050
Connection ~ 5770 3150
Connection ~ 5770 3250
Connection ~ 5770 3350
Connection ~ 5770 3450
Wire Wire Line
	5210 2400 5210 3570
Connection ~ 5210 2670
Connection ~ 5210 2770
Connection ~ 5210 2870
Connection ~ 5210 2970
Connection ~ 5210 3070
Connection ~ 5210 3170
Connection ~ 5210 3270
Connection ~ 5210 3370
Connection ~ 5210 3470
$EndSCHEMATC
