YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.Basic2 = new function() {
        var myColumnDefs = [
            {key:"Name", sortable:true,editor:"textbox",resizeable:false},
            {key:"PhysicalHost", sortable:true, resizeable:false},
            {key:"VirtualHost", sortable:true, resizeable:false},
            {key:"Uptime",sortable:true, resizeable:false},
            {key:'OS', sortable:true,resizeable:false}
        ];

        this.myDataSource = new YAHOO.util.DataSource(window.location.protocol +'//'+ window.location.hostname+'/cgi/server/cgi-bin/main.py?', {connTimeout: 15000})
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            fields: ["Name","PhysicalHost","VirtualHost","Uptime","OS"]
        };

        var oConfigs = {
            paginator: new YAHOO.widget.Paginator({rowsPerPage: 10}),
            initialRequest: "vmAction=userVM"
        };

        this.myDataTable = new YAHOO.widget.DataTable("terminateVM",
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

        this.myDataTable.subscribe("cellDblclickEvent",this.myDataTable.onEventShowCellEditor);
        this.myDataTable.subscribe("editorBlurEvent", this.myDataTable.onEventSaveCellEditor);

        // When cell is edited, pulse the color of the row yellow
        this.onCellEdit = function(oArgs) {
            var elCell = oArgs.editor.cell;
            var oOldData = oArgs.oldData;
            var oNewData = oArgs.newData;

            // Grab the row el and the 2 colors
            var elRow = this.getTrEl(elCell);
            var origColor = YAHOO.util.Dom.getStyle(elRow.cells[0], "backgroundColor");
            var pulseColor = "#ff0";

            // Create a temp anim instance that nulls out when anim is complete
            var rowColorAnim = new YAHOO.util.ColorAnim(elRow.cells, {
                    backgroundColor:{to:origColor, from:pulseColor}, duration:2});
            var onComplete = function() {
                rowColorAnim = null;
                YAHOO.util.Dom.setStyle(elRow.cells, "backgroundColor", "");
            }
            rowColorAnim.onComplete.subscribe(onComplete);
            rowColorAnim.animate();
        }
        this.myDataTable.subscribe("editorSaveEvent", this.onCellEdit);
 
      	this.myDataTable.focus();  

    };
});
