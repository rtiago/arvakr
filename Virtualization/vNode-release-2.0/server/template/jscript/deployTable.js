YAHOO.util.Event.addListener(window, "load", function() {
    YAHOO.vnode.Basic1 = new function() {
      this.connectionCallback = {
       success:function(o) {

          var jsDoc = o.responseText;

          var myColumnDefs = [
            {key:"Name", sortable:true, editor:"textbox",resizeable:false},
            {key:"PhysicalHost", sortable:true, resizeable:false},
            {key:"VirtualHost", sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false},
            {key:"ExpiryTime", sortable:true, resizeable:false},
            {key:"Memory", sortable:true, resizeable:false},
            {key:"Partition", sortable:true, resizeable:false},
            {key:"OSImage", sortable:true, resizeable:false},
            {key:"ExpiryTimeAt", sortable:true, resizeable:false}
          ]; 
          this.myDataSource = new YAHOO.util.DataSource(jsDoc);
          this.myDataSource.dataType = YAHOO.util.DataSource.TYPE_JSON;
          this.myDataSource.responseType = YAHOO.util.DataSource.TYPE_JSON;
          this.myDataSource.responseSchema = {
            fields: ["PhysicalHost","VirtualHost","ExpiryTime","Memory","Partition","OSImage","ExpiryTimeAt","Name"]
          };
          this.myDataTable = new YAHOO.widget.DataTable("basic",
                myColumnDefs, this.myDataSource);  

       	  // Subscribe to events for row selection 
				  this.myDataTable.subscribe("rowMouseoverEvent", this.myDataTable.onEventHighlightRow); 
				  this.myDataTable.subscribe("rowMouseoutEvent", this.myDataTable.onEventUnhighlightRow); 
				  this.myDataTable.subscribe("rowClickEvent", this.myDataTable.onEventSelectRow); 
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

          var myColumnDefs = [
            {key:"VirtualHost", sortable:true, sortOptions:{defaultDir:YAHOO.widget.DataTable.CLASS_DESC},resizeable:false},
            {key:"gliteService1", formatter:YAHOO.widget.DataTable.formatDropdown, dropdownOptions:[{value:'none', text:'none'},{value:'glite-UI', text:'glite-UI'},
                    {value:'glite-BDII_top', text:'glite-BDII_top'},
                    {value:'glite-BDII_site', text:'glite-BDII_site'},
                    {value:'glite-WN', text:'glite-WN'},
                    {value:'glite-WMS', text:'glite-WMS'},
										{value:'lcg-CE', text:'lcg-CE'},
                    {value:'glite-TORQUE_client', text:'TORQUE_client'},
                    {value:'glite-TORQUE_server', text:'TORQUE_server'},
                    {value:'glite-TORQUE_utils', text:'TORQUE_utils'},
 										{value:'glite-MON', text: 'glite-MON'},
										{value:'glite-VOBOX', text: 'glite-VOBOX'},
										{value:'glite-PX', text:'glite-PX'},
										{value:'glite-LB', text: 'glite-LB'},
										{value:'glite-SE_dpm_mysql', text: 'SE_dpm_mysql'},
										{value:'glite-SE_dpm_oracle', text: 'SE_dpm_oracle'},
										{value:'glite-SE_dpm_disk', text: 'SE_dpm_disk'},
										{value:'glite-LFC_mysql', text:'glite-LFC_mysql'},
										{value:'glite-LFC_oracle', text:'glite-LFC_oracle'},
                    ], resizeable:false},
            {key:"gliteService2", formatter:YAHOO.widget.DataTable.formatDropdown,dropdownOptions:[{value:'none', text:'none'},{value:'glite-UI', text:'glite-UI'},
                    {value:'glite-BDII_top', text:'glite-BDII_top'},
                    {value:'glite-BDII_site', text:'glite-BDII_site'},
                    {value:'glite-WN', text:'glite-WN'},
                    {value:'glite-WMS', text:'glite-WMS'},
										{value:'lcg-CE', text:'lcg-CE'},
                    {value:'glite-TORQUE_client', text:'TORQUE_client'},
                    {value:'glite-TORQUE_server', text:'TORQUE_server'},
                    {value:'glite-TORQUE_utils', text:'TORQUE_utils'},
 										{value:'glite-MON', text: 'glite-MON'},
										{value:'glite-VOBOX', text: 'glite-VOBOX'},
										{value:'glite-PX', text:'glite-PX'},
										{value:'glite-LB', text: 'glite-LB'},
										{value:'glite-SE_dpm_mysql', text: 'SE_dpm_mysql'},
										{value:'glite-SE_dpm_oracle', text: 'SE_dpm_oracle'},
										{value:'glite-SE_dpm_disk', text: 'SE_dpm_disk'},
										{value:'glite-LFC_mysql', text:'glite-LFC_mysql'},
										{value:'glite-LFC_oracle', text:'glite-LFC_oracle'},
                    ] ,sortable:true, resizeable:false},
                    {key:"gliteService3", formatter:YAHOO.widget.DataTable.formatDropdown, dropdownOptions:[{value:'none', text:'none'},{value:'glite-UI', text:'glite-UI'},
                    {value:'glite-BDII_top', text:'glite-BDII_top'},
                    {value:'glite-BDII_site', text:'glite-BDII_site'},
                    {value:'glite-WN', text:'glite-WN'},
                    {value:'glite-WMS', text:'glite-WMS'},
										{value:'lcg-CE', text:'lcg-CE'},
                    {value:'glite-TORQUE_client', text:'TORQUE_client'},
                    {value:'glite-TORQUE_server', text:'TORQUE_server'},
                    {value:'glite-TORQUE_utils', text:'TORQUE_utils'},
 										{value:'glite-MON', text: 'glite-MON'},
										{value:'glite-VOBOX', text: 'glite-VOBOX'},
										{value:'glite-PX', text:'glite-PX'},
										{value:'glite-LB', text: 'glite-LB'},
										{value:'glite-SE_dpm_mysql', text: 'SE_dpm_mysql'},
										{value:'glite-SE_dpm_oracle', text: 'SE_dpm_oracle'},
										{value:'glite-SE_dpm_disk', text: 'SE_dpm_disk'},
										{value:'glite-LFC_mysql', text:'glite-LFC_mysql'},
										{value:'glite-LFC_oracle', text:'glite-LFC_oracle'},
                    ],sortable:true, resizeable:false},
                    {key:"gliteService4", formatter:YAHOO.widget.DataTable.formatDropdown, dropdownOptions:[{value:'none', text:'none'},{value:'glite-UI', text:'glite-UI'},
                    {value:'glite-BDII_top', text:'glite-BDII_top'},
                    {value:'glite-BDII_site', text:'glite-BDII_site'},
                    {value:'glite-WN', text:'glite-WN'},
                    {value:'glite-WMS', text:'glite-WMS'},
										{value:'lcg-CE', text:'lcg-CE'},
                    {value:'glite-TORQUE_client', text:'TORQUE_client'},
                    {value:'glite-TORQUE_server', text:'TORQUE_server'},
                    {value:'glite-TORQUE_utils', text:'TORQUE_utils'},
 										{value:'glite-MON', text: 'glite-MON'},
										{value:'glite-VOBOX', text: 'glite-VOBOX'},
										{value:'glite-PX', text:'glite-PX'},
										{value:'glite-LB', text: 'glite-LB'},
										{value:'glite-SE_dpm_mysql', text: 'SE_dpm_mysql'},
										{value:'glite-SE_dpm_oracle', text: 'SE_dpm_oracle'},
										{value:'glite-SE_dpm_disk', text: 'SE_dpm_disk'},
										{value:'glite-LFC_mysql', text:'glite-LFC_mysql'},
										{value:'glite-LFC_oracle', text:'glite-LFC_oracle'},
                    ],sortable:true, resizeable:false},
            {key:"gliteService5", formatter:YAHOO.widget.DataTable.formatDropdown, dropdownOptions:[{value:'none', text:'none'},{value:'glite-UI', text:'glite-UI'},
                    {value:'glite-BDII_top', text:'glite-BDII_top'},
                    {value:'glite-BDII_site', text:'glite-BDII_site'},
                    {value:'glite-WN', text:'glite-WN'},
                    {value:'glite-WMS', text:'glite-WMS'},
										{value:'lcg-CE', text:'lcg-CE'},
                    {value:'glite-TORQUE_client', text:'TORQUE_client'},
                    {value:'glite-TORQUE_server', text:'TORQUE_server'},
                    {value:'glite-TORQUE_utils', text:'TORQUE_utils'},
										{value:'glite-MON', text: 'glite-MON'},
										{value:'glite-VOBOX', text: 'glite-VOBOX'},
										{value:'glite-PX', text:'glite-PX'},
										{value:'glite-LB', text: 'glite-LB'},
										{value:'glite-SE_dpm_mysql', text: 'SE_dpm_mysql'},
										{value:'glite-SE_dpm_oracle', text: 'SE_dpm_oracle'},
										{value:'glite-SE_dpm_disk', text: 'SE_dpm_disk'},
										{value:'glite-LFC_mysql', text:'glite-LFC_mysql'},
										{value:'glite-LFC_oracle', text:'glite-LFC_oracle'},
                    ] ,sortable:true, resizeable:false}
          ];

          this.myDataSource.responseSchema = {
              fields: ["VirtualHost"]
          }
          this.myDataTable3 = new YAHOO.widget.DataTable("yaimgenTable",
                myColumnDefs, this.myDataSource);  
      
      	  this.myDataTable3.subscribe('dropdownChangeEvent', function(oArgs) {
              var elDropdown = oArgs.target;
              var column = this.getColumn(elDropdown);
              var record = this.getRecord(elDropdown);
              var recordIndex = this.getRecordIndex(record);
              setGlite(recordIndex,column.key,elDropdown.options[elDropdown.selectedIndex].value);
          });
          YAHOO.vnode.container.wait.hide();

       }, 
       failure:function(o) {   
        alert('Could not get the data');
        YAHOO.vnode.container.wait.hide();
       },
       timeout: 15000
      };
      YAHOO.util.Connect.asyncRequest('GET', window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?vmAction=getReservedData',this.connectionCallback,null); 
    };
});
