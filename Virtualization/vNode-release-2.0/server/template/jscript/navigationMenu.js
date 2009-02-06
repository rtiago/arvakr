/*
* Copyright (c) Members of the EGEE Collaboration. 2004. 
* See https://www.eu-egee.org/partners/ for details on the copyright
* holders.  
*
* Licensed under the Apache License, Version 2.0 (the "License"); 
* you may not use this file except in compliance with the License. 
* You may obtain a copy of the License at 
*
*     https://www.apache.org/licenses/LICENSE-2.0 
*
* Unless required by applicable law or agreed to in writing, software 
* distributed under the License is distributed on an "AS IS" BASIS, 
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
* See the License for the specific language governing permissions and 
* limitations under the License.
*
* Author:
*   Ricardo Mendes <Ricardo DOT Mendes AT cern DOT ch>
*
*
*/

/*
	Initialize and render the MenuBar when its elements are ready 
  to be scripted.
*/

YAHOO.util.Event.onContentReady("vNodeMenu", function () {
/*
	Instantiate a MenuBar:  The first argument passed to the 
  constructor is the id of the element in the page 
  representing the MenuBar; the second is an object literal 
  of configuration properties.
*/

function onMenuItemClick(p_sType, p_aArgs, p_oValue) {
  if (p_oValue == "startVM") 	{ 
		YAHOO.vnode.container.dialog1.show()
		YAHOO.vnode.container.dialog1.focus()
  }
	else if (p_oValue == "terminateVM") {
		YAHOO.vnode.container.dialog2.show()
		YAHOO.vnode.container.dialog2.focus()
  }
  else if (p_oValue == "stateVM") {
    YAHOO.vnode.container.dialog3.show()
		YAHOO.vnode.container.dialog3.focus()
  }
  else if (p_oValue == "upTimeVM") {
    YAHOO.vnode.container.dialog4.show()
		YAHOO.vnode.container.dialog4.focus()
  }
  else if (p_oValue == "startVG") {
    YAHOO.vnode.container.dialog5.show()
		YAHOO.vnode.container.dialog5.focus()
  }
  else if (p_oValue == "stateVG") {
    YAHOO.vnode.container.dialog6.show()
		YAHOO.vnode.container.dialog6.focus()
  }
  else if (p_oValue == "terminateVG") {
    YAHOO.vnode.container.dialog7.show()
		YAHOO.vnode.container.dialog7.focus()
  }
  else if (p_oValue == "adminPanel") {
    if (checkPermission()) {
      YAHOO.vnode.container.dialog8.show()
	  	YAHOO.vnode.container.dialog8.focus()
    }
    else {
      alert("User is not allowed")
    }
  }
} 

var oMenuBar = new YAHOO.widget.MenuBar("vNodeMenu", { autosubmenudisplay: true, hidedelay: 350, lazyload: true });
/*
  Define an array of object literals, each containing 
  the data necessary to create a submenu.
*/
var aSubmenuData = [
	{
		id: "VMs", 
      itemdata: [ 
         { text: "Start VMs", onclick: { fn: onMenuItemClick, obj: "startVM"} },
         { text: "Terminate VMs", onclick: { fn: onMenuItemClick, obj: "terminateVM"} },
         { text: "State of VMs", onclick: { fn: onMenuItemClick, obj: "stateVM"} },
         { text: "Uptime of VMs", onclick: { fn: onMenuItemClick, obj: "upTimeVM"}  },
      ]
	},

  {
    id: "VGs", 
      itemdata: [
         { text: "Start a VGs", onclick: { fn: onMenuItemClick, obj: "startVG"} },
         { text: "State of VGs", onclick: { fn: onMenuItemClick, obj: "stateVG"} },
         { text: "Terminate VGs", onclick: { fn: onMenuItemClick, obj: "terminateVG"} },               
      ]    
  },
                    
  {
    id: "Admin", 
      itemdata: [
         { text: "Manage", onclick: { fn: onMenuItemClick, obj: "adminPanel"} }       
      ] 
  },
                                      
];

var ua = YAHOO.env.ua,oAnim;  // Animation instance

/*
	"beforeshow" event handler for each submenu of the MenuBar
   instance, used to setup certain style properties before
   the menu is animated.
*/
function onSubmenuBeforeShow(p_sType, p_sArgs) {

	var oBody,
      oElement,
      oShadow,
      oUL;
                

  if (this.parent) {

     oElement = this.element;

     /*
        Get a reference to the Menu's shadow element and 
        set its "height" property to "0px" to syncronize 
        it with the height of the Menu instance.
     */

     oShadow = oElement.lastChild;
     oShadow.style.height = "0px";

                        
     /*
      	Stop the Animation instance if it is currently 
        animating a Menu.
     */ 
                    
     if (oAnim && oAnim.isAnimated()) {  
         oAnim.stop();
         oAnim = null;                   
     }

			/*
         Set the body element's "overflow" property to 
         "hidden" to clip the display of its negatively 
         positioned <ul> element.
      */ 

				oBody = this.body;


				//  Check if the menu is a submenu of a submenu.

				if (this.parent && 
						!(this.parent instanceof YAHOO.widget.MenuBarItem)) {
                        

		/*
				There is a bug in gecko-based browsers where 
				an element whose "position" property is set to 
				"absolute" and "overflow" property is set to 
				"hidden" will not render at the correct width when
				its offsetParent's "position" property is also 
				set to "absolute."  It is possible to work around 
				this bug by specifying a value for the width 
				property in addition to overflow.
		*/

						if (ua.gecko) {
						
								oBody.style.width = oBody.clientWidth + "px";
						
						}
						
						
						/*
								Set a width on the submenu to prevent its 
								width from growing when the animation 
								is complete.
						*/
						
						if (ua.ie == 7) {

								oElement.style.width = oElement.clientWidth + "px";

						}
				
				}

    
				oBody.style.overflow = "hidden";


				/*
						Set the <ul> element's "marginTop" property 
						to a negative value so that the Menu's height
						collapses.
				*/ 

				oUL = oBody.getElementsByTagName("ul")[0];

				oUL.style.marginTop = ("-" + oUL.offsetHeight + "px");
		
		}

}


/*
		"tween" event handler for the Anim instance, used to 
		syncronize the size and position of the Menu instance's 
		shadow and iframe shim (if it exists) with its 
		changing height.
*/

function onTween(p_sType, p_aArgs, p_oShadow) {

		if (this.cfg.getProperty("iframe")) {
		
				this.syncIframe();

		}

		if (p_oShadow) {

				p_oShadow.style.height = this.element.offsetHeight + "px";
		
		}

}


/*
		"complete" event handler for the Anim instance, used to 
		remove style properties that were animated so that the 
		Menu instance can be displayed at its final height.
*/

function onAnimationComplete(p_sType, p_aArgs, p_oShadow) {

		var oBody = this.body,
				oUL = oBody.getElementsByTagName("ul")[0];

		if (p_oShadow) {
		
				p_oShadow.style.height = this.element.offsetHeight + "px";
		
		}


		oUL.style.marginTop = "";
		oBody.style.overflow = "";
		

		//  Check if the menu is a submenu of a submenu.

		if (this.parent && 
				!(this.parent instanceof YAHOO.widget.MenuBarItem)) {


				// Clear widths set by the "beforeshow" event handler

				if (ua.gecko) {
				
						oBody.style.width = "";
				
				}
				
				if (ua.ie == 7) {

						this.element.style.width = "";

				}
		
		}
		
}


/*
		 "show" event handler for each submenu of the MenuBar 
		 instance - used to kick off the animation of the 
		 <ul> element.
*/

function onSubmenuShow(p_sType, p_sArgs) {

		var oElement,
				oShadow,
				oUL;

		if (this.parent) {

				oElement = this.element;
				oShadow = oElement.lastChild;
				oUL = this.body.getElementsByTagName("ul")[0];
		

				/*
						 Animate the <ul> element's "marginTop" style 
						 property to a value of 0.
				*/

				oAnim = new YAHOO.util.Anim(oUL, 
						{ marginTop: { to: 0 } },
						.5, YAHOO.util.Easing.easeOut);


				oAnim.onStart.subscribe(function () {

						oShadow.style.height = "100%";
				
				});


				oAnim.animate();


				/*
						Subscribe to the Anim instance's "tween" event for 
						IE to syncronize the size and position of a 
						submenu's shadow and iframe shim (if it exists)  
						with its changing height.
				*/

				if (YAHOO.env.ua.ie) {
						
						oShadow.style.height = oElement.offsetHeight + "px";


						/*
								Subscribe to the Anim instance's "tween"
								event, passing a reference Menu's shadow 
								element and making the scope of the event 
								listener the Menu instance.
						*/

						oAnim.onTween.subscribe(onTween, oShadow, this);

				}


				/*
						Subscribe to the Anim instance's "complete" event,
						passing a reference Menu's shadow element and making 
						the scope of the event listener the Menu instance.
				*/

				oAnim.onComplete.subscribe(onAnimationComplete, oShadow, this);
		
		}

}


/*
		 Subscribe to the "beforerender" event, adding a submenu 
		 to each of the items in the MenuBar instance.
*/

oMenuBar.subscribe("beforeRender", function () {

		if (this.getRoot() == this) {

				this.getItem(0).cfg.setProperty("submenu", aSubmenuData[0]);
				this.getItem(1).cfg.setProperty("submenu", aSubmenuData[1]);
				this.getItem(2).cfg.setProperty("submenu", aSubmenuData[2]);
				this.getItem(3).cfg.setProperty("submenu", aSubmenuData[3]);

		}

});


/*
		 Subscribe to the "beforeShow" and "show" events for 
		 each submenu of the MenuBar instance.
*/

oMenuBar.subscribe("beforeShow", onSubmenuBeforeShow);
oMenuBar.subscribe("show", onSubmenuShow);


/*
		 Call the "render" method with no arguments since the 
		 markup for this MenuBar instance is already exists in 
		 the page.
*/

oMenuBar.render();         

});




