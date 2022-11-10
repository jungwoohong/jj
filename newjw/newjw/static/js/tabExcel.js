popupListMemory = Array();

function styleJsonAdd(thisObj,jsonObj){

  $.each(jsonObj,function(idx,item){
            
    thisObj.setCellMetaObject(item.row, item.col, item);

  });
}
function hotReadOnlyFun(){
  hot.updateSettings({
    readOnly: true, 
    contextMenu: false, 
    disableVisualSelection: true, 
    manualColumnResize: false, 
    manualRowResize: false, 
    comments: false 
  });

  for (var key in hotObj) {
    hotObj[key].updateSettings({
      readOnly: true, 
      contextMenu: false, 
      disableVisualSelection: true, 
      manualColumnResize: false, 
      manualRowResize: false, 
      comments: false 
    });
  }
}

function hotWrite(){
  hot.updateSettings({
    readOnly: false, 
    contextMenu: true, 
    disableVisualSelection: false, 
    manualColumnResize: true, 
    manualRowResize: true, 
    comments: true 
  });
  update_setting(hot);

  for (var key in hotObj) {
    hotObj[key].updateSettings({
      readOnly: false, 
      contextMenu: true, 
      disableVisualSelection: false, 
      manualColumnResize: true, 
      manualRowResize: true, 
      comments: true 
    });
    update_setting(hotObj[key]);
  }
} 

function tabOpen(obj,objTitle,type,excelJson,loadId,styleJson){

    $.each(obj,function(idx,item) {
      if ($('#tab-'+item).length >=1) return;

      if(type != 'ajax') { 
        let tabTitleHtml = '<li class="nav-item"><a class="nav-link" href="#tab-'+item+'" data-bs-toggle="tab" role="tab" data-id="'+item+'" data-loadid="'+loadId+'"><span>'+objTitle[idx]+'</span></a></li>';
        let tabContentHtml = '<div class="tab-pane" id="tab-'+item+'" role="tabpanel">';
        tabContentHtml +='<div id="excelGrid'+item+'" class="excelGridClass"> </div>';
        tabContentHtml +='</div>';

        $('.nav-tabs').append(tabTitleHtml);
        $('.tab-content').append(tabContentHtml);

        const containerNum = document.querySelector('#excelGrid'+item);
        showExcelTableObj(containerNum,item);
      }
      
      if(type == 'ajax') {
        // 이미 추가된 탭은 제외
        if($.inArray(item,popupListMemory) ==-1) {
            popupListMemory.push(item);
        } else {
            return;
        }
        
        setTimeout(function(){
          $.ajax({        
            type : 'POST',
            url : "/document/docJsonData/",        
            dataType : 'json',        
            data : {id:item},
            success : function(data) {

                $.each(data.data,function(idx,item){
                    let title     = [item.fields.title];
                    let loadId    = 'add';
                    let excelJson = item.fields.json_data.replace(/None/gi, "null");
                    let styleJson = item.fields.style_data;
          
                    excelJson     = JSON.parse(excelJson.replace(/'/gi, "\""));
                    if(excelJson.length <= 1 ) excelJson = excelJson[0];
                    styleJson     = JSON.parse(styleJson.replace(/'/gi, "\"")); 

                      let len = $('.nav-tabs li').length;
                      let name = 'New'+len;
                      let obj = [name];
                      tabOpen(obj,title,'local',excelJson,loadId,styleJson);

                });               
            }
          });
      }, 1000)
      } else if (type == 'local'){
        hotObj[item].loadData(excelJson);
        styleJsonAdd(hotObj[item],styleJson);
      }
   });
  }

  function loadExcelData(id, dataUrl){
    $.ajax({        
      type : 'POST',
      url : dataUrl,        
      dataType : 'json',        
      data : {id:id},
      success : function(data) {
        $.each(data.data,function(idx,item){
          
          let title     = [item.fields.title];
          let loadId    = [item.pk];
          let excelJson = item.fields.json_data.replace(/None/gi, "null");
          let styleJson = item.fields.style_data;
          
          excelJson     = JSON.parse(excelJson.replace(/'/gi, "\""));
          if (styleJson != '' && styleJson != null) styleJson = JSON.parse(styleJson.replace(/'/gi, "\""));
          
          if(excelJson.length <= 1 ) excelJson = excelJson[0];

          if( idx == 0 ) {
            $('.nav-item > .active > span').text(title);
            hot.loadData(excelJson);
            styleJsonAdd(hot,styleJson);
            hot.render();

          } else {
            let len = $('.nav-tabs li').length;
            let name = 'New'+len;
            let obj = [name];
            tabOpen(obj,title,'local',excelJson,loadId,styleJson);

          }
          
          if (typeof(hotReadOnly)!='undefined') {
            if (hotReadOnly) {
              hotReadOnlyFun()
            }
          }
        })
      }
    }); 
  }

  function tabOpenCallingTempl(obj,objTitle,loadId){

    $.each(obj,function(idx,item) {
      if ($('#tab-'+item).length >=1) return;

        let tabTitleHtml = '<li class="nav-item"><a class="nav-link" href="#tab-'+item+'" data-bs-toggle="tab" role="tab" data-id="'+item+'" data-loadid="'+loadId+'"><span>'+objTitle[idx]+'</span></a></li>';
        let tabContentHtml = '<div class="tab-pane" id="tab-'+item+'" role="tabpanel">';
        tabContentHtml +='<div id="excelGrid'+item+'" class="excelGridClass"> </div>';
        tabContentHtml +='</div>';

        $('.nav-tabs').append(tabTitleHtml);
        $('.tab-content').append(tabContentHtml);

        const containerNum = document.querySelector('#excelGrid'+item);
        showExcelTableObj(containerNum,item);

        setTimeout(function(){
          $.ajax({        
            type : 'POST',
            url : "/frame/frameJsonData/",        
            dataType : 'json',        
            data : {id:item},
            success : function(data) {
              let json_data = JSON.parse(data.data[0].fields.json_data.replace(/'/gi, "\""));  
              let style_data = data.data[0].fields.style_data;
              if(style_data !='') style_data = JSON.parse(style_data.replace(/'/gi, "\"")); 
      
              hotObj[item].loadData(json_data);
              styleJsonAdd(hotObj[item],style_data);
            }
          })
        }, 1000)
    })
  }

  function excelDataMake(){

    idxs = 0;
    let arr = new Array();
    

    let sheet = $('#myTab .nav-tabs .nav-item');
    let data  = $('.excelGridClass');
    delete sheet[0];
    sheet.splice(0, 1);

    $.each(sheet,function(idx,item){
      
      let name    = $.trim($(item).text());
      let hotData = "";
      let rs = new Object();

      if(idx == 0 ) {
        if ( $('#excelGrid').length == 0) {
          hotData = hotObj[Object.keys(hotObj)[idx]];
          idxs = 1;
        } else {
          hotData = hot;
        }
        
      } else {
        if(idxs == 1) {
          hotData = hotObj[Object.keys(hotObj)[idx]];
        } else {
          hotData = hotObj[Object.keys(hotObj)[idx-1]];
        }
        
      }

      rs[name] = hotData.getData();
      rs['style'] = hotData.getCellsMeta();

      arr.push(rs);
    });

    return JSON.stringify(arr);

  }
 