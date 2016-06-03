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
LIBS:libHMI
LIBS:HMI-cache
EELAYER 25 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title "PyGuitar HMI LED Circuit"
Date "2015-11-18"
Rev "1"
Comp "Gratefulfrog"
Comment1 "added 3 resistors to complete circuit!"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L +5V #PWR01
U 1 1 564B8496
P 7930 6350
F 0 "#PWR01" H 7930 6200 50  0001 C CNN
F 1 "+5V" H 7930 6490 50  0000 C CNN
F 2 "" H 7930 6350 60  0000 C CNN
F 3 "" H 7930 6350 60  0000 C CNN
	1    7930 6350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 564BB478
P 7940 6450
F 0 "#PWR02" H 7940 6200 50  0001 C CNN
F 1 "GND" H 7940 6300 50  0000 C CNN
F 2 "" H 7940 6450 60  0000 C CNN
F 3 "" H 7940 6450 60  0000 C CNN
	1    7940 6450
	1    0    0    -1  
$EndComp
Text Label 7930 6350 0    60   ~ 0
Vcc
Text Label 7940 6450 0    60   ~ 0
GND
$Comp
L 74HC595 U2
U 1 1 564C135D
P 4870 5120
F 0 "U2" H 5020 5720 70  0000 C CNN
F 1 "74HC595" H 4870 4520 70  0000 C CNN
F 2 "Housings_DIP:DIP-16_W7.62mm" H 4870 5120 60  0001 C CNN
F 3 "" H 4870 5120 60  0000 C CNN
	1    4870 5120
	1    0    0    -1  
$EndComp
Text Label 4570 4570 0    60   ~ 0
Vcc
Text Label 4570 5670 3    60   ~ 0
GND
Text Label 4160 1640 2    60   ~ 0
DI
Text Label 4170 5270 2    60   ~ 0
GND
Text Label 4170 4970 2    60   ~ 0
Vcc
$Comp
L 74HC595 U3
U 1 1 564C4B0F
P 4830 3620
F 0 "U3" H 4980 4220 70  0000 C CNN
F 1 "74HC595" H 4830 3020 70  0000 C CNN
F 2 "Housings_DIP:DIP-16_W7.62mm" H 4830 3620 60  0001 C CNN
F 3 "" H 4830 3620 60  0000 C CNN
	1    4830 3620
	1    0    0    -1  
$EndComp
Text Label 4530 3070 0    60   ~ 0
Vcc
Text Label 4530 4170 3    60   ~ 0
GND
Text Label 4130 3770 2    60   ~ 0
GND
Text Label 4130 3470 2    60   ~ 0
Vcc
Text Label 4560 1540 0    60   ~ 0
Vcc
Text Label 4560 2640 3    60   ~ 0
GND
Text Label 4160 2240 2    60   ~ 0
GND
Text Label 4160 1940 2    60   ~ 0
Vcc
$Comp
L 74HC595 U1
U 1 1 564C516E
P 4810 6610
F 0 "U1" H 4960 7210 70  0000 C CNN
F 1 "74HC595" H 4810 6010 70  0000 C CNN
F 2 "Housings_DIP:DIP-16_W7.62mm" H 4810 6610 60  0001 C CNN
F 3 "" H 4810 6610 60  0000 C CNN
	1    4810 6610
	1    0    0    -1  
$EndComp
Text Label 4510 6060 0    60   ~ 0
Vcc
Text Label 4510 7160 3    60   ~ 0
GND
Text Label 3460 6390 0    60   ~ 0
CLK
Text Label 3460 6490 0    60   ~ 0
LATCH
Text Label 4110 6760 2    60   ~ 0
GND
Text Label 4110 6460 2    60   ~ 0
Vcc
$Comp
L 74HC595 U0
U 1 1 564C517A
P 4830 8080
F 0 "U0" H 4980 8680 70  0000 C CNN
F 1 "74HC595" H 4830 7480 70  0000 C CNN
F 2 "Housings_DIP:DIP-16_W7.62mm" H 4830 8080 60  0001 C CNN
F 3 "" H 4830 8080 60  0000 C CNN
	1    4830 8080
	1    0    0    -1  
$EndComp
Text Label 4530 7530 0    60   ~ 0
Vcc
Text Label 4530 8630 3    60   ~ 0
GND
Text Label 3380 7930 0    60   ~ 0
CLK
Text Label 3380 8030 0    60   ~ 0
LATCH
Text Label 4130 8230 2    60   ~ 0
GND
Text Label 4130 7930 2    60   ~ 0
Vcc
Text Label 5530 8530 0    60   ~ 0
DO
$Comp
L CONN_01X02 P2
U 1 1 56501101
P 7500 6400
F 0 "P2" H 7500 6550 50  0000 C CNN
F 1 "CONN_01X02" V 7600 6400 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 7500 6400 60  0001 C CNN
F 3 "" H 7500 6400 60  0000 C CNN
	1    7500 6400
	-1   0    0    -1  
$EndComp
Text Notes 7310 6440 2    60   ~ 0
Power
Text Notes 7290 7090 2    60   ~ 0
SPI
Text Label 7690 6960 0    60   ~ 0
CLK
Text Label 7690 7060 0    60   ~ 0
LATCH
Text Label 7690 7160 0    60   ~ 0
DI
$Comp
L CONN_02X20 P3
U 1 1 56503AB9
P 7930 2650
F 0 "P3" H 7930 3700 50  0000 C CNN
F 1 "CONN_02X20" V 7930 2650 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x20" H 7930 1700 60  0001 C CNN
F 3 "" H 7930 1700 60  0000 C CNN
	1    7930 2650
	1    0    0    -1  
$EndComp
$Comp
L CONN_02X20 P4
U 1 1 5650F1FD
P 7930 4720
F 0 "P4" H 7930 5770 50  0000 C CNN
F 1 "CONN_02X20" V 7930 4720 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x20" H 7930 3770 60  0001 C CNN
F 3 "" H 7930 3770 60  0000 C CNN
	1    7930 4720
	1    0    0    -1  
$EndComp
Text Label 8180 5670 0    60   ~ 0
GND
Text Label 7690 7500 0    60   ~ 0
DO
$Comp
L R R1
U 1 1 56531284
P 7360 1700
F 0 "R1" V 7440 1700 50  0000 C CNN
F 1 "1K" V 7360 1700 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 1700 30  0001 C CNN
F 3 "" H 7360 1700 30  0000 C CNN
	1    7360 1700
	0    1    1    0   
$EndComp
$Comp
L R R2
U 1 1 5653156A
P 7360 1800
F 0 "R2" V 7440 1800 50  0000 C CNN
F 1 "1K" V 7360 1800 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 1800 30  0001 C CNN
F 3 "" H 7360 1800 30  0000 C CNN
	1    7360 1800
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 56531612
P 7360 1900
F 0 "R3" V 7440 1900 50  0000 C CNN
F 1 "1K" V 7360 1900 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 1900 30  0001 C CNN
F 3 "" H 7360 1900 30  0000 C CNN
	1    7360 1900
	0    1    1    0   
$EndComp
$Comp
L R R4
U 1 1 56531618
P 7360 2000
F 0 "R4" V 7440 2000 50  0000 C CNN
F 1 "1K" V 7360 2000 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2000 30  0001 C CNN
F 3 "" H 7360 2000 30  0000 C CNN
	1    7360 2000
	0    1    1    0   
$EndComp
$Comp
L R R5
U 1 1 56531822
P 7360 2100
F 0 "R5" V 7440 2100 50  0000 C CNN
F 1 "1K" V 7360 2100 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2100 30  0001 C CNN
F 3 "" H 7360 2100 30  0000 C CNN
	1    7360 2100
	0    1    1    0   
$EndComp
$Comp
L R R6
U 1 1 56531828
P 7360 2200
F 0 "R6" V 7440 2200 50  0000 C CNN
F 1 "1K" V 7360 2200 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2200 30  0001 C CNN
F 3 "" H 7360 2200 30  0000 C CNN
	1    7360 2200
	0    1    1    0   
$EndComp
$Comp
L R R7
U 1 1 5653182E
P 7360 2300
F 0 "R7" V 7440 2300 50  0000 C CNN
F 1 "1K" V 7360 2300 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2300 30  0001 C CNN
F 3 "" H 7360 2300 30  0000 C CNN
	1    7360 2300
	0    1    1    0   
$EndComp
$Comp
L R R8
U 1 1 56531834
P 7360 2400
F 0 "R8" V 7440 2400 50  0000 C CNN
F 1 "1K" V 7360 2400 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2400 30  0001 C CNN
F 3 "" H 7360 2400 30  0000 C CNN
	1    7360 2400
	0    1    1    0   
$EndComp
$Comp
L R R9
U 1 1 56534E6A
P 7360 2500
F 0 "R9" V 7440 2500 50  0000 C CNN
F 1 "1K" V 7360 2500 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2500 30  0001 C CNN
F 3 "" H 7360 2500 30  0000 C CNN
	1    7360 2500
	0    1    1    0   
$EndComp
$Comp
L R R10
U 1 1 56534E70
P 7360 2600
F 0 "R10" V 7440 2600 50  0000 C CNN
F 1 "1K" V 7360 2600 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2600 30  0001 C CNN
F 3 "" H 7360 2600 30  0000 C CNN
	1    7360 2600
	0    1    1    0   
$EndComp
$Comp
L R R11
U 1 1 56534E76
P 7360 2700
F 0 "R11" V 7440 2700 50  0000 C CNN
F 1 "1K" V 7360 2700 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2700 30  0001 C CNN
F 3 "" H 7360 2700 30  0000 C CNN
	1    7360 2700
	0    1    1    0   
$EndComp
$Comp
L R R12
U 1 1 56534E7C
P 7360 2800
F 0 "R12" V 7440 2800 50  0000 C CNN
F 1 "1K" V 7360 2800 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2800 30  0001 C CNN
F 3 "" H 7360 2800 30  0000 C CNN
	1    7360 2800
	0    1    1    0   
$EndComp
$Comp
L R R13
U 1 1 56534E82
P 7360 2900
F 0 "R13" V 7440 2900 50  0000 C CNN
F 1 "1K" V 7360 2900 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 2900 30  0001 C CNN
F 3 "" H 7360 2900 30  0000 C CNN
	1    7360 2900
	0    1    1    0   
$EndComp
$Comp
L R R14
U 1 1 56534E88
P 7360 3000
F 0 "R14" V 7440 3000 50  0000 C CNN
F 1 "1K" V 7360 3000 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3000 30  0001 C CNN
F 3 "" H 7360 3000 30  0000 C CNN
	1    7360 3000
	0    1    1    0   
$EndComp
$Comp
L R R15
U 1 1 56534E8E
P 7360 3100
F 0 "R15" V 7440 3100 50  0000 C CNN
F 1 "1K" V 7360 3100 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3100 30  0001 C CNN
F 3 "" H 7360 3100 30  0000 C CNN
	1    7360 3100
	0    1    1    0   
$EndComp
$Comp
L R R16
U 1 1 56534E94
P 7360 3200
F 0 "R16" V 7440 3200 50  0000 C CNN
F 1 "1K" V 7360 3200 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3200 30  0001 C CNN
F 3 "" H 7360 3200 30  0000 C CNN
	1    7360 3200
	0    1    1    0   
$EndComp
$Comp
L R R17
U 1 1 56535EAF
P 7360 3300
F 0 "R17" V 7440 3300 50  0000 C CNN
F 1 "1K" V 7360 3300 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3300 30  0001 C CNN
F 3 "" H 7360 3300 30  0000 C CNN
	1    7360 3300
	0    1    1    0   
$EndComp
$Comp
L R R18
U 1 1 56535EB5
P 7360 3400
F 0 "R18" V 7440 3400 50  0000 C CNN
F 1 "1K" V 7360 3400 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3400 30  0001 C CNN
F 3 "" H 7360 3400 30  0000 C CNN
	1    7360 3400
	0    1    1    0   
$EndComp
$Comp
L R R19
U 1 1 56535EBB
P 7360 3500
F 0 "R19" V 7440 3500 50  0000 C CNN
F 1 "1K" V 7360 3500 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3500 30  0001 C CNN
F 3 "" H 7360 3500 30  0000 C CNN
	1    7360 3500
	0    1    1    0   
$EndComp
$Comp
L R R20
U 1 1 56535EC1
P 7360 3600
F 0 "R20" V 7440 3600 50  0000 C CNN
F 1 "1K" V 7360 3600 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3600 30  0001 C CNN
F 3 "" H 7360 3600 30  0000 C CNN
	1    7360 3600
	0    1    1    0   
$EndComp
$Comp
L R R21
U 1 1 56535ECD
P 7360 3770
F 0 "R21" V 7440 3770 50  0000 C CNN
F 1 "1K" V 7360 3770 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3770 30  0001 C CNN
F 3 "" H 7360 3770 30  0000 C CNN
	1    7360 3770
	0    1    1    0   
$EndComp
$Comp
L R R22
U 1 1 56535ED3
P 7360 3870
F 0 "R22" V 7440 3870 50  0000 C CNN
F 1 "1K" V 7360 3870 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3870 30  0001 C CNN
F 3 "" H 7360 3870 30  0000 C CNN
	1    7360 3870
	0    1    1    0   
$EndComp
$Comp
L R R23
U 1 1 56535ED9
P 7360 3970
F 0 "R23" V 7440 3970 50  0000 C CNN
F 1 "1K" V 7360 3970 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 3970 30  0001 C CNN
F 3 "" H 7360 3970 30  0000 C CNN
	1    7360 3970
	0    1    1    0   
$EndComp
$Comp
L R R24
U 1 1 56535EDF
P 7360 4070
F 0 "R24" V 7440 4070 50  0000 C CNN
F 1 "1K" V 7360 4070 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4070 30  0001 C CNN
F 3 "" H 7360 4070 30  0000 C CNN
	1    7360 4070
	0    1    1    0   
$EndComp
$Comp
L R R25
U 1 1 56535EE5
P 7360 4170
F 0 "R25" V 7440 4170 50  0000 C CNN
F 1 "1K" V 7360 4170 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4170 30  0001 C CNN
F 3 "" H 7360 4170 30  0000 C CNN
	1    7360 4170
	0    1    1    0   
$EndComp
$Comp
L R R26
U 1 1 56535EEB
P 7360 4270
F 0 "R26" V 7440 4270 50  0000 C CNN
F 1 "1K" V 7360 4270 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4270 30  0001 C CNN
F 3 "" H 7360 4270 30  0000 C CNN
	1    7360 4270
	0    1    1    0   
$EndComp
$Comp
L R R27
U 1 1 56535EF1
P 7360 4370
F 0 "R27" V 7440 4370 50  0000 C CNN
F 1 "1K" V 7360 4370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4370 30  0001 C CNN
F 3 "" H 7360 4370 30  0000 C CNN
	1    7360 4370
	0    1    1    0   
$EndComp
$Comp
L R R28
U 1 1 56535EF7
P 7360 4470
F 0 "R28" V 7440 4470 50  0000 C CNN
F 1 "1K" V 7360 4470 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4470 30  0001 C CNN
F 3 "" H 7360 4470 30  0000 C CNN
	1    7360 4470
	0    1    1    0   
$EndComp
$Comp
L R R29
U 1 1 56535EFD
P 7360 4570
F 0 "R29" V 7440 4570 50  0000 C CNN
F 1 "1K" V 7360 4570 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4570 30  0001 C CNN
F 3 "" H 7360 4570 30  0000 C CNN
	1    7360 4570
	0    1    1    0   
$EndComp
$Comp
L R R30
U 1 1 56535F03
P 7360 4670
F 0 "R30" V 7440 4670 50  0000 C CNN
F 1 "1K" V 7360 4670 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4670 30  0001 C CNN
F 3 "" H 7360 4670 30  0000 C CNN
	1    7360 4670
	0    1    1    0   
$EndComp
$Comp
L R R31
U 1 1 56535F09
P 7360 4770
F 0 "R31" V 7440 4770 50  0000 C CNN
F 1 "1K" V 7360 4770 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4770 30  0001 C CNN
F 3 "" H 7360 4770 30  0000 C CNN
	1    7360 4770
	0    1    1    0   
$EndComp
$Comp
L R R32
U 1 1 56538929
P 7360 4870
F 0 "R32" V 7440 4870 50  0000 C CNN
F 1 "1K" V 7360 4870 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4870 30  0001 C CNN
F 3 "" H 7360 4870 30  0000 C CNN
	1    7360 4870
	0    1    1    0   
$EndComp
$Comp
L R R33
U 1 1 5653892F
P 7360 4970
F 0 "R33" V 7440 4970 50  0000 C CNN
F 1 "1K" V 7360 4970 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 4970 30  0001 C CNN
F 3 "" H 7360 4970 30  0000 C CNN
	1    7360 4970
	0    1    1    0   
$EndComp
$Comp
L R R34
U 1 1 56538935
P 7360 5070
F 0 "R34" V 7440 5070 50  0000 C CNN
F 1 "1K" V 7360 5070 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5070 30  0001 C CNN
F 3 "" H 7360 5070 30  0000 C CNN
	1    7360 5070
	0    1    1    0   
$EndComp
$Comp
L R R35
U 1 1 5653893B
P 7360 5170
F 0 "R35" V 7440 5170 50  0000 C CNN
F 1 "1K" V 7360 5170 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5170 30  0001 C CNN
F 3 "" H 7360 5170 30  0000 C CNN
	1    7360 5170
	0    1    1    0   
$EndComp
$Comp
L R R36
U 1 1 56538941
P 7360 5270
F 0 "R36" V 7440 5270 50  0000 C CNN
F 1 "1K" V 7360 5270 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5270 30  0001 C CNN
F 3 "" H 7360 5270 30  0000 C CNN
	1    7360 5270
	0    1    1    0   
$EndComp
$Comp
L R R37
U 1 1 56538947
P 7360 5370
F 0 "R37" V 7440 5370 50  0000 C CNN
F 1 "1K" V 7360 5370 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5370 30  0001 C CNN
F 3 "" H 7360 5370 30  0000 C CNN
	1    7360 5370
	0    1    1    0   
$EndComp
Text Label 5530 7830 0    60   ~ 0
UU0
Text Label 5530 7730 0    60   ~ 0
UU1
Text Label 5530 7630 0    60   ~ 0
UU2
Text Label 5530 7930 0    60   ~ 0
PBLR
Text Label 5530 8030 0    60   ~ 0
PBLL
Text Label 5530 8130 0    60   ~ 0
PBUR
Text Label 5530 8230 0    60   ~ 0
PBUL
Text Label 5510 6860 0    60   ~ 0
MV0
Text Label 5510 6760 0    60   ~ 0
MV1
Text Label 5510 6660 0    60   ~ 0
MV2
Text Label 5510 6560 0    60   ~ 0
MT0
Text Label 5510 6460 0    60   ~ 0
MT1
Text Label 5510 6360 0    60   ~ 0
MT2
Text Label 5510 6260 0    60   ~ 0
TR0
Text Label 5510 6160 0    60   ~ 0
TR1
Text Label 5530 8330 0    60   ~ 0
TR2
Text Label 5560 2340 0    60   ~ 0
AV0
Text Label 5560 2240 0    60   ~ 0
AV1
Text Label 5560 2140 0    60   ~ 0
AV2
Text Label 5560 2040 0    60   ~ 0
AT0
Text Label 5560 1940 0    60   ~ 0
AT1
Text Label 5560 1840 0    60   ~ 0
AT2
Text Label 5560 1740 0    60   ~ 0
BV0
Text Label 5560 1640 0    60   ~ 0
BV1
Text Label 5530 3870 0    60   ~ 0
BV2
Text Label 5530 3770 0    60   ~ 0
BT0
Text Label 5530 3670 0    60   ~ 0
BT1
Text Label 5530 3570 0    60   ~ 0
BT2
Text Label 5530 3470 0    60   ~ 0
CV0
Text Label 5530 3370 0    60   ~ 0
CV1
Text Label 5530 3270 0    60   ~ 0
CV2
Text Label 5530 3170 0    60   ~ 0
CT0
Text Label 5570 5370 0    60   ~ 0
CT1
Text Label 5570 5270 0    60   ~ 0
CT2
Text Label 5570 5170 0    60   ~ 0
DV0
Text Label 5570 5070 0    60   ~ 0
DV1
Text Label 5570 4970 0    60   ~ 0
DV2
Text Label 5570 4870 0    60   ~ 0
DT0
Text Label 5570 4770 0    60   ~ 0
DT1
Text Label 5570 4670 0    60   ~ 0
DT2
Text Label 7210 1700 2    60   ~ 0
AV0
Text Label 7210 1800 2    60   ~ 0
AV1
Text Label 7210 1900 2    60   ~ 0
AV2
Text Label 7210 2000 2    60   ~ 0
AT0
Text Label 7210 2100 2    60   ~ 0
AT1
Text Label 7210 2200 2    60   ~ 0
AT2
Text Label 7210 2300 2    60   ~ 0
BV0
Text Label 7210 2400 2    60   ~ 0
BV1
Text Label 7210 2500 2    60   ~ 0
BV2
Text Label 7210 2600 2    60   ~ 0
BT0
Text Label 7210 2700 2    60   ~ 0
BT1
Text Label 7210 2800 2    60   ~ 0
BT2
Text Label 7210 2900 2    60   ~ 0
CV0
Text Label 7210 3000 2    60   ~ 0
CV1
Text Label 7210 3100 2    60   ~ 0
CV2
Text Label 7210 3200 2    60   ~ 0
CT0
Text Label 7210 3300 2    60   ~ 0
CT1
Text Label 7210 3400 2    60   ~ 0
CT2
Text Label 7210 3500 2    60   ~ 0
DV0
Text Label 7210 3600 2    60   ~ 0
DV1
Text Label 7210 3770 2    60   ~ 0
DV2
Text Label 7210 3870 2    60   ~ 0
DT0
Text Label 7210 3970 2    60   ~ 0
DT1
Text Label 7210 4070 2    60   ~ 0
DT2
Text Label 7210 4270 2    60   ~ 0
MV1
Text Label 7210 4370 2    60   ~ 0
MV2
Text Label 7210 4470 2    60   ~ 0
MT0
Text Label 7210 4570 2    60   ~ 0
MT1
Text Label 7210 4670 2    60   ~ 0
MT2
Text Label 7210 4770 2    60   ~ 0
TR0
Text Label 7210 4870 2    60   ~ 0
TR1
Text Label 7210 4970 2    60   ~ 0
TR2
Text Label 7210 5470 2    60   ~ 0
UU0
Text Label 7210 5570 2    60   ~ 0
UU1
Text Label 7210 5670 2    60   ~ 0
UU2
Text Label 7210 5370 2    60   ~ 0
PBLR
Text Label 7210 5270 2    60   ~ 0
PBLL
Text Label 7210 5170 2    60   ~ 0
PBUR
Text Label 7210 5070 2    60   ~ 0
PBUL
Text Label 7210 4170 2    60   ~ 0
MV0
$Comp
L 74HC595 U4
U 1 1 564C4F9C
P 4860 2090
F 0 "U4" H 5010 2690 70  0000 C CNN
F 1 "74HC595" H 4860 1490 70  0000 C CNN
F 2 "Housings_DIP:DIP-16_W7.62mm" H 4860 2090 60  0001 C CNN
F 3 "" H 4860 2090 60  0000 C CNN
	1    4860 2090
	1    0    0    -1  
$EndComp
$Comp
L C C5
U 1 1 5654642C
P 4560 1200
F 0 "C5" H 4585 1300 50  0000 L CNN
F 1 "100nF" H 4585 1100 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D3_P2.5" H 4598 1050 30  0001 C CNN
F 3 "" H 4560 1200 60  0000 C CNN
	1    4560 1200
	1    0    0    -1  
$EndComp
Text Label 4560 1050 0    60   ~ 0
GND
$Comp
L C C2
U 1 1 56546B96
P 3910 2920
F 0 "C2" H 3935 3020 50  0000 L CNN
F 1 "100nF" H 3935 2820 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D3_P2.5" H 3948 2770 30  0001 C CNN
F 3 "" H 3910 2920 60  0000 C CNN
	1    3910 2920
	1    0    0    -1  
$EndComp
Text Label 3910 2770 0    60   ~ 0
GND
$Comp
L C C4
U 1 1 56547041
P 3960 4420
F 0 "C4" H 3985 4520 50  0000 L CNN
F 1 "100nF" H 3985 4320 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D3_P2.5" H 3998 4270 30  0001 C CNN
F 3 "" H 3960 4420 60  0000 C CNN
	1    3960 4420
	1    0    0    -1  
$EndComp
Text Label 3960 4270 0    60   ~ 0
GND
$Comp
L C C1
U 1 1 565474F6
P 3890 5910
F 0 "C1" H 3915 6010 50  0000 L CNN
F 1 "100nF" H 3915 5810 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D3_P2.5" H 3928 5760 30  0001 C CNN
F 3 "" H 3890 5910 60  0000 C CNN
	1    3890 5910
	1    0    0    -1  
$EndComp
Text Label 3890 5760 0    60   ~ 0
GND
$Comp
L C C3
U 1 1 565478EA
P 3920 7380
F 0 "C3" H 3945 7480 50  0000 L CNN
F 1 "100nF" H 3945 7280 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D3_P2.5" H 3958 7230 30  0001 C CNN
F 3 "" H 3920 7380 60  0000 C CNN
	1    3920 7380
	1    0    0    -1  
$EndComp
Text Label 3920 7230 0    60   ~ 0
GND
$Comp
L CONN_01X01 P17
U 1 1 5654A9F0
P 3730 3170
F 0 "P17" H 3730 3270 50  0000 C CNN
F 1 "CONN_01X01" V 3830 3170 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x01" H 3730 3170 60  0001 C CNN
F 3 "" H 3730 3170 60  0000 C CNN
	1    3730 3170
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X01 P18
U 1 1 5654ABD8
P 3770 4670
F 0 "P18" H 3770 4770 50  0000 C CNN
F 1 "CONN_01X01" V 3870 4670 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x01" H 3770 4670 60  0001 C CNN
F 3 "" H 3770 4670 60  0000 C CNN
	1    3770 4670
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X01 P15
U 1 1 5654AE78
P 3660 6160
F 0 "P15" H 3660 6260 50  0000 C CNN
F 1 "CONN_01X01" V 3760 6160 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x01" H 3660 6160 60  0001 C CNN
F 3 "" H 3660 6160 60  0000 C CNN
	1    3660 6160
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X01 P16
U 1 1 5654B0F0
P 3720 7630
F 0 "P16" H 3720 7730 50  0000 C CNN
F 1 "CONN_01X01" V 3820 7630 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x01" H 3720 7630 60  0001 C CNN
F 3 "" H 3720 7630 60  0000 C CNN
	1    3720 7630
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X02 P11
U 1 1 5654D859
P 3180 7980
F 0 "P11" H 3180 8130 50  0000 C CNN
F 1 "CONN_01X02" V 3280 7980 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 3180 7980 60  0001 C CNN
F 3 "" H 3180 7980 60  0000 C CNN
	1    3180 7980
	-1   0    0    -1  
$EndComp
Text Label 3420 4970 0    60   ~ 0
CLK
Text Label 3420 5070 0    60   ~ 0
LATCH
$Comp
L CONN_01X02 P13
U 1 1 5654E48A
P 3220 5020
F 0 "P13" H 3220 5170 50  0000 C CNN
F 1 "CONN_01X02" V 3320 5020 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 3220 5020 60  0001 C CNN
F 3 "" H 3220 5020 60  0000 C CNN
	1    3220 5020
	-1   0    0    -1  
$EndComp
Text Label 3380 3470 0    60   ~ 0
CLK
Text Label 3380 3570 0    60   ~ 0
LATCH
$Comp
L CONN_01X02 P10
U 1 1 5654E958
P 3180 3520
F 0 "P10" H 3180 3670 50  0000 C CNN
F 1 "CONN_01X02" V 3280 3520 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 3180 3520 60  0001 C CNN
F 3 "" H 3180 3520 60  0000 C CNN
	1    3180 3520
	-1   0    0    -1  
$EndComp
Text Label 3410 1940 0    60   ~ 0
CLK
Text Label 3410 2040 0    60   ~ 0
LATCH
$Comp
L CONN_01X02 P12
U 1 1 5654ED5F
P 3210 1990
F 0 "P12" H 3210 2140 50  0000 C CNN
F 1 "CONN_01X02" V 3310 1990 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 3210 1990 60  0001 C CNN
F 3 "" H 3210 1990 60  0000 C CNN
	1    3210 1990
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X03 P9
U 1 1 5654F32B
P 2580 7750
F 0 "P9" H 2580 7950 50  0000 C CNN
F 1 "CONN_01X03" V 2680 7750 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 2580 7750 60  0001 C CNN
F 3 "" H 2580 7750 60  0000 C CNN
	1    2580 7750
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X03 P8
U 1 1 5654FFC0
P 2550 6360
F 0 "P8" H 2550 6560 50  0000 C CNN
F 1 "CONN_01X03" V 2650 6360 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 2550 6360 60  0001 C CNN
F 3 "" H 2550 6360 60  0000 C CNN
	1    2550 6360
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X02 P14
U 1 1 565500FA
P 3260 6440
F 0 "P14" H 3260 6590 50  0000 C CNN
F 1 "CONN_01X02" V 3360 6440 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 3260 6440 60  0001 C CNN
F 3 "" H 3260 6440 60  0000 C CNN
	1    3260 6440
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X03 P6
U 1 1 56553759
P 2500 3330
F 0 "P6" H 2500 3530 50  0000 C CNN
F 1 "CONN_01X03" V 2600 3330 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 2500 3330 60  0001 C CNN
F 3 "" H 2500 3330 60  0000 C CNN
	1    2500 3330
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3860 5860 5660 5860
Wire Wire Line
	3920 7410 5690 7410
Wire Wire Line
	7700 6450 7940 6450
Wire Wire Line
	7700 6350 7930 6350
Wire Wire Line
	8180 1700 8180 5670
Connection ~ 8180 1800
Connection ~ 8180 1900
Connection ~ 8180 2000
Connection ~ 8180 2100
Connection ~ 8180 2200
Connection ~ 8180 2300
Connection ~ 8180 2400
Connection ~ 8180 2500
Connection ~ 8180 2600
Connection ~ 8180 2700
Connection ~ 8180 2800
Connection ~ 8180 2900
Connection ~ 8180 3000
Connection ~ 8180 3100
Connection ~ 8180 3200
Connection ~ 8180 3300
Connection ~ 8180 3400
Connection ~ 8180 3500
Connection ~ 8180 3600
Connection ~ 8180 3770
Connection ~ 8180 3870
Connection ~ 8180 3970
Connection ~ 8180 4070
Connection ~ 8180 4170
Connection ~ 8180 4270
Connection ~ 8180 4370
Connection ~ 8180 4470
Connection ~ 8180 4570
Connection ~ 8180 4670
Connection ~ 8180 4770
Connection ~ 8180 4870
Connection ~ 8180 4970
Connection ~ 8180 5070
Connection ~ 8180 5170
Connection ~ 8180 5270
Connection ~ 8180 5370
Connection ~ 8180 5470
Connection ~ 8180 5570
Wire Wire Line
	7510 1700 7680 1700
Wire Wire Line
	7680 1800 7510 1800
Wire Wire Line
	7510 1900 7680 1900
Wire Wire Line
	7680 2000 7510 2000
Wire Wire Line
	7680 2100 7510 2100
Wire Wire Line
	7510 2200 7680 2200
Wire Wire Line
	7510 2300 7680 2300
Wire Wire Line
	7680 2400 7510 2400
Wire Wire Line
	7510 2500 7680 2500
Wire Wire Line
	7680 2600 7510 2600
Wire Wire Line
	7510 2700 7680 2700
Wire Wire Line
	7680 2800 7510 2800
Wire Wire Line
	7510 2900 7680 2900
Wire Wire Line
	7680 3000 7510 3000
Wire Wire Line
	7680 3100 7510 3100
Wire Wire Line
	7510 3200 7680 3200
Wire Wire Line
	7680 3300 7510 3300
Wire Wire Line
	7510 3400 7680 3400
Wire Wire Line
	7680 3500 7510 3500
Wire Wire Line
	7510 3600 7680 3600
Wire Wire Line
	7510 3770 7680 3770
Wire Wire Line
	7680 3870 7510 3870
Wire Wire Line
	7510 3970 7680 3970
Wire Wire Line
	7680 4070 7510 4070
Wire Wire Line
	7510 4170 7680 4170
Wire Wire Line
	7680 4270 7510 4270
Wire Wire Line
	7510 4370 7680 4370
Wire Wire Line
	7680 4470 7510 4470
Wire Wire Line
	7510 4570 7680 4570
Wire Wire Line
	7680 4670 7510 4670
Wire Wire Line
	7680 4770 7510 4770
Wire Wire Line
	7680 4870 7510 4870
Wire Wire Line
	7510 4970 7680 4970
Wire Wire Line
	7680 5070 7510 5070
Wire Wire Line
	7510 5170 7680 5170
Wire Wire Line
	7680 5270 7510 5270
Wire Wire Line
	7510 5370 7680 5370
Wire Wire Line
	3930 2890 5610 2890
Wire Wire Line
	3970 4400 5640 4400
Wire Wire Line
	4560 1350 4560 1540
Wire Wire Line
	3910 3070 4530 3070
Wire Wire Line
	3960 4570 4570 4570
Wire Wire Line
	3890 6060 4510 6060
Wire Wire Line
	3920 7530 4530 7530
Wire Wire Line
	5560 2540 5610 2540
Wire Wire Line
	5610 2540 5610 2890
Wire Wire Line
	3930 3170 4130 3170
Wire Wire Line
	3930 2890 3930 3230
Wire Wire Line
	5530 4070 5640 4070
Wire Wire Line
	5640 4070 5640 4400
Wire Wire Line
	3970 4820 3970 4400
Wire Wire Line
	3970 4670 4170 4670
Wire Wire Line
	5570 5570 5660 5570
Wire Wire Line
	5660 5570 5660 5860
Wire Wire Line
	3860 6160 4110 6160
Wire Wire Line
	3860 6260 3860 5860
Wire Wire Line
	5510 7060 5690 7060
Wire Wire Line
	5690 7060 5690 7410
Wire Wire Line
	3920 7410 3920 7650
Wire Wire Line
	4130 7630 3920 7630
Wire Wire Line
	3380 8130 3380 8030
Wire Wire Line
	4130 7830 3380 7830
Wire Wire Line
	3380 7640 3380 7930
Wire Wire Line
	3030 5170 4170 5170
Wire Wire Line
	3420 5170 3420 5070
Wire Wire Line
	2790 4870 4170 4870
Wire Wire Line
	3420 4870 3420 4970
Wire Wire Line
	3380 3670 3380 3570
Wire Wire Line
	4130 3370 3380 3370
Wire Wire Line
	3380 3330 3380 3470
Wire Wire Line
	3410 2140 3410 2040
Wire Wire Line
	4160 1840 3410 1840
Wire Wire Line
	3410 1840 3410 1940
Connection ~ 3380 8130
Connection ~ 3380 7830
Connection ~ 3920 7630
Wire Wire Line
	3460 6490 4110 6490
Wire Wire Line
	4110 6490 4110 6660
Wire Wire Line
	3460 6360 4120 6360
Wire Wire Line
	3460 6300 3460 6390
Wire Wire Line
	2970 6620 3460 6620
Wire Wire Line
	3460 6620 3460 6490
Wire Wire Line
	2910 6300 3460 6300
Connection ~ 3460 6360
Connection ~ 3460 6490
Connection ~ 4110 6360
Wire Wire Line
	2930 6260 3860 6260
Connection ~ 3860 6160
Wire Wire Line
	2850 5030 3030 5030
Wire Wire Line
	3030 5030 3030 5170
Connection ~ 3420 5170
Connection ~ 3420 4870
Wire Wire Line
	2800 4820 3970 4820
Connection ~ 3970 4670
Connection ~ 3380 3670
Wire Wire Line
	2790 3330 3380 3330
Connection ~ 3380 3370
Wire Wire Line
	3930 3230 2880 3230
Connection ~ 3930 3170
Connection ~ 3410 2140
Connection ~ 3410 1850
Wire Wire Line
	2640 1850 2810 1850
Wire Wire Line
	2810 1850 2810 2140
Connection ~ 2810 2140
Wire Wire Line
	2810 2140 4160 2140
Wire Wire Line
	3410 1850 2920 1850
Wire Wire Line
	2920 1850 2920 1950
Wire Wire Line
	2920 1950 2640 1950
Wire Wire Line
	3380 7640 2780 7640
Wire Wire Line
	2780 7640 2780 7650
Wire Wire Line
	2880 8130 2880 7750
Wire Wire Line
	2880 7750 2780 7750
Wire Wire Line
	2880 8130 4130 8130
Wire Wire Line
	2780 7850 3000 7850
Wire Wire Line
	3000 7850 3000 7700
Wire Wire Line
	3000 7700 3920 7700
Wire Wire Line
	3920 7700 3920 7630
$Comp
L CONN_01X02 P5
U 1 1 5655A7D5
P 2440 1900
F 0 "P5" H 2440 2050 50  0000 C CNN
F 1 "CONN_01X02" V 2540 1900 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 2440 1900 60  0001 C CNN
F 3 "" H 2440 1900 60  0000 C CNN
	1    2440 1900
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2700 3230 2790 3230
Wire Wire Line
	2790 3230 2790 3330
Wire Wire Line
	2700 3330 2760 3330
Wire Wire Line
	2760 3330 2760 3670
Connection ~ 2760 3670
Wire Wire Line
	2760 3670 4130 3670
Wire Wire Line
	2700 3430 2880 3430
Wire Wire Line
	2880 3430 2880 3230
$Comp
L CONN_01X03 P7
U 1 1 56552BAB
P 2530 4930
F 0 "P7" H 2530 5130 50  0000 C CNN
F 1 "CONN_01X03" V 2630 4930 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 2530 4930 60  0001 C CNN
F 3 "" H 2530 4930 60  0000 C CNN
	1    2530 4930
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2730 4830 2790 4830
Wire Wire Line
	2790 4830 2790 4870
Connection ~ 2840 4870
Wire Wire Line
	2850 4970 2850 5030
Wire Wire Line
	2850 4970 2730 4970
Wire Wire Line
	2730 4970 2730 4930
Wire Wire Line
	2800 4820 2800 5030
Wire Wire Line
	2800 5030 2730 5030
Wire Wire Line
	2750 6260 2910 6260
Wire Wire Line
	2910 6260 2910 6300
Wire Wire Line
	2970 6620 2970 6360
Wire Wire Line
	2970 6360 2750 6360
Wire Wire Line
	2930 6260 2930 6460
Wire Wire Line
	2930 6460 2750 6460
$Comp
L CONN_01X03 P1
U 1 1 5655F0C4
P 7490 7060
F 0 "P1" H 7490 7260 50  0000 C CNN
F 1 "CONN_01X03" V 7590 7060 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 7490 7060 60  0001 C CNN
F 3 "" H 7490 7060 60  0000 C CNN
	1    7490 7060
	-1   0    0    -1  
$EndComp
$Comp
L CONN_01X01 P19
U 1 1 5655F310
P 7490 7500
F 0 "P19" H 7490 7600 50  0000 C CNN
F 1 "CONN_01X01" V 7590 7500 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x01" H 7490 7500 60  0001 C CNN
F 3 "" H 7490 7500 60  0000 C CNN
	1    7490 7500
	-1   0    0    -1  
$EndComp
$Comp
L R R38
U 1 1 564C39C7
P 7360 5470
F 0 "R38" V 7440 5470 50  0000 C CNN
F 1 "1K" V 7360 5470 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5470 30  0001 C CNN
F 3 "" H 7360 5470 30  0000 C CNN
	1    7360 5470
	0    1    1    0   
$EndComp
$Comp
L R R39
U 1 1 564C3B87
P 7360 5570
F 0 "R39" V 7440 5570 50  0000 C CNN
F 1 "1K" V 7360 5570 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5570 30  0001 C CNN
F 3 "" H 7360 5570 30  0000 C CNN
	1    7360 5570
	0    1    1    0   
$EndComp
$Comp
L R R40
U 1 1 564C3C8B
P 7360 5670
F 0 "R40" V 7440 5670 50  0000 C CNN
F 1 "1K" V 7360 5670 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM10mm" V 7290 5670 30  0001 C CNN
F 3 "" H 7360 5670 30  0000 C CNN
	1    7360 5670
	0    1    1    0   
$EndComp
Wire Wire Line
	7510 5470 7680 5470
Wire Wire Line
	7680 5570 7510 5570
Wire Wire Line
	7510 5670 7680 5670
$EndSCHEMATC
