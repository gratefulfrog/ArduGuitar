# aaa.py

import stm

# set pin A13 to HIGH
@micropython.asm_thumb
def led_on():
    movwt(r0, stm.GPIOA)
    movw(r1, 1 << 13)
    strh(r1, [r0, stm.GPIO_BSRRL])

# set pin A13 to LOW
@micropython.asm_thumb
def led_off():
    movwt(r0, stm.GPIOA)
    movw(r1, 1 << 13)
    strh(r1, [r0, stm.GPIO_BSRRH])

# fails because of bad movt, mov movwt...
@micropython.asm_thumb
def lon(r0,r1):
    strh(r1, [r0, stm.GPIO_BSRRL])

@micropython.asm_thumb
def lof(r0,r1):
    strh(r1, [r0, stm.GPIO_BSRRH])

def setLed(l, on=True):
    arg=stm.GPIOA
    bits = 1 << (14-l)
    if l == 0:
        arg=stm.GPIOB
    if on:
        lon(arg,bits)
    else:
        loff(arg,bits)
        
    
@micropython.asm_thumb
def flash_led(r0):
    # get the GPIOA address in r1
    movwt(r1, stm.GPIOA)

    # get the bit mask for PA14 (the pin LED #2 is on)
    movw(r2, 1 << 14)

    b(loop_entry)

    label(loop1)

    # turn LED on
    strh(r2, [r1, stm.GPIO_BSRRL])

    # delay for a bit
    movwt(r4, 5599900)
    label(delay_on)
    sub(r4, r4, 1)
    cmp(r4, 0)
    bgt(delay_on)

    # turn LED off
    strh(r2, [r1, stm.GPIO_BSRRH])

    # delay for a bit
    movwt(r4, 5599900)
    label(delay_off)
    sub(r4, r4, 1)
    cmp(r4, 0)
    bgt(delay_off)

    # loop r0 times
    sub(r0, r0, 1)
    label(loop_entry)
    cmp(r0, 0)
    bgt(loop1)
    
