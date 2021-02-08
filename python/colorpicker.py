class colorpicker:
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp


	def Launch(self, OPS , PAR, LEFT, RIGHT, BOTTOM, TOP):
		# Launch the color picker setting the operator, par, and position in the process.
		parent.colorpicker.par.Ops = OPS
		parent.colorpicker.par.Par = PAR
		
		parent.colorpicker.par.w = RIGHT - LEFT
		parent.colorpicker.par.h = parent.colorpicker.par.w + op('hue').height
		
		parent.colorpicker.par.x = LEFT
		parent.colorpicker.par.y = max( 0 , (parent.Widget.height - BOTTOM - parent.colorpicker.par.h) )
		
		parent.colorpicker.par.display = 1
		
		parent.colorpicker.store('isModified' , 0)
		
		parent.Widget.op('container_foreground_focus').par.display = 1
		
		
		
	def Close(self):
		# closes the color picker. will still trigger param change callback if value has changed.
		parent.colorpicker.par.display = 0
		
		isModified = parent.colorpicker.fetch('isModified' , 0)
		
		if isModified == 1:
			OPS = parent.colorpicker.par.Ops.eval()
			PAR = parent.colorpicker.par.Par.eval()

			foundPar = getattr( op(OPS[0]).par , PAR , ":ERR:" )
			initPars = []
			if foundPar != ":ERR:":
				initPars = [ foundPar ]

			parent.Widget.ParamChange(pars=initPars)
		
		parent.colorpicker.store('isModified' , 0)
		
		parent.Widget.op('container_foreground_focus').par.display = 0
		
		
	def Set(self,r,g,b):
		# given a set of r/g/b values, set the custom parameters on the target objects.
		# this change will force the color picker graphics to update, avoiding cyclic depend stuff.
		OPS = parent.colorpicker.par.Ops.eval()
		PAR = parent.colorpicker.par.Par.eval()
		
		vals = [ r,g,b ]
		
		for each in OPS:
			for i,parName in enumerate(op('null_src_par').rows()):
				
				parameter = getattr( op(each).par , parName[0].val , ':PAR_ERR:' )
				if parameter != ':PAR_ERR:':
					parameter.val = vals[i]
					
					parent.colorpicker.store('isModified' , 1)
					
		# parent.Widget.op('container_foreground_focus').par.display = 0