EESchema Schematic File Version 4
LIBS:Unity Gain Digipot Vol-tone-cache
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
L Amplifier_Audio:LM1875 U?
U 1 1 5AEF0D72
P 4440 3480
F 0 "U?" H 4470 3660 50  0001 L CNN
F 1 "LM1875" H 4783 3434 50  0001 L CNN
F 2 "Package_TO_SOT_THT:TO-220-5_Vertical_StaggeredType1_Py3.7mm" H 4440 3480 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1875.pdf" H 4440 3480 50  0001 C CNN
	1    4440 3480
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5AEF11BC
P 5550 3740
F 0 "R?" H 5620 3787 50  0001 L CNN
F 1 "1M" H 5620 3694 50  0000 L CNN
F 2 "" V 5480 3740 50  0001 C CNN
F 3 "~" H 5550 3740 50  0001 C CNN
	1    5550 3740
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5AEF1282
P 5230 3740
F 0 "C?" H 5345 3787 50  0001 L CNN
F 1 "20pF" H 4940 3740 50  0000 L CNN
F 2 "" H 5268 3590 50  0001 C CNN
F 3 "~" H 5230 3740 50  0001 C CNN
	1    5230 3740
	1    0    0    -1  
$EndComp
Wire Wire Line
	4740 3480 4880 3480
Wire Wire Line
	5230 3590 5230 3480
Connection ~ 5230 3480
Wire Wire Line
	5230 3480 5550 3480
Wire Wire Line
	5550 3590 5550 3480
Connection ~ 5550 3480
$Comp
L power:GND #PWR?
U 1 1 5AEF1554
P 5390 4000
F 0 "#PWR?" H 5390 3750 50  0001 C CNN
F 1 "GND" H 5395 3824 50  0000 C CNN
F 2 "" H 5390 4000 50  0001 C CNN
F 3 "" H 5390 4000 50  0001 C CNN
	1    5390 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5230 3890 5390 3890
Wire Wire Line
	5560 3890 5560 3900
Connection ~ 5550 3890
Wire Wire Line
	5550 3890 5560 3890
Wire Wire Line
	5390 4000 5390 3890
Connection ~ 5390 3890
Wire Wire Line
	5390 3890 5550 3890
Wire Wire Line
	4880 3480 4880 4070
Wire Wire Line
	4880 4070 4140 4070
Wire Wire Line
	4140 4070 4140 3580
Connection ~ 4880 3480
Wire Wire Line
	4880 3480 5230 3480
$Comp
L power:GND #PWR?
U 1 1 5AEF1D1C
P 6620 4760
F 0 "#PWR?" H 6620 4510 50  0001 C CNN
F 1 "GND" H 6625 4584 50  0000 C CNN
F 2 "" H 6620 4760 50  0001 C CNN
F 3 "" H 6620 4760 50  0001 C CNN
	1    6620 4760
	1    0    0    -1  
$EndComp
Text Label 4340 3180 1    50   ~ 0
+12v
Text Label 7020 4960 3    50   ~ 0
+12v
Text Label 7020 4260 1    50   ~ 0
-12v
Text Label 4340 3780 3    50   ~ 0
-12v
Text Label 7360 4850 0    50   ~ 0
Out+
$Comp
L pspice:INDUCTOR L?
U 1 1 5AEF2227
P 2490 3630
F 0 "L?" V 2537 3587 50  0001 R CNN
F 1 "Coil" V 2490 3850 50  0000 R CNN
F 2 "" H 2490 3630 50  0001 C CNN
F 3 "" H 2490 3630 50  0001 C CNN
	1    2490 3630
	0    -1   -1   0   
$EndComp
$Comp
L Potentiometer_Digital:MAX5436 U?
U 1 1 5AEF2616
P 7120 3330
F 0 "U?" H 6920 2940 50  0001 C CNN
F 1 "MAX5436" H 6790 3020 50  0000 C CNN
F 2 "" H 7120 3330 50  0001 C CNN
F 3 "https://datasheets.maximintegrated.com/en/ds/MAX5436-MAX5439.pdf" H 7120 3330 50  0001 C CNN
	1    7120 3330
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5AEF1264
P 6440 3030
F 0 "#PWR?" H 6440 2780 50  0001 C CNN
F 1 "GND" H 6445 2854 50  0000 C CNN
F 2 "" H 6440 3030 50  0001 C CNN
F 3 "" H 6440 3030 50  0001 C CNN
	1    6440 3030
	-1   0    0    1   
$EndComp
Text Label 7020 3680 3    50   ~ 0
+12v
Text Label 7020 2980 1    50   ~ 0
-12v
Text Label 7350 5010 0    50   ~ 0
Out-
$Comp
L Device:C C?
U 1 1 5AEF2979
P 6440 3180
F 0 "C?" H 6555 3227 50  0001 L CNN
F 1 "10nF" H 6150 3180 50  0000 L CNN
F 2 "" H 6478 3030 50  0001 C CNN
F 3 "~" H 6440 3180 50  0001 C CNN
	1    6440 3180
	1    0    0    -1  
$EndComp
Wire Wire Line
	6620 3330 6440 3330
Wire Notes Line
	4010 4240 4010 2940
Wire Notes Line
	4010 2940 5780 2940
Wire Notes Line
	5780 2940 5780 4240
Wire Notes Line
	5780 4240 4010 4240
Wire Wire Line
	5550 3480 6620 3480
Text Notes 5650 3090 2    50   ~ 0
Unity Gain
Wire Notes Line
	6130 3860 6130 2630
Wire Notes Line
	6130 2630 7910 2630
Wire Notes Line
	7910 2630 7910 3860
Wire Notes Line
	7910 3860 6130 3860
Text Notes 7820 2770 2    50   ~ 0
Tone Control
Wire Wire Line
	6620 4460 6620 3480
Connection ~ 6620 3480
Wire Wire Line
	6620 4610 6380 4610
Wire Wire Line
	6380 4610 6380 5260
Wire Notes Line
	6460 5170 7910 5170
Wire Notes Line
	7910 5170 7910 3980
Wire Notes Line
	7910 3980 6460 3980
Wire Notes Line
	6460 3980 6460 5170
Text Notes 7840 4110 2    50   ~ 0
Vol Control
Wire Wire Line
	6380 5260 8380 5260
Text Label 8380 5260 0    50   ~ 0
Out+
Text Label 8380 5390 0    50   ~ 0
Out-
$Comp
L Potentiometer_Digital:MAX5436 U?
U 1 1 5AEF0EFD
P 7120 4610
F 0 "U?" H 6920 4200 50  0001 C CNN
F 1 "MAX5436" H 6790 4300 50  0000 C CNN
F 2 "" H 7120 4610 50  0001 C CNN
F 3 "https://datasheets.maximintegrated.com/en/ds/MAX5436-MAX5439.pdf" H 7120 4610 50  0001 C CNN
	1    7120 4610
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_DPDT_x2 SW?
U 1 1 5AEF6C9D
P 2990 3480
F 0 "SW?" H 2990 3676 50  0001 C CNN
F 1 "SW_DPDT_x2" H 2990 3677 50  0001 C CNN
F 2 "" H 2990 3480 50  0001 C CNN
F 3 "" H 2990 3480 50  0001 C CNN
	1    2990 3480
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_DPDT_x2 SW?
U 2 1 5AEF6DBB
P 2990 3790
F 0 "SW?" H 2990 3986 50  0001 C CNN
F 1 "SW_DPDT_x2" H 2990 3987 50  0001 C CNN
F 2 "" H 2990 3790 50  0001 C CNN
F 3 "" H 2990 3790 50  0001 C CNN
	2    2990 3790
	1    0    0    1   
$EndComp
Wire Wire Line
	3260 3690 3190 3690
Wire Wire Line
	3330 3890 3190 3890
Wire Wire Line
	2490 3380 2790 3380
Wire Wire Line
	2790 3380 2790 3480
Wire Wire Line
	2490 3880 2790 3880
Wire Wire Line
	2790 3880 2790 3790
Wire Wire Line
	8380 5390 3330 5390
Wire Wire Line
	3330 5390 3330 3890
Connection ~ 3330 3890
Wire Wire Line
	3190 3380 3260 3380
Wire Wire Line
	3260 3690 3260 3380
Connection ~ 3260 3380
Wire Wire Line
	3260 3380 4140 3380
Wire Wire Line
	3190 3580 3330 3580
Wire Wire Line
	3330 3580 3330 3890
Wire Wire Line
	3330 3890 3330 3900
Wire Notes Line
	2740 4100 3450 4100
Wire Notes Line
	3450 4100 3450 3140
Wire Notes Line
	3450 3140 2740 3140
Wire Notes Line
	2740 3140 2740 4100
Text Notes 3370 3250 2    50   ~ 0
Inverter
NoConn ~ 6620 3180
$EndSCHEMATC
