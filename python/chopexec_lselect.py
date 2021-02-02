##### This script is the primary driver for most of the UI's functionality with the mouse and left clicking.
##### It can launch menu pickers, drag sliders, reset parameters, open tooltips, etc.

# define some operator references.
uv = op('null_uv_lselect')
webTop = op('WEB_RENDER')
webInfo = op('WEB_INFO')
tupleLookup = op('null_tupleLookup')
paramInfo = op('null_paramInfo')
dstOpsDat = op('null_dstOps')


# OffToOn is the "DownClick", where we calculate a bunch of things, and do the hard work so
# the whileOn function can operate as quickly as possibly every frame down below.
# we use node storage on this node to store these initial values.
def onOffToOn(channel, sampleIndex, val, prev):
	
	# Get the html title, which contains the 'WebRenderPick' custom data.
	pikStr = webInfo['title',1].val
	pikDict = parent.Widget.ParseTitle(pikStr)
	me.store("pikDict" , pikDict)
	
	# If the user left clicked somewhere, we can be sure the auxilary UI stuffs should be closed, if not already.
	op('field').Close()
	op('menu').Close()
	op('colorpicker').Close()
	op('tooltip').Close()
	
	# first lets make sure our pikDict exists...
	if pikDict != None:
		
		# If it does, extract our mouse position, bottom pixel coord, and hovered element/Par name.
		initX = float( pikDict["X"] )
		initY = float( pikDict["Y"] )
		bottom = float( pikDict["bottom"] )
		initParName = str( pikDict["Par"] )
		
		# we only have 1 source object feeding our UI generation, but we could be addressing
		# the parameters of multiple objects ! get those object(s) now and store them.
		dstOps = [ x[0].val for x in dstOpsDat.rows() ]
		me.store("initOps" , dstOps)
		
		# get and store a list of the values of all the parameters in our source object.
		ValueState = list(map(str,paramInfo.col('value')))
		parent.Widget.store('ValueState' , ValueState)
		
		# now that our data is prepared, lets handle our numerous edge cases. The user might
		# have their mouse over a label, or maybe a spacer. They might also have it over a slider, etc.
		# Edge Case #1 : Labels.
		if initParName.endswith('_l'): # is a label.
			
			# take off the suffix, now that we are in label branch.
			initParName = initParName.replace('_l', '')

			# get the first matching parameter name, of the tuple. 
			# A parameter even if a single value param, is always part of a Tuple, so we can assume length of >= 1
			initParName = [ x.offset(0,1).val for x in tupleLookup.findCells(initParName , cols=[0]) ][0]
			
			# list comp convert our destination operators to a list of destimation parameters, then store it.
			foundPars = [ getattr( op(x).par , initParName , ":PAR_ERR:" ) for x in dstOps ]
			me.store("initPar" , foundPars)
			
			# determine the style of the parameter, and store it.
			style = paramInfo[initParName,'style']
			me.store("style" , style)
		
		# Edge Case #2 : Spacers - not much to do here.
		elif initParName == '_spacer_': # is a spacer
			
			me.store("parCick" , 0)
			me.store("style" , '')
		
		# Edge Case #3 : Tool Tip.
		elif initParName.endswith('_tt'): # is a tooltip.
			
			# take off the suffix, now that we are in this branch.
			toolTipName = initParName.replace('_tt', '')

			# get the first destination op, as the src for the tooltop.
			srcOp = op(dstOps[0])
			
			# if object exists, proceed.
			if srcOp != None:
				
				# get the ubergui config override dat. our tooltip should be in here.
				configFile = srcOp.op('Uberguiconfigoverride')
				
				# if the config file exists, proceed. NOTE: it doesn't have to exist.
				if configFile != None:
					
					# if it does exist, get the matching cell, which is the tooltip text.
					toolTip = configFile[ toolTipName , 1 ]
					
					# if the cell exists, we can launch the tooltip!
					# NOTE: it doesn't have to exist.
					if toolTip != None:
						op('tooltip').Launch( BOTTOM=bottom , MSG=toolTip.val )
		
		# Edge Case #4 : File or Folder Chooser.
		elif initParName.endswith('_fp'): # file or folder chooser.
			
			# take off the suffix, now that we are in this branch., get the param style.
			initParName = initParName.replace('_fp','')
			style = paramInfo[initParName,'style']

			# sub branch:
			if style == "File": # if file, launch file chooser.
				path = ui.chooseFile(title="choose a file.")
				
			elif style == "Folder": # if folder, launch folder chooser.
				path = ui.chooseFolder(title="choose a folder.")
			
			# for each of the destination objects, set the new path to the matching  parameter
			for each in dstOpsDat.rows():
				t = op(each[0])
				if t != None:
					foundPar = getattr( t.par , initParName , ":PAR_ERR:" )
				else:
					foundPar = ":PAR_ERR:"
				if foundPar != ":PAR_ERR:":
					foundPar.val = path
				
		# Edge Case #5 : Menu Picker.
		elif initParName.endswith('_mp'): # menu picker
			
			# take off the suffix, now that we are in this branch.
			initParName = initParName.replace('_mp','')
			
			# get some dimensions of our UI, so we can intelligently overlay our menu picker!
			left = parent.Widget.width/2
			right = float( pikDict["right"] )
			top = float( pikDict["top"] )
			bottom = float( pikDict["bottom"] )
			style = str( paramInfo[initParName,'style'] )
			
			# launch menu picker.
			op('menu').Launch( dstOps , initParName , left , right , bottom , top )
				
		# Edge Case #6 : Color Picker.
		elif initParName.endswith('_cp'): # color picker
			
			# take off the suffix, now that we are in this branch.
			initParName = initParName.replace('_cp','')
			
			# get some dimensions of our UI, so we can intelligently overlay our color picker!
			left = parent.Widget.width/2
			right = float( pikDict["right"] )
			top = float( pikDict["top"] )
			bottom = float( pikDict["bottom"] )
			style = str( paramInfo[initParName,'style'] )
			
			# launch color picker.
			op('colorpicker').Launch( dstOps , initParName , left , right , bottom , top )
		
		# Edge Case #7 : Everything else IE. widget parameter sliders!
		else: # is a widget.
			
			# store an indicator that we clicked an actual par, for later.
			me.store("parCick" , 1)
			
			# if init par existed, fetch style, and normmin and normmax from the paramInfo table.
			if paramInfo[initParName,'style'] != None:
				style = str( paramInfo[initParName,'style'] )
				normMin = float( paramInfo[initParName,'normmin'] )
				normMax = float( paramInfo[initParName,'normmax'] )
			
			# Otherwise, just nullify the variables.
			else:
				style = ''
				normMin = 0
				normMax = 0
			
			# try to get menu item list as a python list, if it fails, it's because it's not a menu param.
			try:
				menunames = eval( str(paramInfo[initParName,'menunames']) )
			except:
				menunames = []
			
			# using list comp, filter our destination operators down to ones that are real.
			foundDstOps = [ op(x) for x in dstOps if op(x) != None ]

			# list comp convert our dest ops to list of actual parameters.
			foundPars = [ getattr( dstOp.par , initParName , ":PAR_ERR:" ) for dstOp in foundDstOps ]

			# filter out pars that did not exist on some objects.
			foundPars = [ each for each in foundPars if each != ":PAR_ERR:" ]
			
			# store some initial x/y position values, and our parameter list. 
			# storing these paramters now means we don't have to re-look them up every frame during a drag. more efficient!
			me.store("initX" , initX)
			me.store("initY" , initY)
			me.store("initPar" , foundPars)

			# we also need the initial value of the parameter, so we know how much relative, we've adjusted the value.
			me.store('initVal' , [each.eval() for each in foundPars])
			
			# we also need some other attributes of our parameter during our drag operations, store those too.
			me.store("normMin" , normMin)
			me.store("normMax" , normMax)
			me.store("style" , style)
			me.store("menunames" , menunames)
			me.store("initParNAME" , initParName)
			
			# if the parameter style is one that can have a slider graphic, we need to set our DragOverlay to mask our active parameter.
			if style in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' , 'Int' , 'Menu' , 'StrMenu' ]:
				parent.Widget.Set_DragOverlay( webTop , 1 , initParName )
			
			# if the parameter style is one that is a button like par, that can have a state, we also want to enable the DragOverlay mask,
			# but really just so we're not dragging/affecting other params accidentally during a rushed drag/click.
			elif style in [ 'Momentary' , 'Toggle' ]:
				parent.Widget.Set_DragOverlay( webTop , 1 , initParName )
				for thisPar in foundPars:
					if thisPar != ":PAR_ERR:":
						
						# just invert the buttons state on this down click.
						thisPar.val = 1 - thisPar.eval()
			
			# if the parameter style is a pulse param, there is no state, but we still want to enable the DragOverlay mask.
			# so we're not dragging/affecting other params accidentally during a rushed drag/click.
			elif style in [ 'Pulse'  ]:
				
				parent.Widget.Set_DragOverlay( webTop , 1 , initParName )
				for thisPar in foundPars:
					if thisPar != ":PAR_ERR:":
						

						# just pulse the parameter, it's the only thing we can do with these types.
						thisPar.pulse()
	
	return

# now that we have done the hard work and stored some initial values, we can deal with our user's dragging actions performed
# while the left mouse button is pressed down!
def whileOn(channel, sampleIndex, val, prev):

	# Get the html title, which contains the 'WebRenderPick' custom data.
	pikStr = webInfo['title',1].val
	pikDict = parent.Widget.ParseTitle(pikStr)
	
	# ensure we're dealing with valid webRenderPick data!
	if pikDict != None:
		
		# get the initial par name, and the dragX position from the renderpick.
		initParName = str( pikDict["Par"] )
		dragX = float( pikDict["X"] )

		# determine if user has dragged mouse any at all.
		# a careful unmoving click is different logic than a moving drag.
		uDist = abs(uv['u'] - uv['rollu'])
		vDist = abs(uv['v'] - uv['rollv'])
		hasUserDraggedMouse = max(uDist,vDist) != 0

		# if user is dragging over a label, that is fine. we just want the prefix.
		if initParName.endswith('_l'):
			initParName = initParName.replace('_l', '')
		
		# if user is dragging over a tooltip, that is fine. we just want the prefix.
		elif initParName.endswith('_tt'):
			initParName = initParName.replace('_tt', '')
		
		# else, assume user is dragging over the parameter slider.
		else:
			pars = me.fetch("initPar" , [])

			# only proceed if we have at least 1 par. Should only have one anyways.
			if len(pars):
				
				# get the first par.
				par = pars[0]
				
				# make sure our pick data and par are valid.
				if pikStr != "" and par != ":PAR_ERR:":
					
					# fetch a bunch of our initial data stored during down click.
					initX = me.fetch("initX" , 0)
					initY = me.fetch("initY" , 0)
					normMin = me.fetch("normMin" , 0)
					normMax = me.fetch("normMax" , 1)
					style = me.fetch("style" , '')
					menunames = me.fetch("menunames" , [])

					# only proceed with this branch IF user has dragged mouse away from initial position.
					if hasUserDraggedMouse:
						
						# Edge Case #1 : any standard float value slider. We just remap from 0-1 to normMin-normMax
						if style in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' ]:
							newVal = tdu.remap( dragX , 0 , 1 , normMin , normMax )
							
							# set this value to all the pars of the selected objects.
							for each in pars:
								if each != ":PAR_ERR:":
									each.val = newVal
						
						# Edge Case #2 : any standard int value slider. We just remap from 0-1 to normMin-normMax, but then round it too.
						elif style in [ 'Int' ]:
							newVal = tdu.remap( dragX , 0 , 1 , normMin , normMax )
							newVal = round(newVal)
							
							# set this value to all the pars of the selected objects.
							for each in pars:
								if each != ":PAR_ERR:":
									each.val = newVal
						
						# Edge Case #3 : any fixed Menu param. We still remap from 0-1 to normMin-normMax, and round.
						elif style in [ 'Menu' ]:
							newVal = tdu.remap( dragX , 0 , 1 , 0 , len(menunames)-1 )
							newVal = int( round(newVal) )
							
							# thanks to menuIndex member, we can set menu's like an integer parameter.
							for each in pars:
								if each != ":PAR_ERR:":
									each.menuIndex = newVal
						
						# Edge Case #4 : any StrMenu param. We will set this the same as above, but leave this branch here
						# incase we want to add specifics to the StrMenu logic later.
						elif style in [ 'StrMenu' ]:
								
							newVal =  tdu.remap( dragX , 0 , 1 , 0 , len(menunames)-1 )
							newVal = int( round(newVal) )
							
							# thanks to menuIndex member, we can set menu's like an integer parameter.
							for each in pars:
								if each != ":PAR_ERR:":
									each.menuIndex = newVal
							
	return


# Most of the work is done, but the up click still has some logic stuffs that needs to happen.
def onOnToOff(channel, sampleIndex, val, prev):
	
	# Get the html title, which contains the 'WebRenderPick' custom data.
	pikStr = webInfo['title',1].val
	pikDict = parent.Widget.ParseTitle(pikStr)
	
	# fetch some of the things we stored on the down click.
	pars = me.fetch("initPar" , [])
	initVals = me.fetch("initVal" , [])
	dstOps = me.fetch("initOps" , [])
	ValueStateDown = parent.Widget.fetch('ValueState')
	
	# get the current state of the parameter.
	ValueStateUp = list(map(str,paramInfo.col('value')))
	
	# we want to call the Parameter Changed script, 
	# but should check to make sure the value has actually changed.
	if (ValueStateUp != ValueStateDown):
		parent.Widget.ParamChange( pars=pars, prevVals=initVals )
	
	# if we had a par..
	if len(pars) > 0:
		par = pars[0]
		
		# if our picking info was valid.
		if pikDict != None:
			
			# get the initial param name.
			initParName = str( pikDict["Par"] )
			
			# If the par name is not the Initial value we get after force restart ...
			if initParName != "INIT":
				
				# get the current X/Y and fetch style from storage.
				initX = float( pikDict["X"] )
				initY = float( pikDict["Y"] )
				style = me.fetch("style" , '')
				
				# we also want the NEXT par in line, as well as it's bounds incase user tabs.
				initParName2 = str( pikDict["Par2"] )
				left = float( pikDict["left2"] )
				right = float( pikDict["right2"] )
				top = float( pikDict["top2"] )
				bottom = float( pikDict["bottom2"] )
				
				# if the user is finishing a left click on a label, this means we want to launch the field for that parameter.
				if initParName.endswith('_l'):
					
					# of course, some parameter types don't have field support, lets make sure it's not one of those.
					if style not in [ 'Menu' , 'StrMenu' , 'Pulse' , 'Toggle' , 'Momentary' ]:
						
						# chop off the suffix, and keep the prefix.
						parTupletName = initParName.replace('_l','')

						# find the first parameter in the tuple, that the label matches. That's where we want to launch the field.
						matchingCells = [ x for x in tupleLookup.findCells(parTupletName , cols=[0]) ]
						matchingCells = [ x.offset(0,1).val for x in matchingCells ]
						initParName = matchingCells[0]
						
						# Launch the field.
						op('field').Launch( dstOps , initParName , left , right , bottom , top )
						parent.Widget.Mouse( webTop , x=0 , y=0 , targetPar=initParName2 )
				
				# If user finished a left click on a tooltip... do nothing (for now). place holder for later
				elif initParName.endswith('_tt'):
					pass
				
				# If user finished a left click on anything else...
				else:
					
					# if the finished click was a momentary button, be sure to set the value back to 0.
					# momentary buttons are unique in this way, easier to make a special catch here than
					# to change the logic more generally.
					if style in [ 'Momentary' , ]:
						par = me.fetch("initPar" , ":PAR_ERR:")
						if par != ":PAR_ERR:":
							par.val = 0

					# if the user finshed the left click for a Pulse, we can now call our param change script.
					# we needed to wait a bit to give the Pulse time to trigger whatever it triggered.
					elif style in [ 'Pulse' , ]:
						parent.Widget.ParamChange( pars=pars, prevVals=initVals )
			
			# if we get this from the gui, we should not act, we're probably setting enable flags.
			else:
				pass
		
		# finally, but only if our initial parameter was valid, set our DragOverlay mask back to off.
		if par != ":PAR_ERR:":
			initParName = par.name
			parent.Widget.Set_DragOverlay( webTop , 0 , initParName  )
	
	return