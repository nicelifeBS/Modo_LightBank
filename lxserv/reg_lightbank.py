# LIGHTBANK, Tim Crowson, July 2014


import lx
import lxu
import lxifc

import PySide

import sil
import lightbank



class LightBank_CustomView(lxifc.CustomView):
	'''
	Defines the Custom Viewport registered by this plugin
	'''
	def __init__ (self):
		self.form = None
		self.item_events = None
		self.ITEM_ADD = 0
		self.ITEM_DELETE = 1
		self.ITEM_RENAME = 2
		self.VALUE_CHANGED = 3
		self.LIGHTITEMSDICT = {
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

		if itemType in self.LIGHTITEMSDICT:

			if listener:
				
				# Ideally the following would trigger more specific actions,
				# but for our purposes broad actions will suffice.
				
				if listener.event == self.ITEM_ADD:
					self.form.ui_panels_addNew()
					
				elif listener.event == self.ITEM_DELETE:
					self.form.ui_panels_removeOld()

				elif listener.event == self.ITEM_RENAME:
					self.form.ui_update_all()

				elif listener.event == self.VALUE_CHANGED:
					self.form.ui_update_channelValuesAll()


	def customview_Init(self, pane):
		'''
		Initialize the viewport, add the LightBank widget, and add a listener.
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
			layout = PySide.QtGui.QGridLayout()
			layout.setContentsMargins( 0,0,0,0 )
			self.form = lightbank.LightBank_Container()
			layout.addWidget(self.form)
			parentWidget.setLayout(layout)

			# Start Item Event listener
			lx.out('LightBank starting - adding Scene Item Listener...')
			self.item_events = sil.ItemEvents (self.itemEvent_Handler)

			# Wrap the listener to ensure we add and remove the same object
			self.com_listener = lx.object.Unknown(self.item_events)
			lx.service.Listener().AddListener(self.com_listener)

			return True

		return False


	def customview_Cleanup (self, pane):
		'''
		Close the viewport and shut down the listener.
		'''
		lx.out('LightBank closed -  removing Scene Item Listener...')
		lx.service.Listener().RemoveListener(self.com_listener)


class ShowLightBank ( lxu.command.BasicCommand ):
	'''
	Modo Command to display LightBank in a new window.
	'''

	def __init__(self):
		lxu.command.BasicCommand.__init__(self)

	def cmd_Interact(self):
		''' '''
		pass

	def basic_Execute(self, msg, flags):
		'''
		Display LightBank in a floating palette.
		'''
		lx.eval("layout.createOrClose viewCookie LightBankLayout width:400 height:600 class:normal title:{LightBank}")


# BLESS THIS MESS!
lx.bless(LightBank_CustomView, "LightBank")
lx.bless(ShowLightBank, "lightbank.show")
