


function Update_ ( jsonStr ) {
	/*
	This function updates the value displayed, and the position of the slider graphic 
	from a json string payload coming from TD. IE when a parameter value changes.
	*/
	var jsonObj = JSON.parse( jsonStr );
	
	for(var i=0; i<jsonObj.length; i++) {  // for each argument
		var id = jsonObj[i][0];
		var val = jsonObj[i][1];
		var slide = jsonObj[i][2];
		
		/* if val is a float value, round display version for readability */ 
		if (!isNaN(parseFloat(val)) && val.toString().indexOf('.') != -1 && val.toString().split(".").length <= 1)
		{
			val = Math.round( parseFloat(val)*100 ) / 100;
		}

		var textEl = document.getElementById( id + '_t' );
		textEl.innerHTML = val;
		var width = textEl.offsetWidth;
		
		var slideEl = document.getElementById( id + '_s' );

		slideEl.style.width = clamp(slide*100 , 0.0 , 100.0)+'%';
		
		
	};
};




function Set_DragOverlay_(depth,element) {
	/*
	DragOverlay is a name for a collection of html div elements that acts
	as a user interaction mask. 

	Normally, when hovering the mouse over a document
	the element that is hovered over changes as soon as the mouse enters a new region.
	This caused issues for adjusting a slider that was initially clicked in, when the mouse
	moves outside of that element, or even outside of that UberGui pane. This is non-intuitive,
	and very frustrating for users, so this mask essentially prevents the webRenderPick from
	detecting a newly hovered UI element, because they are all being covered up by DragOverlay!

	This mask is disabled again as soon as the mouse click is released, allowing interaction with
	any element again.
	*/
	var depthVal = parseInt(depth);
	var opacity = clamp( depthVal , 0 , 1 ) ;
	
	var htmlDoc = document.getElementById("html_master");
	
	var el = document.getElementById( element );
	var rect = el.getBoundingClientRect();
	
	var dragOverlay = document.getElementById( "dragOverlay" );
	dragOverlay.style.zIndex = "" + depthVal;
	dragOverlay.style.opacity = opacity;
	
	var dragOverlayLeft = document.getElementById( "_dragOverlayLeft_" );
	dragOverlayLeft.style.width = (rect.left) + "px";
	
	var dragOverlayRight = document.getElementById( "_dragOverlayRight_" );
	dragOverlayRight.style.width = (rect.right - rect.left) + "px";
	
	var dragOverlayRightRight = document.getElementById( "_dragOverlayRightRight_" );
	dragOverlayRightRight.style.width = (htmlDoc.offsetWidth - rect.right) + "px";
	
	var _darkener_top_ = document.getElementById( "_darkener_top_" );
	_darkener_top_.style.height = rect.top + "px";
	
	var _darkener_bot_ = document.getElementById( "_darkener_bot_" );
	var lastWidgetRect = document.getElementById( "_lastWidget_" ).getBoundingClientRect();
	_darkener_bot_.style.height = (lastWidgetRect.bottom - rect.bottom) + "px";
	_darkener_bot_.style.top = rect.bottom + "px";
	
	
};




function getAbsolutePosition(element) {
	// returns a dictionary containing the absolute offset in x and y, of an html element.
	var r = { x: element.offsetLeft, y: element.offsetTop };
	if (element.offsetParent) {
		var tmp = getAbsolutePosition(element.offsetParent);
		r.x += tmp.x;
		r.y += tmp.y;
	}
	
	return r;
};



function Mouse_( jsonStr ) {
	/*
	This function is incredibly important as it delivers to our title element, and thus our info DAT in TD
	info about what element the mouse is currently hovering over. The info this returns can be thought of as
	the results of a 'webRenderPick' operation, similar to the renderPick CHOP or DAT in TD.

	The big scary block of if/else logic is built specifically around the structure of UberGUI's html.
	So, if you decide to add or change any elements or layouts in this component, be aware that you will
	almost certainly have to dive into this function and re arrange that block accordingly.

	One way to debug errors in td/javascript land is to write out "print statements" to a div somewhere laying over
	the rest of the UI. When you see the numbers stop printing, or freeze - it's usually because there's an error
	in the javascript code, and if you can drill down to the right area, you can print some errors of that specific element,
	or just use process of elimination.

	Anyhow, if you're not making changes to the structure of the html, this function should perform flawlessly, as it's been
	battle tested for well over a year in regular use, with many different sets of custom parameters thrown at it :)
	*/
	var jsonObj = JSON.parse( jsonStr );
	
	var x = jsonObj['x'];
	var y = jsonObj['y'];
	var argPar = jsonObj['par'];

	// document.getElementById( "debug" ).innerHTML = x;
	
	var isScrollHover = 0;
	if (x > document.body.clientWidth){
		isScrollHover = 1;
	}
	else{
		isScrollHover = 0;
	}

	if (isScrollHover == 0){

		if (argPar.length == 0){
			var elements = document.elementsFromPoint(x, y);
			var deepestElement = elements[0];
		}
		
		else{
			
			var deepestElement = document.getElementById( argPar )
		}
		
		var Current_Par_Id = deepestElement.id;
		var deepestElement_class = deepestElement.className;
		var elementCS = getComputedStyle(deepestElement);
		
		var Next_Par_Id = "";

		// If we are hovering over a label
		if ( Current_Par_Id.endsWith("_l") ){
			var tupleBaseName = Current_Par_Id.replace("_l", "");
			var bodyDiv = document.getElementById( tupleBaseName + "_b" );
			Next_Par_Id = bodyDiv.firstElementChild.id;
		}
		
		// If we are hovering over a par
		else{ 
			var Last_Par_Id = deepestElement.parentNode.lastElementChild.id;
			if( Current_Par_Id.endsWith('_cp') || Current_Par_Id.endsWith('_fp') || Current_Par_Id.endsWith('_mp') ){
				Next_Par_Id = "";
			}
			else if ( Last_Par_Id.endsWith('_cp') || Last_Par_Id.endsWith('_fp') || Last_Par_Id.endsWith('_mp') ) {
				if (deepestElement.parentNode.parentNode.id == "_lastWidget_" ) {
					Next_Par_Id == "";
				}
				else if ( deepestElement.parentNode.parentNode.nextElementSibling.className == "spacer_section" ){
					Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.nextElementSibling.children[2].firstElementChild.id;
				}
				else if ( deepestElement.nextElementSibling.id.endsWith('_cp') || deepestElement.nextElementSibling.id.endsWith('_fp') || deepestElement.nextElementSibling.id.endsWith('_mp') ) {
					if (deepestElement.parentNode.parentNode.nextElementSibling.className == "spacer_header") {
						Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.nextElementSibling.nextElementSibling.children[2].firstElementChild.id;
					}
					else{
						Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.children[2].firstElementChild.id;
					}
				}
				else {
					Next_Par_Id = deepestElement.nextElementSibling.id;
				}
			}
			else if ( Last_Par_Id == Current_Par_Id ) {
				if ( deepestElement.parentNode.parentNode.nextElementSibling.className == "spacer_section" ){
					Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.nextElementSibling.children[2].firstElementChild.id;
				}
				else if ( deepestElement.parentNode.parentNode.nextElementSibling.className == "spacer_header" ){
					if ( deepestElement.parentNode.parentNode.nextElementSibling.nextElementSibling.nextElementSibling.className == "spacer_section" ){
						Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.children[2].firstElementChild.id;
					}
					else{
						Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.nextElementSibling.nextElementSibling.children[2].firstElementChild.id;
					}
				}
				else if ( deepestElement.parentNode.parentNode.nextElementSibling.className == "debug" ){
					Next_Par_Id = "";
				}
				else{
					Next_Par_Id = deepestElement.parentNode.parentNode.nextElementSibling.children[2].firstElementChild.id;
				}
			}
			else {
				Next_Par_Id = deepestElement.nextElementSibling.id;
			}
		}
		
		var paddingX = parseFloat(elementCS.paddingLeft) + parseFloat(elementCS.paddingRight);
		var paddingY = parseFloat(elementCS.paddingTop) + parseFloat(elementCS.paddingBottom);

		var borderX = parseFloat(elementCS.borderLeftWidth) + parseFloat(elementCS.borderRightWidth);
		var borderY = parseFloat(elementCS.borderTopWidth) + parseFloat(elementCS.borderBottomWidth);
		
		var deepestBoundRect = deepestElement.getBoundingClientRect();
		
		var elementWidth = Math.round(deepestBoundRect.right - deepestBoundRect.left) - paddingX - borderX;
		var elementHeight = Math.round(deepestBoundRect.bottom - deepestBoundRect.top) - paddingY - borderY;
		
		var pos = getAbsolutePosition(deepestElement);
		
		var localX = x - pos.x;
		var localY = y - pos.y;
		
		var nrmX = (localX+1) / (elementWidth);
		var nrmY = (localY+1) / (elementHeight);

		nrmX = Math.min( nrmX , 1.0 ); // silly rounding error, easy hack/fix here since we always want max of 1 for normalized sliding.
		nrmY = Math.min( nrmY , 1.0 );
		
		if ( Current_Par_Id == "_dragOverlayRight_" ) {
			nrmX = (localX+1) / (elementWidth);
		}
		
		else if ( Current_Par_Id == "_dragOverlayRightRight_" ) {
			nrmX = 1;
		}
		
		else if ( Current_Par_Id == "_dragOverlayLeft_" ) {
			nrmX = 0;
		}
		
		var Title = "";
		var rect = deepestElement.getBoundingClientRect();
		
		var left2 = 0;
		var right2 = 0;
		var top2 = 0;
		var bottom2 = 0;
		
		if ( Next_Par_Id.length > 0 ){
			var nextParEl = document.getElementById( Next_Par_Id );
			var rect2 = nextParEl.getBoundingClientRect();
			left2 = rect2.left;
			right2 = rect2.right;
			top2 = rect2.top;
			bottom2 = rect2.bottom;
		}
		
		if ( Current_Par_Id.length > 0 ) {
			Title = "Par:" + Current_Par_Id + ',left:' + rect.left + ',top:' + rect.top + ',right:' + rect.right + ',bottom:' + rect.bottom;
			Title += ",Par2:" + Next_Par_Id +',left2:' + left2 + ',top2:' + top2 + ',right2:' + right2 + ',bottom2:' + bottom2;
			Title += ',X:' + nrmX + ',Y:' + nrmY ;
		}
		else {
			Title = "";
		}
		
	}
	else{
		Title = "";
	}
	
	// put the webRenderPick info int othe title element finally! we have access to this via the info DAT.
	document.title = Title;
	
};


function clamp(num, min, max) {
	return num <= min ? min : num >= max ? max : num;
}

function remap(value, low1, high1, low2, high2) {
	return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}


function arrayContains(needle, arrhaystack)
{
	return (arrhaystack.indexOf(needle) > -1);
}