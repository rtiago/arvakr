//namespaces
YAHOO.namespace ("vnode");
YAHOO.namespace ("vnode.container");

//global variables
var proto=window.location.protocol+'//'
var path="/cgi/server/cgi-bin/main.py"
var host=window.location.hostname
var username

//global arrays to hold the glite services
myArrayRow0=new Array("none","none","none","none","none");
myArrayRow1=new Array("none","none","none","none","none");
myArrayRow2=new Array("none","none","none","none","none");
myArrayRow3=new Array("none","none","none","none","none");

//function to send asynchronous request to disable the portal
function disablePortalJS(state) {
   YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=disablePortal&vmOption='+state,null,null);
}

function getUsername() {
   YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=getUsername',callbackUsername,null);
}

var UsernameObject = {
	
	handleSuccess:function(o){
    username = o.responseText
 	},

	handleFailure:function(o){
		//failure handler
    YAHOO.vnode.container.block.show();
	}
};

//Callback. Timeout is 15s
var callbackUsername =
{
	success:UsernameObject.handleSuccess,
	failure:UsernameObject.handleFailure,
  timeout: 15000,
	scope: UsernameObject
};


//function to fill the glite arrays with the service chosen by the user
function setGlite(row,key,value) {
  if (key == "gliteService1") {
    if (row == 0) {
      myArrayRow0[0] = value;
    }
    if (row == 1) {
      myArrayRow1[0] = value;
    }
    if (row == 2) {
      myArrayRow2[0] = value;
    }
    if (row == 3) {
      myArrayRow3[0] = value;
    }
  }
  if (key == "gliteService2") {
    if (row == 0) {
      myArrayRow0[1] = value;
    }
    if (row == 1) {
      myArrayRow1[1] = value;
    }
    if (row == 2) {
      myArrayRow2[1] = value;
    }
    if (row == 3) {
      myArrayRow3[1] = value;
    }
  }
  if (key == "gliteService3") {
    if (row == 0) {
      myArrayRow0[2] = value;
    }
    if (row == 1) {
      myArrayRow1[2] = value;
    }
    if (row == 2) {
      myArrayRow2[2] = value;
    }
    if (row == 3) {
      myArrayRow3[2] = value;
    }
  }
  if (key == "gliteService4") {
    if (row == 0) {
      myArrayRow0[3] = value;
    }
    if (row == 1) {
      myArrayRow1[3] = value;
    }
    if (row == 2) {
      myArrayRow2[3] = value;
    }
    if (row == 3) {
      myArrayRow3[3] = value;
    }
  }
}

//function to check if the user has admin priviligies
//still needs to be implemented 
function checkPermission() {
  return true
}

//function to clear the glite services arrays
function unsetGlite() {
 for (j=0;j<5;j++) {
   myArrayRow0[j] = "none";
   myArrayRow1[j] = "none";
   myArrayRow2[j] = "none";
   myArrayRow3[j] = "none";
 }
}

//function to get the VMs that belong to the sitename
function getVGSite(sitename) {
  YAHOO.vnode.Basic10.myDataSource.sendRequest('vmAction=userVG&sitename='+sitename,YAHOO.vnode.Basic10.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.Basic10.myDataTable);
}

//function to auto select a number of virtual machines for the user. It also verifies that the user doesn't deploy more than 4 virtual machines at the same time
function getChecked(val,nr) { 
  if (parseInt(YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getLength()) + parseInt(nr) > 4) {
    alert("You will have more than 4 machines");
    return;
  }
  YAHOO.vnode.container.wait.show();
  YAHOO.util.Connect.asyncRequest('GET',proto + host + path + '?vmAction=autoHosts&&nrHosts=' + nr,YAHOO.vnode.Basic1.connectionCallback,null);
}

//function to get the VMs that are in a given state
function getState(state) {
  if (state == 'Deployed'  || state == 'NotDeployed' || state == 'Failed' || state == 'Terminating' || state == 'Reserved' || state == 'Deploying' || state == 'All' || state == 'Disabled') {
    YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=state'+state,YAHOO.vnode.CustomFormatting.connectionCallback2,null)
  } 
};

//Function to verify if portal is blocked
function isPortalBlocked() {
  YAHOO.util.Connect.asyncRequest('GET',proto + host + path + '?vmAction=checkDisablePortal',callbackPolice,null);
}

//verifies the response of the request 'isPortalBlocked'
var PoliceObject = {
	
	handleSuccess:function(o){
    if (o.responseText == 900) {
      YAHOO.vnode.container.block.show();
    }
    if (o.responseText == 920) {
       var el = new YAHOO.util.Element('disablePortal');
       el.set('checked',true);
    }
    if (o.responseText == 930) {
       var el = new YAHOO.util.Element('disablePortal');
       el.set('checked',false);
    }
   
 	},

	handleFailure:function(o){
		//failure handler
    YAHOO.vnode.container.block.show();
	}
};

//police Callback. Timeout is 15s
var callbackPolice =
{
	success:PoliceObject.handleSuccess,
	failure:PoliceObject.handleFailure,
  timeout: 15000,
	scope: PoliceObject
};

//function to get the VMs that belong to a VG and are in the argument state
function getVGState(state) {
  if (state == 'Deployed' || state == 'Failed' || state == 'Terminating' || state == 'Deploying') {
    YAHOO.vnode.CustomFormatting2.myDataSource.sendRequest('vmAction=stateVG&vgState='+state,YAHOO.vnode.CustomFormatting2.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.CustomFormatting2.myDataTable);
  }
  if (state == 'All') {
    YAHOO.vnode.CustomFormatting2.myDataSource.sendRequest('vmAction=stateVG',YAHOO.vnode.CustomFormatting2.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.CustomFormatting2.myDataTable);
  }
};

//initialize all the modules and get the data 
function init() {
  //AjaxObject callback. Handles the responses from most of the requests
	var AjaxObject = {
		handleSuccess:function(o){
      if (o.responseText == 201) {
        YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=getReservedData',YAHOO.vnode.Basic1.connectionCallback,null);
      }
      else if (o.responseText == 202) { 
        YAHOO.vnode.Basic2.myDataSource.sendRequest('vmAction=userVM',YAHOO.vnode.Basic2.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.Basic2.myDataTable);
      }
      else if (o.reponseText == 203) {
         YAHOO.vnode.Basic10.myDataSource.sendRequest('vmAction=userVG',YAHOO.vnode.Basic10.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.Basic10.myDataTable);
     
      }
      else if (o.responseText == 204) {
				var elState = new YAHOO.util.Element('allAdmin');
        if (elState.get('value') == 'Select...') {
  				YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=stateAll',YAHOO.vnode.CustomFormatting.connectionCallback2,null);
        }
        else
  				YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=state'+elState.get('value'),YAHOO.vnode.CustomFormatting.connectionCallback2,null);
			}
      else if (o.responseText == 500) {
        alert("This VM cannot be deployed - Check VM state or contact administrator")
      }
      else if (o.responseText == 100) {
        YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=stateAll',YAHOO.vnode.CustomFormatting.connectionCallback2,null);
      }
      else {
        YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=getReservedData',YAHOO.vnode.Basic1.connectionCallback,null);
      }
      refreshHostnames();
      refreshPhysicalHosts();
      YAHOO.vnode.container.wait.hide();
		},

		handleFailure:function(o){
			// Failure handler
      alert('Couldnt contact the server')
      YAHOO.vnode.container.wait.hide();
		}

	};

	/*
 	* Define the callback object for success and failure
 	* handlers as well as object scope.
 	*/
	var callback =
	{
		success:AjaxObject.handleSuccess,
		failure:AjaxObject.handleFailure,
		scope: AjaxObject
	};


	// Define various event handlers for Dialogs
	var handleSubmit = function() {
    var el = new YAHOO.util.Element('vmN');
    el.set('value',randomString());
    var myArrayPhyHost=new Array();
    var myArrayVirtHost=new Array();
    var myArrayExpiryTime=new Array();
    var myArrayMemory=new Array();
    var myArrayPartition=new Array();
    var myArrayOSImage=new Array();
    var myArrayName=new Array();
		if (YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getLength() == 0) {
			alert("Please choose a virtual machine.");
    }
    else {
      for (i = 0; i<YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getLength(); i++) {	
        TrElement =YAHOO.vnode.Basic1.connectionCallback.myDataTable.getTrEl(i)
    	  var oRecord = YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecord(TrElement);
        myArrayPhyHost[i] = oRecord.getData("PhysicalHost");
        myArrayVirtHost[i] = oRecord.getData("VirtualHost");
        myArrayExpiryTime[i] = oRecord.getData("ExpiryTime");
        myArrayMemory[i] = oRecord.getData("Memory");
        myArrayPartition[i] = oRecord.getData("Partition");
        myArrayOSImage[i] = oRecord.getData("OSImage");
        myArrayName[i] = oRecord.getData("Name");
        s0 = myArrayPhyHost.join();
        s1 = myArrayVirtHost.join();
        s2 = myArrayExpiryTime.join();
        s3 = myArrayMemory.join();
        s4 = myArrayPartition.join();
        s5 = myArrayOSImage.join();
        s6 = myArrayName.join();
      }
      YAHOO.vnode.container.wait.show();
      YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=deploy&vmOptions=' +  s0 + "," + s1 + "," + s2 + "," + s3 + "," + s4 + "," + s5 + "," + s6, callback, null);
    }
	};

  var handleEnable = function() {
    var myArray2=new Array();
    if (YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getSelectedRows() != '') {
		  var oRecordId = YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getSelectedRows();
			if(confirm('Are you sure?')) {
				for (i = 0; i<oRecordId.length; i++) {	
					var oRecord = YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getRecordSet().getRecord(oRecordId[i]);
          if (oRecord.getData("StateMessage") != "disabled") {
            alert("You cannot enable " + oRecord.getData("VirtualHost"));
            continue;
          }
          myArray2[i] = oRecord.getData("VirtualHost");
          s = myArray2.join();
				}
        YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=enableVM&virtualHostnames=' +  s, callback, null);
			}
    }
  }

  var handleDisable = function() {
    var myArray2=new Array();
    if (YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getSelectedRows() != '') {
		  var oRecordId = YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getSelectedRows();
			if(confirm('Are you sure?')) {
				for (i = 0; i<oRecordId.length; i++) {	
					var oRecord = YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getRecordSet().getRecord(oRecordId[i]);
          if (oRecord.getData("StateMessage") != "available") {
            alert("You cannot disable " + oRecord.getData("VirtualHost"));
            continue;
          }
          myArray2[i] = oRecord.getData("VirtualHost");
          s = myArray2.join();
				}
        YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=disableVM&virtualHostnames=' +  s, callback,null);
			}
    }
  }

  var handleSubmitVG = function() {
    var elS = new YAHOO.util.Element('vmS');
    var elR = new YAHOO.util.Element('vmR');
    if (elS.get('value') == "" || elS.get('value') == "Select..." || elR.get('value') == "" || elR.get('value') == "Select...")
    {
       alert("Invalid Option");
       return;
    }
    var myArrayPhyHost=new Array();
    var myArrayVirtHost=new Array();
    var myArrayExpiryTime=new Array();
    var myArrayMemory=new Array();
    var myArrayPartition=new Array();
    var myArrayOSImage=new Array();
    var myArrayName=new Array();
		if (YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getLength() == 0) {
			alert("Please choose a virtual machine.");
    }
    else {
      for (i = 0; i<YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getLength(); i++) {
        TrElement =YAHOO.vnode.Basic1.connectionCallback.myDataTable.getTrEl(i)
    	  var oRecord = YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecord(TrElement);
        myArrayPhyHost[i] = oRecord.getData("PhysicalHost");
        myArrayVirtHost[i] = oRecord.getData("VirtualHost");
        myArrayExpiryTime[i] = oRecord.getData("ExpiryTime");
        myArrayMemory[i] = oRecord.getData("Memory");
        myArrayPartition[i] = oRecord.getData("Partition");
        myArrayOSImage[i] = oRecord.getData("OSImage")
        myArrayName[i] = oRecord.getData("Name");

        s0 = myArrayPhyHost.join();
        s1 = myArrayVirtHost.join();
        s2 = myArrayExpiryTime.join();
        s3 = myArrayMemory.join();
        s4 = myArrayPartition.join();
        s5 = myArrayOSImage.join();
        s6 = myArrayName.join();
      }
      YAHOO.vnode.container.wait.show();
      YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=deployVG&vmOptions=' +  s0 + "," + s1 + "," + s2 + "," + s3 + "," + s4 + "," + s5 + "," + s6 + '&vmGlite=' + myArrayRow0 + "," + myArrayRow1 + "," + myArrayRow2 + "," + myArrayRow3 + '&vmSitename=' + elS.get('value') + '&vmRepo=' + elR.get('value'), callback, null  );
    }
  };

 
	var handleSuccess = function(o) {
		var response = o.responseText;
    var el = new YAHOO.util.Element('vmN');
    var data = YAHOO.vnode.container.dialog1.getData();
    if (response == 200) {
      YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=getReservedData',YAHOO.vnode.Basic1.connectionCallback,null);
    }
    else if (response == 500) {
      alert("This is host is notDeployed")
    }
    el.set('value',randomString());
		response = response.split("<!")[0];
		document.getElementById("resp").innerHTML = response;
	};


	var handleFailure = function(o) {
		document.getElementById("resp").innerHTML = "Server Response at " + getNowHours() + ":" + getNowMinutes() + ":" + getNowSeconds() + ": Submission failed - " + o.status;
	};

	var handleDelete = function() {
    var myArray=new Array();
    var el = new YAHOO.util.Element('vmN');
    el.set('value',randomString());
		if (YAHOO.vnode.Basic1.connectionCallback.myDataTable.getSelectedRows() != '') {
		  oRecordIdDelete = YAHOO.vnode.Basic1.connectionCallback.myDataTable.getSelectedRows();
			if(confirm('Are you sure?')) {
				for (i = 0; i<oRecordIdDelete.length; i++) {	
					var oRecord = YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getRecord(oRecordIdDelete[i]);
          myArray[i] = oRecord.getData("VirtualHost");
          s = myArray.join();
				}
        unsetGlite();
	YAHOO.vnode.container.wait.show();
        YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=deleteReserve&virtualHostnames=' +  s, callback, null);
			}
		}
	};

  var handleRefresh = function() {
     var el = new YAHOO.util.Element('vmN');
     el.set('value',randomString());
     YAHOO.vnode.container.wait.show();
     YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=getReservedData',YAHOO.vnode.Basic1.connectionCallback,null);
  }

  var handleRefreshTerm = function() {
    YAHOO.vnode.Basic2.myDataSource.sendRequest('vmAction=userVM',YAHOO.vnode.Basic2.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.Basic2.myDataTable);
  }

  var handleRefreshUpTime = function() {
    YAHOO.vnode.Basic3.myDataSource.sendRequest('vmAction=upTime',YAHOO.vnode.Basic3.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.Basic3.myDataTable);
  }

  var handleTerminateAdmin = function() {
    var myArray6=new Array();
    if (YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getSelectedRows() != '') {
		  var oRecordId = YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getSelectedRows();
			if(confirm('Are you sure?')) {
				for (i = 0; i<oRecordId.length; i++) {	
					var oRecord = YAHOO.vnode.CustomFormatting.connectionCallback2.myDataTable.getRecordSet().getRecord(oRecordId[i]);
          myArray6[i] = oRecord.getData("VirtualHost");
          s = myArray6.join();
				}
	      YAHOO.vnode.container.wait.show();
        YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=terminateExtra&virtualHostnames=' +  s, callback, null);
			}
    }
  }

  var handleTerminate = function() {
    myArray2=new Array(); 
    if (YAHOO.vnode.Basic2.myDataTable.getSelectedRows() != '') {
		  var oRecordId = YAHOO.vnode.Basic2.myDataTable.getSelectedRows();
			if(confirm('Are you sure?')) {
				for (i = 0; i<oRecordId.length; i++) {	
					var oRecord = YAHOO.vnode.Basic2.myDataTable.getRecordSet().getRecord(oRecordId[i]);
          myArray2[i] = oRecord.getData("VirtualHost");
          s = myArray2.join();
				}
	      YAHOO.vnode.container.wait.show();
        YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=terminate&virtualHostnames=' +  s, callback, null);
			}
    }
  }

  var handleRefreshVG = function() {
     YAHOO.vnode.Basic10.myDataSource.sendRequest('vmAction=userVG',YAHOO.vnode.Basic10.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.Basic10.myDataTable);
     var el = new YAHOO.util.Element('vmS2');
     el.set('value',"Select...");
  }

  var handleTerminateVG = function() {
    myArray2=new Array();
    if (YAHOO.vnode.Basic10.myDataTable.getSelectedRows() != '') {
		  var oRecordId = YAHOO.vnode.Basic10.myDataTable.getSelectedRows();
			if(confirm('Are you sure?')) {
				for (i = 0; i<oRecordId.length; i++) {	
					var oRecord = YAHOO.vnode.Basic10.myDataTable.getRecordSet().getRecord(oRecordId[i]);
          myArray2[i] = oRecord.getData("VirtualHost");
          s = myArray2.join();
				}
	      YAHOO.vnode.container.wait.show();
        YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=terminate&virtualHostnames=' +  s, callback, null);
			}
    }
  }

  var handleRefreshAdmin = function () {
    var elState = new YAHOO.util.Element('allAdmin');
    if (elState.get('value') == "Select..." || elState.get('value') == "") {
      alert("Please select a state")
      return;
    }
    else {
      YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=state'+elState.get('value'),YAHOO.vnode.CustomFormatting.connectionCallback2,null)
    }
  }

  var handleRefreshState = function () {
    var elState = new YAHOO.util.Element('allStates');
    if (elState.get('value') == "Select..." || elState.get('value') == "") {
      alert("Please select a state")
      return;
    }
    else {
      YAHOO.util.Connect.asyncRequest('GET',proto + host + path +'?vmAction=state'+elState.get('value'),YAHOO.vnode.CustomFormatting.connectionCallback2,null)
    }
  }

  var handleRefreshStatVgs = function () {
    var elState = new YAHOO.util.Element('allStatesVG');
    if (elState.get('value') == "Select..." || elState.get('value') == "") {
      alert("Please select a state")
      return;
    }
    else {
      YAHOO.vnode.CustomFormatting2.myDataSource.sendRequest('vmAction=stateVG&vgState='+elState.get('value'),YAHOO.vnode.CustomFormatting2.myDataTable.onDataReturnInitializeTable, YAHOO.vnode.CustomFormatting2.myDataTable);
    }
  }

  var handleTerminateAllVG = function () {
    alert("Not implemented")
  }

  var handleTerminateSiteVG = function () {
    var elS2 = new YAHOO.util.Element('vmS2');
    if (elS2.get('value') == "Select..." || elS2.get('value') == "") {
      alert("Pick a valid sitename");
      return;
    }
    else {
  	  YAHOO.vnode.container.wait.show();
      YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=terminateVG&&vmOption=site&vmSite=' + elS2.get('value'), callback, null);
    }
  }
  
	var handleAdd = function() {
		var data = this.getData();
		if (YAHOO.vnode.Basic1.connectionCallback.myDataTable.getRecordSet().getLength() < 4) {
      //alert(username.replace('\n', '', 'g'));
      if (data.physicalHost.match(/lxb76*/) && username.replace('\n', '', 'g') != 'lponcet' ) {
        alert('This machine is for Louis Poncet. Pick another machine');
        return;
      }
      if (data.virtualHostnames.match(/lxb76*/) && username.replace('\n', '', 'g') != 'lponcet' ) {
        alert('That virtual machine is for Louis Poncet. Pick another virtual machine');
        return;
      }
      /*
      if (data.physicalHost.match(/^(lxxen104.cern.ch|lxxen103.cern.ch)/)) {
 				if (data.virtualHostnames.match(/ctb-generic-(1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-1])/)) {         
          alert('lxxen104 machine can only be deployed with hostnames vtb-generic-[1-15]');
          return;
        }
        if (data.osImageVM.match(/.-64/)) {
          alert('Impossible to start 64 bit images on this machine - use the other hosts lxxen0*');
          return;
        }
      }
			else  {
				if (data.virtualHostnames.match(/vtb-generic-./)) {
					alert('lxxen machines can only be deployed with hostnames ctb-generic-[40-79]');
					return;
				}
			}
      */
      if (data.physicalHost != 'Select...' && data.virtualHostnames != 'Select...' && data.expiryTimeVM != 'Select...' && data.memoryVM != 'Select...' && data.partitionVM != 'Select...' && data.osImageVM != 'Select...') {
       el = new YAHOO.util.Element('actionScript');el.set("value","reserve");
       YAHOO.vnode.container.wait.show();
       var el = new YAHOO.util.Element('vmN');
       el.set('value',randomString());
       if (data.imageFilename == "") {
          YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=reserve&physicalHost=' + data.physicalHost + "&virtualHostnames=" + data.virtualHostnames + "&expiryTimeVM=" + data.expiryTimeVM +  "&memoryVM=" + data.memoryVM + "&partitionVM=" + data.partitionVM + "&vmName=" + data.vmName + "&osImageVM=" + data.osImageVM , callback, null);
       }
       else {
          YAHOO.util.Connect.asyncRequest('GET', proto + host + path +'?vmAction=reserve&physicalHost=' + data.physicalHost + "&virtualHostnames=" + data.virtualHostnames + "&expiryTimeVM=" + data.expiryTimeVM +  "&memoryVM=" + data.memoryVM + "&partitionVM=" + data.partitionVM + "&vmName=" + data.vmName + "&imageFilename=" + data.imageFilename , callback, null);
       }
     }
     else {
        alert('Fill out the comboBoxes');
     }
		}
		else {
			alert("You can't add more Virtual Machines");
		}
	};

  //define the visual container when waiting for server data
	YAHOO.vnode.container.wait = 
		new YAHOO.widget.Panel("wait",  
			{ width:"240px", 
			  fixedcenter:true, 
			  close:false, 
			  draggable:false, 
			  zindex:4,
			  modal:true,
			  visible:false
			} 
		);

	YAHOO.vnode.container.wait.setHeader("Loading, please wait...");
	YAHOO.vnode.container.wait.setBody('<img src="/server/template/html/img/loading.gif" />');
	YAHOO.vnode.container.wait.render(document.body);

  // Define the visual block container
	YAHOO.vnode.container.block = 
		new YAHOO.widget.Panel("block",  
			{ width:"430px", 
			  fixedcenter:true, 
			  close:false, 
			  draggable:false, 
			  zindex:4,
			  modal:true,
			  visible:false
			} 
		);

	YAHOO.vnode.container.block.setHeader("Portal is blocked - Come back later");
	YAHOO.vnode.container.block.setBody('<img src="/server/template/html/img/block.jpg" />')
  YAHOO.vnode.container.block.setFooter("<b>Reason: Updating the Portal...</b>");
	YAHOO.vnode.container.block.render(document.body);

	// Instantiate the deploy VM Dialog
	YAHOO.vnode.container.dialog1 = new YAHOO.widget.Dialog("dialogDeployVMs", 
							{ width : "75em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : false,
								draggable:true,
                //dragOnly:true,
                close:true,
                underlay: "none",
								hideaftersubmit:false,
							  buttons : [ { text:"Deploy", handler:handleSubmit, isDefault:true },
								      { text:"Add", handler:handleAdd },
 								      { text:"Delete", handler:handleDelete },
                      { text:"Refresh", handler:handleRefresh }]
							});
	// Wire up the success and failure handlers
	YAHOO.vnode.container.dialog1.callback = { success: handleSuccess, failure: handleFailure };

  var h_kl1 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:68 },                               
                                                   { fn:YAHOO.vnode.container.dialog1.hide, 
                                                   scope:YAHOO.vnode.container.dialog1, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog1.cfg.queueProperty("keylisteners", h_kl1); 

	// Render the Dialog
	YAHOO.vnode.container.dialog1.render();

	// Instantiate the terminate VM Dialog
	YAHOO.vnode.container.dialog2 = new YAHOO.widget.Dialog("terminateVMs", 
							{ width : "65em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : true,
								//draggable:true,
                dragOnly:true,
                close:true,
                underlay: "none",
							  buttons : [ { text:"Refresh", handler:handleRefreshTerm, isDefault:true },{ text:"Terminate", handler:handleTerminate }]
							});

  var h_kl2 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:84 },                               
                                                   { fn:YAHOO.vnode.container.dialog2.hide, 
                                                   scope:YAHOO.vnode.container.dialog2, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog2.cfg.queueProperty("keylisteners", h_kl2); 


	// Render the Dialog
	YAHOO.vnode.container.dialog2.render();

	// Instantiate the state VM Dialog
	YAHOO.vnode.container.dialog3 = new YAHOO.widget.Dialog("stateOfVMs", 
							{ width : "50em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : true,
								draggable:true,
                close:true,
                underlay: "none",
							  buttons : [ { text:"Refresh", handler:handleRefreshState, isDefault:true }]
							});

  var h_kl3 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:83 },                               
                                                   { fn:YAHOO.vnode.container.dialog3.hide, 
                                                   scope:YAHOO.vnode.container.dialog3, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog3.cfg.queueProperty("keylisteners", h_kl3); 


	// Render the Dialog
	YAHOO.vnode.container.dialog3.render();

	// Instantiate the upTime VM Dialog
	YAHOO.vnode.container.dialog4 = new YAHOO.widget.Dialog("upTimeVMs", 
							{ width : "55em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : true,
								draggable:true,
                close:true,
                underlay: "none",
							  buttons : [ { text:"Refresh", handler:handleRefreshUpTime, isDefault:true }]
							});

  var h_kl4 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:85 },                               
                                                   { fn:YAHOO.vnode.container.dialog4.hide, 
                                                   scope:YAHOO.vnode.container.dialog4, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog4.cfg.queueProperty("keylisteners", h_kl4); 

	// Render the Dialog
	YAHOO.vnode.container.dialog4.render();

	// Instantiate the deploy VG Dialog
	YAHOO.vnode.container.dialog5 = new YAHOO.widget.Dialog("startVGs", 
							{ width : "85em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : false,
								draggable:true,
                close:true,
                underlay: "none",
                buttons: [ { text:"Deploy Virtual Grid", handler:handleSubmitVG, isDefault:true }]
							});

  var h_kl5 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:86 },                               
                                                   { fn:YAHOO.vnode.container.dialog5.hide, 
                                                   scope:YAHOO.vnode.container.dialog5, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog5.cfg.queueProperty("keylisteners", h_kl5); 


	// Render the Dialog
	YAHOO.vnode.container.dialog5.render();

	// Instantiate the state VG Dialog
	YAHOO.vnode.container.dialog6 = new YAHOO.widget.Dialog("stateVGs", 
							{ width : "60em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : true,
								draggable:true,
                close:true,
                underlay: "none",
							  buttons : [ { text:"Refresh", handler:handleRefreshStatVgs, isDefault:true }]
							});

  var h_kl6 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:67 },                               
                                                   { fn:YAHOO.vnode.container.dialog6.hide, 
                                                   scope:YAHOO.vnode.container.dialog6, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog6.cfg.queueProperty("keylisteners", h_kl6); 

	// Render the Dialog
	YAHOO.vnode.container.dialog6.render();

	// Instantiate the terminate VG Dialog
	YAHOO.vnode.container.dialog7 = new YAHOO.widget.Dialog("terminateVGs", 
							{ width : "35em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : true,
								draggable:true,
                close:true,
                underlay: "none",
                buttons : [ { text:"Terminate", handler:handleTerminateVG },{ text:"Terminate Site", handler:handleTerminateSiteVG }, { text:"Terminate All", handler:handleTerminateAllVG}, { text:"Refresh", handler:handleRefreshVG, isDefault:true}]
							});

  var h_kl7 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:88 },                               
                                                   { fn:YAHOO.vnode.container.dialog7.hide, 
                                                   scope:YAHOO.vnode.container.dialog7, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog7.cfg.queueProperty("keylisteners", h_kl7); 

	// Render the Dialog
	YAHOO.vnode.container.dialog7.render();


	// Instantiate the admin Dialog
	YAHOO.vnode.container.dialog8 = new YAHOO.widget.Dialog("admins", 
							{ width : "50em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : true,
								draggable:true,
                close:true,
                underlay: "none",
                buttons : [ { text:"Terminate", handler:handleTerminateAdmin}, {text:"Refresh", handler:handleRefreshAdmin}, {text: "Disable", handler:handleDisable},{text: "Enable", handler:handleEnable}]
							});

  var h_kl8 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:65 },                               
                                                   { fn:YAHOO.vnode.container.dialog8.hide, 
                                                   scope:YAHOO.vnode.container.dialog8, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog8.cfg.queueProperty("keylisteners", h_kl8); 

	// Render the Dialog
	YAHOO.vnode.container.dialog8.render();

	// Instantiate the terminate VM Dialog
	YAHOO.vnode.container.dialog9 = new YAHOO.widget.Dialog("siteInfo", 
							{ width : "40em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : false,
								//draggable:true,
                dragOnly:true,
                close:true,
                underlay: "none",
							});
 
  var h_kl9 = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:90 },                               
                                                   { fn:YAHOO.vnode.container.dialog9.hide, 
                                                   scope:YAHOO.vnode.container.dialog9, 
                                                   correctScope:true } ); 
  
  YAHOO.vnode.container.dialog9.cfg.queueProperty("keylisteners", h_kl9);

 	// Instantiate the service_type dialog
	YAHOO.vnode.container.dialog_service_type = new YAHOO.widget.Dialog("serviceType", 
							{ width : "40em",
							  fixedcenter : false,
							  visible : false, 
							  constraintoviewport : false,
                dragOnly:true,
                close:true,
                underlay: "none",
							});
 
  var h_kl_service_type = new YAHOO.util.KeyListener(document, { alt:true, shift: true,keys:74 },                               
                                                               { fn:YAHOO.vnode.container.dialog_service_type.hide, 
                                                                 scope:YAHOO.vnode.container.dialog_service_type, 
                                                                 correctScope:true } ); 
  
  YAHOO.vnode.container.dialog_service_type.cfg.queueProperty("keylisteners", h_kl_service_type);  


	// Render the Dialog
	YAHOO.vnode.container.dialog_service_type.render();


  // Setup the proxies and the overlay for the dialogs
  YAHOO.vnode.container.manager = new YAHOO.widget.OverlayManager();

  var el = new YAHOO.util.Element('vmN');
  el.set('value',randomString());

  var dd1 = new YAHOO.util.DDProxy("dialogDeployVMs_h");
 
  (dd1.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd1.getDragEl());
    YAHOO.util.Dom.setXY("dialogDeployVMs_c",getXY,false); 
    //YAHOO.vnode.container.overlay1.syncPosition();
  });

  var dd2 = new YAHOO.util.DDProxy("terminateVMs_h");

  (dd2.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd2.getDragEl());
    YAHOO.util.Dom.setXY("terminateVMs_c",getXY,false);
    //YAHOO.vnode.container.overlay2.syncPosition();
  });

  var dd3 = new YAHOO.util.DDProxy("stateOfVMs_h");

  (dd3.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd3.getDragEl());
    YAHOO.util.Dom.setXY("stateOfVMs_c",getXY,false);
    //YAHOO.vnode.container.overlay3.syncPosition();
  });

  var dd4 = new YAHOO.util.DDProxy("upTimeVMs_h");

  (dd4.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd4.getDragEl());
    YAHOO.util.Dom.setXY("upTimeVMs_c",getXY,false);
  });

  var dd5 = new YAHOO.util.DDProxy("startVGs_h");

  (dd5.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd5.getDragEl());
    YAHOO.util.Dom.setXY("startVGs_c",getXY,false);  
  });

  var dd6 = new YAHOO.util.DDProxy("stateVGs_h");

  (dd6.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd6.getDragEl());
    YAHOO.util.Dom.setXY("stateVGs_c",getXY,false);
  });

  var dd7 = new YAHOO.util.DDProxy("terminateVGs_h");

  (dd7.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd7.getDragEl());
    YAHOO.util.Dom.setXY("terminateVGs_c",getXY,false);
  });

  var dd8 = new YAHOO.util.DDProxy("admins_h");

  (dd8.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd8.getDragEl());
    YAHOO.util.Dom.setXY("admins_c",getXY,false);
  });

  var dd9 = new YAHOO.util.DDProxy("siteInfo_h");

  (dd9.endDrag = function() {
    getXY = YAHOO.util.Dom.getXY(dd9.getDragEl());
    YAHOO.util.Dom.setXY("siteInfo_c",getXY,false);
  });

  //Key Listeners
  YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog1);

  //shift-D
  var kl1 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:68 },  
                                                 { fn:fnCallback,
                                                   scope:YAHOO.vnode.container.dialog1, 
                                                   correctScope:true } );  
  kl1.enable(); 

  //shift-T
  var kl2 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:84 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog2, 
                                                   correctScope:true } );  
  kl2.enable(); 

  //shift-S
  var kl3 = new YAHOO.util.KeyListener(document, { alt:true,shift:true, keys:83 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog3, 
                                                   correctScope:true } );  
  kl3.enable(); 

  //shift-U
  var kl4 = new YAHOO.util.KeyListener(document, { alt:true,shift:true, keys:85 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog4, 
                                                   correctScope:true } );  
  kl4.enable();

   //shift-V
  var kl5 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:86 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog5, 
                                                   correctScope:true } );  
  kl5.enable();

   //shift-C
  var kl6 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:67 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog6, 
                                                   correctScope:true } );  
  kl6.enable();

   //shift-X
  var kl7 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:88 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog7, 
                                                   correctScope:true } );  
  kl7.enable();

   //shift-A
  var kl8 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:65 },  
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog8, 
                                                   correctScope:true } );  
  kl8.enable();

  //shift-Z
  var kl9 = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:90 }, 
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog9, 
                                                   correctScope:true } );  
  kl9.enable();

  //shift-J
  var kl_service_type = new YAHOO.util.KeyListener(document, { alt:true, shift:true, keys:74 }, 
                                                 { fn:fnCallback,  
                                                   scope:YAHOO.vnode.container.dialog_service_type, 
                                                   correctScope:true } );  
  kl_service_type.enable();
 

  function fnCallback(e) {
    //alert(YAHOO.vnode.container.manager.getActive());
    if (this.id == "dialogDeployVMs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog1.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog1);
    }
    else if (this.id == "terminateVMs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog2.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog2);
    }
    else if (this.id == "stateOfVMs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog3.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog3);
    }
    else if (this.id == "upTimeVMs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog4.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog4);
    }
    else if (this.id == "startVGs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog5.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog5);
    }
    else if (this.id == "stateVGs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog6.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog6);
    }
    else if (this.id == "terminateVGs") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog7.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog7);
    }
    else if (this.id == "admins") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog8.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog8);
    }
    else if (this.id == "siteInfo") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog9.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog9);
    }
    else if (this.id == "serviceType") {
      if (e == "keyPressed") {
        YAHOO.vnode.container.dialog_service_type.show();
      }
      YAHOO.vnode.container.manager.focus(YAHOO.vnode.container.dialog_service_type);
    }
  }

  YAHOO.util.Event.addListener("dialogDeployVMs", "click", fnCallback);
  YAHOO.util.Event.addListener("terminateVMs", "click", fnCallback);
  YAHOO.util.Event.addListener("stateOfVMs", "click", fnCallback);
  YAHOO.util.Event.addListener("upTimeVMs", "click", fnCallback);
  YAHOO.util.Event.addListener("startVGs", "click", fnCallback);
  YAHOO.util.Event.addListener("stateVGs", "click", fnCallback);
  YAHOO.util.Event.addListener("terminateVGs", "click", fnCallback);
  YAHOO.util.Event.addListener("admins", "click", fnCallback);
  YAHOO.util.Event.addListener("siteInfo", "click", fnCallback);


 (dd1.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd1.getDragEl(), 'height',YAHOO.util.Dom.getStyle("dialogDeployVMs", 'height') );
  });

 (dd2.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd2.getDragEl(), 'height',YAHOO.util.Dom.getStyle("terminateVMs", 'height') );
  });

 (dd3.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd3.getDragEl(), 'height',YAHOO.util.Dom.getStyle("stateOfVMs", 'height') );
  });

 (dd4.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd4.getDragEl(), 'height',YAHOO.util.Dom.getStyle("upTimeVMs", 'height') );
  });

 (dd5.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd5.getDragEl(), 'height',YAHOO.util.Dom.getStyle("startVGs", 'height') );
  });

 (dd6.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd6.getDragEl(), 'height',YAHOO.util.Dom.getStyle("stateVGs", 'height') );
  });

 (dd7.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd7.getDragEl(), 'height',YAHOO.util.Dom.getStyle("terminateVGs", 'height') );
  });

 (dd8.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd8.getDragEl(), 'height',YAHOO.util.Dom.getStyle("admins", 'height') );
  });

 (dd9.startDrag = function() {

    YAHOO.util.Dom.setStyle(dd9.getDragEl(), 'height',YAHOO.util.Dom.getStyle("siteInfo", 'height') );
  });

  // register the dialogs on the overlay manager
  YAHOO.vnode.container.manager.register([YAHOO.vnode.container.dialog1,
                                            YAHOO.vnode.container.dialog2,
                                            YAHOO.vnode.container.dialog3,
                                            YAHOO.vnode.container.dialog4,
                                            YAHOO.vnode.container.dialog5,
                                            YAHOO.vnode.container.dialog6,
                                            YAHOO.vnode.container.dialog7,
                                            YAHOO.vnode.container.dialog8,
                                            YAHOO.vnode.container.dialog9,
                                            YAHOO.vnode.container.dialog_service_type,
                                            ]);
 
}
YAHOO.util.Event.onDOMReady(init);

