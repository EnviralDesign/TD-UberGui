class menu:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp


	def Launch(self, OPS , PAR, LEFT, RIGHT, BOTTOM, TOP):
		'''
		Launching the menu picker works by taking the parameter and it's menu labels
		and generating a replicated list of components to click on.

		The resulting index of the clicked item, will be used in the Set() function
		to set the parameter.
		'''
		
		# init and set some styling params of the widget.
		parent.menu.par.Ops = [ x for x in OPS ]
		parent.menu.par.Par = PAR
		parent.menu.par.w = RIGHT - LEFT
		parent.menu.par.h = 100
		parent.menu.par.x = LEFT
		parent.menu.par.y = max( 0 , (parent.Widget.height - BOTTOM - parent.menu.par.h) )
		
		# get the current menu state and labels.
		currentVal = getattr( op(OPS[0]).par , PAR ).val
		menuLabels = getattr( op(OPS[0]).par , PAR ).menuLabels
		
		# update the table of options. this feed the replicator.
		op('table_options').clear()
		op('table_options').appendRows( menuLabels )
		
		# turn on the menu picker widget finally.
		parent.menu.par.display = 1
		parent.Widget.op('container_foreground_focus').par.display = 1
	
	def Close(self):
		# turns off the menu picker.
		parent.menu.par.display = 0
		parent.Widget.op('container_foreground_focus').par.display = 0
	
	def Set(self, menuIndex=0):
		# set the value of the menu parameters using the provided menu index.
		
		OPS = parent.menu.par.Ops.eval()
		PAR = parent.menu.par.Par.eval()
		for each in OPS:
		
			parameter = getattr( op(each).par , PAR , ":PAR_ERR:" )
			if parameter != ":PAR_ERR:":
				
				if parameter.menuIndex != menuIndex:
					parent.Widget.ParamChange(pars=[parameter])
				
				parameter.menuIndex = menuIndex
		
		parent.menu.par.display = 0
		parent.Widget.op('container_foreground_focus').par.display = 0
		
		return
		