##### This script is run any time the user scrolls their mouse wheel, A lot of different things
##### can happen depending on what the mouse is hovering over at that time, so this has some branching
##### logic to accomodate all of that.


import copy

# define some operator references.
webInfo = op('WEB_INFO')
paramInfo = op('null_paramInfo')
mod = op('null_mod')
scrollTimer = op('timer_scrollChange')
scrollTimerCallbacks = op('timer_scrollChange_callbacks')
dstOpsDat = op('null_dstOps')
delayedScrollSet = op('scrollSet_delayed')

# any time the mouse wheel value changes, this function is called.
def onValueChange(panelValue):
	
	# funny thing about the mouse wheel, is if you scroll a notch, you get a non-zero value, then a zero.
	# zero can obviously be calculated, but it's wasted cpu cycles since it doesn't do anything.
	# this if statement only executes a scroll IF the value is one of those non-zero ones.
	if panelValue != 0:
		
		# if user scrolls, assume they are either trying to scroll vertically, or adjust a slider.
		# so lets make sure all our auxiliary UI are closed.
		op('field').Close()
		op('menu').Close()
		op('colorpicker').Close()
		op('tooltip').Close()
		
		# cook modifiers CHOP. Nothing else has been requesting it.
		mod.cook(force=1)
		shift = int(mod['shift'])
		ctrl = int(mod['ctrl'])
		
		# if scroll timer is running, re-cue it.
		if scrollTimer['running'] == 1:
			scrollTimer.par.cuepulse.pulse()
		
		# if scroll timer has ended, get the current parameter values
		# and store them for now as latest, and restart scrolltimer.
		else:
			ValueState = list(map(str,paramInfo.col('value')))
			parent.Widget.store('ValueState' , ValueState)
			scrollTimer.par.start.pulse()
		
		# parse our webRenderPick dat.
		pikStr = webInfo['title',1].val
		pikDict = parent.Widget.ParseTitle(pikStr)
		
		# make sure our renderpick data is valid.
		if pikDict != None:
			
			# get the parameter we're hovering over.
			initParName = str( pikDict["Par"] )
			
			# if user scrolled on a label, proceed.
			if initParName.endswith('_l'):
				
				# chop off suffix, and keep prefix
				initParName = initParName.replace('_l', '')
				
			# if user scrolled on an actual paramter slider, proceed.
			else:
				
				# get some relevant info, numeric range, style, and menu names if it exists.
				normMin = float( paramInfo[initParName,'normmin'] or 0 )
				normMax = float( paramInfo[initParName,'normmax'] or 0 )
				style = str( paramInfo[initParName,'style'] )
				try:
					menunames = eval( str(paramInfo[initParName,'menunames']) )
				except:
					menunames = []
				
				# scale down the default StepSize by factor of 50.
				# TODO: make this default more meaningful or parameter specific?
				normStepSize = (normMax - normMin) / 50

				# init some lists.
				initPars = []
				initVals = []
				
				# iterate through all of the destination operators.
				for thisOp in dstOpsDat.rows():
					thisOp = op(thisOp[0])
					
					# if operator exists, get the parameter we're trying to adjust.
					if thisOp != None:
						foundPar = getattr( thisOp.par , initParName , ":PAR_ERR:" )
					else:
						foundPar = ":PAR_ERR:"
					

					# now, if that parameter exists too... proceed.
					if foundPar != ":PAR_ERR:":
						
						# if we're scrolling pretty much any float/numeric parameter we handle it like this.
						if style in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'WH' , 'XY' , 'XYZ' ]:
							
							# for shift, we scroll more, x10
							if shift:
								increment = panelValue * normStepSize * 10
							
							# for ctrl, we scroll less, /10
							elif ctrl:
								increment = panelValue * normStepSize * .1
							
							# else if no modifiers, we just scroll the normal amount.
							else:
								increment = panelValue * normStepSize

							# get the current value of the par right now.
							curVal = foundPar.eval()

							# add these to the initpar list and initval list.
							initPars += [ foundPar ]
							initVals += [ curVal ]

							# calculate the new value, current plus increment
							newVal = curVal + increment
							foundPar.val = newVal
						
						# scrolling ints are a bit different. 
						if style in [ 'Int' ]:
							
							# we mult our increments by whole numbers, only up.
							# this usually works well as integers are not usually spatial, 
							# and thus smaller increments makes sense.
							if shift:
								increment = panelValue * 10
							elif ctrl:
								increment = panelValue * 2
							else:
								increment = panelValue * 1
							
							# get the current value of the par right now, increment, and set.
							curVal = foundPar.eval()
							newVal = curVal + increment
							foundPar.val = newVal
						
						# scrolling menus are similar to ints, but no modifiers are used. the increment is always factor of 1.
						elif style in [ 'Menu' ]:
							increment = panelValue
							curVal = foundPar.eval()
							foundPar.menuIndex = tdu.clamp( foundPar.menuIndex + increment , 0 , len(menunames)-1 )
							
						# scrolling strmenus are similar, but a bit more annoying since the str may not exist in the menuNames list.
						# so we have some extra try/catch logic to reset things to the first item, if there are no valid ones.
						elif style in [ 'StrMenu' ]:
							increment = panelValue
							curVal = foundPar.eval()
							if curVal == '':
								curVal = 0
							try:
								curVal = int(curVal)
								chosemMenuName = menunames[curVal]
							except:
								chosemMenuName = curVal
							
							curMenuIndex = menunames.index(chosemMenuName)
							newIndex = tdu.clamp( curMenuIndex + increment , 0 , len(menunames)-1 )
							
							foundPar.val = menunames[newIndex]

				# store the latest pars and values.
				me.store('initPar', initPars)
				me.store('initVal', initVals)
		
	return
	