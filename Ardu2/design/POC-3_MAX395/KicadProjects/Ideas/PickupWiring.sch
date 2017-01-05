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
LIBS:PickupWiring-cache
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
L GND #PWR01
U 1 1 586A50A6
P 3260 3280
F 0 "#PWR01" H 3260 3030 50  0001 C CNN
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
	2790 3280 3040 3280
Wire Wire Line
	3040 3280 3260 3280
Connection ~ 3040 3280
Wire Wire Line
	2790 2980 3040 2980
Wire Wire Line
	3040 2980 3290 2980
Connection ~ 3040 2980
Text Label 3290 2980 0    60   ~ 0
AmpInput
Text Notes 3290 3250 0    60   ~ 0
<- What is the effect, if any,\n     of this resistor?
$Comp
L POT RV?
U 1 1 586CC04C
P 5410 2520
F 0 "RV?" V 5206 2520 50  0001 C CNN
F 1 "500K POT" V 5410 2620 50  0000 C CNN
F 2 "" H 5410 2520 50  0000 C CNN
F 3 "" H 5410 2520 50  0000 C CNN
	1    5410 2520
	0    1    1    0   
$EndComp
$Comp
L POT RV?
U 1 1 586CC096
P 5410 2920
F 0 "RV?" V 5296 2920 50  0001 C CNN
F 1 "500K POT" V 5410 2830 50  0000 C CNN
F 2 "" H 5410 2920 50  0000 C CNN
F 3 "" H 5410 2920 50  0000 C CNN
	1    5410 2920
	0    -1   -1   0   
$EndComp
$Comp
L L L?
U 1 1 586CC199
P 5120 2370
F 0 "L?" H 5172 2415 50  0001 L CNN
F 1 "Pickup" V 5060 2250 50  0000 L CNN
F 2 "" H 5120 2370 50  0000 C CNN
F 3 "" H 5120 2370 50  0000 C CNN
	1    5120 2370
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 586CC3DF
P 5560 3220
F 0 "#PWR02" H 5560 2970 50  0001 C CNN
F 1 "GND" H 5565 3049 50  0001 C CNN
F 2 "" H 5560 3220 50  0000 C CNN
F 3 "" H 5560 3220 50  0000 C CNN
	1    5560 3220
	1    0    0    -1  
$EndComp
Wire Wire Line
	5120 2520 5260 2520
Wire Wire Line
	5120 2920 5260 2920
Wire Wire Line
	5560 3220 5120 3220
Wire Wire Line
	5560 2220 5560 2520
Wire Wire Line
	5560 2520 5560 2920
Wire Wire Line
	5560 2920 5560 3220
Connection ~ 5560 3220
Connection ~ 5560 2920
Wire Wire Line
	5120 2220 5560 2220
Connection ~ 5560 2520
Wire Wire Line
	5410 2670 5410 2720
Wire Wire Line
	5410 2720 5410 2770
Connection ~ 5410 2720
Wire Wire Line
	5410 2720 5670 2720
Text Label 5670 2720 0    60   ~ 0
AmpInput
$Comp
L L L?
U 1 1 586CC632
P 5120 3070
F 0 "L?" H 5172 3115 50  0001 L CNN
F 1 "Pickup" V 5060 2950 50  0000 L CNN
F 2 "" H 5120 3070 50  0000 C CNN
F 3 "" H 5120 3070 50  0000 C CNN
	1    5120 3070
	1    0    0    -1  
$EndComp
$Comp
L POT RV?
U 1 1 586CC63D
P 5410 3590
F 0 "RV?" V 5206 3590 50  0001 C CNN
F 1 "500K POT" V 5410 3690 50  0000 C CNN
F 2 "" H 5410 3590 50  0000 C CNN
F 3 "" H 5410 3590 50  0000 C CNN
	1    5410 3590
	0    1    1    0   
$EndComp
$Comp
L POT RV?
U 1 1 586CC643
P 5410 3990
F 0 "RV?" V 5296 3990 50  0001 C CNN
F 1 "500K POT" V 5410 3900 50  0000 C CNN
F 2 "" H 5410 3990 50  0000 C CNN
F 3 "" H 5410 3990 50  0000 C CNN
	1    5410 3990
	0    -1   -1   0   
$EndComp
$Comp
L L L?
U 1 1 586CC649
P 5120 3590
F 0 "L?" H 5172 3635 50  0001 L CNN
F 1 "Pickup" V 5060 3470 50  0000 L CNN
F 2 "" H 5120 3590 50  0000 C CNN
F 3 "" H 5120 3590 50  0000 C CNN
	1    5120 3590
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 586CC64F
P 5260 4140
F 0 "#PWR03" H 5260 3890 50  0001 C CNN
F 1 "GND" H 5265 3969 50  0001 C CNN
F 2 "" H 5260 4140 50  0000 C CNN
F 3 "" H 5260 4140 50  0000 C CNN
	1    5260 4140
	1    0    0    -1  
$EndComp
Text Label 5670 3790 0    60   ~ 0
AmpInput
$Comp
L L L?
U 1 1 586CC661
P 5120 3990
F 0 "L?" H 5172 4035 50  0001 L CNN
F 1 "Pickup" V 5060 3870 50  0000 L CNN
F 2 "" H 5120 3990 50  0000 C CNN
F 3 "" H 5120 3990 50  0000 C CNN
	1    5120 3990
	1    0    0    -1  
$EndComp
Wire Wire Line
	5560 3590 5560 3790
Wire Wire Line
	5560 3790 5560 3990
Wire Wire Line
	5560 3790 5670 3790
Connection ~ 5560 3790
Wire Wire Line
	5120 3840 5410 3840
Wire Wire Line
	5120 3740 5410 3740
Wire Wire Line
	5120 3440 5260 3440
Connection ~ 5260 3990
Connection ~ 5260 3590
Wire Wire Line
	5260 3440 5260 3590
Wire Wire Line
	5260 3590 5260 3990
Wire Wire Line
	5260 4140 5260 4000
Wire Wire Line
	5120 4140 5260 4140
Text Notes 5780 2900 0    60   ~ 0
Standard configuration
Text Notes 5780 3970 0    60   ~ 0
Reversed Configuration
$EndSCHEMATC
