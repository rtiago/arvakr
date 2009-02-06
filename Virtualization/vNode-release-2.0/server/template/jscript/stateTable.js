/*Implemented in adminTable.js */
YAHOO.util.Event.addListener(window, "load", function() {

    YAHOO.vnode.CustomFormatting = new function() {

				this.myCustomFormatter = function(elCell, oRecord, oColumn, oData) {
						alert(oColumn);
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
						else if (oData == "reserved") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#333366');
						}
						else if (oData == "terminating") {
							YAHOO.util.Dom.setStyle(elCell, 'background-color', '#CCCC00');
						}
				};
        var myColumnDefs = [
            {key:"VirtualHost", sortable:true, resizeable:false},
            {key:"StateMessage", sortable:true, resizeable:false},
            {key:"Message", sortable:true,resizeable:false},
            {key:"StateColor", formatter:this.myCustomFormatter, sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false, width:60}
        ];

        this.myDataSource = new YAHOO.util.DataSource(window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?')
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["VirtualHost","StateMessage","Message","StateColor"]
        };
        var oConfigs = {
            paginator: new YAHOO.widget.Paginator({rowsPerPage: 10}),
            initialRequest: "vmAction=stateAll"
        };
        this.myDataTable = new YAHOO.widget.DataTable("stateVM",
                myColumnDefs, this.myDataSource, oConfigs,{selectionMode:"single"} );


        this.myDataTable.subscribe("rowMouseoverEvent", this.myDataTable.onEventHighlightRow);
        this.myDataTable.subscribe("rowMouseoutEvent", this.myDataTable.onEventUnhighlightRow);
    };
});
