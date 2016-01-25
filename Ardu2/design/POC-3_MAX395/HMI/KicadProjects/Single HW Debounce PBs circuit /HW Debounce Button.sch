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
LIBS:HW Debounce Button-cache
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
L SW_PUSH SW1
U 1 1 566DB135
P 3500 2980
F 0 "SW1" V 3500 3160 50  0000 C CNN
F 1 "SW_PUSH" V 3500 2900 50  0001 C CNN
F 2 "misc:AB2_PB_MOM_6MM_PTH_BLK" H 3500 2980 50  0001 C CNN
F 3 "" H 3500 2980 50  0000 C CNN
	1    3500 2980
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR01
U 1 1 566DB239
P 4410 3280
F 0 "#PWR01" H 4410 3030 50  0001 C CNN
F 1 "GND" H 4410 3130 50  0000 C CNN
F 2 "" H 4410 3280 50  0000 C CNN
F 3 "" H 4410 3280 50  0000 C CNN
	1    4410 3280
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR02
U 1 1 566DB25A
P 4390 2100
F 0 "#PWR02" H 4390 1950 50  0001 C CNN
F 1 "VCC" H 4390 2250 50  0000 C CNN
F 2 "" H 4390 2100 50  0000 C CNN
F 3 "" H 4390 2100 50  0000 C CNN
	1    4390 2100
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 566DB317
P 3720 2550
F 0 "R2" V 3610 2560 50  0000 C CNN
F 1 "1K" V 3720 2550 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3650 2550 50  0001 C CNN
F 3 "" H 3720 2550 50  0000 C CNN
	1    3720 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	3500 2550 3570 2550
Wire Wire Line
	3500 3280 3950 3280
Wire Wire Line
	3950 3280 4410 3280
Wire Wire Line
	4410 3280 3950 3280
Wire Wire Line
	3950 3280 4410 3280
Wire Wire Line
	4410 3280 4790 3280
Wire Wire Line
	4790 3280 5240 3280
Connection ~ 4410 3280
Wire Wire Line
	3950 2480 3950 2550
Wire Wire Line
	3950 2550 3950 2810
Connection ~ 3950 2550
$Comp
L CP1 C1
U 1 1 5675BF29
P 3950 2960
F 0 "C1" H 4010 2830 50  0000 L CNN
F 1 "1uF" H 4065 2960 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 3950 2960 50  0001 C CNN
F 3 "" H 3950 2960 50  0000 C CNN
	1    3950 2960
	1    0    0    -1  
$EndComp
Wire Wire Line
	3500 2550 3500 2680
Wire Wire Line
	3950 3280 3950 3110
$Comp
L R R3
U 1 1 56929606
P 3950 2330
F 0 "R3" H 4020 2376 50  0000 L CNN
F 1 "47k" V 3950 2280 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 3880 2330 50  0001 C CNN
F 3 "" H 3950 2330 50  0000 C CNN
	1    3950 2330
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 2180 3950 2100
Wire Wire Line
	3950 2100 4390 2100
Wire Wire Line
	4390 2100 5240 2100
Text Notes 3360 3660 0    60   ~ 0
Measured Switch Pin Spacing: 4.535 x 6.42mm
Wire Wire Line
	3870 2550 3950 2550
Wire Wire Line
	3950 2550 4050 2550
Text Label 4050 2550 0    60   ~ 0
Pin1
$Comp
L SW_PUSH SW2
U 1 1 56A4BAC7
P 4790 2980
F 0 "SW2" V 4790 3180 50  0000 C CNN
F 1 "SW_PUSH" V 4790 2900 50  0001 C CNN
F 2 "misc:AB2_PB_MOM_6MM_PTH_BLK" H 4790 2980 50  0001 C CNN
F 3 "" H 4790 2980 50  0000 C CNN
	1    4790 2980
	0    -1   -1   0   
$EndComp
$Comp
L R R1
U 1 1 56A4BAD3
P 5010 2550
F 0 "R1" V 4910 2560 50  0000 C CNN
F 1 "1K" V 5010 2550 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 4940 2550 50  0001 C CNN
F 3 "" H 5010 2550 50  0000 C CNN
	1    5010 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	4790 2550 4860 2550
Wire Wire Line
	5240 2480 5240 2550
Wire Wire Line
	5240 2550 5240 2810
Connection ~ 5240 2550
$Comp
L CP1 C2
U 1 1 56A4BADC
P 5240 2960
F 0 "C2" H 5280 2840 50  0000 L CNN
F 1 "1uF" H 5355 2960 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Radial_D5_L11_P2" H 5240 2960 50  0001 C CNN
F 3 "" H 5240 2960 50  0000 C CNN
	1    5240 2960
	1    0    0    -1  
$EndComp
Wire Wire Line
	4790 2550 4790 2680
Wire Wire Line
	5240 3280 5240 3110
$Comp
L R R4
U 1 1 56A4BAE4
P 5240 2330
F 0 "R4" H 5310 2376 50  0000 L CNN
F 1 "47k" V 5240 2280 50  0000 L CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 5170 2330 50  0001 C CNN
F 3 "" H 5240 2330 50  0000 C CNN
	1    5240 2330
	1    0    0    -1  
$EndComp
Wire Wire Line
	5240 2100 5240 2180
Wire Wire Line
	5160 2550 5240 2550
Wire Wire Line
	5240 2550 5340 2550
Text Label 5340 2550 0    60   ~ 0
Pin2
Connection ~ 3950 3280
Connection ~ 4790 3280
Connection ~ 4390 2100
Text Label 5940 3090 2    60   ~ 0
GND
Text Label 5940 2990 2    60   ~ 0
VCC
Text Label 5940 2870 2    60   ~ 0
Pin2
Text Label 5940 2770 2    60   ~ 0
Pin1
$Comp
L CONN_01X02 P2
U 1 1 56A4C5E0
P 6140 3040
F 0 "P2" H 6217 3032 50  0000 L CNN
F 1 "CONN_01X02" H 6217 2986 50  0001 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 6140 3040 50  0001 C CNN
F 3 "" H 6140 3040 50  0000 C CNN
	1    6140 3040
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P3
U 1 1 56A4C6E2
P 6140 3250
F 0 "P3" H 6217 3242 50  0000 L CNN
F 1 "CONN_01X02" H 6217 3196 50  0001 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 6140 3250 50  0001 C CNN
F 3 "" H 6140 3250 50  0000 C CNN
	1    6140 3250
	1    0    0    -1  
$EndComp
Text Label 5940 3200 2    60   ~ 0
VCC
Text Label 5940 3300 2    60   ~ 0
GND
$Comp
L CONN_01X02 P1
U 1 1 56A4C82A
P 6140 2820
F 0 "P1" H 6217 2812 50  0000 L CNN
F 1 "CONN_01X02" H 6217 2766 50  0001 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 6140 2820 50  0001 C CNN
F 3 "" H 6140 2820 50  0000 C CNN
	1    6140 2820
	1    0    0    -1  
$EndComp
$EndSCHEMATC
