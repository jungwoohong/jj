function navFun(id,fisrt,next){
    $('.firstLi').eq(fisrt).addClass('active');
    $('#'+id).addClass('show');
    $('#'+id).find('.sidebar-item').eq(next).addClass('active');
}

var filesVal ="";
var uploadFiles = [];

function DropFile(dropAreaId, fileListId) {
    let dropArea = document.getElementById(dropAreaId);
    let fileList = document.getElementById(fileListId);
  
    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }
  
    function highlight(e) {
      preventDefaults(e);
      dropArea.classList.add("highlight");
    }
  
    function unhighlight(e) {
      preventDefaults(e);
      dropArea.classList.remove("highlight");
    }
  
    function handleDrop(e) {
        
      unhighlight(e);
      let dt = e.dataTransfer;
      let files = dt.files;
  
      handleFiles(files);
  
      const fileList = document.getElementById(fileListId);
      if (fileList) {
        fileList.scrollTo({ top: fileList.scrollHeight });
      }
    }
  
    function handleFiles(files) {
      if (files.length != 1) {
        alert("하나 이상은 안됩니다.");
        return;
      }  
      var reg = /(.csv|.xls|.xlsx)$/;
      if (!files[0].name.match(reg)) {
        alert("확장자는 엑셀 확장자만 가능합니다.");
        return;
      }

      uploadFiles.push(files);
      if(uploadFiles.length >=2) {
        alert("하나 이상은 안됩니다.");
        return;
      }
      filesVal = files;      
      files = [...files];            
      files.forEach(previewFile);

      
    }
  
    function previewFile(file) {
      
      fileList.appendChild(renderFile(file));
    }
  
    function renderFile(file) {
      let fileDOM = document.createElement("div");
      fileDOM.className = "file fileDiv";
      fileDOM.innerHTML = `
        <div class="thumbnail">
          <img src="/static/img/fileImg.jpg" alt="파일타입 이미지" class="image">
        </div>
        <div class="details">
          <header class="header">
            <span class="name">${file.name}</span>
            <span class="size">${file.size}</span>
          </header>
          <div class="progress">
            <div class="bar"></div>
          </div>
          <div class="status">
            <span class="percent">100% done</span>
            <span class="speed">90KB/sec</span>
          </div>
        </div>
      `;
      return fileDOM;
    }
  
    dropArea.addEventListener("dragenter", highlight, false);
    dropArea.addEventListener("dragover", highlight, false);
    dropArea.addEventListener("dragleave", unhighlight, false);
    dropArea.addEventListener("drop", handleDrop, false);
  
    return {
      handleFiles
    };
  }



  function formError(obj){
    
    $(document).removeClass('invalid');
    $('label[id$="-error"]').hide();

    Object.entries(obj).forEach(entry => {
      const [key, value] = entry;
      $('#'+key).addClass('is-invalid');
      $('#'+key+'-error').html(value);
      $('#'+key+'-error').show();
      $('#'+key).focus();
    });
  }
  function setDate(input,input2){

    let startDate = $('#'+input);
    let endDate = $('#'+input2);
  
    if(startDate.val()=='') {
      startDate.val(start.format("YYYY.MM.DD"));
    } else {
      start = moment(new Date(startDate.val()));
    }
    if(endDate.val()=='') {
      endDate.val(end.format("YYYY.MM.DD"));
    } else {
      end = moment(new Date(endDate.val()));
    }    
  }

var daterangepickerLocalKr = {
  "format": "YYYY-MM-DD",
  "separator": " ~ ",
  "applyLabel": "확인",
  "cancelLabel": "취소",
  "fromLabel": "From",
  "toLabel": "To",
  "customRangeLabel": "Custom",
  "weekLabel": "W",
  "daysOfWeek": ["월", "화", "수", "목", "금", "토", "일"],
  "monthNames": ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
  "firstDay": 1
};

function ioAction(){

  let typeCheck = updateCheck;
  switch(typeCheck) {
    case 1:  // 수정모드
      hotReadOnly = false;
      daterangepickerHide = false;
      hotWrite();
      daterangepickerShow('dateShow');

      $('.card-title').html('문서 수정');
      $('.io-inputAttr').attr('disabled',false);
      $('.io-input').removeClass('disabled');
      $('.io-inputHide, .displayHide').show();  
      $('.io-inputShow ').hide();
         
    break;
  
    case 2:  // 읽기모드
    console.log('asdfasdfasdf')
      hotReadOnly = true;
      daterangepickerHide = true;

      $('.io-inputAttr').attr('disabled',true);
      $('.io-input').addClass('disabled'); 
      $('.io-inputShow ').show();
      $('.io-inputHide ').hide();
    break;
  
    default:
      
      break;
  }
}