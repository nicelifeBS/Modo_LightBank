import lx
import lxifc


# Item Events
ITEM_ADD            = 0
ITEM_DELETE         = 1
ITEM_RENAME         = 2
VALUE_CHANGED       = 3

# Selection Events
SELEVENT_ADD        = 0
SELEVENT_REMOVE     = 1
SELEVENT_CURRENT    = 2
SELEVENT_TIME       = 3
SELEVENT_TIMERANGE  = 4


#----------------------------------------------------------------------------------------------------------------------
# SceneItemListener - Helper class
#----------------------------------------------------------------------------------------------------------------------
class ItemEvents (lxifc.SceneItemListener):
	'''
	'''
	def __init__ (self, callback):
		self.listenerService = lx.service.Listener ()
		self.listenerService.AddListener (self)
		self.callback = callback
		self.event = None
		self.item = None
		self.action = None
		self.index = None

	def __del__ (self):
		self.listenerService.RemoveListener (self)

	def eventHandler (self, event, item, action, index):
		self.event = event
		self.item = item
		self.action = action
		self.index = index
		self.callback (self)

	def sil_ItemAdd(self, item):
		self.eventHandler (ITEM_ADD, item, None, None)

	def sil_ItemRemove(self, item):
		self.eventHandler (ITEM_DELETE, item, None, None)

	def sil_ItemName(self, item):
		self.eventHandler (ITEM_RENAME, item, None, None)

	def sil_ChannelValue(self, action, item, index):
		self.eventHandler (VALUE_CHANGED, item, action, index)

	def sil_SceneCreate(self, scene):
		pass

	def sil_SceneDestroy(self, scene):
		pass

	def sil_SceneFilename(self, scene, fileName):
		pass

	def sil_SceneClear(self, scene):
		pass

	def sil_ItemPreChange(self, scene):
		pass

	def sil_ItemPostDelete(self, scene):
		pass

	def sil_ItemParent(self, item):
		pass

	def sil_ItemChild(self, item):
		pass

	def sil_ItemAddChannel(self, item):
		pass

	def sil_ItemLocal(self, item):
		pass

	def sil_ItemSource(self, item):
		pass

	def sil_ItemPackage(self, item):
		pass

	def sil_LinkAdd(self, graph, itemFrom, itemTo):
		pass

	def sil_LinkRemBefore(self, graph, itemFrom, itemTo):
		pass

	def sil_LinkRemAfter(self, graph, itemFrom, itemTo):
		pass

	def sil_LinkSet(self, graph, itemFrom, itemTo):
		pass

	def sil_ChanLinkAdd(self, graph, itemFrom, chanFrom, itemTo, chanTo):
		pass

	def sil_ChanLinkRemAfter(self, graph, itemFrom, chanFrom, itemTo, chanTo):
		pass

	def sil_ChanLinkSet(self, graph, itemFrom, chanFrom, itemTo, chanTo):
		pass



#-----------------------------------------------------------------------------------------------------------------------
# SelectionListener - Helper class by Matt Cox
#----------------------------------------------------------------------------------------------------------------------
class SelectionEvents (lxifc.SelectionListener):
	'''
	The SelectionEvent class is a helper class that is used to track
	selection and time changes in the current scene. It's initialized
	by passing it a callback function. When the selection or time changes,
	the callback function is called, passing it the SelectionEvent object,
	so it can be queried for it's current state.
	'''
    
	def __init__ (self, callback):
		self.lsn_svc = lx.service.Listener ()
		self.lsn_svc.AddListener (self)
		self.callback = callback
		self.event = None
		self.type = None
		self.subType = None
        
	def __del__ (self):
		self.lsn_svc.RemoveListener (self)
    
	def eventHandler (self, event, type, subType):
		self.event = event
		self.type = type
		self.subType = subType
		self.callback (self)
    
	def selevent_Add (self, type, subType):
		self.eventHandler (SELEVENT_ADD, type, subType)
    
	def selevent_Remove (self, type, subType):
		self.eventHandler (SELEVENT_REMOVE, type, subType)
        
	def selevent_Current (self, type):
		self.eventHandler (SELEVENT_CURRENT, type, None)
        
	def selevent_Time (self, time):
		self.eventHandler (SELEVENT_TIME, None, None)
        
	def selevent_TimeRange (self, type):
		self.eventHandler (SELEVENT_TIMERANGE, type, None)
