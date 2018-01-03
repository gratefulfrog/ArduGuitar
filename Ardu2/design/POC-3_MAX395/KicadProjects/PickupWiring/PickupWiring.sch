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
LIBS:MiscellaneousDevices
LIBS:switches
LIBS:switch-misc
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
L POT RV2
U 1 1 586CC096
P 5320 1880
F 0 "RV2" V 5206 1880 50  0001 C CNN
F 1 "500K Tone POT" V 5420 2220 50  0000 C CNN
F 2 "" H 5320 1880 50  0000 C CNN
F 3 "" H 5320 1880 50  0000 C CNN
	1    5320 1880
	0    1    -1   0   
$EndComp
Text Label 6190 2470 2    60   ~ 0
Amp_Input
$Comp
L SWITCH_SPDT SW9
U 1 1 586F8075
P 5150 3440
F 0 "SW9" V 5150 3722 50  0001 C CNN
F 1 "SWITCH_SPDT" H 5150 3633 50  0001 C CNN
F 2 "" H 5150 3440 60  0000 C CNN
F 3 "" H 5150 3440 60  0000 C CNN
	1    5150 3440
	0    1    1    0   
$EndComp
$Comp
L L L1
U 1 1 586FBCEB
P 2760 1800
F 0 "L1" H 2812 1845 50  0001 L CNN
F 1 "A: (N1) Neck-North_screws" V 2600 1490 50  0000 L CNN
F 2 "" H 2760 1800 50  0000 C CNN
F 3 "" H 2760 1800 50  0000 C CNN
	1    2760 1800
	0    1    1    0   
$EndComp
$Comp
L L L2
U 1 1 586FBCFA
P 2760 1960
F 0 "L2" H 2812 2005 50  0001 L CNN
F 1 "B: (N2) Neck-South_no_screws" V 2860 1590 50  0000 L CNN
F 2 "" H 2760 1960 50  0000 C CNN
F 3 "" H 2760 1960 50  0000 C CNN
	1    2760 1960
	0    1    1    0   
$EndComp
Text Label 2610 1800 2    60   ~ 0
N-Red
Text Label 2910 1800 0    60   ~ 0
N-White
Text Label 2910 1960 0    60   ~ 0
N-Black
Text Label 2610 1960 2    60   ~ 0
N-Green
$Comp
L L L3
U 1 1 586FBD88
P 2800 2530
F 0 "L3" H 2852 2575 50  0001 L CNN
F 1 "C: (B1) Bridge-North_no_screws" V 2630 2110 50  0000 L CNN
F 2 "" H 2800 2530 50  0000 C CNN
F 3 "" H 2800 2530 50  0000 C CNN
	1    2800 2530
	0    1    1    0   
$EndComp
$Comp
L L L4
U 1 1 586FBD8E
P 2800 2690
F 0 "L4" H 2852 2735 50  0001 L CNN
F 1 "D: (B2) Bridge-South_screws" V 2890 2300 50  0000 L CNN
F 2 "" H 2800 2690 50  0000 C CNN
F 3 "" H 2800 2690 50  0000 C CNN
	1    2800 2690
	0    1    1    0   
$EndComp
Text Label 2650 2530 2    60   ~ 0
B-Red
Text Label 2950 2530 0    60   ~ 0
B-White
Text Label 2950 2690 0    60   ~ 0
B-Black
Text Label 2650 2690 2    60   ~ 0
B-Green
$Comp
L CONN_01X08 P4
U 1 1 586FC2CD
P 4860 1140
F 0 "P4" V 5071 1135 50  0001 C CNN
F 1 "5-Pos Selector" V 4982 1135 50  0000 C CNN
F 2 "" H 4860 1140 50  0000 C CNN
F 3 "" H 4860 1140 50  0000 C CNN
	1    4860 1140
	0    -1   -1   0   
$EndComp
Text Notes 4030 700  0    60   ~ 0
Blue PCB is underneath, behind this view
Text Label 4710 2650 2    60   ~ 0
G_Out+
Text Label 5010 2650 0    60   ~ 0
G_Out-
Text Label 4610 1340 3    60   ~ 0
BG
Text Label 4610 1340 1    60   ~ 0
BW
Text Label 4710 1340 3    60   ~ 0
BR
Text Label 4810 1340 3    60   ~ 0
BB
Text Label 4910 1340 3    60   ~ 0
NR
Text Label 5010 1340 3    60   ~ 0
NB
Text Label 5110 1340 3    60   ~ 0
NW
Text Label 5110 1340 1    60   ~ 0
NG
Text Notes 5370 1600 0    60   ~ 0
Switching: \nLeft to Right:\n0: (+AB)\n1: B\n2: (+BC)\n3: C\n4: (+CD)\n
$Comp
L CONN_01X01 P1
U 1 1 586FD441
P 2710 1480
F 0 "P1" H 2629 1259 50  0001 C CNN
F 1 "Neck_Pup_Sheild" H 2629 1349 50  0000 C CNN
F 2 "" H 2710 1480 50  0000 C CNN
F 3 "" H 2710 1480 50  0000 C CNN
	1    2710 1480
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X01 P2
U 1 1 586FD4BD
P 2760 2940
F 0 "P2" H 2679 2719 50  0001 C CNN
F 1 "Bridge_Pup_Sheild" H 2760 3050 50  0000 C CNN
F 2 "" H 2760 2940 50  0000 C CNN
F 3 "" H 2760 2940 50  0000 C CNN
	1    2760 2940
	-1   0    0    1   
$EndComp
$Comp
L SWITCH_SPDT SW7
U 1 1 586FD7B8
P 4550 3440
F 0 "SW7" V 4550 3722 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4550 3633 50  0001 C CNN
F 2 "" H 4550 3440 60  0000 C CNN
F 3 "" H 4550 3440 60  0000 C CNN
	1    4550 3440
	0    1    1    0   
$EndComp
$Comp
L SWITCH_SPDT SW5
U 1 1 586FD7E1
P 5150 4630
F 0 "SW5" V 5150 4912 50  0001 C CNN
F 1 "SWITCH_SPDT" H 5150 4823 50  0001 C CNN
F 2 "" H 5150 4630 60  0000 C CNN
F 3 "" H 5150 4630 60  0000 C CNN
	1    5150 4630
	0    -1   -1   0   
$EndComp
$Comp
L SWITCH_SPDT SW3
U 1 1 586FD837
P 4750 4630
F 0 "SW3" V 4750 4912 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4750 4823 50  0001 C CNN
F 2 "" H 4750 4630 60  0000 C CNN
F 3 "" H 4750 4630 60  0000 C CNN
	1    4750 4630
	0    1    -1   0   
$EndComp
$Comp
L SWITCH_SPDT SW1
U 1 1 586FD83D
P 4350 3440
F 0 "SW1" V 4350 3722 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4350 3633 50  0001 C CNN
F 2 "" H 4350 3440 60  0000 C CNN
F 3 "" H 4350 3440 60  0000 C CNN
	1    4350 3440
	0    1    1    0   
$EndComp
$Comp
L SWITCH_SPDT SW10
U 1 1 586FD9BC
P 4950 3440
F 0 "SW10" V 4950 3722 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4950 3633 50  0001 C CNN
F 2 "" H 4950 3440 60  0000 C CNN
F 3 "" H 4950 3440 60  0000 C CNN
	1    4950 3440
	0    -1   1    0   
$EndComp
$Comp
L SWITCH_SPDT SW8
U 1 1 586FD9C2
P 4750 3440
F 0 "SW8" V 4750 3722 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4750 3633 50  0001 C CNN
F 2 "" H 4750 3440 60  0000 C CNN
F 3 "" H 4750 3440 60  0000 C CNN
	1    4750 3440
	0    1    1    0   
$EndComp
$Comp
L SWITCH_SPDT SW6
U 1 1 586FD9C8
P 4950 4630
F 0 "SW6" V 4950 4912 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4950 4823 50  0001 C CNN
F 2 "" H 4950 4630 60  0000 C CNN
F 3 "" H 4950 4630 60  0000 C CNN
	1    4950 4630
	0    1    -1   0   
$EndComp
$Comp
L SWITCH_SPDT SW4
U 1 1 586FD9CE
P 4550 4630
F 0 "SW4" V 4550 4912 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4550 4823 50  0001 C CNN
F 2 "" H 4550 4630 60  0000 C CNN
F 3 "" H 4550 4630 60  0000 C CNN
	1    4550 4630
	0    1    -1   0   
$EndComp
$Comp
L SWITCH_SPDT SW2
U 1 1 586FD9D4
P 4350 4630
F 0 "SW2" V 4350 4912 50  0001 C CNN
F 1 "SWITCH_SPDT" H 4350 4823 50  0001 C CNN
F 2 "" H 4350 4630 60  0000 C CNN
F 3 "" H 4350 4630 60  0000 C CNN
	1    4350 4630
	0    1    -1   0   
$EndComp
Text Label 6190 2570 2    60   ~ 0
AMP_GND
$Comp
L CONN_01X02 P5
U 1 1 586FDCF9
P 6390 2520
F 0 "P5" H 6466 2560 50  0001 L CNN
F 1 "Output Jack" H 6466 2515 50  0000 L CNN
F 2 "" H 6390 2520 50  0000 C CNN
F 3 "" H 6390 2520 50  0000 C CNN
	1    6390 2520
	1    0    0    -1  
$EndComp
Text Notes 5350 4170 0    60   ~ 0
10PDT:\nOut: Carvin Control\nIn:  PyGuitar Control
Text Label 4750 4780 3    60   ~ 0
N-Red
Text Label 5150 4780 3    60   ~ 0
N-White
Text Label 4950 4780 3    60   ~ 0
N-Green
Text Label 4550 4780 3    60   ~ 0
N-Black
Text Label 4350 3290 1    60   ~ 0
Amp_Input
Text Label 4350 4780 3    60   ~ 0
AMP_GND
Text Label 4750 3290 1    60   ~ 0
B-Black
Text Label 4950 3290 1    60   ~ 0
B-Green
Text Label 4550 3290 1    60   ~ 0
B-Red
Text Label 5150 3290 1    60   ~ 0
B-White
Text Label 4400 3590 3    60   ~ 0
G_Out+
$Comp
L CONN_01X01 P3
U 1 1 586FE8B6
P 2780 3400
F 0 "P3" H 2699 3179 50  0001 C CNN
F 1 "Metal_Bridge_GND" H 2780 3510 50  0000 C CNN
F 2 "" H 2780 3400 50  0000 C CNN
F 3 "" H 2780 3400 50  0000 C CNN
	1    2780 3400
	-1   0    0    1   
$EndComp
Text Label 2980 3400 0    60   ~ 0
AMP_GND
Text Label 2960 2940 0    60   ~ 0
AMP_GND
Text Label 2910 1480 0    60   ~ 0
AMP_GND
$Comp
L CONN_01X10 P6
U 1 1 586FEAD7
P 6390 3170
F 0 "P6" H 6467 3210 50  0001 L CNN
F 1 "HD15 Carvin to PyGuitar" H 6467 3165 50  0000 L CNN
F 2 "" H 6390 3170 50  0000 C CNN
F 3 "" H 6390 3170 50  0000 C CNN
	1    6390 3170
	1    0    0    -1  
$EndComp
Text Label 6190 2720 2    60   ~ 0
OUT+
Text Label 6190 2820 2    60   ~ 0
OUT-
Text Label 6190 2920 2    60   ~ 0
A+
Text Label 6190 3020 2    60   ~ 0
A-
Text Label 6190 3120 2    60   ~ 0
B+
Text Label 6190 3220 2    60   ~ 0
B-
Text Label 6190 3320 2    60   ~ 0
C+
Text Label 6190 3420 2    60   ~ 0
C-
Text Label 6190 3520 2    60   ~ 0
D+
Text Label 6190 3620 2    60   ~ 0
D-
Text Label 4800 4480 1    60   ~ 0
NR
Text Label 4700 4480 1    60   ~ 0
A+
Text Label 4300 3590 3    60   ~ 0
OUT+
Text Label 5100 4480 1    60   ~ 0
A-
Text Label 4500 4480 1    60   ~ 0
B-
Text Label 4900 4480 1    60   ~ 0
B+
Text Label 4500 3590 3    60   ~ 0
C+
Text Label 5100 3590 3    60   ~ 0
C-
Text Label 4900 3590 3    60   ~ 0
D+
Text Label 4300 4480 1    60   ~ 0
OUT-
NoConn ~ 5210 1340
NoConn ~ 4510 1340
Text Label 4600 3590 3    60   ~ 0
BR
Text Label 5200 3590 3    60   ~ 0
BW
Text Label 5200 4480 1    60   ~ 0
NW
$Comp
L POT RV1
U 1 1 586CC04C
P 4490 2030
F 0 "RV1" V 4286 2030 50  0001 C CNN
F 1 "500K Vol Pot" H 4490 1800 50  0000 C CNN
F 2 "" H 4490 2030 50  0000 C CNN
F 3 "" H 4490 2030 50  0000 C CNN
	1    4490 2030
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 586FC179
P 5550 2030
F 0 "C2" H 5665 2075 50  0001 L CNN
F 1 "22nF" H 5665 1986 50  0000 L CNN
F 2 "" H 5588 1880 50  0000 C CNN
F 3 "" H 5550 2030 50  0000 C CNN
	1    5550 2030
	1    0    0    -1  
$EndComp
NoConn ~ 5170 1880
Wire Wire Line
	5010 1340 5010 2650
Wire Wire Line
	4710 1340 4710 1730
Wire Wire Line
	4710 2030 4710 2650
Wire Wire Line
	4810 1340 4910 1340
Wire Wire Line
	4800 4480 4800 3590
Connection ~ 4710 1730
Wire Wire Line
	4490 1730 4490 1880
Connection ~ 5010 2180
Wire Wire Line
	5010 2180 5010 2170
Wire Wire Line
	4640 2030 4710 2030
$Comp
L C C1
U 1 1 586FC1DD
P 4710 1880
F 0 "C1" H 4825 1925 50  0001 L CNN
F 1 "180pF" H 4825 1836 50  0000 L CNN
F 2 "" H 4748 1730 50  0000 C CNN
F 3 "" H 4710 1880 50  0000 C CNN
	1    4710 1880
	1    0    0    -1  
$EndComp
Wire Wire Line
	4490 1730 5320 1730
Connection ~ 4710 2030
Wire Wire Line
	5470 1880 5550 1880
Wire Wire Line
	4490 2180 5550 2180
$Comp
L CONN_01X01 P7
U 1 1 586FFEBA
P 2790 3790
F 0 "P7" H 2709 3569 50  0001 C CNN
F 1 "Componet_Bay_Shielding_GND" H 2790 3900 50  0000 C CNN
F 2 "" H 2790 3790 50  0000 C CNN
F 3 "" H 2790 3790 50  0000 C CNN
	1    2790 3790
	-1   0    0    1   
$EndComp
Text Label 2990 3790 0    60   ~ 0
AMP_GND
Text Notes 4550 960  2    60   ~ 0
0
Text Notes 4880 890  2    60   ~ 0
2
Text Notes 5220 960  2    60   ~ 0
4
Text Notes 5070 930  2    60   ~ 0
3
Text Notes 4710 920  2    60   ~ 0
1
Text Notes 5230 1140 2    30   ~ 0
4 3 2 1 0
Text Notes 4880 1140 2    39   ~ 0
c
Text Notes 4730 1140 2    30   ~ 0
4 3 2 1 0
Text Label 4400 4480 1    60   ~ 0
G_Out-
Wire Wire Line
	4600 4480 4600 4320
Wire Wire Line
	4600 4320 4400 4320
Wire Wire Line
	4400 4320 4400 4480
Wire Wire Line
	5000 4480 5000 4320
Wire Wire Line
	5000 4320 5200 4320
Wire Wire Line
	5200 4320 5200 4480
Text Label 4700 3590 3    60   ~ 0
D-
Wire Wire Line
	5000 3590 5000 3800
Wire Wire Line
	5000 3800 5200 3800
Wire Wire Line
	5200 3800 5200 3590
$EndSCHEMATC
