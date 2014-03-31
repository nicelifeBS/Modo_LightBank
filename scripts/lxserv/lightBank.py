#----------------------------------------------------------------------------------------------------------------------
# INFO
#----------------------------------------------------------------------------------------------------------------------
# LIGHTBANK, Tim Crowson, March 2014

# Created primarily as an exercise for testing PySide in Modo 801 Linux

# Registers a new Custom Viewport which offers access to limited controls
# for all lights simultaneously, including the following:
# - radiant intensity
# - light color
# - diffuse contribution
# - specular contribution
# - on/off
# - a Solo mode which enables the current light and disables all others.
#   (Note: other light panels are locked out until the light is unsoloed.)

#----------------------------------------------------------------------------------------------------------------------
# ISSUES
#----------------------------------------------------------------------------------------------------------------------
# 1. When a light is created or deleted, the light's name is incorrectly displayed as the item's internal ident instead. 
#    Use the Refresh button to clean this up.
# 2. The Scene Item Listener is not properly removed when LightBank is closed.

#--------------------------------------------------------------------------------------------------------------------


import os
import sys

import lx
import lxu
import lxifc

import PySide
from PySide.QtGui import *
from PySide.QtCore import *

# import the UI classes
import lightList_UI
import lightPanel_UI

# import the Modo listener classes
import listeners

version = "0.3"

# Get basic services
sceneServ = lx.service.Scene()
selServ = lx.service.Selection()
cmdServ = lx.service.Command()
platServ = lx.service.Platform()


# Item Events
ITEM_ADD      = 0
ITEM_DELETE   = 1
ITEM_RENAME   = 2
VALUE_CHANGED = 3


# Light Item Types
lightItemsDict = {
				133: 'LightMaterial',
				138: 'Directional',
				139: 'Point',
				140: 'Spot',
				141: 'Area',
				142: 'Cylinder',
				143: 'Dome',
				144: 'Portal',
				145: 'Photometric'
				}


# light state storage
lightPreSoloStates = {}

# Define the contents of the 'About' screen, as html
aboutText = '''
Version %s- <a href="http://www.timcrowson.com" style="text-decoration:none; color: #DBBC86">Tim Crowson</a> - March 2014 <br/><br/><br/>

This plugin was created as an exercise for testing PySide in MODO 801 Linux. <br/><br/><br/><br/><br/>
<span style="color: #f49c1c;"><em>DESCRIPTION</em></span><br/><br/>
LightBank offers access to limited controls for all lights simultaneously, including the following:
<ul>
	<li>Radiant Intensity</li>
	<li>Material Color</li>
	<li>Diffuse Contribution percentage</li>
	<li>Specular Contribution percentage</li>
	<li>Render on/off</li>
	<li>Solo mode</li>
	<li>Global Illumination toggle</li>
</ul>
<br/><br/>
<span style="color: #f49c1c;"><em>KNOWN ISSUES</em></span>
<ul>
	<li>When a light is created or deleted, the light's name is incorrectly displayed as the item's internal ident instead. Use the Refresh button to clean this up.</li>
	<li>The Scene Item Listener is not properly removed when LightBank is closed. </li>
</ul>
'''%version


#----------------------------------------------------------------------------------------------------------------------
# Helper functions
#----------------------------------------------------------------------------------------------------------------------
def getItemByName (name):
	'''
	Look up an item by name and return it as an object
	'''
	scene = lxu.select.SceneSelection ().current ()
	return scene.ItemLookup(name)


def getLightMaterial (light):
	'''
	Get the light material associated with a light primitive
	'''
	scene = lxu.select.SceneSelection().current()
	lightMat_type = lx.service.Scene ().ItemTypeLookup (lx.symbol.sITYPE_LIGHTMATERIAL)

	graph = lx.object.ItemGraph (scene.GraphLookup (lx.symbol.sGRAPH_PARENT))
	sub_count = graph.RevCount (light)

	for i in range (sub_count):
		lightMat = graph.RevByIndex (light, i)
		if lightMat.TestType (lightMat_type) == True:
			return lightMat
	return None


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
class LightBank_Container( QWidget, lightList_UI.Ui_Form ):
	"""
	The main LightBank list, to which we'll add subwidgets for each light
	"""

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.setupUi(self)
		self.setConnections()

		# force some initial UI elements
		self.resourceRoot = os.path.dirname(__file__) + "/resources/"
		self.refreshButton.setIcon(QIcon(self.resourceRoot + 'refresh.png'))
		self.lightList.setResizeMode(QListView.Adjust)

		# populate the light list
		self.update_All()
		self.update_GIState()


	def __del__(self):
		lx.out('LightBank Container class destructor called...')


	def setConnections(self):
		'''
		Connect signals and slots
		'''
		self.refreshButton.released.connect(self.manualRefresh)
		self.giCheckBox.stateChanged.connect(self.toggle_GI)
		self.aboutButton.released.connect(self.showAbout)


	def getExistingLightEntities(self):
		'''
		Return two lists of Python objects: one of the lights in the scene,
		and one of the light panels in the UI
		'''
		lightsInScene = []
		existingPanels = []

		scene = lxu.select.SceneSelection().current()
		light_type = sceneServ.ItemTypeLookup(lx.symbol.sITYPE_LIGHT)
		lightCount = scene.ItemCount(light_type)

		# create a list of lights in the scene
		for i in range (lightCount):
			lightsInScene.append( scene.ItemByIndex(light_type, i) ) 

		# create a list of panels in the UI
		for i in range(self.lightList.count()):
			item = self.lightList.item(i)
			panel = self.lightList.itemWidget(item)
			existingPanels.append(panel)

		return lightsInScene, existingPanels


	def update_GIState(self):
		'''
		Update the display state of the Global Illumination toggle based on the scene settings
		'''
		scene = lxu.select.SceneSelection().current()
		channelRead = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, selServ.GetTime())
		renderItem = scene.AnyItemOfType(sceneServ.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
		currentGIState = channelRead.Value(renderItem, 'globEnable')
		self.giCheckBox.setChecked(currentGIState)


	def toggle_GI(self):
		'''
		Toggle GI on and off in the scene
		'''
		giState = self.giCheckBox.isChecked()
		scene = lxu.select.SceneSelection().current()
		renderItem = scene.AnyItemOfType(sceneServ.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
		cmdServ.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, "item.channel name:{globEnable} value:%s item:{%s}" % (giState, renderItem.Ident()))


	def panels_RemoveOld(self):
		'''
		Remove panels for lights which no longer exist in the scene
		'''
		lightsInScene, existingPanels = self.getExistingLightEntities()
		existingSceneIdents = [light.Ident() for light in lightsInScene]

		for i in range(self.lightList.count()):
			item = self.lightList.item(i)
			if item:
				panel = self.lightList.itemWidget(item)
				if not panel.ident in existingSceneIdents:
					self.lightList.takeItem(self.lightList.row(item))

		# Update the row variables on each panel
		self.update_PanelRows()


	def panels_AddNew(self):
		'''
		Update the number of panels based on lights in the scene
		'''
		lightsInScene, existingPanels = self.getExistingLightEntities()
		existingPanelIdents = [panel.ident for panel in existingPanels]

		for light in lightsInScene:
			lightIdent = light.Ident()

			if not lightIdent in existingPanelIdents:

				# Define the panel.
				qItem = QListWidgetItem()
				panel = LightBank_Panel(lightIdent)
				panel.compactSizeHint = panel.sizeHint()				
				qItem.setSizeHint(panel.sizeHint())

				# Set the panel title.
				panel.lightNameLineEdit.setText(light.UniqueName())

				# Add the panel to the list.
				self.lightList.addItem(qItem)
				self.lightList.setItemWidget(qItem, panel)

		# Update the row variables on each panel
		self.update_PanelRows()


	def update_PanelTitles(self):
		'''
		Update the panel titles based on each light's UniqueName() property
		'''
		scene = lxu.select.SceneSelection().current()
		light_type = sceneServ.ItemTypeLookup(lx.symbol.sITYPE_LIGHT)

		# for each light, store its ident and uniqueName as a key-value pair
		lightsInScene = {}
		for i in range (scene.ItemCount(light_type)):
			light = scene.ItemByIndex(light_type, i)
			lightsInScene[light.Ident()] = light.UniqueName()

		# use the dictionnary above to set the panel titles
		for i in range(self.lightList.count()):
			qItem = self.lightList.item(i)
			panel = self.lightList.itemWidget(qItem)
			lightName = lightsInScene[panel.ident]
			panel.lightNameLineEdit.setText(lightName)


	def update_PanelLightTypes(self):
		'''
		Update the light type description in the title bar
		'''
		lightsInScene, existingPanels = self.getExistingLightEntities()

		for panel in existingPanels:
			panelIdent = panel.ident
			for light in lightsInScene:
				if panelIdent == light.Ident():
					panel.lightTypeLabel.setText( lightItemsDict[light.Type()] )


	def update_PanelValues(self, panel, light):
		'''
		Update the values on the light panel according to channel values in the scene.
		Takes a QObject for the panel, and a Modo Python object for the light
		'''

		# create a channelRead object
		scene = lxu.select.SceneSelection ().current ()
		channelRead = scene.Channels (lx.symbol.s_ACTIONLAYER_EDIT, selServ.GetTime ())

		# Get the intensity value of the light
		radiance = channelRead.Value(light, 'radiance')
		panel.intensitySlider.setValue(radiance*10)
		panel.intensitySpinBox.setValue(radiance)

		# Get the render state of the light item (on/off/default(Yes))
		renderState = channelRead.Value(light, 'render')
		if renderState  == 'off':
			panel.lightEnabledCheckbox.setChecked(False)
		else:
			panel.lightEnabledCheckbox.setChecked(True)

		# Get the Color of the light's material
		lightMat = getLightMaterial(light)
		
		if lightMat:
			colorRed = channelRead.Double (lightMat, lightMat.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_LIGHTCOL + '.R'))
			colorGreen = channelRead.Double (lightMat, lightMat.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_LIGHTCOL + '.G'))
			colorBlue = channelRead.Double (lightMat, lightMat.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_LIGHTCOL + '.B'))
			color = QColor().fromRgbF( colorRed, colorGreen, colorBlue)
			panel.colorPickButton.setStyleSheet('QPushButton{background-color: rgb(%s, %s, %s);}'%(color.red(), color.green(), color.blue()))

			# Get the Diffuse contribution of the light's material
			affectDiff = channelRead.Double (lightMat, lightMat.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_DIFFUSE))
			panel.diffuseSlider.setValue(affectDiff*100)
			panel.diffuseSpinBox.setValue(affectDiff*100)

			# Get the Specular contribution of the light's material
			affectSpec = channelRead.Double (lightMat, lightMat.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_SPECULAR))
			panel.specularSlider.setValue(affectSpec*100)
			panel.specularSpinBox.setValue(affectSpec*100)


	
	def update_PanelValuesAll(self):
		'''
		Update all values on all panels
		'''
		# Get the existing light entities
		lightsInScene, existingPanels = self.getExistingLightEntities()

		for panel in existingPanels:
			panelIdent = panel.ident
			for light in lightsInScene:
				if panelIdent == light.Ident():
					self.update_PanelValues(panel, light)


	def update_PanelRows(self):
		'''
		Update the 'rowContainer' for each panel in the UI.
		This is basically a cheap hack to store the current row a panel is on,
		since deriving the row once a widget is set on a QListWidgetItem is tricky.
		'''
		for i in range(self.lightList.count()):
			item = self.lightList.item(i)
			panel = self.lightList.itemWidget(item)
			row = str(self.lightList.row(item))
			panel.rowContainer.setText(row) 


	def update_All(self):
		'''
		Called by the constructor
		'''
		self.panels_RemoveOld()
		self.panels_AddNew()
		self.update_PanelLightTypes()
		self.update_PanelValuesAll()
		self.update_PanelTitles()


	def manualRefresh(self):
		'''
		Called by the 'Refresh' button
		'''
		self.update_GIState()
		self.update_PanelLightTypes()
		self.update_PanelValuesAll()
		self.update_PanelTitles()


	def showAbout(self):
		'''
		Display info about LightBank in a modal window
		'''
		box = QMessageBox()
		box.setWindowTitle('About LightBank...')
		box.setContentsMargins(0,20,40,40)
		box.setText(aboutText)
		box.exec_()


#----------------------------------------------------------------------------------------------------------------------
class LightBank_Panel( QWidget, lightPanel_UI.Ui_Form):
	'''
	The panel generated for each light. For each QListWidgetItem
	added to the light list, we spawn one of these custom widgets
	and apply it via QListWidgetItem.setWidget()
	'''

	def __init__(self, ident, parent=None):
		QWidget.__init__(self, parent)
		self.setupUi(self)
		self.row = None
		self.ident = ident
		self.identContainer.setText(ident)
		self.compactSizeHint = None
		self.optionsWidget.hide()
		self.optionsCheckbox.setProperty('disclosure', True)
		self.setConnections()


	def setConnections(self):
		'''
		Connect signals and slots
		'''
		self.lightNameLineEdit.editingFinished.connect(self.set_LightName)
		self.lightNameLineEdit.returnPressed.connect(self.set_LightName)

		self.intensitySlider.sliderReleased.connect(self.update_intensitySpinBox)
		self.intensitySpinBox.editingFinished.connect(self.update_intensitySlider)

		self.lightEnabledCheckbox.stateChanged.connect(self.toggle_LightEnabled)
		self.lightSoloButton.clicked.connect(self.toggle_LightSolo)
		self.colorPickButton.released.connect(self.set_LightColor)
		self.optionsCheckbox.stateChanged.connect(self.toggle_OptionsWidget)

		self.diffuseSlider.sliderReleased.connect(self.update_diffuseSpinBox)
		self.diffuseSpinBox.editingFinished.connect(self.update_diffuseSlider)

		self.specularSlider.sliderReleased.connect(self.update_specularSpinBox)
		self.specularSpinBox.editingFinished.connect(self.update_specularSlider)


	def update_intensitySpinBox(self):
		'''
		Update the intensity spin box according to the intensityslider
		'''
		self.intensitySpinBox.setValue(float(self.intensitySlider.value())/10)
		self.set_LightIntensity()


	def update_intensitySlider(self):
		'''
		Update the intensity slider according to the intensity spin box
		'''
		self.intensitySlider.setValue(self.intensitySpinBox.value()*10)
		self.set_LightIntensity()


	def update_diffuseSlider(self):
		'''
		Update the diffuse slider according to the diffuse spin box
		'''
		self.diffuseSlider.setValue(self.diffuseSpinBox.value())
		self.set_LightDiffuseContribution()


	def update_diffuseSpinBox(self):
		'''
		Update the diffuse spin box according to the diffuse slider
		'''
		self.diffuseSpinBox.setValue(self.diffuseSlider.value())
		self.set_LightDiffuseContribution()


	def update_specularSlider(self):
		'''
		Update the diffuse slider according to the diffuse spin box
		'''
		self.specularSlider.setValue(self.specularSpinBox.value())
		self.set_LightSpecContribution()


	def update_specularSpinBox(self):
		'''
		Update the diffuse spin box according to the diffuse slider
		'''
		self.specularSpinBox.setValue(self.specularSlider.value())
		self.set_LightSpecContribution()


	def toggle_LightEnabled(self):
		'''
		Toggle the visibility of the target light item
		'''
		if self.lightEnabledCheckbox.isChecked():
			value = 'default'
		else:
			value = 'off'

		lightItem = getItemByName(self.lightNameLineEdit.text())
		cmdServ.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, "item.channel name:{render} value:%s item:{%s}" % (value, lightItem.Ident()))


	def toggle_LightSolo(self):
		'''
		Toggle the solo state of the target light item
		'''

		scene = lxu.select.SceneSelection ().current ()
		light_type = sceneServ.ItemTypeLookup (lx.symbol.sITYPE_LIGHT)
		channelRead = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, selServ.GetTime())
		parent = self.parentWidget().parentWidget().parentWidget()
		thisPanelIdent = self.ident


		# solo this light
		if self.lightSoloButton.isChecked():

			# store original render states
			for i in range(scene.ItemCount(light_type)):
				item = scene.ItemByIndex(light_type, i)
				lightIdent = item.Ident()
				lightPreSoloStates[lightIdent] = channelRead.Value(item, 'render') 

			# set new render states
			for i in range(scene.ItemCount(light_type)):
				item = scene.ItemByIndex(light_type, i)
				lightIdent = item.Ident()

				# disable all other lights
				if lightIdent != thisPanelIdent:
					cmdServ.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, "item.channel name:{render} value:off item:{%s}" % lightIdent)

				# enable this light
				cmdServ.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, "item.channel name:{render} value:off item:{%s}" % thisPanelIdent)

			# update UI
			self.lightEnabledCheckbox.setChecked(True)

			for i in range (parent.lightList.count()):
				panelItem = parent.lightList.item(i)
				panelWidget = parent.lightList.itemWidget(panelItem)
				if panelWidget.identContainer.text() != thisPanelIdent:
					panelWidget.lightSoloButton.setChecked(False)
					panelWidget.setEnabled(False)


		# restore pre-solo state
		else:
			for i in range(scene.ItemCount(light_type)):
				item = scene.ItemByIndex(light_type, i)
				lightIdent = item.Ident()

				# retrieve the original render state from our dictionary
				originalState = lightPreSoloStates[lightIdent]

				# set the value
				cmdServ.ExecuteArgString( -1, lx.symbol.iCTAG_NULL, "item.channel name:{render} value:%s item:{%s}" %(originalState, lightIdent) )

			# re-enable other widgets
			for i in range (parent.lightList.count()):
				panelItem = parent.lightList.item(i)
				panelWidget = parent.lightList.itemWidget(panelItem)
				panelWidget.setEnabled(True)



	def toggle_OptionsWidget(self):
		'''
		Toggle the options panel
		'''
		# there's got to be a less silly way to get the main widget...
		parent = self.parentWidget().parentWidget().parentWidget()

		row = int(self.rowContainer.text())
		panelItem = parent.lightList.item(row)

		if self.optionsCheckbox.isChecked():
			self.optionsWidget.show()
			panelItem.setSizeHint(self.sizeHint())
		else:
			self.optionsWidget.hide()
			panelItem.setSizeHint(self.compactSizeHint)


	def set_LightName(self):
		'''
		Rename the light item in the scene
		'''
		newName = self.lightNameLineEdit.text()
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "item.name %s item:{%s}" % ( newName, self.ident))


	def set_LightIntensity(self):
		'''
		Set the intensity of the corresponding light
		'''
		radiance = float(self.intensitySpinBox.value())
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "item.channel name:{radiance} value:%f item:{%s}" % (radiance, self.ident))


	def set_LightColor(self):
		'''
		Set the material color for the corresponding light using Modo's color picker
		'''
		lightItem = getItemByName(self.ident)
		lightMat = getLightMaterial(lightItem)
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "select.color rgb:{item.channel {lightMaterial$lightCol} ? item:{%s}}" % (lightMat.Ident()))
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "layout.createOrClose ColorPicker ColorPicker true @macros.layouts@ColorPicker@ width:610 height:550 persistent:true style:popover opaque:true" )


	def set_LightDiffuseContribution(self):
		'''
		Set the diffuse contribution of the corresponding light
		'''
		diffuse = float(self.diffuseSpinBox.value())
		lightItem = getItemByName(self.ident)
		lightMat = getLightMaterial(lightItem)
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "item.channel name:{diffuse} value:%f item:{%s}" % (diffuse/100, lightMat.Ident()))


	def set_LightSpecContribution(self):
		'''
		Set the specular contribution of the corresponding light
		'''
		spec = float(self.specularSpinBox.value())
		lightItem = getItemByName(self.ident)
		lightMat = getLightMaterial(lightItem)
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "item.channel name:{specular} value:%f item:{%s}" % (spec/100, lightMat.Ident()))




#----------------------------------------------------------------------------------------------------------------------
class lightBank(lxifc.CustomView):
	'''
	Defines the Custom Viewport registered by this plugin
	'''
	def __init__ (self):
		self.form = None
		self.item_events = None


	def __del__(self):
		lx.out('LightBank CustomView class destructor called.')


	def itemEvent_Handler (self, listener):
		'''
		This function is called when certain events happen in the scene.
		The SceneItemListener class passes an object to this function,
		which parses it for data about the item and the event type.
		'''

		# The item is initially returned as an 'unknown' type.
		# We can use lx.object.Item() to cast this as an item-type object.
		item = lx.object.Item(self.item_events.item)
		itemType = item.Type()

		if itemType in lightItemsDict:

			if listener:
				if listener.event == ITEM_ADD:
					self.form.panels_AddNew()
					
				elif listener.event == ITEM_DELETE:
					self.form.panels_RemoveOld()

				elif listener.event == ITEM_RENAME:
					self.form.manualRefresh()

				elif listener.event == VALUE_CHANGED:
					self.form.update_PanelValuesAll()



	def customview_Init(self, pane):
		'''
		'''
		# Get the pane
		if pane == None:
			return False

		custPane = lx.object.CustomPane(pane)

		if custPane.test() == False:
			return False

		# Get the parent QWidget
		parent = custPane.GetParent()
		parentWidget = lx.getQWidget(parent)

		# Check that it suceeds
		if parentWidget != None:
			layout = QGridLayout()
			layout.setContentsMargins(2,2,2,2)
			self.form = LightBank_Container()
			layout.addWidget(self.form)
			parentWidget.setLayout(layout)

			# Start Item Event listener
			lx.out('LightBank starting - adding Scene Item Listener...')
			self.item_events = listeners.ItemEvents (self.itemEvent_Handler)
			return True

		return False


	def customview_Cleanup (self, pane):
		'''
		'''
		lx.out('LightBank CustomView class cleanup called...')
		self.item_events.listenerService.RemoveListener(self.item_events)


# BLESS THIS MESS!
lx.bless(lightBank, "LightBank")