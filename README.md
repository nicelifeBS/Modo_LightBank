### LightBank for Modo 801 Linux

LightBank is an experimental kit for configuring multiple lights easily, gathering common controls into a concise interface. It was originally designed as a testbed for creating PySide-based Custom Viewports in Modo 801 on Linux. The feature set is deliberately restricted and would likely be of limited use for actual production. The primary goals of this kit are...
* to implement a Qt-based Custom Viewport
* to allow a two-way flow when adjusting channel values (changes in the scene get reflected in the custom viewport, and vice-versa) through a Scene Item Listener
* to offer some degree of practical application
* to be deployed as a self-contained kit


[![](http://www.timcrowson.com/wp-content/uploads/2014/07/lightbank_001-1024x638.jpg)](http://www.timcrowson.com/wp-content/uploads/2014/07/lightbank_001.jpg)

***


### Features
Since the primary goals do not describe a fully production-ready toolset, the features are limited to the following:
* Provide basic information about a light, such as its name and type
* Enable/Disable a light
* Solo a light (disable all others)
* Toggle Global Illumination
* Quickly set a light's color
* Adjust a light's intensity, diffuse contribution, and specular contribution separately

***

### Installation
LightBank is only available for Modo 801 on Linux, since its Windows and Mac versions do not yet offer PySide-based Custom Viewports.

1. Download [LightBank](http://www.timcrowson.com/downloads/lightbank/LightBank.zip)
2. Place the kit in your Modo "User's Scripts" directory usually `/home/username/.luxology/Scripts`
3. Restart Modo

***

### Usage
From any of Modo's default horizontal toolbars, click the `LightBank ` button...

![](http://www.timcrowson.com/wp-content/uploads/2014/07/lb_button.png)

LightBank will appear in a new floating palette, populated with a list of all the lights in your scene...

![](http://www.timcrowson.com/wp-content/uploads/2014/07/lb_list.jpg)

Use the controls to adjust your light settings...

![](http://www.timcrowson.com/wp-content/uploads/2014/07/lightbank_key.jpg)

LightBank is aware of changes to lights in the scene:
* If you add a new light, a new light panel will be created in LightBank.
* If you rename a light in the scene, its name will be updated in Lightbank.
* If you change a light's type, this will also update in LightBank.
* Changes to channel values (if they have a counterpart in LightBank), will also update.
* Deleting a light in the scene deletes it from LightBank as well.

> About Solo Mode...
> Pressing the `S` button will solo the target light. This will turn off all other lights in the scene, and disable other light panels in LightBank. While solo mode is enabled, you cannot interact with other light panels in LightBank (although it is possible to interact with them in the scene itself!). Unchecking the `S` button will restore lights to whatever state they were in prior to enabling solo mode. 
