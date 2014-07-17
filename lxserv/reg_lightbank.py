#------------------------------------------------------------------------------
# INFO
#------------------------------------------------------------------------------
# LIGHTBANK, Tim Crowson, July 2014



import os
import sys

import lx
import lxu
import lxifc

import PySide
from PySide.QtGui import *
from PySide.QtCore import *

import sil
import lightbank


# Get basic services
SCENESERVICE = lx.service.Scene()
SELSERVICE = lx.service.Selection()
CMDSERVICE = lx.service.Command()
PLATSERVICE = lx.service.Platform()

# Item Events
ITEM_ADD      = 0
ITEM_DELETE   = 1
ITEM_RENAME   = 2
VALUE_CHANGED = 3


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

#----------------------------------------------------------------------------------------------------------------------
class LightBank_CustomView(lxifc.CustomView):
	'''
	Defines the Custom Viewport registered by this plugin
	'''
	def __init__ (self):
		self.form = None
		self.item_events = None

	def __del__(self):
		pass

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

		if itemType in LIGHTITEMSDICT:

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
		'''
		lx.out('LightBank closed -  removing Scene Item Listener...')
		lx.service.Listener().RemoveListener(self.com_listener)


# BLESS THIS MESS!
lx.bless(LightBank_CustomView, "LightBank")