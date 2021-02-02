##### This script monitors lots of deeper parameter data from the source object, and when any of it changes,
##### it attempts to re-calculate the displayed value, and slider position if applicable. The parameter dat really
##### makes this process awesome, because it outputs min/max settings, section, menu names, etc which can alter
##### the range of a slider for instance.


def onRowChange(dat, rows):
	# define some things.
	SRC = op(op('null_srcOp')[0,0])
	uberGuiOverrideDat = SRC.op('Uberguiconfigoverride')
	data = []

	# iterate over all the table rows that changed..
	for rowID in rows:
		
		# collect some preliminary data bout the changed row/parameter.
		style = dat[rowID,'style'].val
		name  = dat[rowID,'name'].val
		tupletname  = dat[rowID,'tupletname'].val
		
		# just placeholders, we'll fill these in down below.
		value = ''
		slide = 0
		
		# Edge Case #1 : menu params. We want to display 
		# the selected item's menu label. so some lookup stuff happens for that.
		# then we calc the slider position based on the index of the chosen item.
		if style in [ 'Menu' , 'StrMenu' ]:
			menuindex = int(dat[rowID,'menuindex'])
			menulabels = dat[rowID,'menulabels'].val
			menulabels = eval(menulabels)
			try: # using try/except so that we can silently fail for StrMenu types.
				value = menulabels[menuindex]
				slide = tdu.remap( menuindex , 0 , len(menulabels)-1 , 0 , 1 )
			except: # if user puts in incorrect string to StrMenu, we just set to 0/blank.
				value = ''
				slide = 0
		
		# Edge Case #2 : buttons that can have state changes.
		# conveniently, the param DAT outputs menu items ['off', 'on'] even for buttons, so
		# we can take advantage of that for a value to show, and set our slider to 0% or 100%
		elif style in [ 'Momentary' , 'Toggle' ]:
			
			menuindex = int(dat[rowID,'value'])
			menulabels = dat[rowID,'menulabels'].val
			menulabels = eval(menulabels)
			value = menulabels[menuindex]
			slide = menuindex
		

		# Edge Case #3 : pulse buttons don't really have states, they just trigger things instantly.
		# So for these we want the slider to always be 0%, and the value to just be the param label.
		# this encourages developers to name the pulse button's label something action oriented, 
		# for instance "Open Window" or "Start Render", etc.
		elif style in [ 'Pulse' ]:
			
			value = dat[rowID,'label'].val
			slide = 0
			
		# Ok done with edge cases, we are able to process all other parameter types under this next logical branch!
		else:
			
			# get the custom user provided format of the parameter, if there is any.
			if uberGuiOverrideDat != None:
				CustomFormat = uberGuiOverrideDat[tupletname,'style'].val if uberGuiOverrideDat[tupletname,'style'] != None else None
				CustomFormat = CustomFormat if CustomFormat != '' else None
			else:
				CustomFormat = None
			
			 # If no custom format was specified, do the default thing.
			if CustomFormat == None:
				
				# try to treat it numerically, but if it fails, it's probably string based.
				try:
					value = float(dat[rowID,'value'])
					value = int(float(value) * 1000) / 1000
					normmin = float(dat[rowID,'normmin'])
					normmax = float(dat[rowID,'normmax'])
					slide = tdu.remap( value , normmin , normmax , 0 , 1 )
					
				# assuming it's a string.
				except:
					value = dat[rowID,'value'].val
					slide = 0
			
			# one of the custom ubergui override formats is Rgba255. 
			# This essentially allows you to work with color values as integers, in the range of 0-255.
			elif CustomFormat in [ 'Rgba255' ]:
				
				# try to treat it numerically, but if it fails, it's probably string based.
				try:
					value = float(dat[rowID,'value'])
					normmin = float(dat[rowID,'normmin'])
					normmax = float(dat[rowID,'normmax'])
					slide = tdu.remap( value , normmin , normmax , 0 , 1 )
					value = int(round(value * 255))
				
				# assuming it's a string.
				except:
					value = dat[rowID,'value'].val
					slide = 0

			# if CustomFormat is spaceToUnderscore or tduLegal this means we are working with a name parameter
			# or something like that, where we cannot have spaces. Since this script is dealing with display only values
			# it's assumed the string is already formatted correctly and this is just placeholder incase we need to 
			# do more with the display side of this edge case.
			elif CustomFormat in [ 'spaceToUnderscore' , 'tduLegal' ]:
				value = dat[rowID,'value'].val
				slide = 0

		# add the changed names, value, and slider pos to our data list
		data += [[ name , value , slide ]]

	# Update those changes to the web render top.
	parent.Widget.Update( op('WEB_RENDER') , data )
		
	return