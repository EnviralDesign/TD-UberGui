##### This script handles several keyboard hotkey functions, like tab, esc, and enter.



# define some operator references.
insideChop = op('panel_uv_inside')
webRenderTop = op('WEB_RENDER')
paramInfo = op('null_paramInfo')
webInfo = op('WEB_INFO')
srcOpDat = op('null_srcOp')

def onKey(dat, key, character, alt, lAlt, rAlt, ctrl, lCtrl, rCtrl, shift, lShift, rShift, state, time):

	# if button state was True, and the user currently has focus in the UberGui panel..
	if state and parent.Widget.panel.focusselect == 1:
		
		# if they pressed tab, we want to move field to next parameter.
		if key == 'tab':
			
			# if they haven't actually submitted the value from the field previously, do so for them now.
			op('field').Set()
			
			# parse and fetch the next parameter name from the webRenderPick dat.
			pikStr = webInfo['title',1].val
			pikDict = parent.Widget.ParseTitle(pikStr)
			nextParName = str(pikDict['Par2'])
			
			# set the next parameter in the webrender using the mouse function.
			# this executes some javascript that establishes the next param as current
			# so the user can keep hitting tab to iterate through many.
			parent.Widget.Mouse( webRenderTop , x=0 , y=0 , targetPar=nextParName )
			
			# run the tab code delayed by a frame.
			op('delayed_tab').run(delayFrames=1)
		
		# if the user hit escape, just close the current field, with out submitting the value.
		if key == 'esc':
			op('field').Close()
		
		# if they pressed enter, Set the value from the field, then close it.
		if key == 'enter':
			op('field').Set()
			op('field').Close()
	
	return

def onShortcut(dat, shortcutName, time):
	return;
	