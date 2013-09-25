/*
at init:
*  In the preset pack loading, a test for the cycle labal keyword and a handler for the loading of the cycle
   file must be provided.
*  care must be taken on creation of the default preset file

During cycling:
*  At the gui level, gui.currentPreset must be set to the index value of the current preset that is active,
   at each cycle increment, the gui.currentPreset must be properly re-assigned; so the cycling mechanism
   must have a handle to the gui, maybe via the model?
*  in the model, the doPreset method must be called - this will update the currentPresetName. 
   doPreset() conveniently takes a presetName as argument!!! Life Is Good!

on ANY click:
*  Cycling must be cancelled, so the gui must have a handle to the cycling mechanism, via the model I would expect

on a hold on a preset:
*  care must be taken about the writing of the preset file to not screw up the cycling mechanics.

at Cycle start:
*  The model must instantiate the Cycle object and follow up on the incrementing via the gui's draw calls. Thus the gui.draw()
   must call the model's cycling mechanism for testing the passage of time;
   

model.conf:
  String cyclePresetLabel ; ok 
   
*/
