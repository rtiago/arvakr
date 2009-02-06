
function refreshHostnames() {
  comboHostnames.store.load();
}

function refreshPhysicalHosts() {
  comboPhysicalHost.store.load();
}

Ext.onReady(function(){
    Ext.QuickTips.init();


    // simple array store
    var storeHostnames = new Ext.data.Store({
          proxy: new Ext.data.HttpProxy({
              url: window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?vmAction=availableHostnames'
          }),
          reader: new Ext.data.JsonReader({
              root: 'myData',
              fields:  [{name: 'Hostnames'}]
          }),
          autoLoad: true,
          listeners: {
            'load' : function() {
              if (storeHostnames.getTotalCount() != 0) {
                comboHostnames.setValue(storeHostnames.getAt(0).get('Hostnames'));
              }
              else {
                comboHostnames.setValue("Select...");
              }
            }
          }
    });
    comboHostnames = new Ext.form.ComboBox({
        store: storeHostnames,
        displayField: 'Hostnames',
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'virtualHost',
        listeners: {
          'beforequery' : function() {
            this.store.load();
            this.store.sort('Hostnames','DESC');
          }
        }
    });

    var storePhysical = new Ext.data.Store({
          proxy: new Ext.data.HttpProxy({
              url: window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?vmAction=availablePhy'
          }),
          reader: new Ext.data.JsonReader({
              root: 'myData',
              fields:  [{name: 'Physical'}]
          }),
          autoLoad: true,
          listeners: {
            'load' : function() {
              if (storePhysical.getTotalCount() != 0) {
                comboPhysicalHost.setValue(storePhysical.getAt(0).get('Physical'));
              }
              else {
                comboPhysicalHost.setValue("Select...");
              }
            }
          }
    });
    comboPhysicalHost = new Ext.form.ComboBox({
        store: storePhysical,
        displayField:'Physical',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'phyHost',
        listeners: {
          'beforequery' : function() {
            this.store.load();
          }
        }
    });

    var storeMemory = new Ext.data.SimpleStore({
        fields: ['abbr', 'memory'],
        data : Ext.vnodedata.memory
    });
    var comboMemory = new Ext.form.ComboBox({
        store: storeMemory,
        displayField:'memory',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        value: '256',
        selectOnFocus:true,
        applyTo: 'memory',
        width: 120
    });

    var storeExpiryTime = new Ext.data.SimpleStore({
        fields: ['abbr', 'expiryTime'],
        data : Ext.vnodedata.expiryTime
    });
    var comboExpiryTime = new Ext.form.ComboBox({
        store: storeExpiryTime,
        displayField:'expiryTime',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        value: '0',
        selectOnFocus:true,
        applyTo: 'expiryTime',
        width: 120
    });

    var storePartition = new Ext.data.SimpleStore({
        fields: ['abbr', 'partition'],
        data : Ext.vnodedata.partition
    });
    var comboPartition = new Ext.form.ComboBox({
        store: storePartition,
        displayField:'partition',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        value: '5',
        applyTo: 'partition',
        width: 100
    });

    var storeImage = new Ext.data.SimpleStore({
        fields: ['abbr', 'osimage'],
        data : Ext.vnodedata.osimage
    });
    var comboImage = new Ext.form.ComboBox({
        store: storeImage,
        displayField:'osimage',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        value: 'SLC-4-32',
        applyTo: 'osImage',
        width: 120
    });

    var storeStateVM = new Ext.data.SimpleStore({
        fields: ['abbr', 'state'],
        data : Ext.vnodedata.statesvms
    });
    var comboStateVM = new Ext.form.ComboBox({
        store: storeStateVM,
        displayField:'state',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'allStates',
        width: 120,
        listeners: {
          'select' : function() {
            getState(this.getValue());
          }
        }
    });

    var servicesVM = new Ext.data.SimpleStore({
        fields: ['abbr', 'service'],
        data : Ext.vnodedata.servicevm
    });
    var comboServicesVM = new Ext.form.ComboBox({
        store: servicesVM,
        displayField:'service',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'services',
        width: 120,
        listeners: {
          'select' : function() {
            getState(this.getValue());
          }
        }
    });

    var storeStateAdmin = new Ext.data.SimpleStore({
        fields: ['abbr', 'state'],
        data : Ext.vnodedata.stateadmin
    });
    var comboStateAdmin = new Ext.form.ComboBox({
        store: storeStateAdmin,
        displayField:'state',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'allAdmin',
        width: 120,
        listeners: {
          'select' : function() {
            getState(this.getValue());
          }
        }
    });

    var storeRepo = new Ext.data.SimpleStore({
        fields: ['abbr', 'repository'],
        data : Ext.vnodedata.repovm
    });
    var comboRepo = new Ext.form.ComboBox({
        store: storeRepo,
        displayField:'repository',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'vmR',
        width: 120
    });

    var storeNumbVM = new Ext.data.SimpleStore({
        fields: ['abbr', 'numb'],
        data : Ext.vnodedata.numbvm
    });
    var comboNumbVM = new Ext.form.ComboBox({
        store: storeNumbVM,
        displayField:'numb',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'vmNumb',
        width: 120
    });

    var storeStateVG = new Ext.data.SimpleStore({
        fields: ['abbr', 'state'],
        data : Ext.vnodedata.statesvgs
    });
    var comboStateVG = new Ext.form.ComboBox({
        store: storeStateVG,
        displayField:'state',
        typeAhead: true,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'allStatesVG',
        width: 120,
        listeners: {
          'select' : function() {
            getVGState(this.getValue());
          }
        }
    });


    var storeSiteNames = new Ext.data.Store({
          proxy: new Ext.data.HttpProxy({
              url: window.location.protocol+'//'+window.location.hostname+'/cgi/server/cgi-bin/main.py?vmAction=userSiteNames'
          }),
          reader: new Ext.data.JsonReader({
              root: 'myData',
              fields:  [{name: 'site'}]
          })
    });
    var comboSiteNames = new Ext.form.ComboBox({
        store: storeSiteNames,
        displayField:'site',
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'vmS',
        listeners: {
          'beforequery' : function() {
            this.store.load();
          }
        }
    });

    var comboSiteNames = new Ext.form.ComboBox({
        store: storeSiteNames,
        displayField:'site',
        mode: 'local',
        editable: false,
        triggerAction: 'all',
        emptyText:'Select...',
        selectOnFocus:true,
        applyTo: 'vmS2',
        listeners: {
          'beforequery' : function() {
            this.store.load();
          },
          'select' : function() {
            getVGSite(this.getValue());
          }
        }
    });
});

