LightBank
=========


Created primarily as an exercise for testing PySide in Modo 801 Linux

DESCRIPTION
Registers a new Custom Viewport which offers access to limited controls for all lights simultaneously, including the following:
- radiant intensity
- material color
- diffuse contribution
- specular contribution
- on/off
- solo

KNOWN ISSUES
- The QWidget is not deleted when the viewport is closed
- Because of the above, the Scene Item Listener is not removed
- Solo functionality has faulty logic
- The SIL is returning values from the middle of events rather than after their completion
