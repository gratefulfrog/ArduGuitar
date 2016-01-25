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
L SW_PUSH SW1
U 1 1 56A63E6D
P 4060 3290
F 0 "SW1" V 4050 3550 50  0000 R CNN
F 1 "SW_PUSH" V 4014 3236 50  0001 R CNN
F 2 "misc:AB2_PB_MOM_6MM_PTH_BLK" H 4060 3290 50  0001 C CNN
F 3 "" H 4060 3290 50  0000 C CNN
	1    4060 3290
	0    -1   -1   0   
$EndComp
$Comp
L SW_PUSH SW2
U 1 1 56A63ECB
P 4530 3290
F 0 "SW2" V 4530 3480 50  0000 C CNN
F 1 "SW_PUSH" H 4530 3190 50  0001 C CNN
F 2 "misc:AB2_PB_MOM_6MM_PTH_BLK" H 4530 3290 50  0001 C CNN
F 3 "" H 4530 3290 50  0000 C CNN
	1    4530 3290
	0    -1   -1   0   
$EndComp
$Comp
L CONN_01X03 P1
U 1 1 56A63F23
P 4950 3310
F 0 "P1" H 5028 3302 50  0000 L CNN
F 1 "CONN_01X03" H 5027 3256 50  0001 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 4950 3310 50  0001 C CNN
F 3 "" H 4950 3310 50  0000 C CNN
	1    4950 3310
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 56A64124
P 4750 3590
F 0 "#PWR01" H 4750 3340 50  0001 C CNN
F 1 "GND" H 4758 3416 50  0000 C CNN
F 2 "" H 4750 3590 50  0000 C CNN
F 3 "" H 4750 3590 50  0000 C CNN
	1    4750 3590
	1    0    0    -1  
$EndComp
Wire Wire Line
	4060 3590 4750 3590
Connection ~ 4530 3590
Wire Wire Line
	4750 3590 4750 3410
Wire Wire Line
	4750 3310 4690 3310
Wire Wire Line
	4690 3310 4690 2990
Wire Wire Line
	4690 2990 4530 2990
Wire Wire Line
	4750 2960 4750 3210
Wire Wire Line
	4750 2960 4060 2960
Wire Wire Line
	4060 2960 4060 2990
$EndSCHEMATC
