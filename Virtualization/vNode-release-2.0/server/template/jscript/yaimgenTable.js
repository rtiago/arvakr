YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.Basic5 = new function() {
        var myColumnDefs = [
            {key:"Name", sortable:true, resizeable:false},
            {key:"PhysicalHost", sortable:true, resizeable:false},
            {key:"VirtualHost", sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false},
            {key:"gliteService1", formatter:YAHOO.widget.DataTable.formatDropdown,sortable:true, resizeable:false},
            {key:"gliteService2", formatter:YAHOO.widget.DataTable.formatDropdown,sortable:true, resizeable:false},
            {key:"gliteService3", formatter:YAHOO.widget.DataTable.formatDropdown,sortable:true, resizeable:false},
            {key:"gliteService4", formatter:YAHOO.widget.DataTable.formatDropdown,sortable:true, resizeable:false},
            {key:"gliteService5", formatter:YAHOO.widget.DataTable.formatDropdown,sortable:true, resizeable:false}
        ];

        this.myDataSource = new YAHOO.util.DataSource(window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?',{connTimeout: 15000});

        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["PhysicalHost","VirtualHost","Name"]
        };

        this.myDataTable = new YAHOO.widget.DataTable("yaimgenTable",
                myColumnDefs, this.myDataSource, {initialRequest:"vmAction=getReservedData"});  

       	// Subscribe to events for row selection 
				this.myDataTable.subscribe("rowMouseoverEvent", this.myDataTable.onEventHighlightRow); 
				this.myDataTable.subscribe("rowMouseoutEvent", this.myDataTable.onEventUnhighlightRow); 

    };
});
