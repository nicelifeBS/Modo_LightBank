#----------------------------------------------------------------------------------------------------------------------
# INFO
#----------------------------------------------------------------------------------------------------------------------
# LIGHTBANK, Tim Crowson, January 2014

# Created primarily as an exercise for testing PySide in Modo 801 Linux

# Registers a new Custom Viewport which offers access to limited controls
# for all lights simultaneously, including the following:
# - radiant intensity
# - material color
# - diffuse contribution
# - specular contribution
# - on/off
# - solo

#----------------------------------------------------------------------------------------------------------------------
# ISSUES
#----------------------------------------------------------------------------------------------------------------------
# - The QWidget is not deleted when the viewport is closed
# - Because of the above, the Scene Item Listener is not removed
# - Solo functionality has faulty logic
# - The SIL is returning values from the middle of events rather than after their completion

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
from listeners import *


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


# Light Types
lightTypesDict = {
				138: 'Directional',
				139: 'Point',
				140: 'Spot',
				141: 'Area',
				142: 'Cylinder',
				143: 'Dome',
				144: 'Portal',
				145: 'Photometric'
				}


# Define the contents of the 'About' button, as html
aboutText = '''
Version 0.1 - <a href="http://www.timcrowson.com" style="text-decoration:none; color: #DBBC86">Tim Crowson</a> - January 2014 <br/><br/><br/>

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
	<li>The QWidget is not deleted when the viewport is closed</li>
	<li>Because of the above, the Scene Item Listener is not removed</li>
	<li>Solo functionality has faulty logic</li>
	<li>The Scene Item Listener is returning values from the middle of events rather than after their completion</li>
	<li>When a light is created or deleted, the panel will not update propely because of the above issues with the SIL. Use the Refresh button for now.</li>
</ul>
'''


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
	Gets the light material associated with a light.
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
class LightBank_Container( QWidget, lightList_UI.Ui_Form ):
	"""
	The main LightBank list, to which we'll add subwidgets for each light
	"""

	def __init__(self, parent=None, selected=[], flag=0, *args):
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


	def closeEvent(self, event):
		lx.out('LightBank : Closing Scene Item Listener...')
		# This closeEvent() method is what I can't trigger successfully,
		# presumably because I don't have the widget parented correctly...


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
				panel = LightBank_Panel()
				panel.compactSizeHint = panel.sizeHint()				
				qItem.setSizeHint(panel.sizeHint())

			 	# Store the ident
				panel.ident = lightIdent

				# Set the panel title.
				# Currently this will reflect the Ident() due to 
				# a limitation with the SIL methods which get fired
				# in the middle of an event (and thus prior to the internal 
				# renaming of the item) rather than after their completion.
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
					panel.lightTypeLabel.setText( lightTypesDict[light.Type()] )

		
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
		lightMaterial = getLightMaterial(light)
		
		if lightMaterial:
			colorRed = channelRead.Double (lightMaterial, lightMaterial.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_LIGHTCOL + '.R'))
			colorGreen = channelRead.Double (lightMaterial, lightMaterial.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_LIGHTCOL + '.G'))
			colorBlue = channelRead.Double (lightMaterial, lightMaterial.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_LIGHTCOL + '.B'))
			color = QColor().fromRgbF( colorRed, colorGreen, colorBlue)
			panel.colorPickButton.setStyleSheet('QPushButton{background-color: rgb(%s, %s, %s);}'%(color.red(), color.green(), color.blue()))

			# Get the Diffuse contribution of the light's material
			affectDiff = channelRead.Double (lightMaterial, lightMaterial.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_DIFFUSE))
			panel.diffuseSlider.setValue(affectDiff*100)
			panel.diffuseSpinBox.setValue(affectDiff*100)

			# Get the Specular contribution of the light's material
			affectSpec = channelRead.Double (lightMaterial, lightMaterial.ChannelLookup (lx.symbol.sICHAN_LIGHTMATERIAL_SPECULAR))
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
		since deriving the row once a widget is set on a QListWidgetItem seems tricky.
		Probably feasible by traversing the parents. Will fix it soon...
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

	def __init__(self,parent=None,selected=[],flag=0, *args):
		QWidget.__init__(self, parent)
		self.setupUi(self)
	
		self.row = None
		self.ident = None
		self.compactSizeHint = None

		self.optionsWidget.hide()
		self.optionsCheckbox.setProperty('disclosure', True)

		self.setConnections()


	def setConnections(self):
		'''
		Connect signals and slots
		'''
		self.lightNameLineEdit.editingFinished.connect(self.set_LightName)

		self.intensitySlider.sliderReleased.connect(self.update_intensitySpinBox)
		self.intensitySpinBox.valueChanged.connect(self.set_LightIntensity)

		self.lightEnabledCheckbox.stateChanged.connect(self.toggle_LightEnabled)
		self.lightSoloButton.clicked.connect(self.toggle_LightSolo)
		self.colorPickButton.released.connect(self.set_LightColor)
		self.optionsCheckbox.stateChanged.connect(self.toggle_OptionsWidget)

		self.diffuseSlider.sliderReleased.connect(self.update_diffuseSpinBox)
		self.diffuseSpinBox.valueChanged.connect(self.set_LightDiffuseContribution)

		self.specularSlider.sliderReleased.connect(self.update_specularSpinBox)
		self.specularSpinBox.valueChanged.connect(self.set_LightSpecContribution)



	def update_intensitySpinBox(self):
		'''
		Update the intensity spin box according to the intensityslider
		'''
		self.intensitySpinBox.setValue(float(self.intensitySlider.value())/10)


	def update_intensitySlider(self):
		'''
		Update the intensity slider according to the intensity spin box
		'''
		self.intensitySlider.setValue(self.intensitySpinBox.value()*10)


	def update_diffuseSlider(self):
		'''
		Update the diffuse slider according to the diffuse spin box
		'''
		self.diffuseSlider.setValue(self.diffuseSpinBox.value())


	def update_diffuseSpinBox(self):
		'''
		Update the diffuse spin box according to the diffuse slider
		'''
		self.diffuseSpinBox.setValue(self.diffuseSlider.value())


	def update_specularSlider(self):
		'''
		Update the diffuse slider according to the diffuse spin box
		'''
		self.specularSlider.setValue(self.specularSpinBox.value())


	def update_specularSpinBox(self):
		'''
		Update the diffuse spin box according to the diffuse slider
		'''
		self.specularSpinBox.setValue(self.specularSlider.value())


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

		for i in range(scene.ItemCount(light_type)):
			item = scene.ItemByIndex(light_type, i)

			if not self.lightSoloButton.isChecked():
				cmdServ.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, "item.channel name:{render} value:default item:{%s}" % item.Ident())

			elif self.lightSoloButton.isChecked():
				lightName = item.UniqueName()
				if lightName != self.lightNameLineEdit.text():
					cmdServ.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, "item.channel name:{render} value:off item:{%s}" % item.Ident())
	

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
		lightMaterial = getLightMaterial(lightItem)
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "select.color rgb:{item.channel {lightMaterial$lightCol} ? item:{%s}}" % (lightMaterial.Ident()))
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "layout.createOrClose ColorPicker ColorPicker true @macros.layouts@ColorPicker@ width:610 height:550 persistent:true style:popover opaque:true" )


	def set_LightDiffuseContribution(self):
		'''
		Set the diffuse contribution of the corresponding light
		'''
		diffuse = float(self.diffuseSpinBox.value())
		lightItem = getItemByName(self.ident)
		lightMaterial = getLightMaterial(lightItem)
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "item.channel name:{diffuse} value:%f item:{%s}" % (diffuse/100, lightMaterial.Ident()))


	def set_LightSpecContribution(self):
		'''
		Set the specular contribution of the corresponding light
		'''
		spec = float(self.specularSpinBox.value())
		lightItem = getItemByName(self.ident)
		lightMaterial = getLightMaterial(lightItem)
		cmdServ.ExecuteArgString (-1, lx.symbol.iCTAG_NULL, "item.channel name:{specular} value:%f item:{%s}" % (spec/100, lightMaterial.Ident()))




#----------------------------------------------------------------------------------------------------------------------
class lightBank(lxifc.CustomView):
	'''
	Defines the Custom Viewport registered by this plugin
	'''
	def __init__ (self):
		self.form = None
		self.item_events = None


	def __del__(self):
		lx.out('LightBank closing - removing Scene Item Listener...')


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

		if listener.event == ITEM_ADD:
			if itemType in lightTypesDict:
				self.form.panels_AddNew()

		elif listener.event == ITEM_DELETE:
			if itemType in lightTypesDict:
				self.form.panels_RemoveOld()

		elif listener.event == ITEM_RENAME:
			pass

		elif listener.event == VALUE_CHANGED:
			self.form.update_PanelValuesAll()
			# if itemType in lightTypesDict or itemType == 133:
			# 	if itemType == 133:  #light material
			# 		light = item.Parent()
			# 		lightIdent = light.Ident()
			# 	else:
			# 		light = item
			# 		lightIdent = item.Ident()

			# 	lightsInScene, existingPanels = self.form.getExistingLightEntities()
			# 	for panel in existingPanels:
			# 		if panel.ident == lightIdent:
			# 			self.form.update_PanelValues(panel, light)


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
			self.item_events = ItemEvents (self.itemEvent_Handler)
			return True

		return False



# BLESS THIS MESS!
lx.bless(lightBank, "LightBank")