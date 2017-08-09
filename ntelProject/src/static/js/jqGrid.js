/*
 *
 *   ntel - Utils Javascript
 *   version 1.0
 *
 */
/*
 * jqGrid 공통화 및 Customized
 */
$.fn.jqGridInit = function(opts) {
    var _this = this; 

};

/*
 * jqGrid용 Class
 */
var jqGridCls ={
    /*
     * Class Member
     */
    $target: null,             // jqGrid Target Object
    $pager: null,
    $data: null,
    $url: null,
    $datatype: "local",
    $autowidth: true,
    $shrinkToFit: false,
    $rowNum: 20,
    $rowList: [10, 20, 30], 
    $colNames: null,
    $colModel: null,
    $formatter: {
         currency : {
            thousandsSeparator: ",",
            defaultValue: '0',
            decimalPlaces: 0
         }
    },
    $multiselect: false,
    $multiselectWidth: 30,
    $viewrecords: true,
    $caption: null,
    $add: true,
    $edit: true,
    $addtext: null,
    $edittext: null,
    $hidegrid: false, 
    $ondblClickRow: null,
    $onSelectRow: null,
    $loadComplete: null,
    $emptyrecords: "전체 : 0 건",
    $recordtext: "전체 : {2}건",
//        url: "{% url 'sysman:use__app_req__list__json' %}",
//        mtype: "post",
//        data: {},
//        datatype: "json",
        height: "600",
        autowidth: true,
        shrinkToFit: false,
        rowNum: 20,
        rowList: [10, 20, 30],    
    // 초기화 
    init: function(opt) {
        
        
        
    }    
   
};



/*
 * 데이터에서 useYn(boolean)에 따른 사용여부 표기값 
 */
$.jqGridUseYn = function(useYn){
	useYnNm = ""
	if(useYn == true) useYnNm = "사용"
    else if(useYn == false) useYnNm = "미사용"
    return useYnNm;
};


/*
 * 금액일 경우 -/+에 따른 속성
 */
$.jqGridMoneyAttr = function(moneyVal){
    try{
        return Number(moneyVal.replace(",", "")) < 0 ? "style='color: darkred;'" : "";
    } catch(e) {
        return "";   
    }
}


/*
 * 하이라이트 컬럼 속성
 */
$.jqGridHighlightColAttr = function(){
    return "style='background-color: #FFFEE7; font-weight: bold;'";
}


/*
 * 전화번호 세팅
 */
$.jqGridTelNo = function(telNo1, telNo2, telNo3) {
    
    var telNo = $.n2s(telNo1);
    
    if(!$.isEmpty(telNo2)) telNo = telNo + "-" + telNo2;
    if(!$.isEmpty(telNo3)) telNo = telNo + "-" + telNo3;
    
    return telNo;
    
};


$.jqGridStatus = function(code) {
    
    var status = "";
    
    switch(code) {
        case "00": 
            status = "승인요청";
            break;
        case "90": 
            status = "승인요청";
            break;
        default:
            break;            
    }
    
    return status;
};
