# Makefile to cross compile python files into mpy for inclusion
# in the micropython firmware

CC = /home/bob/MiscProjects/micropython/mpy-cross/mpy-cross 
STMHAL=/home/bob/MiscProjects/micropython/stmhal
SCRIPT_DIR=$(STMHAL)/scripts
BOARD=PYBV10

TRG=$(patsubst %.py,%.mpy,$(wildcard *.py))


all: $(TRG)

%.mpy: %.py
	cd $(SCRIPT_DIR) && $(CC) $<

.PHONY: firmware

firmware: all
	cd $(STMHAL) && $(MAKE) BOARD=$(BOARD) clean
	cd $(STMHAL) && $(MAKE) BOARD=$(BOARD) FROZEN_MPY_DIR=$(SCRIPT_DIR)

deploy: firmware
	cd $(STMHAL) && sudo $(MAKE) BOARD=$(BOARD) deploy


.PHONY: clean

clean:
	-rm *.mpy
