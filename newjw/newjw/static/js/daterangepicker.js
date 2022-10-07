function cb(start, end) {
    let dtStart = start.format("YYYY.MM.DD");
    let dtEnd   = end.format("YYYY.MM.DD");

    $(".dateShow span").html(dtStart + " - " + dtEnd);
    $('#start_date').val(dtStart);
    $('#end_date').val(dtEnd);
  }


$(document).ready(function(){
    if($(".dateShow").length > 0){
        $(".dateShow").daterangepicker({
            startDate: start,
            endDate: end,
            "locale": daterangepickerLocalKr,
            ranges: {
              "14일간": [moment(),moment().subtract(-14, "days")],
              "30일간": [moment(),moment().subtract(-29, "days")],
              "60일간": [moment(),moment().subtract(-59, "days")],
            }
          }, cb);
          cb(start, end); 
    }
});