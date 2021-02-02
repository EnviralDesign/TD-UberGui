import json

class UG4:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		
		
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
			
			parTuplets = [ x for x in SRC.customTuplets if x[0].enable == True and x[0].page.name.isupper() ]
			
			FirstHeader = 1
			
			for ID,tuplet in enumerate(parTuplets):
				
				# Generate section label.
				PAGE = tuplet[0].page.name
				if PAGE not in discoveredPages:
					discoveredPages += [ PAGE ]
					
					if FirstHeader == 0:
						HTML += "<div class='spacer_header' id='_spacer_' ></div>\n\n"
					FirstHeader = 0
					
					HTML += "<div class='header_container'>%s</div>\n\n"%(PAGE)
				
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
	
	
	def Update(self , webRenderTop , flatArgList ):
	
		jsonArgsList = json.dumps(flatArgList).replace("'", '"')
		script = "Update_('{0}')".format(jsonArgsList)
		
		try:
			webRenderTop.executeJavaScript(script)
		except:
			pass


	def Mouse(self , webRenderTop , x=0, y=0 , targetPar='' ):
		
		argDict = {'x':x, 'y':y , 'par':targetPar}
		jsonArgsList = json.dumps(argDict).replace("'", '"')

		script = "Mouse_('{0}')".format(jsonArgsList)
		webRenderTop.executeJavaScript(script)
		webRenderTop.interactMouse( x , parent.Widget.height-y , pixels=True )
		
		
		
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
		
		
	def Launch(self, srcOp , DstOps):
		'''
		SrcOp = single operator reference
		DstOps = list of operator references.
		'''
		
		parent.Widget.par.Inputop = srcOp
		parent.Widget.par.Outputops = ' '.join([ x.path for x in DstOps ])
		
	def Clear(self):
		
		parent.Widget.par.Inputop = ''
		parent.Widget.par.Outputops = ''
		
		op('HTML').text = ''
		
	
	
	def IsStringFloat(self, arg_ = ''):

		# hasDecimal = True if str(arg_).find('.') != -1 else False
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
		paramChangeDat = parent.Widget.par.Paramchangescript.eval()
		if paramChangeDat != None:
			paramChangeDat.run(pars,prevVals)
		else:
			debug('A parameter has been changed..')
		