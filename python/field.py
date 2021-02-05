paramInfo = parent.Widget.op('null_paramInfo')

class field:

	'''
	Extension for the field component. This is a very important comp, because it bridges the gap
	between pure html/css implementation which was not really possible or practical using fields,
	and a hybrid, which UberGui ultimately is.

	Essentially, when launched, the field overlays directly onto the html element the user dbl clicked on.
	Styling between field and chromium is close enough to not break continuity imo, but there are small differences.

	Once you type in a new value and submit that, it writes the value to the custom parameter, and that in turn
	causes the web render to update it's values.
	'''


	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	
	def Launch_Delayed( self , OPS , PAR , LEFT , RIGHT , BOTTOM , TOP , delayFrames=1 ):
		# sometimes the field should be launched with a delay. a conveinent wrapper for that.
		op('delayed_launch').run(OPS , PAR , LEFT , RIGHT , BOTTOM , TOP , delayFrames=delayFrames)
		return
	
	def Launch(self, OPS , PAR, LEFT, RIGHT, BOTTOM, TOP):
		# normal way to launch the field. it needs to know what ops to write to, the custom parameter to write to, and it's position to overlay.
		if paramInfo[PAR,'tupletname'] != None:
			ugOverrideDat = op((parent.field.par.Ops.eval()[0] if isinstance(parent.field.par.Ops.eval(),list) else '') + '/Uberguiconfigoverride')
			tupletName = paramInfo[ PAR , 'tupletname' ].val if paramInfo[ PAR , 'tupletname' ] != None else None
			CustomFormat = ugOverrideDat[tupletName,'style'] if ugOverrideDat != None else None
		else:
			CustomFormat = ""

		# init and set some field parameters.
		CustomFormat = CustomFormat if CustomFormat!= "" else None
		parent.Widget.par.Fieldmode = 1
		parent.field.par.Ops = OPS
		parent.field.par.Par = PAR
		parent.field.par.w = RIGHT - LEFT
		parent.field.par.h = BOTTOM - TOP
		parent.field.par.x = LEFT
		parent.field.par.y = parent.Widget.height - BOTTOM

		# get the current par if it's object exists.
		currentPar = getattr( op(OPS[0]).par , PAR ) if op(OPS[0]) != None else None

		# find out if the par exists, by trying to retrieve the valid attribute.
		doesParExist = getattr( currentPar , 'valid' , False )
		
		# this if/else logic block handles various edge cases for interpreting how to initialize
		# the value that already exists in the par. IE rounding long floats, or making sure ints look like ints, etc.
		if doesParExist != None:
			
			
			currentVal = currentPar.val
			currentStyle = currentPar.style
			
			if currentStyle in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' ]:
				
				if CustomFormat == None:
					currentVal = round(currentVal , 4)
				
				elif CustomFormat in [ "Rgba255" ]:
					currentVal = int( round(currentVal * 255) )
					
			elif currentStyle in [ 'Int' ]:
				currentVal = int(currentVal)
			
			elif currentStyle in [ 'Str' , 'CHOP' , 'COMP' , 'DAT' , 'MAT' , 'panelCOMP' , 'SOP' , 'TOP' , 'Python' ]:
				currentVal = currentVal
				
			else:
				debug('shouldnt be seeing this, no other pars should go to fields..')
			
			# set the field's value finally, and enable/turn it on and set focus.
			op('string')[0,0] = currentVal
			parent.Widget.op('container_foreground_focus').par.display = 1
			parent.field.par.display = 1
			parent.field.panel.focus = 1
			parent.field.setKeyboardFocus(selectAll=True)
			op('delayed_focus').run(delayFrames=1)
		
	
	def Set(self):
		# there are various triggers that will set the value from the field to the parameter. 
		# Primarily this is the enter key, tab can work too for quick rapid fire entry.

		# remove focus from the field, and get the most recently entered value.
		parent.field.panel.focus = 0
		val = op('string')[0,0].val

		# get our target operators and parameter for reference.
		OPS = parent.field.par.Ops.eval()
		PAR = parent.field.par.Par.eval()
		parameter = getattr( op(OPS[0]).par , PAR )
		
		# get custom override info, if any exists.
		ugOverrideDat = op((parent.field.par.Ops.eval()[0] if len(parent.field.par.Ops.eval()) > 0 else '') + '/Uberguiconfigoverride')
		tupletName = paramInfo[ PAR , 'tupletname' ].val
		CustomFormat = str(ugOverrideDat[tupletName,'style']) if ugOverrideDat != None else None
		STYLE = parameter.style

		# this if/else logic block handles various edge cases for interpreting how to initialize
		# the value that already exists in the par. IE rounding long floats, or making sure ints look like ints, etc.
		if STYLE in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' , 'Int' ]:
			
			val = parent.Widget.String_Numeric_Parse(val)
			
			if CustomFormat == None:
				pass
			
			elif CustomFormat in [ "Rgba255" ]:
				val = val / 255

		elif STYLE in [ 'Str' ]:

			if CustomFormat == None:
				pass

			elif CustomFormat in [ "spaceToUnderscore" ]:
				val = val.replace(' ','_')

			elif CustomFormat in [ "tduLegal" ]:
				val = tdu.legalName(val)
				val = val.replace('/','_')
		
		else:
			pass
		
		# init some variables.
		didChange = 0
		initPars = []
		initVals = []

		# iterate through all the operators we want to adjust, and if the param exists on it, set it.
		# the didChange variable is used later to determine if any values actually changed, which is 
		# helpful for triggering our param change script properly.
		for each in OPS:
			
			foundPar = getattr( op(each).par , PAR , ':PAR_ERR:' )
			if foundPar != ':PAR_ERR:':
				
				if foundPar.eval() != val:
					initPars += [ foundPar ]
					initVals += [ foundPar.eval() ]
					didChange = 1
		
				foundPar.val = val
		
		# if changes happened, trigger our param change callback script.
		if didChange == 1:
			parent.Widget.ParamChange(pars=initPars, prevVals=initVals)

		# be sure to reset the double click component so user can dbl click again anywhere.
		parent.Widget.ResetDblClick()
		parent.Widget.op('container_foreground_focus').par.display = 0
		
		return
		
	def Delayed_Close(self):
		# triggered if user cancels field interaction, but with a delay.
		op('delayed_close').run(delayFrames=1)
		
	def Close(self):
		# triggered if user cancels field interaction.
		parent.field.par.display = 0
		parent.Widget.par.Fieldmode = 0
		parent.Widget.op('container_foreground_focus').par.display = 0