# ps2.py
# date 2015 09 26
# status: draft
"""
    0x00 (device ID)  for the standard PS/2 mouse
    OxAA (BAT) - Basic Assurance Test,
    0xFA (ACK)
    0xFC (Error)
    0xFF (Reset) - The mouse responds to this command with "acknowledge" (0xFA) then enters reset mode.
    0xFE (Resend) - The host sends this command whenever it receives invalid data from the mouse. The mouse 
                    responds by resending the last packet it sent to the host. If the mouse responds to the 
                    "Resend" command with another invalid packet, the host may either issue another "Resend" 
                    command, issue an "Error" (0xFC) command, cycle the mouse's power supply to reset the 
                    mouse, or it may inhibit communication (by bringing the clock line low). This command 
                    is not buffered, which means "Resend" will never be sent in response to the "Resend" command.
    0xF6 (Set Defaults) - The mouse responds with "acknowledge" (0xFA) then loads the following values: 
                          Sampling rate = 100, resolution = 4 counts/mm, Scaling = 1:1, data reporting = disabled. 
                          The mouse then resets its movement counters and enters stream mode.
    0xF5 (Disable Data Reporting) - The mouse responds with "acknowledge" (0xFA) then disables data reporting and 
                                    resets its movement counters. This only affects data reporting in stream mode 
                                    and does not disable sampling. Disabled stream mode functions the same as remote mode.
    0xF4 (Enable Data Reporting) - The mouse responds with "acknowledge" (0xFA) then enables data reporting and 
                                   resets its movement counters. This command may be issued while the mouse is 
                                   in remote mode, but it will only affect data reporting in stream mode.
    0xF3 (Set Sample Rate) - The mouse responds with "acknowledge" (0xFA) then reads one more byte from the host. 
                             The mouse saves this byte as the new sample rate. After receiving the sample rate, 
                             the mouse again responds with "acknowledge" (0xFA) and resets its movement counters. 
                             Valid sample rates are 10, 20, 40, 60, 80, 100, and 200 samples/sec.
    0xF2 (Get Device ID) - The mouse responds with "acknowledge" (0xFA) followed by its device ID (0x00 for 
                           the standard PS/2 mouse). The mouse should also reset its movement counters.
    0xF0 (Set Remote Mode) - The mouse responds with "acknowledge" (0xFA) then resets its movement counters 
                             and enters remote mode.
    0xEE (Set Wrap Mode) - The mouse responds with "acknowledge" (0xFA) then resets its movement counters 
                           and enters wrap mode.
    0xEC (Reset Wrap Mode) - The mouse responds with "acknowledge" (0xFA) then resets its movement counters 
                             and enters the mode it was in prior to wrap mode (stream mode or remote mode).
    0xEB (Read Data) - The mouse responds with "acknowledge" (0xFA) then sends a movement data packet. This 
                       is the only way to read data in remote mode. After the data packet has successfully 
                       been sent, the mouse resets its movement counters.
    0xEA (Set Stream Mode) - The mouse responds with "acknowledge" (0xFA) then resets its movement counters 
                             and enters stream mode.
    0xE9 (Status Request) - The mouse responds with "acknowledge" (0xFA) then sends the following 
                            3-byte status packet (then resets its movement counters): 
"""


class PS22Mouse:
    ACK                  = 0xFA
    BAT                  = OxAA 
    DeviceID             = 0x00
    DisableDataReporting = 0xF5
    EnableDataReporting  = 0xF4 
    Error                = 0xFC
    GetDeviceID          = 0xF2
    ReadData             = 0xEB
    Resend               = 0xFE
    Reset                = 0xFF
    ResetWrapMode        = 0xEC
    SetDefaults          = 0xF6 
    SetRemoteMode        = 0xF0
    SetSampleRate        = 0xF3
    SetStreamMode        = 0xEA
    SetWrapMode          = 0xEE
    StatusRequest        = 0xE9

    
    

    def PS2Mouse(self,clkPinID,dataPinID):
        self.clk = clkPinID
        self.data = dataPinID

    def 
