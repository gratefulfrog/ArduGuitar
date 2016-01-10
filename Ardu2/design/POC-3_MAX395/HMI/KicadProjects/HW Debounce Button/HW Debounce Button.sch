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
F 0 "SW1" V 3650 3090 50  0001 C CNN
F 1 "SW_PUSH" V 3500 2900 50  0001 C CNN
F 2 "" H 3500 2980 50  0000 C CNN
F 3 "" H 3500 2980 50  0000 C CNN
	1    3500 2980
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR01
U 1 1 566DB239
P 3740 3280
F 0 "#PWR01" H 3740 3030 50  0001 C CNN
F 1 "GND" H 3740 3130 50  0000 C CNN
F 2 "" H 3740 3280 50  0000 C CNN
F 3 "" H 3740 3280 50  0000 C CNN
	1    3740 3280
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR02
U 1 1 566DB25A
P 4160 2100
F 0 "#PWR02" H 4160 1950 50  0001 C CNN
F 1 "VCC" H 4160 2250 50  0000 C CNN
F 2 "" H 4160 2100 50  0000 C CNN
F 3 "" H 4160 2100 50  0000 C CNN
	1    4160 2100
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 566DB278
P 4160 2330
F 0 "R1" V 4240 2330 50  0001 C CNN
F 1 "40k" V 4160 2330 50  0000 C CNN
F 2 "" V 4090 2330 50  0000 C CNN
F 3 "" H 4160 2330 50  0000 C CNN
	1    4160 2330
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 566DB317
P 3720 2550
F 0 "R2" V 3800 2550 50  0001 C CNN
F 1 "1K" V 3720 2550 50  0000 C CNN
F 2 "" V 3650 2550 50  0000 C CNN
F 3 "" H 3720 2550 50  0000 C CNN
	1    3720 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	3500 2550 3570 2550
Wire Wire Line
	3500 3280 3950 3280
Connection ~ 3740 3280
Wire Wire Line
	3870 2550 4220 2550
Text GLabel 4220 2550 2    60   Input ~ 0
Pin
Wire Wire Line
	3950 2480 3950 2810
Connection ~ 3950 2550
$Comp
L CP1 C1
U 1 1 5675BF29
P 3950 2960
F 0 "C1" H 4065 3006 50  0001 L CNN
F 1 "1uF" H 4065 2960 50  0000 L CNN
F 2 "" H 3950 2960 50  0000 C CNN
F 3 "" H 3950 2960 50  0000 C CNN
	1    3950 2960
	1    0    0    -1  
$EndComp
Wire Wire Line
	4160 2100 4160 2180
Wire Wire Line
	4160 2480 4160 2550
Connection ~ 4160 2550
Wire Wire Line
	3500 2550 3500 2680
Wire Wire Line
	3950 3280 3950 3110
$Comp
L R R?
U 1 1 56929606
P 3950 2330
F 0 "R?" H 4020 2376 50  0001 L CNN
F 1 "47k" V 3950 2280 50  0000 L CNN
F 2 "" V 3880 2330 50  0000 C CNN
F 3 "" H 3950 2330 50  0000 C CNN
	1    3950 2330
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 2180 3950 2100
Wire Wire Line
	3950 2100 4160 2100
Wire Notes Line
	4060 2760 4060 1650
Wire Notes Line
	4060 1650 4710 1650
Wire Notes Line
	4710 1650 4710 2760
Wire Notes Line
	4710 2760 4060 2760
Text Notes 4200 1780 0    60   ~ 0
Pyboard
$EndSCHEMATC
