function navFun(id,fisrt,next){
    $('.firstLi').eq(fisrt).addClass('active');
    $('#'+id).addClass('show');
    $('#'+id).find('.sidebar-item').eq(next).addClass('active');
}