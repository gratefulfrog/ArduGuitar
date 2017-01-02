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
EELAYER 26 0
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
L L L?
U 1 1 586A4FDA
P 2790 3130
F 0 "L?" H 2842 3175 50  0001 L CNN
F 1 "Pickup Coil" V 2740 2910 50  0000 L CNN
F 2 "" H 2790 3130 50  0000 C CNN
F 3 "" H 2790 3130 50  0000 C CNN
	1    2790 3130
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 586A50A6
P 3260 3280
F 0 "#PWR?" H 3260 3030 50  0001 C CNN
F 1 "GND" H 3265 3109 50  0001 C CNN
F 2 "" H 3260 3280 50  0000 C CNN
F 3 "" H 3260 3280 50  0000 C CNN
	1    3260 3280
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 586A526C
P 3040 3130
F 0 "R?" H 3110 3175 50  0001 L CNN
F 1 "500K" H 3110 3130 50  0000 L CNN
F 2 "" V 2970 3130 50  0000 C CNN
F 3 "" H 3040 3130 50  0000 C CNN
	1    3040 3130
	1    0    0    -1  
$EndComp
Wire Wire Line
	2790 3280 3260 3280
Connection ~ 3040 3280
Wire Wire Line
	2790 2980 3290 2980
Connection ~ 3040 2980
Text Label 3290 2980 0    60   ~ 0
AmpInput
Text Notes 3290 3250 0    60   ~ 0
<- What is the effect, if any,\n     of this resistor?
$EndSCHEMATC
