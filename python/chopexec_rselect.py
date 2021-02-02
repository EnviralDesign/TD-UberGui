##### Similar to chopexec_lselect, however there is a lot less that happens on right click down and up.
##### So, this script will be much shorter. Really, the only thing we are handling here is the resetting of parameter values.

# define some operator references.
uv = op('null_uv_lselect')
webTop = op('WEB_RENDER')
webInfo = op('WEB_INFO')
tupleLookup = op('null_tupleLookup')
paramInfo = op('null_paramInfo')
dstOpsDat = op('null_dstOps')


def onOffToOn(channel, sampleIndex, val, prev):
	
	# get list of all current values and store.
	ValueState = list(map(str,paramInfo.col('value')))
	me.store('ValueState' , ValueState)
	
	# get the webRenderPick data.
	pikStr = webInfo['title',1].val
	pikDict = parent.Widget.ParseTitle(pikStr)

	# init some lists.
	InitPars = []
	InitVals = []
	
	# if picking data is valid.
	if pikDict != None:
		
		# calc the initial par name.
		initParName = str( pikDict["Par"] )
		
		# Edge Case #1 : User Right Clicked a label.
		if initParName.endswith('_l'):
			
			# Chop off suffix, and keep prefix
			initParName = initParName.replace('_l', '')
			
			# do a tuplet lookup, and get all params in that tuplet row.
			foundCells = tupleLookup.findCells(initParName, cols=['tupletname'])
			desiredParNames = [x.offset(0,1).val for x in foundCells]
			
			# now iterate through that tuplet row.
			for thisOp in dstOpsDat.rows():
				thisOp = op(thisOp[0])
				
				# for each param, reset to default.
				for parName in desiredParNames:
					
					foundParam = getattr( thisOp.par , parName , ':PAR_ERR:' )
					if foundParam != ':PAR_ERR:':
						InitVals += [ foundParam.eval() ]
						foundParam.val = foundParam.default
						InitPars += [ foundParam ]
	
	# store init pars and vals
	me.store('InitPars', InitPars)
	me.store('InitVals', InitVals)
	
	return

# nothing happens currently while right click is held down.
def whileOn(channel, sampleIndex, val, prev):
	return

# on right click release, we check to see if our values changed after the reset to default action.
# if they did, they we want to trigger the param changed script.
def onOnToOff(channel, sampleIndex, val, prev):
	
	ValueStateDown = me.fetch('ValueState')
	InitPars = me.fetch('InitPars')
	InitVals = me.fetch('InitVals')
	ValueStateUp = list(map(str,paramInfo.col('value')))
	if (ValueStateUp != ValueStateDown):
		parent.Widget.ParamChange(pars=InitPars, prevVals=InitVals)
	
	return