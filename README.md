LightBank
=========


*DESCRIPTION:* <br/>
Created primarily as an exercise for testing PySide in *Modo 801 Linux*. Registers a new Custom Viewport which offers access to limited controls for all lights simultaneously. Offers the following controls:
- Enable/Disable
- Intensity
- Color
- Diffuse Contribution
- Specular Contribution
- Light Renaming (lights can be renamed in either the scene or LightBank)
- a Solo mode which enables the current light and disables all others. *(Note: other light panels are locked out until the light is unsoloed.)*

___

*INSTALLATION:* <br/>
LightBank is only available on Linux.
[Download LightBank](http://www.timcrowson.com/downloads/lightbank/LightBank.zip), and place it inside ~/.luxology/Scripts.


___

*KNOWN ISSUES:* <br/>
- When a light is created or deleted, the light's name is incorrectly displayed as the item's internal ident instead. Use the Refresh button to clean this up until a fix is ready. 
- The Scene Item Listener is not properly removed when LightBank is closed.
