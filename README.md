LightBank
=========


*DESCRIPTION:* <br/>
Created primarily as an exercise for testing PySide in *Modo 801 Linux*. Registers a new Custom Viewport which offers access to limited controls for all lights simultaneously. Offers the following:
- enable/disable
- radiant intensity
- material color
- diffuse contribution
- specular contribution
- light renaming (lights can be renamed in either the scene or LightBank)
- a Solo mode which enables the current light and disables all others. Other light panels are locked out until the light is unsoloed.

___

*INSTALLATION:* <br/>
Download the ZIP, rename it to 'LightBank' and place it inside ~/.luxology/Scripts.


___

*KNOWN ISSUES:* <br/>
- Having difficulty properly closing the parent QWidget.
- Because of the above, the Scene Item Listener is not removed.
- When a light is created or duplicated, the light's unique name is returned as its internal ident instead. Press the Refresh button to get the latest names.
