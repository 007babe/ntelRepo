/*
 *
 *   ntel - Utils Javascript
 *   version 1.0
 *
 */

/*
 * 빈값 체크
 */
$.isEmpty = function(value){
    if(value == "" || value == null || value == "null" || value == "undefined" || value == undefined || ( value != null && typeof value == "object" && !Object.keys(value).length)){
        return true
    } else {
        return false
    }
};

/*
 * 빈값을 ""로 변환
 */
$.n2s = function(value){
    return $.isEmpty(value) ? "" : value;
};

/*
 * ovalue가 null이면 ovalue로 변환
 */
$.nvl = function(ovalue, cvalue){
    return $.isEmpty(ovalue) ? cvalue : ovalue;
};

/*
 * 숫자를 통화형식으로 변환
 */
$.num2cur = function(num) {
    num += "";
    var firstDigit = num.substr(0, 1);
    var numberDigit = num.substr(1).replace(/[^0-9]/g, "");
    return (firstDigit + numberDigit).replace(/\B(?=(\d{3})+(?!\d))/g, ",");    
};

/*
 * 통화형식을 숫자로 변환
 */
$.cur2num = function(cur) {
    return cur.replace(/[^0-9\-]/g, "");
};

/*
 *  다음 Tab 객체로 이동
 */
$.moveTabNext = function(id) {
    var _itemNext = $.isEmpty(id) ? null : $("#" + id);

    if(!$.isEmpty(_itemNext)) {
        _itemNext.trigger("focus");
        _itemNext.trigger("select");
    }
};