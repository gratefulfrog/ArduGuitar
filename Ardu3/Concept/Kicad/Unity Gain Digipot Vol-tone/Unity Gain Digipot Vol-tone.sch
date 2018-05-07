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
P 3740 1480
F 0 "U?" H 3770 1660 50  0001 L CNN
F 1 "LM1875" H 4083 1434 50  0001 L CNN
F 2 "Package_TO_SOT_THT:TO-220-5_Vertical_StaggeredType1_Py3.7mm" H 3740 1480 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1875.pdf" H 3740 1480 50  0001 C CNN
	1    3740 1480
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5AEF11BC
P 4850 1740
F 0 "R?" H 4920 1787 50  0001 L CNN
F 1 "1M" H 4920 1694 50  0000 L CNN
F 2 "" V 4780 1740 50  0001 C CNN
F 3 "~" H 4850 1740 50  0001 C CNN
	1    4850 1740
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5AEF1282
P 4530 1740
F 0 "C?" H 4645 1787 50  0001 L CNN
F 1 "20pF" H 4240 1740 50  0000 L CNN
F 2 "" H 4568 1590 50  0001 C CNN
F 3 "~" H 4530 1740 50  0001 C CNN
	1    4530 1740
	1    0    0    -1  
$EndComp
Wire Wire Line
	4040 1480 4180 1480
Wire Wire Line
	4530 1590 4530 1480
Connection ~ 4530 1480
Wire Wire Line
	4530 1480 4850 1480
Wire Wire Line
	4850 1590 4850 1480
Connection ~ 4850 1480
$Comp
L power:GND #PWR?
U 1 1 5AEF1554
P 4690 2000
F 0 "#PWR?" H 4690 1750 50  0001 C CNN
F 1 "GND" H 4695 1824 50  0000 C CNN
F 2 "" H 4690 2000 50  0001 C CNN
F 3 "" H 4690 2000 50  0001 C CNN
	1    4690 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4530 1890 4690 1890
Wire Wire Line
	4860 1890 4860 1900
Connection ~ 4850 1890
Wire Wire Line
	4850 1890 4860 1890
Wire Wire Line
	4690 2000 4690 1890
Connection ~ 4690 1890
Wire Wire Line
	4690 1890 4850 1890
Wire Wire Line
	4180 1480 4180 2070
Wire Wire Line
	4180 2070 3440 2070
Wire Wire Line
	3440 2070 3440 1580
Connection ~ 4180 1480
Wire Wire Line
	4180 1480 4530 1480
$Comp
L power:GND #PWR?
U 1 1 5AEF1D1C
P 4850 5080
F 0 "#PWR?" H 4850 4830 50  0001 C CNN
F 1 "GND" H 4855 4904 50  0000 C CNN
F 2 "" H 4850 5080 50  0001 C CNN
F 3 "" H 4850 5080 50  0001 C CNN
	1    4850 5080
	1    0    0    -1  
$EndComp
Text Label 3640 1180 1    50   ~ 0
+12v
Text Label 4450 4580 1    50   ~ 0
+12v
Text Label 4450 5280 3    50   ~ 0
-12v
Text Label 3640 1780 3    50   ~ 0
-12v
Text Label 7910 5030 0    50   ~ 0
Out+
$Comp
L pspice:INDUCTOR L?
U 1 1 5AEF2227
P 1790 1630
F 0 "L?" V 1837 1587 50  0001 R CNN
F 1 "Coil" V 1790 1850 50  0000 R CNN
F 2 "" H 1790 1630 50  0001 C CNN
F 3 "" H 1790 1630 50  0001 C CNN
	1    1790 1630
	0    -1   -1   0   
$EndComp
$Comp
L Potentiometer_Digital:MAX5436 U?
U 1 1 5AEF2616
P 4100 3250
F 0 "U?" H 3900 2860 50  0001 C CNN
F 1 "MAX5436" H 3770 2940 50  0000 C CNN
F 2 "" H 4100 3250 50  0001 C CNN
F 3 "https://datasheets.maximintegrated.com/en/ds/MAX5436-MAX5439.pdf" H 4100 3250 50  0001 C CNN
	1    4100 3250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5AEF1264
P 4900 3250
F 0 "#PWR?" H 4900 3000 50  0001 C CNN
F 1 "GND" H 4905 3074 50  0000 C CNN
F 2 "" H 4900 3250 50  0001 C CNN
F 3 "" H 4900 3250 50  0001 C CNN
	1    4900 3250
	0    -1   -1   0   
$EndComp
Text Label 4200 3600 3    50   ~ 0
-12v
Text Label 4200 2900 1    50   ~ 0
+12v
Text Label 8030 6000 0    50   ~ 0
Out-
Wire Notes Line
	3310 2240 3310 940 
Wire Notes Line
	3310 940  5080 940 
Wire Notes Line
	5080 940  5080 2240
Wire Notes Line
	5080 2240 3310 2240
Wire Wire Line
	4850 1480 5260 1480
Text Notes 4950 1090 2    50   ~ 0
Unity Gain
Wire Notes Line
	3310 3780 3310 2550
Wire Notes Line
	3310 2550 5090 2550
Wire Notes Line
	5090 2550 5090 3780
Wire Notes Line
	5090 3780 3310 3780
Text Notes 5000 2690 2    50   ~ 0
Tone Control
Wire Notes Line
	3640 5580 5090 5580
Wire Notes Line
	5090 5580 5090 4390
Wire Notes Line
	5090 4390 3640 4390
Wire Notes Line
	3640 4390 3640 5580
Text Notes 5020 4520 2    50   ~ 0
Vol Control
$Comp
L Potentiometer_Digital:MAX5436 U?
U 1 1 5AEF0EFD
P 4350 4930
F 0 "U?" H 4150 4520 50  0001 C CNN
F 1 "MAX5436" H 4020 4620 50  0000 C CNN
F 2 "" H 4350 4930 50  0001 C CNN
F 3 "https://datasheets.maximintegrated.com/en/ds/MAX5436-MAX5439.pdf" H 4350 4930 50  0001 C CNN
	1    4350 4930
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_DPDT_x2 SW?
U 1 1 5AEF6C9D
P 2290 1480
F 0 "SW?" H 2290 1676 50  0001 C CNN
F 1 "SW_DPDT_x2" H 2290 1677 50  0001 C CNN
F 2 "" H 2290 1480 50  0001 C CNN
F 3 "" H 2290 1480 50  0001 C CNN
	1    2290 1480
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_DPDT_x2 SW?
U 2 1 5AEF6DBB
P 2290 1790
F 0 "SW?" H 2290 1986 50  0001 C CNN
F 1 "SW_DPDT_x2" H 2290 1987 50  0001 C CNN
F 2 "" H 2290 1790 50  0001 C CNN
F 3 "" H 2290 1790 50  0001 C CNN
	2    2290 1790
	1    0    0    -1  
$EndComp
Wire Wire Line
	1790 1380 2090 1380
Wire Wire Line
	2090 1380 2090 1480
Wire Wire Line
	1790 1880 2090 1880
Wire Wire Line
	2090 1880 2090 1790
Wire Notes Line
	2040 2100 2750 2100
Wire Notes Line
	2750 2100 2750 1140
Wire Notes Line
	2750 1140 2040 1140
Wire Notes Line
	2040 1140 2040 2100
Text Notes 2670 1250 2    50   ~ 0
Inverter
Wire Wire Line
	2490 1380 2570 1380
Wire Wire Line
	2490 1580 2490 1690
Wire Wire Line
	2490 1890 2570 1890
Wire Wire Line
	2570 1890 2570 1380
Connection ~ 2570 1380
Wire Wire Line
	2570 1380 3440 1380
Wire Wire Line
	2630 1690 2490 1690
Connection ~ 2490 1690
$Comp
L Device:R R?
U 1 1 5AF0CD52
P 6980 5290
F 0 "R?" H 7050 5337 50  0001 L CNN
F 1 "1M" H 7050 5244 50  0000 L CNN
F 2 "" V 6910 5290 50  0001 C CNN
F 3 "~" H 6980 5290 50  0001 C CNN
	1    6980 5290
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5AF0CD58
P 6660 5290
F 0 "C?" H 6775 5337 50  0001 L CNN
F 1 "20pF" H 6370 5290 50  0000 L CNN
F 2 "" H 6698 5140 50  0001 C CNN
F 3 "~" H 6660 5290 50  0001 C CNN
	1    6660 5290
	1    0    0    -1  
$EndComp
Wire Wire Line
	6170 5030 6310 5030
Wire Wire Line
	6660 5140 6660 5030
Connection ~ 6660 5030
Wire Wire Line
	6660 5030 6980 5030
Wire Wire Line
	6980 5140 6980 5030
Connection ~ 6980 5030
$Comp
L power:GND #PWR?
U 1 1 5AF0CD64
P 6820 5550
F 0 "#PWR?" H 6820 5300 50  0001 C CNN
F 1 "GND" H 6825 5374 50  0000 C CNN
F 2 "" H 6820 5550 50  0001 C CNN
F 3 "" H 6820 5550 50  0001 C CNN
	1    6820 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6660 5440 6820 5440
Wire Wire Line
	6990 5440 6990 5450
Connection ~ 6980 5440
Wire Wire Line
	6980 5440 6990 5440
Wire Wire Line
	6820 5550 6820 5440
Connection ~ 6820 5440
Wire Wire Line
	6820 5440 6980 5440
Wire Wire Line
	6310 5030 6310 5620
Wire Wire Line
	6310 5620 5570 5620
Wire Wire Line
	5570 5620 5570 5130
Connection ~ 6310 5030
Wire Wire Line
	6310 5030 6660 5030
Text Label 5770 4730 1    50   ~ 0
+12v
Text Label 5770 5330 3    50   ~ 0
-12v
Wire Notes Line
	5440 5790 5440 4490
Wire Notes Line
	5440 4490 7210 4490
Wire Notes Line
	7210 4490 7210 5790
Wire Notes Line
	7210 5790 5440 5790
Wire Wire Line
	6980 5030 8050 5030
Text Notes 7080 4640 2    50   ~ 0
Unity Gain
$Comp
L Device:C C?
U 1 1 5AEF2979
P 4750 3250
F 0 "C?" H 4865 3297 50  0001 L CNN
F 1 "10nF" H 4460 3250 50  0001 L CNN
F 2 "" H 4788 3100 50  0001 C CNN
F 3 "~" H 4750 3250 50  0001 C CNN
	1    4750 3250
	0    1    1    0   
$EndComp
$Comp
L Amplifier_Audio:LM1875 U?
U 1 1 5AF177B2
P 5870 3500
F 0 "U?" H 5900 3680 50  0001 L CNN
F 1 "LM1875" H 6213 3454 50  0001 L CNN
F 2 "Package_TO_SOT_THT:TO-220-5_Vertical_StaggeredType1_Py3.7mm" H 5870 3500 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1875.pdf" H 5870 3500 50  0001 C CNN
	1    5870 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5AF177B8
P 6980 3760
F 0 "R?" H 7050 3807 50  0001 L CNN
F 1 "1M" H 7050 3714 50  0000 L CNN
F 2 "" V 6910 3760 50  0001 C CNN
F 3 "~" H 6980 3760 50  0001 C CNN
	1    6980 3760
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5AF177BE
P 6660 3760
F 0 "C?" H 6775 3807 50  0001 L CNN
F 1 "20pF" H 6370 3760 50  0000 L CNN
F 2 "" H 6698 3610 50  0001 C CNN
F 3 "~" H 6660 3760 50  0001 C CNN
	1    6660 3760
	1    0    0    -1  
$EndComp
Wire Wire Line
	6170 3500 6310 3500
Wire Wire Line
	6660 3610 6660 3500
Connection ~ 6660 3500
Wire Wire Line
	6660 3500 6980 3500
Wire Wire Line
	6980 3610 6980 3500
Connection ~ 6980 3500
$Comp
L power:GND #PWR?
U 1 1 5AF177CA
P 6820 4020
F 0 "#PWR?" H 6820 3770 50  0001 C CNN
F 1 "GND" H 6825 3844 50  0000 C CNN
F 2 "" H 6820 4020 50  0001 C CNN
F 3 "" H 6820 4020 50  0001 C CNN
	1    6820 4020
	1    0    0    -1  
$EndComp
Wire Wire Line
	6660 3910 6820 3910
Wire Wire Line
	6990 3910 6990 3920
Connection ~ 6980 3910
Wire Wire Line
	6980 3910 6990 3910
Wire Wire Line
	6820 4020 6820 3910
Connection ~ 6820 3910
Wire Wire Line
	6820 3910 6980 3910
Wire Wire Line
	6310 3500 6310 4090
Wire Wire Line
	6310 4090 5570 4090
Wire Wire Line
	5570 4090 5570 3600
Connection ~ 6310 3500
Wire Wire Line
	6310 3500 6660 3500
Text Label 5770 3200 1    50   ~ 0
+12v
Text Label 5770 3800 3    50   ~ 0
-12v
Wire Notes Line
	5440 4260 5440 2960
Wire Notes Line
	5440 2960 7210 2960
Wire Notes Line
	7210 2960 7210 4260
Wire Notes Line
	7210 4260 5440 4260
Wire Wire Line
	6980 3500 7390 3500
Text Notes 7080 3110 2    50   ~ 0
Unity Gain
Wire Wire Line
	4850 4780 4850 4350
$Comp
L Amplifier_Audio:LM1875 U?
U 1 1 5AF0CD4C
P 5870 5030
F 0 "U?" H 5900 5210 50  0001 L CNN
F 1 "LM1875" H 6213 4984 50  0001 L CNN
F 2 "Package_TO_SOT_THT:TO-220-5_Vertical_StaggeredType1_Py3.7mm" H 5870 5030 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm1875.pdf" H 5870 5030 50  0001 C CNN
	1    5870 5030
	1    0    0    -1  
$EndComp
Wire Wire Line
	2630 6000 8030 6000
Wire Wire Line
	2630 1690 2630 6000
Wire Wire Line
	4600 3400 5570 3400
Wire Wire Line
	5270 1490 5270 3100
Wire Wire Line
	4600 3100 5270 3100
Wire Wire Line
	5570 4930 4850 4930
Wire Wire Line
	4850 4350 7390 4350
Wire Wire Line
	7390 3500 7390 4350
$EndSCHEMATC
