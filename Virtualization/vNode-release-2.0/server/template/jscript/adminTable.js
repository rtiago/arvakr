YAHOO.util.Event.addListener(window, "load", function() {

    YAHOO.vnode.CustomFormatting = new function() {

      this.connectionCallback2 = {
        success:function(o) {
      
        var jsDoc = o.responseText;

				this.myCustomFormatter = function(elCell, oRecord, oColumn, oData) {
            if(oData == "available") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#003300');
						}
						else if (oData == "deploying") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#FFFF00');
						}
						else if (oData == "failed") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#FF0000');
						}
						else if (oData == "deployed") {
  						YAHOO.util.Dom.setStyle(elCell, 'background-color', '#00FF00');
						}
						else if (oData == "deployedNV") {
  						YAHOO.util.Dom.setStyle(elCell, 'background-color', '#FFAA00');
						}
						else if (oData == "reserved") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#333366');
						}
						else if (oData == "terminating") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#CCCC00');
						}
						else if (oData == "disabled") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#444444');
						}
				};
        var myColumnDefs = [
            {key:"VirtualHost", sortable:true, resizeable:false},
            {key:"StateMessage", sortable:true, resizeable:false},
            {key:"Message", sortable:true,resizeable:false},
            {key:"StateColor", formatter:this.myCustomFormatter, sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false, width:60}
         ];


        this.myDataSource = new YAHOO.util.DataSource(jsDoc);
        this.myDataSource.dataType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["VirtualHost","StateMessage","Message","StateColor"]
        };
        var oConfigs = {
            paginator: new YAHOO.widget.Paginator({rowsPerPage: 10})
        };
        this.myDataTable = new YAHOO.widget.DataTable("admin",
                myColumnDefs, this.myDataSource, oConfigs,{selectionMode:"single"} );

      this.myDataTable.subscribe("rowMouseoverEvent", this.myDataTable.onEventHighlightRow);
      this.myDataTable.subscribe("rowMouseoutEvent", this.myDataTable.onEventUnhighlightRow);
      this.myDataTable.subscribe("rowClickEvent", this.myDataTable.onEventSelectRow);
    
      this.myDataTable.selectRow(this.myDataTable.getTrEl(0));

        var myColumnDefs4 = [

            {key:"VirtualHost", sortable:true, resizeable:false},
            {key:"StateMessage", sortable:true, resizeable:false},
            {key:"Message", sortable:true,resizeable:false},
            {key:"StateColor", formatter:this.myCustomFormatter, sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false, width:60}
        ];


        this.myDataSource.responseSchema = {
            fields: ["VirtualHost","StateMessage","Message","StateColor"]
        };
        var oConfigs = {
            paginator: new YAHOO.widget.Paginator({rowsPerPage: 10})
        };
        this.myDataTable4 = new YAHOO.widget.DataTable("stateVM",
                myColumnDefs4, this.myDataSource, oConfigs ,{selectionMode:"single"} );


        this.myDataTable4.subscribe("rowMouseoverEvent", this.myDataTable4.onEventHighlightRow);
        this.myDataTable4.subscribe("rowMouseoutEvent", this.myDataTable4.onEventUnhighlightRow);
				YAHOO.vnode.container.wait.hide();
      },
      failure:function(o) {
				YAHOO.vnode.container.wait.hide();
        alert("Failure");
      },
      timeout: 1200000
    };
    YAHOO.util.Connect.asyncRequest('GET',window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?vmAction=stateAll',this.connectionCallback2,null)
    };
});
