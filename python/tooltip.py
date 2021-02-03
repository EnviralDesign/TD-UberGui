class tooltip:
	"""
	the tool tip will launch showing whatever description is in the Uberguioverrideconfig dat, located in the source object.
	If you don't have that dat, or the row doesn't exist, this tool will just silently fail to launch.
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

	def Launch(self , BOTTOM=0 , MSG = "message goes here" ):
		op('text_tooltip').text = MSG
		parent.tooltip.par.display = 1
		parent.tooltip.par.y = max( parent.Widget.height - BOTTOM - parent.tooltip.par.h , 0 )
		
	def Close(self):
		parent.tooltip.par.display = 0