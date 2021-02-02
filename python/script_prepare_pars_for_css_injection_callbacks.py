def removeDups(seq):
	# remove dups while preserving order.
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]



def onCook(scriptOp):
	scriptOp.clear()
	StyleParsDat = scriptOp.inputs[0]

	# get a list of all parameters in the first column of the input dat, while mapping that list to strings instead of table cells.
	parNameCol = list(map(str,StyleParsDat.col(0)))[1::]

	# we are looking for two types of parameters, single value params, and then 3 value colors params (rgb).
	normalStylePars = []
	colorStylePars = []

	# iterate over each parameter name.
	for pName in parNameCol:
		
		# if a parameter ends with color[rgb], we add it to our color params list.
		if pName.endswith('colorr') or pName.endswith('colorg') or pName.endswith('colorb'):
			colorStylePars += [ pName ]
		
		# if it's anything else, just add it to the normal pars style list.
		else:
			normalStylePars += [ pName ]


	# lists to store final param names and values.
	p = []
	v = []

	# handling the regular pars is easy, just generate the unique identifier for find/replace later, and add the value.
	p += [ "|+|"+x+"|+|" for x in normalStylePars ]
	v += [ StyleParsDat[x,'value'] for x in normalStylePars ]


	# for color pars, we have to take every set of 3 par values that represent a color, and remap to 0-255, and put together into a string "R,G,B"
	parNameBase = [ x[0:-1] for x in colorStylePars ] # take off the last letter, which is the r, g or b.
	parNameBaseUnique = removeDups( parNameBase ) # now we will have duplicates, remove those while preserving order.
	parIdent = [ "|+|"+x+"|+|" for x in parNameBaseUnique ] # create the variable identifier - with out the rgb suffix.
	
	# list comp and generate our comma separated color strings.
	parColors = [ "%i,%i,%i"%( round(StyleParsDat[x+'r','value']*255) , round(StyleParsDat[x+'g','value']*255) , round(StyleParsDat[x+'b','value']*255) ) for x in parNameBaseUnique ]

	# add these to the final par/val lists.
	p += parIdent
	v += parColors
	
	# write it all out to the dat as two columns.
	scriptOp.appendCol( p )
	scriptOp.appendCol( v )
	

	return
