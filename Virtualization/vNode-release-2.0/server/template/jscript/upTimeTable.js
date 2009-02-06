YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.Basic3 = new function() {
        var myColumnDefs = [
            {key:"Owner", sortable:true, resizeable:false},
            {key:"PhysicalHost", sortable:true, resizeable:false},
            {key:"VirtualHost", sortable:true, resizeable:false},
            {key:"UpTime", sortable:true, resizeable:false}
        ];
        this.myDataSource = new YAHOO.util.DataSource(window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?',{connTimeout: 15000})
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["Owner","PhysicalHost","VirtualHost","UpTime"]
        };

        var oConfigs = {
            paginator: new YAHOO.widget.Paginator({rowsPerPage: 10}),
            initialRequest: "vmAction=upTime"
        };
        this.myDataTable = new YAHOO.widget.DataTable("upTimeVM",
                myColumnDefs, this.myDataSource, oConfigs ,{selectionMode:"single"} );


        this.myDataTable.subscribe("rowMouseoverEvent", this.myDataTable.onEventHighlightRow);
        this.myDataTable.subscribe("rowMouseoutEvent", this.myDataTable.onEventUnhighlightRow);

    };
});
