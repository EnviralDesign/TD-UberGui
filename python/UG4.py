import json
import traceback

class UG4:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.paramInfo = op('null_paramInfo')
		self.webInfo = op('WEB_INFO')
		self.webRenderTop = op('WEB_RENDER')
		self.scrollTimer = op('timer_scrollChange')
		self.srcOpDat = op('null_srcOp')
		self.dstOpsDat = op('null_dstOps')
		self.tupleLookup = op('null_tupleLookup')
		self.publicLookup = op('null_public')
		self.delayedDoubleClick = op('delayed_double_click')
		self.delayedLeftClickDown = op('delayed_left_click_down')
		self.delayedLeftClickUp = op('delayed_left_click_up')
		self.uvLselect = op('null_uv_lselect')

		self.fieldCOMP = op('field')
		self.menuCOMP = op('menu')
		self.colorpickerCOMP = op('colorpicker')
		
		
	def Regenerate(self, SRC ):
		'''
		This function rebuils the entire HTML body of text from the custom parameter data coming from the source object.
		'''
		# define some things.
		HTML = op('PRE_HTML')
		HTML_FINAL = op('HTML')
		
		# reset some things.
		HTML = ''
		discoveredPages = []
		TILES = {}
		
		if SRC != None:
			
			uberGuiOverrideDat = SRC.op('Uberguiconfigoverride')
			
			publicPageNames = self.publicLookup.row(1)[0].val.split(',')
			parTuplets = [ x for x in SRC.customTuplets if x[0].enable == True and x[0].page.name in publicPageNames ]
			
			FirstHeader = 1
			
			for ID,tuplet in enumerate(parTuplets):
				
				# Generate section label.
				PAGE = tuplet[0].page.name
				if PAGE not in discoveredPages:
					discoveredPages += [ PAGE ]
					
					if FirstHeader == 0:
						HTML += "<div class='spacer_header' id='_spacer_' ></div>\n\n"
					FirstHeader = 0
					
					HTML += "<div class='header_container' id='%s_p'>%s</div>\n\n"%(PAGE,PAGE)
				
				# Get name of tuplet. 
				tupletName = tuplet[0].tupletName
				tupletLabel = tuplet[0].label
				tupletSection = tuplet[0].startSection
				tupletStyle = tuplet[0].style
				
				# get the custom format of the parameter, if there is any.
				if uberGuiOverrideDat != None:
					CustomFormat = uberGuiOverrideDat[tupletName,'style'].val if uberGuiOverrideDat[tupletName,'style'] != None else None
					CustomFormat = CustomFormat if CustomFormat != '' else None
				else:
					CustomFormat = None
				
				if tupletSection == 1:
					HTML += "<div class='spacer_section' id='_spacer_' ></div>\n\n"
				
				isSingle = len(tuplet) == 1
				# Generate the container for the entire widget row.
				
				if ID >= len(parTuplets)-1: # if this is the last widget...
					HTML += '<div class="widget_container" id="_lastWidget_">\n'
				else:
					HTML += '<div class="widget_container">\n'
				
				
				if tupletStyle in [ 'Pulse' ]:
					# Generate the label for the widget row. this is based on the tuplet name, and occupies the left side.
					HTML += "  <div class='widget_label' id='%s_l' style='display:none' >%s</div>\n"%( tupletName , tupletLabel )
				else:
					# Generate the label for the widget row. this is based on the tuplet name, and occupies the left side.
					HTML += "  <div class='widget_label' id='%s_l'>%s</div>\n"%( tupletName , tupletLabel )
					
				
				# Generate the tool tip hoverable div container.
				HTML += "    <div class='widget_tooltip' id='%s_tt'>&quest;</div>\n"%( tupletName )
				
				
				
				if tupletStyle in [ 'Pulse' ]:
					# Generate the label for the widget row. this is based on the tuplet name, and occupies the left side.
					HTML += "  <div class='widget_body' id='%s_b' style='width:100%%'>\n"%( tupletName )
				else:
					# Generate the value widget area, which occupies the right side. This can contain one or more widget sliders.
					HTML += "  <div class='widget_body' id='%s_b'>\n"%( tupletName )

				
				
				
				# for each parameter in the row tuplet. Most of the time this will only be 1 anyways. RGB for ex can have 3 though.
				for parIndex,par in enumerate(tuplet):
					
					# for menu type params, we need to handle things a bit differently.
					if par.style in [ 'Menu' , 'StrMenu' ]:
						
						# try to identify which menu index we have. strMenu's have the ability to silently error, so try/except catches that.
						try:
							labelIndex = par.menuNames.index(par.eval())
							label = par.menuLabels[labelIndex]
						except:
							labelIndex = 0
							label = ''
						
						# create the wrapper container for the parameter widget.
						HTML += "    <div class='widget_item' id='%s' >\n"%( par.name )
						
						# calculate and generate slider width as a percentage.
						widthPercentage = tdu.remap( labelIndex , 0 , len(par.menuLabels)-1 , 0 , 100 )
						HTML += "      <div class='widget_slider' id='%s_s' style='width:%i%%' ></div>\n"%( par.name , int(widthPercentage) )
						
						# draw the text over the slider graphic.
						HTML += "      <div class='widget_text' id='%s_t' >%s</div>\n"%( par.name , label )
						
						HTML += "    </div>\n"
					
					elif par.style in [ 'Momentary' , 'Toggle' ]:
						
						labelIndex = par.eval()
						label = par.menuLabels[labelIndex]
						
						# create the wrapper container for the parameter widget.
						HTML += "    <div class='widget_item' id='%s' >\n"%( par.name )
						
						# calculate and generate slider width as a percentage.
						widthPercentage = tdu.remap( labelIndex , 0 , len(par.menuLabels)-1 , 0 , 100 )
						HTML += "      <div class='widget_slider' id='%s_s' style='width:%i%%' ></div>\n"%( par.name , int(widthPercentage) )
						
						# draw the text over the slider graphic.
						HTML += "      <div class='widget_text' id='%s_t' >%s</div>\n"%( par.name , label )
						
						HTML += "    </div>\n"
					
					elif par.style in [ 'Pulse' ]:
						
						label = "Pulse"
						
						# create the wrapper container for the parameter widget.
						HTML += "    <div class='widget_item' id='%s' >\n"%( par.name )
						
						# draw the text over the slider graphic.
						HTML += "      <div class='widget_text' id='%s_t' style='text-align: center;' >%s</div>\n"%( par.name , par.label )
						
						HTML += "    </div>\n"
						
					
					# if we're dealing with anything else...
					else:
						
						# if we're dealing with float type parameters.
						val = par.eval()

						
						
						# create the wrapper container for the parameter widget.
						HTML += "    <div class='widget_item' id='%s' >\n"%( par.name )
						
						if par.style in [ 'Float', 'RGB', 'RGBA', 'UV' , 'UVW' , 'WH'  , 'XY'  , 'XYZ' ]:
							widthPercentage = tdu.remap( val , par.min , par.max , 0 , 100 )
							HTML += "      <div class='widget_slider' id='%s_s' style='width:%i%%' ></div>\n"%( par.name , int(widthPercentage) )
							
						
							if CustomFormat == None:
								
								if self.IsStringFloat(val) == True:
									val = int(float(val) * 1000) / 1000
								
								HTML += "      <div class='widget_text' id='%s_t' >%s</div>\n"%( par.name , val )
							elif CustomFormat in [ 'Rgba255' ]:
								
								HTML += "      <div class='widget_text' id='%s_t' >%s</div>\n"%( par.name , int(round(val*255)) )
								
								
						elif par.style in [ 'Int' ]:
								widthPercentage = tdu.remap( val , par.min , par.max , 0 , 100 )
								HTML += "      <div class='widget_slider' id='%s_s' style='width:%i%%' ></div>\n"%( par.name , int(widthPercentage) )
								
								val = int(val)
								HTML += "      <div class='widget_text' id='%s_t' >%s</div>\n"%( par.name , val )
							
						else:
							HTML += "      <div class='widget_text' id='%s_t' >%s</div>\n"%( par.name , val )
							
						
						HTML += "    </div>\n"
				
				
				if tupletStyle in [ 'RGB' , 'RGBA' ]:
					# create the wrapper container for the parameter widget.
					HTML += "    <div class='widget_ItemChooser' id='%s_cp' >\n"%( tuplet[0].name ) # cp == colorPicker
					HTML += "    ...</div>\n"
				
				
				elif par.style in [ 'Menu' , 'StrMenu' ]:
					# create the wrapper container for the parameter widget.
					HTML += "    <div class='widget_ItemChooser' id='%s_mp' >\n"%( tuplet[0].name ) # mp == menuPicker
					HTML += "    ...</div>\n"
				
				
				elif tupletStyle in [ 'File' , 'Folder' ]:
					# create the wrapper container for the parameter widget.
					HTML += "    <div class='widget_ItemChooser' id='%s_fp' >\n"%( tuplet[0].name ) # fp == file/folder picker
					HTML += "    ...</div>\n"
				
				
				HTML += "  </div>\n"
				
				HTML += '</div>\n\n'
			
			
		
			HTML_FINAL.text = HTML
			
		else:
			HTML_FINAL.text = ''
	
	
	def ParseTitle(self,titleStr):
		'''
		Parse the title tag of the html, into a python dictionary.
		'''
		try:
			op('WEB_INFO').cook(force=1)
			return { pair.split(':')[0]:pair.split(':')[1] for pair in titleStr.split(',') }
		except:
			return None
	
	def Update_Changed_Params( self , rows ):
		'''
		This function monitors lots of deeper parameter data from the source object, and when any of it changes,
		it attempts to re-calculate the displayed value, and slider position if applicable. The parameter dat really
		makes this process awesome, because it outputs min/max settings, section, menu names, etc which can alter
		the range of a slider for instance.
		'''

		# define some things.
		SRC = op(self.srcOpDat[0,0])
		uberGuiOverrideDat = SRC.op('Uberguiconfigoverride')
		data = []

		# iterate over all the table rows that changed..
		for rowID in rows:
			
			# collect some preliminary data bout the changed row/parameter.
			style = self.paramInfo[rowID,'style'].val
			name  = self.paramInfo[rowID,'name'].val
			tupletname  = self.paramInfo[rowID,'tupletname'].val
			
			# just placeholders, we'll fill these in down below.
			value = ''
			slide = 0
			
			# Edge Case #1 : menu params. We want to display 
			# the selected item's menu label. so some lookup stuff happens for that.
			# then we calc the slider position based on the index of the chosen item.
			if style in [ 'Menu' , 'StrMenu' ]:
				menuindex = int(self.paramInfo[rowID,'menuindex'])
				menulabels = self.paramInfo[rowID,'menulabels'].val
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
				
				menuindex = int(self.paramInfo[rowID,'value'])
				menulabels = self.paramInfo[rowID,'menulabels'].val
				menulabels = eval(menulabels)
				value = menulabels[menuindex]
				slide = menuindex
			

			# Edge Case #3 : pulse buttons don't really have states, they just trigger things instantly.
			# So for these we want the slider to always be 0%, and the value to just be the param label.
			# this encourages developers to name the pulse button's label something action oriented, 
			# for instance "Open Window" or "Start Render", etc.
			elif style in [ 'Pulse' ]:
				
				value = self.paramInfo[rowID,'label'].val
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
						value = float(self.paramInfo[rowID,'value'])
						value = int(float(value) * 1000) / 1000
						normmin = float(self.paramInfo[rowID,'normmin'])
						normmax = float(self.paramInfo[rowID,'normmax'])
						slide = tdu.remap( value , normmin , normmax , 0 , 1 )
						
					# assuming it's a string.
					except:
						value = self.paramInfo[rowID,'value'].val
						slide = 0
				
				# one of the custom ubergui override formats is Rgba255. 
				# This essentially allows you to work with color values as integers, in the range of 0-255.
				elif CustomFormat in [ 'Rgba255' ]:
					
					# try to treat it numerically, but if it fails, it's probably string based.
					try:
						value = float(self.paramInfo[rowID,'value'])
						normmin = float(self.paramInfo[rowID,'normmin'])
						normmax = float(self.paramInfo[rowID,'normmax'])
						slide = tdu.remap( value , normmin , normmax , 0 , 1 )
						value = int(round(value * 255))
					
					# assuming it's a string.
					except:
						value = self.paramInfo[rowID,'value'].val
						slide = 0

				# if CustomFormat is spaceToUnderscore or tduLegal this means we are working with a name parameter
				# or something like that, where we cannot have spaces. Since this script is dealing with display only values
				# it's assumed the string is already formatted correctly and this is just placeholder incase we need to 
				# do more with the display side of this edge case.
				elif CustomFormat in [ 'spaceToUnderscore' , 'tduLegal' ]:
					value = self.paramInfo[rowID,'value'].val
					slide = 0

			# add the changed names, value, and slider pos to our data list
			data += [[ name , value , slide ]]

		# Update those changes to the web render top.
		self.Update( op('WEB_RENDER') , data )

		return

	def Update(self , webRenderTop , flatArgList ):
		
		jsonArgsList = json.dumps(flatArgList).replace("'", '"')
		script = "Update_('{0}')".format(jsonArgsList)
		
		try:
			webRenderTop.executeJavaScript(script)
		except:
			pass


	def Mouse(self , webRenderTop , x=0, y=0 , targetPar='' , mouse=False ):
		
		argDict = {'x':x, 'y':y , 'par':targetPar}
		jsonArgsList = json.dumps(argDict).replace("'", '"')

		script = "Mouse_('{0}')".format(jsonArgsList)
		webRenderTop.executeJavaScript(script)
		webRenderTop.interactMouse( x , self.ownerComp.height-y , pixels=True , left=mouse )


	def Interact_LeftClick_Down( self ):
		'''
		Interact_LeftClick_Down is the "DownClick", where we calculate a bunch of things, and do the hard work so
		the _While function can operate as quickly as possibly every frame down below.
		we use node storage to store these initial values.
		'''

		# Get the html title, which contains the 'WebRenderPick' custom data.
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)
		self.ownerComp.store("pikDict" , pikDict)
		
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
			# initParValue = self.paramInfo[initParName,'value'].val if self.paramInfo[initParName,'menuindex'].val == '' else self.paramInfo[initParName,'menuindex'].val
			
			# we only have 1 source object feeding our UI generation, but we could be addressing
			# the parameters of multiple objects ! get those object(s) now and store them.
			dstOps = [ x[0].val for x in self.dstOpsDat.rows() ]
			self.ownerComp.store("initOps" , dstOps)
			
			# get and store a list of the values of all the parameters in our source object.
			ValueState = list(map(str,self.paramInfo.col('value')))
			self.ownerComp.store('ValueState' , ValueState)
			
			# now that our data is prepared, lets handle our numerous edge cases. The user might
			# have their mouse over a label, or maybe a spacer. They might also have it over a slider, etc.
			# Edge Case #1 : Labels.
			if initParName.endswith('_l'): # is a label.
				
				# take off the suffix, now that we are in label branch.
				initParName = initParName.replace('_l', '')

				# get the first matching parameter name, of the tuple. 
				# A parameter even if a single value param, is always part of a Tuple, so we can assume length of >= 1
				initParName = [ x.offset(0,1).val for x in self.tupleLookup.findCells(initParName , cols=[0]) ][0]
				
				# list comp convert our destination operators to a list of destimation parameters, then store it.
				foundPars = [ getattr( op(x).par , initParName , ":PAR_ERR:" ) for x in dstOps ]
				self.ownerComp.store("initPar" , foundPars)
				
				# determine the style of the parameter, and store it.
				style = self.paramInfo[initParName,'style']
				self.ownerComp.store("style" , style)
			
			# Edge Case #2 : Spacers - not much to do here.
			elif initParName == '_spacer_': # is a spacer
				
				self.ownerComp.store("parCick" , 0)
				self.ownerComp.store("style" , '')
			
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
				style = self.paramInfo[initParName,'style']

				# sub branch:
				if style == "File": # if file, launch file chooser.
					path = ui.chooseFile(title="choose a file.")
					
				elif style == "Folder": # if folder, launch folder chooser.
					path = ui.chooseFolder(title="choose a folder.")
				
				# for each of the destination objects, set the new path to the matching  parameter
				for each in self.dstOpsDat.rows():
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
				left = (self.ownerComp.par.Labelvaluesplit.eval() * ( (self.ownerComp.width-self.ownerComp.par.Scrollbarwidth.eval()) / self.ownerComp.width )) * self.ownerComp.width
				right = float( pikDict["right"] )
				top = float( pikDict["top"] )
				bottom = float( pikDict["bottom"] )
				style = str( self.paramInfo[initParName,'style'] )
				
				# launch menu picker.
				op('menu').Launch( dstOps , initParName , left , right , bottom , top )
					
			# Edge Case #6 : Color Picker.
			elif initParName.endswith('_cp'): # color picker
				
				# take off the suffix, now that we are in this branch.
				initParName = initParName.replace('_cp','')
				
				# get some dimensions of our UI, so we can intelligently overlay our color picker!
				left = (self.ownerComp.par.Labelvaluesplit.eval() * ( (self.ownerComp.width-self.ownerComp.par.Scrollbarwidth.eval()) / self.ownerComp.width )) * self.ownerComp.width
				right = float( pikDict["right"] )
				top = float( pikDict["top"] )
				bottom = float( pikDict["bottom"] )
				style = str( self.paramInfo[initParName,'style'] )
				
				# launch color picker.
				op('colorpicker').Launch( dstOps , initParName , left , right , bottom , top )


			# Edge Case #7 : nothing happens if the user dbl clicks on a page header.
			elif initParName.endswith('_p'):
				pass
			
			# Edge Case #7 : Everything else IE. widget parameter sliders!
			else: # is a widget.
				
				# store an indicator that we clicked an actual par, for later.
				me.store("parCick" , 1)
				
				# if init par existed, fetch style, and normmin and normmax from the paramInfo table.
				if self.paramInfo[initParName,'style'] != None:
					style = str( self.paramInfo[initParName,'style'] )
					normMin = float( self.paramInfo[initParName,'normmin'] )
					normMax = float( self.paramInfo[initParName,'normmax'] )
				
				# Otherwise, just nullify the variables.
				else:
					style = ''
					normMin = 0
					normMax = 0
				
				# try to get menu item list as a python list, if it fails, it's because it's not a menu param.
				try:
					menunames = eval( str(self.paramInfo[initParName,'menunames']) )
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
				self.ownerComp.store("initX" , initX)
				self.ownerComp.store("initY" , initY)
				self.ownerComp.store("initPar" , foundPars)

				# we also need the initial value of the parameter, so we know how much relative, we've adjusted the value.
				self.ownerComp.store('initVal' , [each.eval() for each in foundPars])
				
				# we also need some other attributes of our parameter during our drag operations, store those too.
				self.ownerComp.store("normMin" , normMin)
				self.ownerComp.store("normMax" , normMax)
				self.ownerComp.store("style" , style)
				self.ownerComp.store("menunames" , menunames)
				self.ownerComp.store("initParNAME" , initParName)
				
				# if the parameter style is one that can have a slider graphic, we need to set our DragOverlay to mask our active parameter.
				if style in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' , 'Int' , 'Menu' , 'StrMenu' ]:
					# print('ddfgfj',initParName)
					self.Set_DragOverlay( self.webRenderTop , 1 , initParName )
				
				# if the parameter style is one that is a button like par, that can have a state, we also want to enable the DragOverlay mask,
				# but really just so we're not dragging/affecting other params accidentally during a rushed drag/click.
				elif style in [ 'Momentary' , 'Toggle' ]:
					self.Set_DragOverlay( self.webRenderTop , 1 , initParName )
					for thisPar in foundPars:
						if thisPar != ":PAR_ERR:":
							
							# just invert the buttons state on this down click.
							thisPar.val = 1 - thisPar.eval()
				
				# if the parameter style is a pulse param, there is no state, so no drag overlay..
				elif style in [ 'Pulse'  ]:
					
					# self.Set_DragOverlay( self.webRenderTop , 1 , initParName )
					for thisPar in foundPars:
						if thisPar != ":PAR_ERR:":
							

							# just pulse the parameter, it's the only thing we can do with these types.
							thisPar.pulse()
		
		return


	def Interact_LeftClick_While( self , uDist , vDist , inputType ):
		'''
		Now that we have done the hard work and stored some initial values, we can deal 
		with our user's dragging actions performed while the left mouse button is pressed down.
		'''
		# return
		# Get the html title, which contains the 'WebRenderPick' custom data.
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)
		
		# ensure we're dealing with valid webRenderPick data!
		if pikDict != None:
			
			# get the initial par name, and the dragX position from the renderpick.
			initParName = str( pikDict["Par"] )
			
			if inputType == 'mouse':
				dragX = float( pikDict["X"] )
			elif inputType == 'touch':
				leftEdge = float( pikDict["left"] )
				rightEdge = float( pikDict["right"] )
				dragX = float( uDist )
				dragX = dragX * self.ownerComp.width
				dragX = tdu.clamp( dragX , leftEdge , rightEdge )
				dragX = tdu.remap( dragX, leftEdge , rightEdge, 0 , 1 )

			# determine if user has dragged mouse any at all.
			# a careful unmoving click is different logic than a moving drag.
			uDistAbs = abs(uDist)
			vDistAbs = abs(vDist)
			hasUserDraggedMouse = max(uDistAbs,vDistAbs) != 0

			# print(hasUserDraggedMouse)

			# if user is dragging over a label, that is fine. we just want the prefix.
			if initParName.endswith('_l'):
				initParName = initParName.replace('_l', '')
			
			# if user is dragging over a tooltip, that is fine. we just want the prefix.
			elif initParName.endswith('_tt'):
				initParName = initParName.replace('_tt', '')

			# nothing happens if the user dbl clicks on a page header.
			elif initParName.endswith('_p'):
				pass
			
			# else, assume user is dragging over the parameter slider.
			else:
				pars = self.ownerComp.fetch("initPar" , [])

				# only proceed if we have at least 1 par. Should only have one anyways.
				if len(pars):
					
					# get the first par.
					par = pars[0]
					
					# make sure our pick data and par are valid.
					if pikStr != "" and par != ":PAR_ERR:":
						
						# fetch a bunch of our initial data stored during down click.
						initX = self.ownerComp.fetch("initX" , 0)
						initY = self.ownerComp.fetch("initY" , 0)
						normMin = self.ownerComp.fetch("normMin" , 0)
						normMax = self.ownerComp.fetch("normMax" , 1)
						style = self.ownerComp.fetch("style" , '')
						menunames = self.ownerComp.fetch("menunames" , [])

						# only proceed with this branch IF user has dragged mouse away from initial position.
						if hasUserDraggedMouse:
							# Edge Case #1 : any standard float value slider. We just remap from 0-1 to normMin-normMax
							if style in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' ]:

								newVal = tdu.remap( dragX , 0 , 1 , normMin , normMax )#  + float(initParValue)
								
								# set this value to all the pars of the selected objects.
								for each in pars:
									if each != ":PAR_ERR:":
										each.val = newVal
							
							# Edge Case #2 : any standard int value slider. We just remap from 0-1 to normMin-normMax, but then round it too.
							elif style in [ 'Int' ]:
								newVal = tdu.remap( dragX , 0 , 1 , normMin , normMax )#  + int(initParValue)
								newVal = round(newVal)
								
								# set this value to all the pars of the selected objects.
								for each in pars:
									if each != ":PAR_ERR:":
										each.val = newVal
							
							# Edge Case #3 : any fixed Menu param. We still remap from 0-1 to normMin-normMax, and round.
							elif style in [ 'Menu' ]:
								newVal = tdu.remap( dragX , 0 , 1 , 0 , len(menunames)-1 )#  + int(initParValue)
								newVal = int( round(newVal) )
								
								# thanks to menuIndex member, we can set menu's like an integer parameter.
								for each in pars:
									if each != ":PAR_ERR:":
										each.menuIndex = newVal
							
							# Edge Case #4 : any StrMenu param. We will set this the same as above, but leave this branch here
							# incase we want to add specifics to the StrMenu logic later.
							elif style in [ 'StrMenu' ]:
									
								newVal =  tdu.remap( dragX , 0 , 1 , 0 , len(menunames)-1 )#  + int(initParValue)
								newVal = int( round(newVal) )
								
								# thanks to menuIndex member, we can set menu's like an integer parameter.
								for each in pars:
									if each != ":PAR_ERR:":
										each.menuIndex = newVal
		return


	def Interact_LeftClick_Up( self , asMouse=True):
		'''
		# Most of the work is done, but the up click still has some logic stuffs that needs to happen.
		'''

		# Get the html title, which contains the 'WebRenderPick' custom data.
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)
		
		# fetch some of the things we stored on the down click.
		pars = self.ownerComp.fetch("initPar" , [])
		initVals = self.ownerComp.fetch("initVal" , [])
		dstOps = self.ownerComp.fetch("initOps" , [])
		ValueStateDown = self.ownerComp.fetch('ValueState',[])
		
		# get the current state of the parameter.
		ValueStateUp = list(map(str,self.paramInfo.col('value')))
		
		# we want to call the Parameter Changed script, 
		# but should check to make sure the value has actually changed.
		if (ValueStateUp != ValueStateDown):
			self.ownerComp.ParamChange( pars=pars, prevVals=initVals )
		
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
					style = self.ownerComp.fetch("style" , '')
					
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
							matchingCells = [ x for x in self.tupleLookup.findCells(parTupletName , cols=[0]) ]
							matchingCells = [ x.offset(0,1).val for x in matchingCells ]
							initParName = matchingCells[0]
							
							# Launch the field.
							if asMouse == True:
								op('field').Launch( dstOps , initParName , left , right , bottom , top )
								self.ownerComp.Mouse( self.webRenderTop , x=0 , y=0 , targetPar=initParName2 )
					
					# If user finished a left click on a tooltip... do nothing (for now). place holder for later
					elif initParName.endswith('_tt'):
						pass

					# nothing happens if the user dbl clicks on a page header.
					elif initParName.endswith('_p'):
						pass
					
					# If user finished a left click on anything else...
					else:
						
						# if the finished click was a momentary button, be sure to set the value back to 0.
						# momentary buttons are unique in this way, easier to make a special catch here than
						# to change the logic more generally.
						if style in [ 'Momentary' , ]:
							if par != ":PAR_ERR:":
								par.val = 0

						# if the user finshed the left click for a Pulse, we can now call our param change script.
						# we needed to wait a bit to give the Pulse time to trigger whatever it triggered.
						elif style in [ 'Pulse' , ]:
							self.ParamChange( pars=pars, prevVals=initVals )
				
				# if we get this from the gui, we should not act, we're probably setting enable flags.
				else:
					pass
			
			# finally, but only if our initial parameter was valid, set our DragOverlay mask back to off.
			if par != ":PAR_ERR:":
				initParName = par.name
				self.Set_DragOverlay( self.webRenderTop , 0 , initParName  )

		return


	def Interact_RightClick_Down( self ):
		
		# get list of all current values and store.
		ValueState = list(map(str,self.paramInfo.col('value')))
		self.ownerComp.store('ValueState' , ValueState)
		
		# Get the html title, which contains the 'WebRenderPick' custom data.
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)

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
				foundCells = self.tupleLookup.findCells(initParName, cols=['tupletname'])
				desiredParNames = [x.offset(0,1).val for x in foundCells]
				
				# now iterate through that tuplet row.
				for thisOp in self.dstOpsDat.rows():
					thisOp = op(thisOp[0])
					
					# for each param, reset to default.
					for parName in desiredParNames:
						
						foundParam = getattr( thisOp.par , parName , ':PAR_ERR:' )
						if foundParam != ':PAR_ERR:':
							InitVals += [ foundParam.eval() ]
							foundParam.val = foundParam.default
							InitPars += [ foundParam ]

			# nothing happens if the user dbl clicks on a page header.
			elif initParName.endswith('_p'):
				pass
		
		# store init pars and vals
		self.ownerComp.store('InitPars', InitPars)
		self.ownerComp.store('InitVals', InitVals)

		return


	def Interact_RightClick_While( self , uDist , vDist ):
		return


	def Interact_RightClick_Up( self ):
		
		ValueStateDown = self.ownerComp.fetch('ValueState')
		InitPars = self.ownerComp.fetch('InitPars')
		InitVals = self.ownerComp.fetch('InitVals')
		ValueStateUp = list(map(str,self.paramInfo.col('value')))
		if (ValueStateUp != ValueStateDown):
			self.ParamChange(pars=InitPars, prevVals=InitVals)

		return

	def Interact_Touch_Drag( self , action , v_displacement , u , v ):
		'''
		Wrapper Interaction function for touch screen wackyness.
		action = ['down','while','up']
		v_displacement = instantaneous amount to move scroll wheel by.
		'''
		ScrollContext = self.GetScrollContext()
		self.ownerComp.Trigger_Escape()

		

		# LEFT
		if ScrollContext == 'scroll':
			Scrollratemultiplier = self.ownerComp.par.Touchscrollratemultiplier.eval()
			wheel = v_displacement * Scrollratemultiplier
			self.webRenderTop.interactMouse(0, 0, wheel=wheel , pixels=True)


		# MIDDLE
		elif ScrollContext == 'adjust':
			
			if action == 'while':
				if self.ownerComp.fetch('sliderFreeze') == True:
					self.ownerComp.Interact_LeftClick_While( u , v , inputType = 'touch' )

			elif action == 'up':
				self.delayedLeftClickUp.run(delayFrames=1)
			
			pass


		# RIGHT
		elif ScrollContext == 'scrollbar':
			
			# while the drag is happening.
			if action == 'while':
				self.ownerComp.Interact_Hover( True , u , v )
			
			# must "release" the mouse scroll bar drag event when done, 
			# otherwise weird stuff happens where scroll wheel and scrollbar drag conflict.
			elif action == 'up':
				self.ownerComp.Mouse( self.webRenderTop, 0 , 0 , '' , False )

		return

	def Interact_Touch_Tap( self , action , u , v ):
		'''
		Wrapper Interaction function for touch screen wackyness.
		action = ['down','while','up']
		'''
		ScrollContext = self.GetScrollContext()

		# LEFT
		if ScrollContext == 'scroll':
			
			if action == 'down':
				self.Interact_Hover( 0 , u , v )
				# pass
			
			if action == 'while':
				pass

			elif action == 'up':
				self.ownerComp.Interact_Hover( 0 , u , v )
				self.delayedLeftClickDown.run(delayFrames=1)
				self.delayedLeftClickUp.run(delayFrames=2)

		# MIDDLE
		elif ScrollContext == 'adjust':
			
			if action == 'down':
				self.ownerComp.store('sliderFreeze',False)
				self.ownerComp.Interact_Hover( 0 , u , v )
				self.delayedLeftClickDown.run(delayFrames=1)
				self.delayedDoubleClick.run(delayFrames=2)
				# pass
			
			if action == 'while':
				pass

			elif action == 'up':
				self.delayedLeftClickUp.run(delayFrames=1)
				# pass

		# RIGHT
		elif ScrollContext == 'scrollbar':
			pass

		return

	# def Interact_Hover( self , select , u , v ):
	# 	# calculate the X and Y position in absolute pixel values. This is what the render top wants.
	# 	x = int(u * self.ownerComp.width)
	# 	x = tdu.clamp(x , 0 , self.ownerComp.width)
	# 	y = int( self.ownerComp.height - int(v * self.ownerComp.height) )


	def Interact_Hover( self , select , u , v ):
		'''
		select = state of the left select during a hover. Not used for adjusting sliders, but important for logic.
		'''

		# calculate the X and Y position in absolute pixel values. This is what the render top wants.
		x = int(u * self.ownerComp.width)
		x = tdu.clamp(x , 0 , self.ownerComp.width)
		y = int( self.ownerComp.height - int(v * self.ownerComp.height) )

		# get u position as clamped 0-1
		u = tdu.clamp( u , 0 , 1 )
		initParName = self.ownerComp.fetch("initParNAME" , '')
		ScrollContext = self.GetScrollContext()

		# print(select,u,v)
		
		if ScrollContext == 'scrollbar':
			# send the mouse position, and last initialized par name to Mouse function.
			self.ownerComp.Mouse( self.webRenderTop, x , y , '' , select )

		elif ScrollContext == 'adjust':
			# get the initParName from the left select script dat storage.
			# initParName = self.ownerComp.fetch("initParNAME" , '')
			if select == 1:
				forcedParName = initParName
			else:
				forcedParName = ''
			self.ownerComp.Mouse( self.webRenderTop, x , y , forcedParName , select )

		elif ScrollContext == 'scroll':
			# send the mouse position, and last initialized par name to Mouse function.
			self.ownerComp.Mouse( self.webRenderTop, x , y , '' , select )



	def Interact_Scroll( self , scrollDisplace , inputType , asPixels=False ):
		'''
		scrollDisplace: An instantaneous scroll amount, not a cumulative one.

		This function is a wrapper for all scrolling functionality, which usually does not happen 
		during other functionality like mouse movement, or drag, etc. further more, if user is using
		touch input, we want to separate other interactions from scrolling in a dif way.
		'''

		ScrollContext = self.ownerComp.GetScrollContext()

		# if the user was in scroll context...
		if ScrollContext == 'scroll':

			# calculate some booleans based on mouse position.
			IsInsidePanel = int(self.ownerComp.panel.inside)

			 # if user provided scroll input via mouse...
			if inputType == 'mouse':
				# CanWeScroll = IsInsidePanel
				Scrollratemultiplier = self.ownerComp.par.Mousescrollratemultiplier.eval()
				ExponentialScrollRateMultiplier = abs((scrollDisplace * scrollDisplace)) * self.ownerComp.par.Mousescrollacelleration.eval()
				wheel = scrollDisplace * IsInsidePanel * Scrollratemultiplier * ExponentialScrollRateMultiplier
			elif inputType == 'touch':
				Scrollratemultiplier = self.ownerComp.par.Touchscrollratemultiplier.eval()
				wheel = scrollDisplace * Scrollratemultiplier

			# op('constant1').par.value0 = wheel
			# if wheel != 0:
			# send interaction to the web render top - u/v doesn't matter here since all we want is a scroll comamnd.
			self.webRenderTop.interactMouse(0, 0, wheel=wheel , pixels=asPixels)

		# if user scrolled over a value
		# funny thing about the mouse wheel, is if you scroll a notch, you get a non-zero value, then a zero.
		# zero can obviously be calculated, but it's wasted cpu cycles since it doesn't do anything.
		# this if statement only executes a scroll IF the value is one of those non-zero ones.
		if ScrollContext=='adjust' and scrollDisplace != 0 and inputType == 'mouse':
			
			# get some variables.
			ctrl = bool(op('null_mod')['ctrl'])
			shift = bool(op('null_mod')['shift'])

			# if user scrolls, assume they are either trying to scroll vertically, or adjust a slider.
			# so lets make sure all our auxiliary UI are closed.
			op('field').Close()
			op('menu').Close()
			op('colorpicker').Close()
			op('tooltip').Close()

			# if scroll timer is running, re-cue it.
			if self.scrollTimer['running'] == 1:
				self.scrollTimer.par.cuepulse.pulse()

			# if scroll timer has ended, get the current parameter values
			# and store them for now as latest, and restart scrolltimer.
			else:
				ValueState = list(map(str,self.paramInfo.col('value')))
				self.ownerComp.store('ValueState' , ValueState)
				self.scrollTimer.par.start.pulse()

			# parse our webRenderPick dat.
			pikStr = self.webInfo['title',1].val
			pikDict = self.ParseTitle(pikStr)

			# make sure our renderpick data is valid.
			if pikDict != None:
				
				# get the parameter we're hovering over.
				initParName = str( pikDict["Par"] )
				
				# if user scrolled on a label, proceed.
				if initParName.endswith('_l'):
					
					# chop off suffix, and keep prefix
					initParName = initParName.replace('_l', '')

				# nothing happens if the user dbl clicks on a page header.
				elif initParName.endswith('_p'):
					pass
						
				# if user scrolled on an actual paramter slider, proceed.
				else:
					
					# get some relevant info, numeric range, style, and menu names if it exists.
					normMin = float( self.paramInfo[initParName,'normmin'] or 0 )
					normMax = float( self.paramInfo[initParName,'normmax'] or 0 )
					style = str( self.paramInfo[initParName,'style'] )
					try:
						menunames = eval( str(self.paramInfo[initParName,'menunames']) )
					except:
						menunames = []
					
					# scale down the default StepSize by factor of 50.
					# TODO: make this default more meaningful or parameter specific?
					normStepSize = (normMax - normMin) / 50

					# init some lists.
					initPars = []
					initVals = []
					
					# iterate through all of the destination operators.
					for thisOp in self.dstOpsDat.rows():
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
									increment = scrollDisplace * normStepSize * 10
								
								# for ctrl, we scroll less, /10
								elif ctrl:
									increment = scrollDisplace * normStepSize * .1
								
								# else if no modifiers, we just scroll the normal amount.
								else:
									increment = scrollDisplace * normStepSize

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
									increment = scrollDisplace * 10
								elif ctrl:
									increment = scrollDisplace * 2
								else:
									increment = scrollDisplace * 1
								
								# get the current value of the par right now, increment, and set.
								curVal = foundPar.eval()
								newVal = curVal + increment
								foundPar.val = newVal
							
							# scrolling menus are similar to ints, but no modifiers are used. the increment is always factor of 1.
							elif style in [ 'Menu' ]:
								increment = scrollDisplace
								curVal = foundPar.eval()
								foundPar.menuIndex = tdu.clamp( foundPar.menuIndex + increment , 0 , len(menunames)-1 )
								
							# scrolling strmenus are similar, but a bit more annoying since the str may not exist in the menuNames list.
							# so we have some extra try/catch logic to reset things to the first item, if there are no valid ones.
							elif style in [ 'StrMenu' ]:
								increment = scrollDisplace
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
					self.ownerComp.store('initPar', initPars)
					self.ownerComp.store('initVal', initVals)

		return

		
		
		
	def Set_DragOverlay(self, webRenderTop , state=0 , elementID='' ):
		'''
		sets the z index of the drag overlay to in front, or behind.
		this is used to cleanly drag the mouse left and right even
		if the cursor leaves the bounds of the initially selected widget.
		'''
		state = 99 if state == 1 else -99
		
		# print(state,)
		script = "Set_DragOverlay_('{0}','{1}')".format(state,elementID)
		webRenderTop.executeJavaScript(script)


	def Trigger_DelayedScrollChange( self ):
		# this timer chop gives us a slight delay before triggering the parameter changed script.
		ValueStateDown = self.ownerComp.fetch('ValueState')
		ValueStateUp = list(map(str,self.paramInfo.col('value')))
		if (ValueStateUp != ValueStateDown):
			self.ownerComp.ParamChange( 
				pars=self.ownerComp.fetch("initPar" , []) ,
				prevVals=self.ownerComp.fetch("initVal" , []) ,
				)
		return


	def Trigger_DelayedDoubleClick( self ):
		'''
		This is called when user doubleclicks anywhere in the UI. Most places do not have 
		doubleclick functionality, but if the user double clicks in certain types of parameters
		like a numeric value field, this will launch the field, and they can enter a value by hand.
		'''

		# Get the html title, which contains the 'WebRenderPick' custom data.
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)

		# get the initial par name.
		initParName = str( pikDict.get("Par","") )

		# nothing happens if the user dbl clicks on a label.
		if initParName.endswith('_l'):
			pass

		# nothing happens if the user dbl clicks on a tooltip.
		elif initParName.endswith('_tt'):
			pass

		# nothing happens if the user dbl clicks on a page header.
		elif initParName.endswith('_p'):
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
				style = str( self.paramInfo[initParName,'style'] )
				
				# only proceed if the parameter style is one that supports field entry.
				if style not in [ 'Menu' , 'StrMenu' , 'Pulse' , 'Toggle' , 'Momentary' ]:
					
					# get all the destination objects.
					dstOps = [ x.path for x in map(op,self.dstOpsDat.col(0)) if x != None ]

					# if there is at least one destination object, Launch the field.
					if len(dstOps):
						op('field').Launch_Delayed( dstOps , initParName , left , right , bottom , top , 0 )

		return


	def Set_TabNextTarget( self ):
		'''
		handles seeking out the next field to tab to, when called.
		'''

		# if button state was True, and the user currently has focus in the UberGui panel..
		if self.ownerComp.panel.focusselect == 1:
			
			# if they haven't actually submitted the value from the field previously, do so for them now.
			op('field').Set()
			
			# parse and fetch the next parameter name from the webRenderPick dat.
			pikStr = self.webInfo['title',1].val
			pikDict = self.ParseTitle(pikStr)
			nextParName = str(pikDict['Par2'])
			
			# set the next parameter in the webrender using the mouse function.
			# this executes some javascript that establishes the next param as current
			# so the user can keep hitting tab to iterate through many.
			self.Mouse( self.webRenderTop , x=0 , y=0 , targetPar=nextParName )
		return

	def Trigger_TabNextTarget( self ):
		'''
		When user hits the tab key, the field will shift to the next available valid parameter
		allowing rapid fire entry across multiple parameters. This has to be triggered with a delay,
		hence living in a separate text file like this.
		'''

		# parse webRenderPick data.
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)

		# get some information about the current parameter.
		initParName = str( pikDict["Par"] )
		left = float( pikDict["left"] )
		right = float( pikDict["right"] )
		top = float( pikDict["top"] )
		bottom = float( pikDict["bottom"] )
		style = str( self.paramInfo[initParName,'style'] )

		# user can't use field entry for these, so we avoid them.
		if style not in [ 'Menu' , 'StrMenu' , 'Pulse' , 'Toggle' ,  ]:
			
			# launch the field.
			dstPaths = [ x[0].val for x in self.dstOpsDat.rows() ]
			op('field').Launch( dstPaths , initParName , left , right , bottom , top )

		return

	def Trigger_Escape_If_Auxguis_Unused( self ):

		if self.fieldCOMP.panel.inside == False and self.menuCOMP.panel.inside == False and self.colorpickerCOMP.panel.inside == False:
			self.fieldCOMP.Close()
			self.menuCOMP.Close()
			self.colorpickerCOMP.Close()

		return

	def Trigger_Escape( self ):
		'''
		When user hits the escape key
		'''
		self.fieldCOMP.Close()
		return

	def Trigger_Enter( self ):
		'''
		When user hits the enter key
		'''
		self.fieldCOMP.Set()
		self.fieldCOMP.Close()
		return
	
		
	def Launch(self, srcOp , DstOps):
		'''
		SrcOp = single operator reference
		DstOps = list of operator references.
		'''
		
		self.ownerComp.par.Inputop = srcOp
		self.ownerComp.par.Outputops = ' '.join([ x.path for x in DstOps ])
		
	def Clear(self):
		
		self.ownerComp.par.Inputop = ''
		self.ownerComp.par.Outputops = ''
		
		op('HTML').text = ''
		
	
	
	def IsStringFloat(self, arg_ = ''):
		try:
			float(arg_)
			isFloat = True
		except:
			isFloat = False
			
		# if hasDecimal and isFloat:
		if isFloat:
			
			return True
		else:
			return False

	def GetStyleOfCurrent( self ):
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)
		style = str( self.paramInfo[pikDict['Par'],'style'] )
		return style

	def IsPickingDataValid( self ):
		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)
		if pikDict == None:
			return False
		elif pikDict['Par'] == 'INIT':
			return False
		else:
			return True

	def IsHoveredParamFieldCompatible( self ):

		pikStr = self.webInfo['title',1].val
		pikDict = self.ParseTitle(pikStr)

		initParName = str( pikDict["Par"] )
		style = str( self.paramInfo[initParName,'style'] )

		# print(style)
		return style

	def SetScrollContext(self, uVal):
		# given a normalized U val, we determine if our mouse wheel context is scroll,or adjust.
		uSplitVal = self.ownerComp.par.Labelvaluesplit.eval()
		Wheelcontext = self.ownerComp.par.Wheelcontext.eval()
		ScrollbarFractional = 1-(self.ownerComp.par.Scrollbarwidth.eval() / self.ownerComp.width)

		# if the uVal is above ScrollbarFractional, our mouse is inside the scrollbar on the right.
		if (uVal > ScrollbarFractional):
			if Wheelcontext != 'scrollbar':
				self.ownerComp.par.Wheelcontext = 'scrollbar'

		# if the above fails, we know the mouse is to the left of scrollbar. so we just check if it's right of split.
		elif (uVal > tdu.remap( uSplitVal , 0 , 1 , 0 , ScrollbarFractional ) ):
			if Wheelcontext != 'adjust':
				self.ownerComp.par.Wheelcontext = 'adjust'

		# if above fails, we know the only remaining option is that it's in the left side, amongst the labels.
		else:
			if Wheelcontext != 'scroll':
				self.ownerComp.par.Wheelcontext = 'scroll'
		return

	def GetScrollContext(self):
		# get mouse wheel context
		return self.ownerComp.par.Wheelcontext.eval()
	
	
	def String_Numeric_Parse(self, arg_ = ''):
	
		val = arg_
		error_ = False
		
		try:
			val = eval(val)
		except:
		
			val = val.replace(' ','')
			
			val = val.replace('mm','*.1')
			val = val.replace('cm','*1')
			val = val.replace('in','*2.54')
			val = val.replace('ft','*30.48')
			val = val.replace('m','*100')
			val = val.replace('yd','*91.44')
			
			try:
				val = eval(val)
			except:
				val = 0
		
		return val
		
	def ParseString(self, style = '', arg_=''):
		
		val = arg_
		
		if style in [ 'Float' , 'RGB' , 'RGBA' , 'UV' , 'UVW' , 'XY' , 'XYZ' , 'WH' , 'Int' ]:
			if self.IsStringFloat(val):
				val = val
			
			elif self.StringUnitTest(val):
				pass
			else:
				debug('value not proper numeric float, reverting..')
		
		
		return
		
		
	def ResetDblClick(self):
		
		op('base_double_click_detect').op('unstore_all_clicks').run()
		
		
	def ParamChange(self, pars=[], prevVals=[]):
		paramChangeDat = self.ownerComp.par.Paramchangescript.eval()
		if paramChangeDat != None:
			paramChangeDat.run(pars,prevVals)
		else:
			debug('A parameter has been changed..')

	def SetMode_Mouse(self):
		if self.ownerComp.par.Inputmode.eval() != 'mouse':
			self.ownerComp.par.Inputmode = 'mouse'

	def SetMode_Touch(self):
		if self.ownerComp.par.Inputmode.eval() != 'touch':
			self.ownerComp.par.Inputmode = 'touch'