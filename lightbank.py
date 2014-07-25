#------------------------------------------------------------------------------
# INFO
#------------------------------------------------------------------------------
# LIGHTBANK, Tim Crowson, July 2014

# Created primarily as an exercise for testing PySide in Modo 801 Linux
# Registers a new Custom Viewport which offers access to limited controls
# for all lights simultaneously.



#------------------------------------------------------------------------------
# IMPORTS

import os
import sys

import lx
import lxu
import lxifc

import PySide
from PySide.QtGui import *
from PySide.QtCore import *

__VERSION = "0.5"


#------------------------------------------------------------------------------
# PATHS

FILESERVICE = lx.service.File()
SCRIPTSPATH = FILESERVICE.FileSystemPath(lx.symbol.sSYSTEM_PATH_SCRIPTS)
KITPATH = os.path.join(SCRIPTSPATH,  'LightBank')

RESRCPATH = os.path.join(KITPATH, 'resrc')


#------------------------------------------------------------------------------
# Get basic services
SCENESERVICE = lx.service.Scene()
SELSERVICE = lx.service.Selection()
CMDSERVICE = lx.service.Command()


#------------------------------------------------------------------------------
# Import the UIs
sys.path.append(RESRCPATH)
import lightList_UI
import lightPanel_UI


#------------------------------------------------------------------------------
# Item Events
ITEM_ADD      = 0
ITEM_DELETE   = 1
ITEM_RENAME   = 2
VALUE_CHANGED = 3


#------------------------------------------------------------------------------
# Light Item Types
LIGHTITEMSDICT = {
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
LIGHTPRESOLOSTATES = {}


#------------------------------------------------------------------------------
# Helpers
#------------------------------------------------------------------------------
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


def modoCmd (commandString):
	'''
	Pass a command to Modo so that it gets logged to the undo stack.
	This is a utility wrapper to minimize lengthy command strings later.
	'''
	CMDSERVICE.ExecuteArgString(-1, lx.symbol.iCTAG_NULL, commandString)



#------------------------------------------------------------------------------
class LightBank_Container( QWidget, lightList_UI.Ui_Form ):
	'''
	The main LightBank list, to which we'll add subwidgets for each light
	'''

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.setupUi(self) # boilerplate
		self.setConnections()

		# force some initial UI elements
		self.resourceRoot = RESRCPATH
		self.refreshButton.setIcon(QIcon( os.path.join(RESRCPATH, 'refresh.png')))
		self.lightList.setResizeMode(QListView.Adjust)

		# populate the light list
		self.update_All()
		self.update_GIState()


	def paintEvent(self, event):
		'''
	 	Force an update to the panel titles after the callback triggered by the Listener has completed.
	 	This is necessary to get the latest light names as they appear in the Item List, otherwise
	 	panel titles for new lights will reflect internal ident names instead.
		'''
		self.update_PanelTitles()
		self.update_PanelLightTypes()
		QWidget.paintEvent(self, event)


	def setConnections(self):
		'''
		Connect signals and slots
		'''
		self.refreshButton.released.connect(self.update_All)
		self.giCheckBox.stateChanged.connect(self.toggle_GI)


	def getExistingLightEntities(self):
		'''
		Return two lists of Python objects: one of the lights in the scene,
		and one of the light panels in the UI
		'''
		lightsInScene = []
		existingPanels = []

		scene = lxu.select.SceneSelection().current()
		light_type = SCENESERVICE.ItemTypeLookup(lx.symbol.sITYPE_LIGHT)
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
		channelRead = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, SELSERVICE.GetTime())
		renderItem = scene.AnyItemOfType(SCENESERVICE.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
		currentGIState = channelRead.Value(renderItem, 'globEnable')
		self.giCheckBox.setChecked(currentGIState)


	def toggle_GI(self):
		'''
		Toggle GI on and off in the scene
		'''
		giState = self.giCheckBox.isChecked()
		scene = lxu.select.SceneSelection().current()
		renderItem = scene.AnyItemOfType(SCENESERVICE.ItemTypeLookup(lx.symbol.sITYPE_RENDER))
		modoCmd("item.channel name:{globEnable} value:%s item:{%s}" % (giState, renderItem.Ident()))


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
		light_type = SCENESERVICE.ItemTypeLookup(lx.symbol.sITYPE_LIGHT)

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
					panel.lightTypeLabel.setText( LIGHTITEMSDICT[light.Type()] )


	def update_PanelValues(self, panel, light):
		'''
		Update the values on the light panel according to channel values in the scene.
		Takes a QObject for the panel, and a Modo Python object for the light
		'''

		# create a channelRead object
		scene = lxu.select.SceneSelection ().current ()
		channelRead = scene.Channels (lx.symbol.s_ACTIONLAYER_EDIT, SELSERVICE.GetTime ())

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
		Update everything
		'''
		self.panels_RemoveOld()
		self.panels_AddNew()
		self.update_PanelLightTypes()
		self.update_PanelValuesAll()
		self.update_PanelTitles()


#----------------------------------------------------------------------------------------------------------------------
class LightBank_Panel( QWidget, lightPanel_UI.Ui_Form):
	'''
	The panel generated for each light. For each QListWidgetItem
	added to the light list, we spawn one of these custom widgets
	and apply it via QListWidgetItem.setWidget()
	'''

	def __init__(self, ident, parent=None):
		QWidget.__init__(self, parent)
		self.setupUi(self) # boilerplate
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
		modoCmd("item.channel name:{render} value:%s item:{%s}" %(value, lightItem.Ident()))


	def toggle_LightSolo(self):
		'''
		Toggle the solo state of the target light item
		'''

		scene = lxu.select.SceneSelection ().current ()
		light_type = SCENESERVICE.ItemTypeLookup (lx.symbol.sITYPE_LIGHT)
		channelRead = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, SELSERVICE.GetTime())
		parent = self.parentWidget().parentWidget().parentWidget()
		thisPanelIdent = self.ident


		# solo this light
		if self.lightSoloButton.isChecked():

			# store original render states
			for i in range(scene.ItemCount(light_type)):
				item = scene.ItemByIndex(light_type, i)
				lightIdent = item.Ident()
				LIGHTPRESOLOSTATES[lightIdent] = channelRead.Value(item, 'render') 

			# set new render states
			for i in range(scene.ItemCount(light_type)):
				item = scene.ItemByIndex(light_type, i)
				lightIdent = item.Ident()

				# disable all other lights
				if lightIdent != thisPanelIdent:
					modoCmd("item.channel name:{render} value:off item:{%s}" % lightIdent)

				# enable this light
				modoCmd("item.channel name:{render} value:off item:{%s}" % thisPanelIdent)

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
				originalState = LIGHTPRESOLOSTATES[lightIdent]

				# set the value
				modoCmd("item.channel name:{render} value:%s item:{%s}" %(originalState, lightIdent))

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
		modoCmd("item.name %s item:{%s}" % ( newName, self.ident))


	def set_LightIntensity(self):
		'''
		Set the intensity of the corresponding light
		'''
		radiance = float(self.intensitySpinBox.value())
		modoCmd("item.channel name:{radiance} value:%f item:{%s}" % (radiance, self.ident))


	def set_LightColor(self):
		'''
		Set the material color for the corresponding light using Modo's color picker
		'''
		lightItem = getItemByName(self.ident)
		lightMat = getLightMaterial(lightItem)
		modoCmd("select.color rgb:{item.channel {lightMaterial$lightCol} ? item:{%s}}" % (lightMat.Ident()))
		modoCmd("layout.createOrClose ColorPicker ColorPicker true @macros.layouts@ColorPicker@ width:610 height:550 persistent:true style:popover opaque:true")


	def set_LightDiffuseContribution(self):
		'''
		Set the diffuse contribution of the corresponding light
		'''
		diffuse = float(self.diffuseSpinBox.value())
		lightItem = getItemByName(self.ident)
		lightMat = getLightMaterial(lightItem)
		modoCmd("item.channel name:{diffuse} value:%f item:{%s}" % (diffuse/100, lightMat.Ident()))


	def set_LightSpecContribution(self):
		'''
		Set the specular contribution of the corresponding light
		'''
		spec = float(self.specularSpinBox.value())
		lightItem = getItemByName(self.ident)
		lightMat = getLightMaterial(lightItem)
		modoCmd("item.channel name:{specular} value:%f item:{%s}" % (spec/100, lightMat.Ident()))
