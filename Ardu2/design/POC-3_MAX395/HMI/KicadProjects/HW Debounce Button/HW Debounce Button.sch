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
L SW_PUSH SW?
U 1 1 566DB135
P 3500 2980
F 0 "SW?" V 3650 3090 50  0000 C CNN
F 1 "SW_PUSH" V 3500 2900 50  0001 C CNN
F 2 "" H 3500 2980 50  0000 C CNN
F 3 "" H 3500 2980 50  0000 C CNN
	1    3500 2980
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR?
U 1 1 566DB239
P 3740 3280
F 0 "#PWR?" H 3740 3030 50  0001 C CNN
F 1 "GND" H 3740 3130 50  0000 C CNN
F 2 "" H 3740 3280 50  0000 C CNN
F 3 "" H 3740 3280 50  0000 C CNN
	1    3740 3280
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR?
U 1 1 566DB25A
P 3500 2060
F 0 "#PWR?" H 3500 1910 50  0001 C CNN
F 1 "VCC" H 3500 2210 50  0000 C CNN
F 2 "" H 3500 2060 50  0000 C CNN
F 3 "" H 3500 2060 50  0000 C CNN
	1    3500 2060
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 566DB278
P 3500 2290
F 0 "R?" V 3580 2290 50  0001 C CNN
F 1 "40k" V 3500 2290 50  0000 C CNN
F 2 "" V 3430 2290 50  0000 C CNN
F 3 "" H 3500 2290 50  0000 C CNN
	1    3500 2290
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 566DB317
P 3720 2550
F 0 "R?" V 3800 2550 50  0001 C CNN
F 1 "10k" V 3720 2550 50  0000 C CNN
F 2 "" V 3650 2550 50  0000 C CNN
F 3 "" H 3720 2550 50  0000 C CNN
	1    3720 2550
	0    1    1    0   
$EndComp
$Comp
L C C?
U 1 1 566DB36E
P 3950 3130
F 0 "C?" H 3975 3230 50  0001 L CNN
F 1 "1µF" H 3975 3030 50  0000 L CNN
F 2 "" H 3988 2980 50  0000 C CNN
F 3 "" H 3950 3130 50  0000 C CNN
	1    3950 3130
	1    0    0    -1  
$EndComp
Wire Wire Line
	3500 2440 3500 2550
Wire Wire Line
	3500 2550 3500 2680
Wire Wire Line
	3570 2550 3500 2550
Connection ~ 3500 2550
Wire Wire Line
	3500 3280 3740 3280
Wire Wire Line
	3740 3280 3950 3280
Connection ~ 3740 3280
Wire Wire Line
	3870 2550 3950 2550
Wire Wire Line
	3950 2550 4220 2550
Text GLabel 4220 2550 2    60   Input ~ 0
Vout
Wire Wire Line
	3500 2060 3500 2140
Wire Wire Line
	3950 2980 3950 2550
Connection ~ 3950 2550
$EndSCHEMATC
