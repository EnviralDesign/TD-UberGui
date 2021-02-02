##### This script will take the ambient user interaction, like mouse movement/position
##### and send this into the web render top as just mouse position. This is important because
##### when we eventually do click something, we want to already know what the mouse is over.
##### It is also important for hover effects and things like that.


# define references to some operators.
uv = op('null_uv_inside')
webTop = op('WEB_RENDER')
chopexec_lselect = op('chopexec_lselect')

def whileOn(channel, sampleIndex, val, prev):
	
	# get u position as clamped 0-1
	u = float(uv['u'])
	u = tdu.clamp( u , 0 , 1 )

	# find out if mouse is in the right side, or left side.
	isInRightSide = int(u >= .5 and u <= 1.0)

	# get the initParName from the left select script dat storage.
	initParName = chopexec_lselect.fetch("initParNAME" , '')
	forcedParName = ['',initParName][ min(int(uv['select']) , isInRightSide) ]

	# calculate the X and Y position in absolute pixel values. This is what the render top wants.
	x = int(u * parent.Widget.width)
	x = tdu.clamp(x , 0 , parent.Widget.width)
	y = int( parent.Widget.height - int(uv['v'] * parent.Widget.height) )
	
	# send the mouse position, and last initialized par name to Mouse function.
	parent.Widget.Mouse( webTop, x , y , forcedParName )
	
	return
	
	
def onOnToOff(channel, sampleIndex, val, prev):
	
	# clear the interaction by hovering to pixel 0,0 when mouse leaves container.
	webTop.interactMouse( 0 , 0 , pixels=True )
	
	return