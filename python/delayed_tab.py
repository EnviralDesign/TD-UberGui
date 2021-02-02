##### When user hits the tab key, the field will shift to the next available valid parameter
##### allowing rapid fire entry across multiple parameters. This has to be triggered with a delay,
##### hence living in a separate text file like this.


# define some operator references.
insideChop = op('panel_uv_inside')
webRenderTop = op('WEB_RENDER')
paramInfo = op('null_paramInfo')
webInfo = op('WEB_INFO')
dstOpsDat = op('null_dstOps')

# parse webRenderPick data.
pikStr = webInfo['title',1].val
pikDict = parent.Widget.ParseTitle(pikStr)

# get some information about the current parameter.
initParName = str( pikDict["Par"] )
left = float( pikDict["left"] )
right = float( pikDict["right"] )
top = float( pikDict["top"] )
bottom = float( pikDict["bottom"] )
style = str( paramInfo[initParName,'style'] )

# user can't use field entry for these, so we avoid them.
if style not in [ 'Menu' , 'StrMenu' , 'Pulse' , 'Toggle' ,  ]:
	
	# launch the field.
	dstPaths = [ x[0].val for x in dstOpsDat.rows() ]
	op('field').Launch( dstPaths , initParName , left , right , bottom , top )