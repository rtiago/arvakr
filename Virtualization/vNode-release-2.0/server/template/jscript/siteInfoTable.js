YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.BasicSiteInfo = new function() {

        // Custom formatter for "Value" column to preserve line breaks
        var formatAddress = function(elCell, oRecord, oColumn, oData) {
            elCell.innerHTML = "<pre class=\"address\">" + oData + "</pre>";
        };

        var myColumnDefs = [
            {key:"Enable", formatter:YAHOO.widget.DataTable.formatCheckbox},
            {key:"Variable"},
            {key:"Value", width:200, formatter: formatAddress,editor:"textarea"}
        ];

        this.myDataSource = new YAHOO.util.DataSource(YAHOO.vnode.siteInfo);
        this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
        this.myDataSource.responseSchema = {
            resultsList: "items",
            fields: [
                {key:"Enable"},
                {key:"Variable"},
                {key:"Value"}
            ]
        };

        this.myDataTable = new YAHOO.widget.DataTable("siteinfo",
                myColumnDefs, this.myDataSource, {scrollable:true,height:"20em"});


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

//      	this.myDataTable.focus(); 

    };
});
