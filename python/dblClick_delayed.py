##### This is called when user doubleclicks anywhere in the UI. Most places do not have 
##### doubleclick functionality, but if the user double clicks in certain types of parameters
##### like a numeric value field, this will launch the field, and they can enter a value by hand.


# define some operator references.
webInfo = op('WEB_INFO')
srcOpDat = op('null_srcOp')
dstOpsDat = op('null_dstOps')
paramInfo = op('null_paramInfo')

# parse webRenderPick data.
pikStr = webInfo['title',1].val
pikDict = op('chopexec_lselect').fetch("pikDict",{})

# get the initial par name.
initParName = str( pikDict.get("Par","") )

# nothing happens if the user dbl clicks on a label.
if initParName.endswith('_l'):
	pass

# nothing happens if the user dbl clicks on a tooltip.
elif initParName.endswith('_tt'):
	pass

# this is a troubleshooting branch. this message shouldn't happen, but if it does indicates where the problem lies.
elif initParName == '_dragOverlayRight_':
	debug('Couldnt launch UI for %s'%(initParName))

# if we're here, it's assumed the user dbl clicked on an actual parameter.
else:
	
	# if param and pik is valid...
	if pikDict != None and initParName != "":
		
		# get some info about the parameter user dbl clickedo n.
		left = float( pikDict["left"] )
		right = float( pikDict["right"] )
		top = float( pikDict["top"] )
		bottom = float( pikDict["bottom"] )
		initParName = str( pikDict["Par"] )
		style = str( paramInfo[initParName,'style'] )
		
		# only proceed if the parameter style is one that supports field entry.
		if style not in [ 'Menu' , 'StrMenu' , 'Pulse' , 'Toggle' , 'Momentary' ]:
			
			# get all the destination objects.
			dstOps = [ x.path for x in map(op,dstOpsDat.col(0)) if x != None ]

			# if there is at least one destination object, Launch the field.
			if len(dstOps):
				op('field').Launch_Delayed( dstOps , initParName , left , right , bottom , top , 0 )

# '''