YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.Basic10 = new function() {
        var myColumnDefs = [
            {key:"PhysicalHost", sortable:true, resizeable:false},
            {key:"VirtualHost", sortable:true, resizeable:false}
        ];
        this.myDataSource = new YAHOO.util.DataSource(window.location.protocol + '//' + window.location.hostname +'/cgi/server/cgi-bin/main.py?', {connTimeout: 15000})
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["PhysicalHost","VirtualHost"]
        };

        var oConfigs = {
            paginator: new YAHOO.widget.Paginator({rowsPerPage: 10}),
            initialRequest: "vmAction=userVG"
        };

        this.myDataTable = new YAHOO.widget.DataTable("terminateVG",
                myColumnDefs, this.myDataSource, oConfigs);

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
