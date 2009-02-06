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
*	Author:
*		Ricardo Mendes <Ricardo DOT Mendes AT cern DOT ch>
*/

YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.Basic4 = new function() {
        var myColumnDefs = [
            {key:"Name", sortable:true, resizeable:false},
            {key:"PhysicalHost", sortable:true, resizeable:false},
            {key:"VirtualHost", sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false},
            {key:"ExpiryTime", sortable:true, resizeable:false},
            {key:"Memory", sortable:true, resizeable:false},
            {key:"Partition", sortable:true, resizeable:false},
            {key:"OSImage", sortable:true, resizeable:false},
            {key:"ExpiryTimeAt", sortable:true, resizeable:false}
        ];

        this.myDataSource = new YAHOO.util.DataSource(window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?');

        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["PhysicalHost","VirtualHost","ExpiryTime","Memory","Partition","OSImage","ExpiryTimeAt","Name"]
        };

        this.myDataTable = new YAHOO.widget.DataTable("vgTable",
                myColumnDefs, this.myDataSource, {initialRequest:"vmAction=getReservedData", timeout:15000});  

       	// Subscribe to events for row selection 
				this.myDataTable.subscribe("rowMouseoverEvent", this.myDataTable.onEventHighlightRow); 
				this.myDataTable.subscribe("rowMouseoutEvent", this.myDataTable.onEventUnhighlightRow); 
				this.myDataTable.subscribe("rowClickEvent", this.myDataTable.onEventSelectRow); 
				// Programmatically select the first row 
				this.myDataTable.selectRow(this.myDataTable.getTrEl(0));

      // Programmatically select the first row 
      	this.myDataTable.selectRow(this.myDataTable.getTrEl(0)); 
      // Programmatically bring focus to the instance so arrow selection works immediately 
      	this.myDataTable.focus();  
 
    };
});
