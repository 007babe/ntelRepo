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

    if($.isEmpty(_this) || $.isEmpty(opts)) return false;
    
    _this.jqGrid({
        // Options
        // 참조 http://www.trirand.com/jqgridwiki/doku.php?id=wiki:options 
        ajaxGridOptions   : $.nvl(opts.ajaxGridOptions, new Object()),
        ajaxSelectOptions : $.nvl(opts.ajaxSelectOptions, new Object()),
        altclass          : $.nvl(opts.altclass, ""),
        altRows           : $.nvl(opts.altRows, false),
        autoencode        : $.nvl(opts.autoencode, false),
        autowidth         : $.nvl(opts.autowidth, true),                  // 자동 Width 설정
        caption           : $.nvl(opts.caption, ""),                      // Grid Caption
        cellLayout        : $.nvl(opts.cellLayout, 5),                    // cell 속성 paddingLeft(2) + paddingRight (2) + borderLeft (1) = 5
        cellEdit          : $.nvl(opts.cellEdit, false),                  // 셀 수정가능 여부
        cellsubmit        : $.nvl(opts.cellsubmit, "remote"),
        cellurl           : opts.cellurl,
        cmTemplate        : opts.cmTemplate,
        colModel          : $.nvl(opts.colModel, new Array()),            // 컬럼 모델
        colNames          : $.nvl(opts.colNames, new Array()),            // 컬럼 이름(title)
        data              : $.nvl(opts.data, new Array()),                // data
        datastr           : opts.datastr,                    // data string
        datatype          : $.nvl(opts.datatype, "local"),                // Data 형식("local", "json", "xml")
        deepempty         : $.nvl(opts.deepempty, false),
        deselectAfterSort : $.nvl(opts.deselectAfterSort, true),
        direction         : $.nvl(opts.direction, ""),
        editurl           : opts.editurl,
        emptyrecords      : $.nvl(opts.emptyrecords, "전체 : 0 건"),      // 데이터 0건 표시
        ExpandColClick    : $.nvl(opts.ExpandColClick, true),
        ExpandColumn      : opts.ExpandColumn,
        footerrow         : $.nvl(opts.footerrow, false),
        forceFit          : $.nvl(opts.forceFit, false),
        gridstate         : $.nvl(opts.gridstate, "visible"),
        gridview          : $.nvl(opts.gridview, false),
        grouping          : $.nvl(opts.grouping, false),
        headertitles      : $.nvl(opts.headertitles, false),
        height            : $.nvl(opts.height, "630"),                    // Grid Height
        hiddengrid        : $.nvl(opts.hiddengrid, false),
        hidegrid          : $.nvl(opts.hidegrid, false),                  // Grid 숨기기 기능
        hoverrows         : $.nvl(opts.hoverrows, true),
        idPrefix          : $.nvl(opts.idPrefix, ""),
        ignoreCase        : $.nvl(opts.ignoreCase, false),
        inlineData        : $.nvl(opts.inlineData, {}),
        jsonReader        : $.nvl(opts.jsonReader, new Array()),
        lastpage          : $.nvl(opts.lastpage, 0),
        lastsort          : $.nvl(opts.lastsort, 0),
        loadonce          : $.nvl(opts.loadonce, false),
        loadtext          : $.nvl(opts.loadtext, "데이터 로딩중..."),     // 데이터 로딩중 메시지
        loadui            : $.nvl(opts.loadui, "enable"),
        mtype             : $.nvl(opts.mtype, "GET"),
        multikey          : $.nvl(opts.multikey, ""),
        multiboxonly      : $.nvl(opts.multiboxonly, false),
        multiselect       : $.nvl(opts.multiselect, false),
        multiselectWidth  : $.nvl(opts.multiselectWidth, 30),
        multiSort         : $.nvl(opts.multiSort, false),
        page              : $.nvl(opts.page, 20),
        pager             : $.nvl(opts.pager, ""),
        pagerpos          : $.nvl(opts.pagerpos, "center"),
        pgbuttons         : $.nvl(opts.pgbuttons, true),
        pginput           : $.nvl(opts.pginput, true),
        pgtext            : opts.pgtext,
        prmNames          : opts.prmNames,
        postData          : $.nvl(opts.postData, new Array()),
        reccount          : $.nvl(opts.reccount, 0),
        recordpos         : $.nvl(opts.recordpos, "right"),
        records           : opts.records,
        recordtext        : $.nvl(opts.recordtext, "전체 : {2}건"),       // {0}시작, {1}끝, {2}전체
        resizeclass       : $.nvl(opts.resizeclass, ""),
        rowList           : $.nvl(opts.rowList, [10, 20, 30]),            // 페이지별 노출 건수 단위
        rownumbers        : $.nvl(opts.rownumbers, true),                 // row 번호
        rowNum            : $.nvl(opts.rowNum, 20),
        rowTotal          : opts.rowTotal,
        rownumWidth       : $.nvl(opts.rownumWidth, 25),
        savedRow          : $.nvl(opts.savedRow, new Array()),
        scroll            : $.nvl(opts.scroll, false),
        scrollOffset      : $.nvl(opts.scrollOffset, 18),
        scrollTimeout     : $.nvl(opts.scrollTimeout, 200),
        scrollrows        : $.nvl(opts.scrollrows, false),
        selarrrow         : $.nvl(opts.selarrrow, false),
        selrow            : opts.selrow,
        shrinkToFit       : $.nvl(opts.shrinkToFit, true),               // boolean or integer
        sortable          : $.nvl(opts.sortable, false),
        sortname          : $.nvl(opts.sortname, ""),
        sortorder         : $.nvl(opts.sortorder, "asc"),
        subGrid           : $.nvl(opts.subGrid, false),
        subGridOptions    : $.nvl(opts.subGridOptions, new Object()),
        subGridModel      : $.nvl(opts.subGridModel, new Array()),
        subGridType       : opts.subGridType,
        subGridUrl        : $.nvl(opts.subGridUrl, ""),
        subGridWidth      : $.nvl(opts.subGridWidth, 20),
        toolbar           : $.nvl(opts.toolbar, [false, '']),
        toppager          : $.nvl(opts.toppager, false),
        totaltime         : $.nvl(opts.totaltime, 0),
        treedatatype      : opts.treedatatype,
        treeGrid          : $.nvl(opts.treeGrid, false),
        treeGridModel     : opts.treeGridModel,
        treeIcons         : opts.treeIcons,
        treeReader        : opts.treeReader,
        tree_root_level   : $.nvl(opts.tree_root_level, 0),
        url               : opts.url,
        userData          : $.nvl(opts.userData, new Array()),
        userDataOnFooter  : $.nvl(opts.userDataOnFooter, false),
        viewrecords       : $.nvl(opts.viewrecords, true),
        viewsortcols      : $.nvl(opts.viewsortcols, [false, 'vertical', true]),
//        width             : opts.width,
        xmlReader         : opts.xmlReader, 
        // Events
        // 참조 http://www.trirand.com/jqgridwiki/doku.php?id=wiki:events
        afterInsertRow    : opts.afterInsertRow,
        beforeProcessing  : opts.beforeProcessing,
        beforeRequest     : opts.beforeRequest,
        beforeSelectRow   : opts.beforeSelectRow,
        gridComplete      : opts.gridComplete,
        loadBeforeSend    : opts.loadBeforeSend,
        loadComplete      : opts.loadComplete,
        loadError         : opts.loadError,
        onCellSelect      : opts.onCellSelect, // 확인 필요
        ondblClickRow     : opts.ondblClickRow,
        onHeaderClick     : opts.onHeaderClick,
        onPaging          : opts.onPaging,
        onRightClickRow   : opts.onRightClickRow,
        onSelectAll       : opts.onSelectAll,
        onSelectRow       : opts.onSelectRow,
        onSortCol         : opts.onSortCol,
        rowattr           : opts.rowattr,
        resizeStart       : opts.resizeStart,
        resizeStop        : opts.resizeStop,
        serializeGridData : opts.serializeGridData,       
        // Formatter
        // http://www.trirand.com/jqgridwiki/doku.php?id=wiki:predefined_formatter
        formatter: {
            integer: {
                thousandsSeparator: "",
                defaultValue: '0'
            },
            number: {
                thousandsSeparator: ",",
                decimalSeparator: ".",
                defaultValue: '0'
            },
            currency: {
                thousandsSeparator: ",",
                decimalSeparator: ".",
                defaultValue: '0',
                decimalPlaces: 0
            },
            date: { 
                dayNames: [
                    "일", "월", "화", "수", "목", "금", "토",
                    "일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"
                ],
                AmPm : ["오전", "오후", "오전", "오후"],
                S: function(j) {
                    return "";
                },
                srcformat: "Y-m-d H:i:s",
                newformat: "Y-m-d",
                reformatAfterEdit : false
            },
            baseLinkUrl: '',
            showAction: '',
            target: '',
            checkbox: {
                disabled:true
            },
            idName : 'id'            
        },
        // Etc
        add: true,
        edit: true,
        addtext: '추가',
        edittext: '수정'
    });
};

$.resizeJqGridWidth = function(grid_id, div_id, width){
    $(window).bind('resize', function() {
        $('#' + grid_id).setGridWidth(width, true); //Back to original width
        $('#' + grid_id).setGridWidth($('#' + div_id).width(), true); //Resized to new width as per window
    }).trigger('resize');
}


/*
 * 데이터에서 useYn(boolean)에 따른 사용여부 표기값
 */
$.jqGridUseYn = function(useYn){
	var useYnNm = ""
	if(useYn == true) useYnNm = "사용"
    else if(useYn == false) useYnNm = "미사용"

    return useYnNm;
};

/*
 * 데이터에서 useYn(boolean)에 따른 Attribute
 */
$.jqGridUseYnAttr = function(useYn){

    var attr = "";
	if(useYn == true) attr = "style='color: green; font-weight: bold;'";
    else if(useYn == false) attr = "style='color: darkred; font-weight: bold;'";

    return attr;
};

/*
 * 데이터에서 userAuth에 따른 Attribute
 */
$.jqGridUserAuthAttr = function(userAuth){
    var attr = "";
	switch(userAuth) {
	    case "S0001M": // 시스템관리자
	        attr = "style='background-color: #FFFEE7; font-weight: bold; color: green;'"
	        break;
	    case "S0001C": // 대표    
	        attr = "style='background-color: #FFFEE7; font-weight: bold; color: darkred;'"
	        break;
	    default:
	        break;
	}
    return attr;
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
 * 일반 하이라이트 컬럼 속성
 */
$.jqGridHighlightColAttr = function(isLink){
    return "style='background-color: #FFFEE7; font-weight: bold;" + (isLink ? "cursor: pointer;": "") + "'";
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

/*
 * Status Cell 속성 
 */
$.jqGridStatusCss = function(statusCss) {
    return rtn = "style='" + statusCss + "'";
};


/*
 * 접속제한 관련 속성
 */
$.jqGridConnLimit = function(connLimit) {
    connLimit = $.n2s(connLimit);
    console.log(connLimit);
    var rtnData = ""
    
    if(connLimit.indexOf("P") > -1) rtnData += "PC차단";
    if(connLimit.indexOf("M") > -1) rtnData += "모바일차단";
    
    return rtnData;    
}; 
 
/*
 *
 */
$.jqGridSwich = function(cellvalue, options, rowObject) { 
    var inputId = "ck" + options.colModel.name + options.rowId;

    var rtnVal = '<div class="setings-item"><div class="switch">'
               + '    <div class="onoffswitch">'
               + '        <input id="' + inputId + '" type="checkbox" class="onoffswitch-checkbox">'
               + '        <label class="onoffswitch-label" for="' + inputId + '">'
               + '            <span class="onoffswitch-inner"></span>'
               + '            <span class="onoffswitch-switch"></span>'
               + '        </label>'
               + '    </div>'
               + '</div></div>'
               ;
    
    return rtnVal
};  