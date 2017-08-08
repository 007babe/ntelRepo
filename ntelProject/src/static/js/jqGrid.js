/*
 *
 *   ntel - Utils Javascript
 *   version 1.0
 *
 */


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
 * 금액일 경우 -/+에 따른 속성
 */
$.jqGridHighlightColAttr = function(){
    return "style='background-color: #FFFEE7; font-weight: bold;'";
}
