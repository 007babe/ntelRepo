/*
 *
 *   ntel - Common Javascript
 *   version 1.0
 *
 */

var console = window.console || {log:function(){}};

$(document).ready(function() {
    // AjaxSetup
    $.gfAjaxSetup();

    // 가능한 추가 하지 마시요
    // ajax 실행시 로딩중 Spinner 표시
    $(document).ajaxStart(function() {
    }).ajaxSend(function( event, jqxhr, settings ) {
//        $.gfToggleLoading($("#boxContents"), true);
//        $.gfToggleLoading($(document.body), true);
    }).ajaxComplete(function( event, xhr, settings ) {
//        $.gfToggleLoading($("#boxContents"), false);
//        $.gfToggleLoading($(document.body), false);
    });

});

/*
 * 시스템 전역 데이터 전체 세팅 (gv.js > gSysGDs 등록 정보 참조)
 */
$.gfSetGlobalDataAll = function() {

    $.each(gSysGDs, function(i, item) {
        var key    = item.key;
        var url    = item.url;
        var cbFunc = item.cbFunc
        var useYn  = item.useYn;
        var desc   = item.desc;

        // Key와 동일한 전역 데이터용 Global 변수 생성
        $.globalEval("var " + key + " = new Object();");

        // 시스템 사용 전역 데이터 가져오기
        $.gfGetGlobalData({
           key : key,
           url : url,
           cbFunc : cbFunc
        });
    });
};

/*
 * 시스템 전역 데이터 해당 Key 세팅 (gv.js > gSysGDs 등록 정보 참조)
 */
$.gfSetGlobalData = function(key) {

    if($.isEmpty(key)) return; // key가 없을 경우 return

    // 그룹코드(grpCd) 값에 의한 Filtering
    var gSysGDsF = $.grep(gSysGDs, function(el, inx){
        return el.key == key;
    });

    // Filtering 결과가 1개 일 경우만 처리(여러개 일경우는 처리 안함 -> key 확인 필요)
    if(gSysGDsF.length == 1) {
        // 시스템 사용 전역 데이터 가져오기
        $.gfGetGlobalData({
           key : gSysGDsF.key,
           url : gSysGDsF.url,
           cbFunc : gSysGDsF.cbFunc
        });
    }
}

/*
 * 시스템 사용 전역 데이터 가져오기(Ajax json)
 */
$.gfGetGlobalData = function(opts) {

    if($.isEmpty(opts) || $.isEmpty(opts.key) || $.isEmpty(opts.url)) return; // option이 없을 경우 return

    // 옵션
    var key = opts.key; // 데이터 Key(필수)
    var url = opts.url; // 데이터 URL(필수)
    var cbFunc = opts.cbFunc // 정상 처리후 호출 콜백 함수명

    $.gfAjax({
        url: url,
        dataType: "json",
//        contentType: "application/json; charset=utf-8",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        beforeSendFunc: function(data, textStatus, jqXHR) {
            $("#btnRegData").prop('disabled', true);
        },
        doneFunc: function(data, textStatus, jqXHR) {
            try {
                eval(key + " = $.parseJSON(JSON.stringify(data.resultData));");
                if(!$.isEmpty(cbFunc)) {
                    eval(cbFunc)
                }
            } catch(err) {
                console.log("gfGetGlobalData Error!!! : Key[" + key + "], Url[" + url + "]");
                console.log(err);
            }
        },
        failFunc: function(jqXHR, textStatus, errorThrown) {
        },
        alwaysFunc: function(jqXHR, textStatus, errorThrown) {
            $("#btnRegData").prop('disabled', false);
        },
    });
};

/*
 * 현재일자, 시간 정보 관련 함수
 */
$.gfSetCurrentDateTime = function() {
    gCurrentDateTime = new Date();

    // 서버시간으로 세팅하는 로직 추가 필요
//    console.log("Setted to gCurrentDateTime [" + gCurrentDateTime + "]");
};

/*
 * 메뉴 관련  이벤트 초기화  함수
 */
$.gfInitEventMenu = function() {
    // 메뉴 클릭시 이벤트 세팅
    $("a[type='menu']").on("click", $.gfHandlerClickMenu);
};

/*
 * 메뉴 클릭 이벤트 Handler 함수
 */
$.gfHandlerClickMenu = function(opts) {
    var _this = $(this)

    $("li[type='menu']").removeClass("active"); // 메뉴그룹 전체 Acitve 해제
    _this.closest("li").addClass("active"); // 현재 클릭한 메뉴가 속한 메뉴그룹 Active 세팅

    // 메뉴에 해당하는 메인 Contents 호출
    $.gfLoadContentsData({
        params: _this.attr("params"),
        menuId: _this.attr("menuId")
    });

    // 쿠키에 현재 메뉴 세팅
    $.cookie("menuInfo", _this.attr("menuInfo"));
}

/*
 * 우측 Main Contens Reloading용
 */
$.gfReloadContentsData = function(opts) {

    // opts가 없을 경우 현재 선택된 메뉴의 페이지로 세팅
    if($.isEmpty(opts)){
        _menu = $("li[type='menu'].active > a");

        opts = {
            menuId: _menu.attr("menuId"),
            params: _menu.attr("params")
        }
    }

    $.gfLoadContentsData(opts);
};

/*
 * 우측 Main Contens Loading용
 */
$.gfLoadContentsData = function(opts) {
    // 옵션이 없을 경우
    if($.isEmpty(opts)) return false;

    var _maincontents = $("#mainContents");
    var menuId = opts.menuId;
    var params = $.isEmpty(opts.params) ? {} : opts.params;

    params.menuId = menuId;

    $.gfAjax({
        type: "POST",
        url: "/main/menu/",
        data: params,
        async: true,
        successFunc: function(data, textStatus, jqXHR) {
            _maincontents.empty().append(data);
        },
        failFunc: function(jqXHR, textStatus, errorThrown) {
            // Http Error처리
            $.gfHttpErrorPopup({
                jqXHR : jqXHR,
                textStatus : textStatus,
                errorThrown : errorThrown,
                loginRequired : true,
                loginCompletedFunc: function() {
                    // 로그인 후 처리 이벤트
                }
            });
        },
        spinTarget: $("#boxContents"),
    });
};


/*
 * 최초 선택 화면 처리(쿠키 이용)
 */
$.gfLoadInitPage = function () {

    // 메뉴정보가 없을 경우
    if(!$.gfIsValidMenu()) {

        // 메뉴리스트 중에서 제일 첫번째 세팅
        var upMenuId = GD_SYS_MENU[0].upMenuId;
        var menuId   = GD_SYS_MENU[0].menuId;

        $.cookie("menuInfo", upMenuId + "," + menuId);
    }

    var menuInfo = $.cookie("menuInfo").split(',');

    var upMenuId = menuInfo[0];
    var menuId = menuInfo[1];

    // 초기 메뉴 선택 세팅(click event)
    $('#upmenu_' + upMenuId).trigger('click');
    $('#menu_' + menuId).trigger('click');
};

/*
 * 쿠키에 메뉴정보가 있는지 메뉴정보가 존재하는지 확인
 */
$.gfIsValidMenu = function() {
    var isValidMenu = false;

    // 쿠키에 메뉴정보가 없을 경우
    if($.isEmpty($.cookie("menuInfo"))) return false;

    // 메뉴가 공통메뉴 데이터에 있을 경우
    var menuId = $.cookie("menuInfo").split(',')[1];
    $.each(GD_SYS_MENU, function(index, value) {
        if(menuId == value.menuId) {
            isValidMenu = true;
            return;
        }
    });
    return isValidMenu;
};


/*
 * 공통Popup용
 * 주의 사항
 * 1. attrs의 key로 사용불가 사항
 *    id, data-backdrop, tabindex, role, aria-hidden
 */
$.gfCommonPopUp = function(opts) {
    if($.isEmpty(opts)) return;

    var popUrl = opts.popUrl; // 필수
    var modalId = $.isEmpty(opts.modalId) ? "divCommonModalPopup" : opts.modalId;
    var _divModal = $(modalId);
    var width = opts.width;
    var attrs = $.isEmpty(opts.attrs) ? new Object() : opts.attrs; // modalId의 Popup Div의 속성에 추가 할 내용(key, value)
    var params = opts.params;
    var loginRequired = $.isEmpty(opts.loginRequired) ? true : opts.loginRequired;
    var animate = $.isEmpty(opts.animate) ? "fadeIn" : opts.animate;

    $.gfAjax({
        type: "POST",
        url: popUrl,
        data: params,
        async: true,
        successFunc: function(data, textStatus, jqXHR) {
            var _divPop = $("<div/>").attr("id", modalId)
                                     .attr("data-backdrop", "static")
                                     .attr("tabindex", "-1")
                                     .attr("role", "dialog")
                                     .attr("aria-hidden", "true")
                                     .addClass("modal inmodal")
                                     ;
            // attrs의 값을 div 속성으로 추가
            if($.type(attrs) === "object") {
                $.each(attrs, function(key, value) {
                    _divPop.attr(key, value);
                });
            }

            // divPop에 html 추가
            _divPop.empty().append(data)

            var _modalDialog = _divPop.children(".modal-dialog");

            // div 너비 지정
            if(!$.isEmpty(width)){
                _modalDialog.css("width", width + "px");
            }

            // animate 설정
            if(!$.isEmpty(animate)){
                _modalDialog.children(".modal-content").addClass("animated").addClass(animate);
            }

            // body에 추가
            $(document.body).append(_divPop);

            // 모달 Show 이벤트
            _divPop.on("show.bs.modal", function(e) {
            });

            // 모달 Show 완료 이벤트
            _divPop.on("shown.bs.modal", function(e) {
                // 모달 노출 후 초기화 실행
                if(!$.isEmpty($.fnInitPop)){
                    $.fnInitPop();
                }
            });

            // 모달 Hide 이벤트
            _divPop.on("hide.bs.modal", function(e) {
            });

            // 모달 Hide 완료 이벤트
            _divPop.on("hidden.bs.modal", function(e) {
                _divPop.off("shown.bs.modal");
                _divPop.remove(); // 기존 모달 팝업 지우기
            });


            // 팝업 보이기
            _divPop.modal("show");

        },
        failFunc: function(jqXHR, textStatus, errorThrown) {
            // Http Error처리
            $.gfHttpErrorPopup({
                jqXHR : jqXHR,
                textStatus : textStatus,
                errorThrown : errorThrown,
                loginRequired : loginRequired
            });
        }
    });
};

/*
 * 공통팝업 닫기
 */
$.gfCommonPopUpClose = function(_target) {
    _target = $.isEmpty(_target) ? $('#divCommonModalPopup') : _target;
    _target.modal('hide');
}


/*
 * 에러발생시 모달 창
 */
/*
$.gfErrorPopUp = function(modalId, errCd, errMsg, w, h) {
    $.ajax({
        type: "POST",
        url: "/static/popupError.html",
        success: function(html) {
            $("#modalPopup").empty().append(html);
            $('#modalPopup').modal("show");
        }
    });
};
*/

/*
 * Loading용 Spinner 처리
 */
$.gfToggleLoading = function(_target, flag){
    if(_target.children(".spinWrap").children("#spinWrap").length == 0) {
        var divSpin = "<div id='spinWrap' class='sk-spinner sk-spinner-wave'>"
                    + "    <div class='sk-rect1'></div>"
                    + "    <div class='sk-rect2'></div>"
                    + "    <div class='sk-rect3'></div>"
                    + "    <div class='sk-rect4'></div>"
                    + "    <div class='sk-rect5'></div>"
                    + "</div>";
        _target.children(".spinWrap").prepend(divSpin);
    }

    if(flag) {
        _target.children(".spinWrap").addClass("sk-loading");
    } else {
        _target.children(".spinWrap").removeClass("sk-loading");
    }
};

/*
 * Data debugging용(공통 함수)
 */
$.traceData = function(param) {
    var paramType = $.type(param);
    switch(paramType) {
        case "object" :
            $.each(param, function(key, value) {
                console.log("Key:[" + key + "], value[" + value + "]\n");
            });
            break;
        case "array" :
            $.each(param, function(index, value) {
                console.log("Index:[" + index + "], value[" + value + "]\n");
            });
            break;
        default :
            break;
    }
    console.log("<<traceData type[" + paramType + "]\n");
};


/*
 * 검색 Chosen 초기화
 */
$.gfInitChosen = function(formOnly) {
    var conditionSelector = "select[formType='chosen']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    var _target = $(conditionSelector);

    _target.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetChosen();
    });
};

/*
 * 검색 Chosen Customized
 * https://harvesthq.github.io/chosen/options.html
 */
$.fn.gfSetChosen = function(opts) {
    var _this = this;

    // 검색 Chosen 세팅
    _this.chosen({
        width: "100%",                       // 너비
        no_results_text: "검색결과 없음...", // 검색결과가 없을 경우 Text
        case_sensitive_search: false,        // 대소문자 구분
//        inherit_select_classes: true,
        search_contains: true,               // 검색어 시작지점
        disable_search_threshold: 3,         // 3개 이하의 검색결과가 나오는 경우 검색입력을 숨김
        allow_single_deselect: true
    });

    var select = $.n2s(_this.attr("id"));
    var selectChosen = select + "_chosen";

    var sWidth = $.n2s(_this.attr("sWidth")); // 검색창 너비
    var tabPrev = $.n2s(_this.attr("tabPrev")); // 탭 이동시 이전 form 객체 명
    var dispAttr = $.n2s(_this.attr("dispAttr")); // 보여질 값 속성필드명

    var dataKey = $.n2s(_this.attr("dataKey")); // 세팅대상 데이터(gv.js의 key)
    var optGroup = $.n2s(_this.attr("optGroup")); // 그룹옵션 필드
    var filters = $.n2s(_this.attr("filters")); // 데이터 조건
    var objFilters = {};
    var setValue = $.n2s(_this.attr("setValue")); // 선택되어질 값(option의 value)
    var loadData = $.n2s(_this.attr("loadData")); // 데이터를 로딩할지 여부

    var _selectChosen = $("#" + selectChosen);
    var _tabPrev;
    var _chosenResult = _selectChosen.find("ul.chosen-results");

    // 검색 창 너비 조정
    if(!$.isEmpty(sWidth)) {
        _selectChosen.children("div .chosen-drop").css("width", sWidth + "px");
    }

    // 이전 탭(tabPrev) 설정을 했을 경우
    if(!$.isEmpty(tabPrev)) {
        // tab을 눌렀을 때 이전 객체의 이벤트 처리
        $("#" + tabPrev).on("keydown", function(e, params) {
            var code = e.keyCode || e.which;
            if(code === 9 && !e.shiftKey) {
                _this.trigger("chosen:open");
                e.preventDefault();
            }
        });
    }

    // 검색창 Keydown 이벤트 처리
    _selectChosen.on("keydown", function(e, params) {
        var code = e.keyCode || e.which;

        // Tab Key
        if(code === 9){
            // shift tab
            if(e.shiftKey) {
                if(!$.isEmpty(tabPrev)) {
                    var _selectPrev = $("#" + $("#" + tabPrev).attr("id").replace("_chosen", ""));
                    // 이전 탭의 선택자가 Chosen 일경우
                    if(_selectPrev.hasClass("chosen-select")) {
                        _selectPrev.trigger("chosen:open");
                        e.preventDefault();
                    }
                }
            }

            var _optSelected = $("option:selected", _this);
            var dispValue = _optSelected.is("[dvalue]") ? _optSelected.attr("dvalue") : _optSelected.text();
            if(!$.isEmpty(_this.val())) {
                _selectChosen.children("a.chosen-single").children("span").first().text(dispValue);
            }
        }
    });

    // 검색창 Mouseup 이벤트 처리
    _selectChosen.on("mouseup", function(e, params) {
        var _optSelected = $("option:selected", _this);
        var dispValue = _optSelected.is("[dvalue]") ? _optSelected.attr("dvalue") : _optSelected.text();
        if(!$.isEmpty(_this.val())) {
            _selectChosen.children("a.chosen-single").children("span").first().text(dispValue);
        }
    });

    // 검색창 Keyup 이벤트 처리
    _selectChosen.on("keyup", function(e, params) {
        var code = e.keyCode || e.which;
        // Enter Key
        if(code === 13) {
            var _optSelected = $("option:selected", _this);
            var dispValue = _optSelected.is("[dvalue]") ? _optSelected.attr("dvalue") : _optSelected.text();
            if(!$.isEmpty(_this.val())) {
                _selectChosen.children("a.chosen-single").children("span").first().text(dispValue);
            }
        }
    });

    // 값이 바뀌었을 때 처리
    _this.on("change", function(e, parmas) {
        var _this = $(this);
        var _optSelected = $("option:selected", this);
        var dispValue = _optSelected.is("[dvalue]") ? _optSelected.attr("dvalue") : _optSelected.text();

        if(!$.isEmpty(_this.val())) {
            _selectChosen.children("a.chosen-single").children("span").first().text(dispValue);
        }
    });

    // 데이터 세팅(loadData="Y"일 경우)
    if(loadData == "Y") {
        // 입고 단말기(개통가능한) 데이터 세팅하기
        _this.gfSetChosenData({
            dataKey: dataKey,
            optGroup: optGroup,
            filters: objFilters,
            setValue: setValue
        });
    }

};

/*
 * 달력 Picker 세팅 Customized
 * https://github.com/eternicode/bootstrap-datepicker
 * https://bootstrap-datepicker.readthedocs.io/en/stable/index.html
 */
$.fn.gfSetDatePicker = function() {
    var _this = this;

    // 필드별 설정 세팅
    _this.each(function(inx, item) {
        var _item = $(item);

        _item.datepicker({
            format: "yyyy-mm-dd",
            language: "kr",
            todayBtn: "linked",
            keyboardNavigation: false,
            forceParse: false,
            calendarWeeks: true,
            autoclose: true, // default: false
            calendarWeeks: false,
            clearBtn: false, // defualt : false
            daysOfWeekHighlighted: "0,6",
            weekStart: 0,
            currentText: "hahahah",
            enableOnReadonly: false, // default : true
//            datesDisabled: ['2017-04-06', '2017-04-21'],
            onSelect: function() {
//                console.log("onSelect!!!");
            },
            beforeShowMonth: function (date){
            }
        });

        var _objDateFields = _item.children("span").children("input");

        // input 이벤트 : 숫자 & "-"만 입력되도록 제어
        _objDateFields.off("input").on("input", function(e, params) {
            var _this = $(this);
            var _picker = _this.closest(".input-group.date");

            _this.val(_this.val().replace(/[^0-9\-]/g, ""));
        });


        // blur 이벤트 : 날짜가 변경되었을 경우
        _objDateFields.off("blur").on("blur", function(e, params) {
            var _this = $(this);
            var _picker = _this.closest(".input-group.date"); // Datepicker

            _this.val(_this.val().replace(/[^0-9\-]/g, "").replace(/([0-9]{4})([0-9]+)([0-9]{2})/,"$1-$2-$3"));

            // 입력한 날짜가 올바른 날짜인지 확인
            if(!$.gfIsValidedDate(_this.val())) {
                _picker.datepicker("setDate", "");
                _picker.datepicker().trigger("changeDate");

                return false;
            }

            // picker changeDate 발생
            _picker.datepicker().trigger("changeDate");
        });

        // Datepicker 변경 이벤트
        _item.datepicker().on("changeDate", function(e, param) {
            var _picker = $(this);
        });

        // 현재일자 세팅
        _item.datepicker("setDate", $.gfGetNowDateTime(_objDateFields.attr("nowDate")));

        // 사용불가(disabled) 세팅
        _item.gfDisabledDatePicker(!$.isEmpty(_item.attr("disabled")));
    });

};

/*
 * 달력 Picker 초기화(Customiazed)
 */
$.gfInitDatePicker = function(formOnly) {

    var conditionSelector = "div[formType='datePicker']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // 달력 Picker 각각의 selector를 구해온다
    var _datePicker = $(conditionSelector); // date picker
    _datePicker.gfSetDatePicker();
}

/*
 * 체크박스/라디오버튼(icheck) Customized
 *
 */
$.fn.gfSetCheckbox = function() {
    var _this = this;

    _this.iCheck({
        checkboxClass: "icheckbox_square-green",
        radioClass: "iradio_square-green"
    });
};

/*
 * 체크박스/라디오버튼(icheck) 초기화(Customiazed)
 */
$.gfInitCheckbox = function(formOnly) {

    var conditionSelector = "div[formType='iChecks']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // Checkbox selector를 구해온다
    var _checkbox = $(conditionSelector); // i-checks 객체
    _checkbox.gfSetCheckbox();
};

/*
 * Readonly 텍스트 박스 초기화
 */
$.gfInitTextReadonly = function(formOnly) {
    var conditionSelector = "span[formtype='text-r']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    var _target = $(conditionSelector);

    _target.each(function(inx, item) {
        var _item = $(item);
        var placeholder = $.isEmpty(_item.attr("placeholder")) ? "" : _item.attr("placeholder");
        var value = $.isEmpty(_item.attr("value")) ? "" : _item.attr("value");

        if(value == "") {
            _item.text(placeholder);
            _item.removeClass("text-r").addClass("text-r nv");
        }
    });
}

/*
 * Readonly 텍스트 박스 값 세팅
 * opt는 차후 확장용
 */
$.fn.gfSetTextReadonly = function(value, text, opt) {

    var _this = this;
    var placeholder = $.isEmpty(_this.attr("placeholder")) ? "" : _this.attr("placeholder");

    // 빈 값일 경우
    if($.isEmpty(value)) {
        _this.text(placeholder);
        _this.attr("value", $.n2s(value));
        _this.removeClass("text-r").addClass("text-r nv");
    } else {
        _this.text($.isEmpty(text) ? value : text);
        _this.attr("value", value);
        _this.removeClass("nv");
    }
}

/*
 * 날짜 형식 체크
 */
$.gfIsValidedDate = function(dateVal) {
    var validformat = /^\d{4}\-\d{2}\-\d{2}$/; //Basic check for format validity
    var yearfield, monthfield, dayfield, dayobj;

    if($.isEmpty(dateVal)) return true;

    if(!validformat.test(dateVal)) {
        return false;
    } else { //Detailed check for valid date ranges
        yearfield = dateVal.split("-")[0];
        monthfield = dateVal.split("-")[1];
        dayfield = dateVal.split("-")[2];
        dayobj = new Date(yearfield, monthfield - 1, dayfield);
    }

    if((dayobj.getMonth() + 1 != monthfield) || (dayobj.getDate() != dayfield) || (dayobj.getFullYear() != yearfield)) {
        return false;
    } else {
        return true;
    }

    return false;
};

/*
 * 금액필드 세팅
 */
$.fn.gfSetCurrency = function() {
    var _currency = this;

    // Input Event
    _currency.off("input").on("input", function(e, params) {
        var _this = $(this);

        // 숫자, "-" 를 제외한 문자를 제거 하기
        _this.val(_this.val().replace(/[^0-9\-]/g, ""));


        // -를 입력할 경우 처리
        var firstDigit = _this.val().substr(0, 1);
        var numberDigit = _this.val().substr(1).replace(/[^0-9]/g, "");

        // 첫번째 0 없애기
        if(firstDigit == "-") { // 음수(-) 일 경우
            numberDigit = numberDigit.replace(/(^0+)/, "");
        } else { // 음수(-) 가 아닐 경우
            if(firstDigit == "0") {
                firstDigit = "";
                numberDigit = numberDigit.replace(/(^0+)/, "");
            }
        }

        _this.val((firstDigit + numberDigit).replace(/\B(?=(\d{3})+(?!\d))/g, ","));

        // - 일경우 색상처리
        if(/^\-/.test(_this.val())) {
            _this.css("color", "red");
        } else {
            _this.css("color", "inherit");
        }

    });

    // blur Event
    _currency.off("blur").on("blur", function(e, params) {
        var _this = $(this);

        // -만 입력될경우 없애기
        if(_this.val() == "-") _this.val("");

        // 숫자만 입력받게 하기, 콤마, - 넣기
        _this.val(_this.val().replace(/[^0-9\-]/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));

        // - 일경우 색상처리
        if(/^\-/.test(_this.val())) {
            _this.css("color", "red");
        } else {
            _this.css("color", "inherit");
        }
    });
};

/*
 * 금액필드 초기화
 */
$.gfInitCurrency = function(formOnly) {

    var conditionSelector = "input[formType='currency']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // 달력 Picker 각각의 selector를 구해온다
    var _currency = $(conditionSelector); // 금액필드
    _currency.gfSetCurrency();
};

/*
 * 전화번호(지역번호) 필드 세팅
 */
$.fn.gfSetTelNo1 = function() {
    var _item = this;

    // Key Up Event
    _item.on("input", function(e, params) {
        var _this = $(this);

        // 숫자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9]/g, ""));

        if(_this.val().length >= 4 || $.inArray(_this.val(), gArrFirstTelNo) > -1) {
            $.moveTabNext(_item.attr("tabNext"));
        }
    });
};

/*
 * 전화번호(국번) 필드 세팅
 */
$.fn.gfSetTelNo2 = function() {
    var _item = this;

    // Key Up Event
    _item.on("input", function(e, params) {
        var _this = $(this);

        // 숫자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9]/g, ""));

        if(_this.val().length >= 4) {
            $.moveTabNext(_item.attr("tabNext"));
        }
    });
};

/*
 * 전화번호(전번) 필드 세팅
 */
$.fn.gfSetTelNo3 = function() {
    var _item = this;

    // Key Up Event
    _item.on("input", function(e, params) {
        var _this = $(this);

        // 숫자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9]/g, ""));

        if(_this.val().length >= 4) {
            $.moveTabNext(_item.attr("tabNext"));
        }
    });
};

/*
 * 전화번호 필드 초기화
 */
$.gfInitTelNo = function(formOnly) {

    var conditionSelector1 = "input[formType='tel1']";
    var conditionSelector2 = "input[formType='tel2']";
    var conditionSelector3 = "input[formType='tel3']";

    if(!$.isEmpty(formOnly)) {
        conditionSelector1 + "[formOnly='" + formOnly + "']";
        conditionSelector2 + "[formOnly='" + formOnly + "']";
        conditionSelector3 + "[formOnly='" + formOnly + "']";
    }

    // 전화번호 각각의 selector를 구해온다
    var _tel1 = $(conditionSelector1); // 전화 지역번호
    var _tel2 = $(conditionSelector2); // 전화 국번호
    var _tel3 = $(conditionSelector3); // 전화 전화번호

    _tel1.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetTelNo1();
    });

    _tel2.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetTelNo2();
    });

    _tel3.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetTelNo3();
    });
};

/*
 * 사업자번호(1) 필드 세팅
 */
$.fn.gfSetBizLicNo1 = function() {
    var _item = this;

    // Key Up Event
    _item.on("keyup", function(e, params) {
        var _this = $(this);

        // 숫자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9]/g, ""));

        if(_this.val().length >= 3) {
            $.moveTabNext(_item.attr("tabNext"));
        }
    });
};

/*
 * 사업자번호(2) 필드 세팅
 */
$.fn.gfSetBizLicNo2 = function() {
    var _item = this;

    // Key Up Event
    _item.on("keyup", function(e, params) {
        var _this = $(this);

        // 숫자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9]/g, ""));

        if(_this.val().length >= 2) {
            $.moveTabNext(_item.attr("tabNext"));
        }
    });
};

/*
 * 사업자번호(3) 필드 세팅
 */
$.fn.gfSetBizLicNo3 = function() {
    var _item = this;

    // Key Up Event
    _item.on("keyup", function(e, params) {
        var _this = $(this);

        // 숫자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9]/g, ""));

        if(_this.val().length >= 5) {
            $.moveTabNext(_item.attr("tabNext"));
        }
    });
};

/*
 * 사업자번호 필드 초기화
 */
$.gfInitBizLicNo = function(formOnly) {

    var conditionSelector1 = "input[formType='bizLic1']";
    var conditionSelector2 = "input[formType='bizLic2']";
    var conditionSelector3 = "input[formType='bizLic3']";

    if(!$.isEmpty(formOnly)) {
        conditionSelector1 + "[formOnly='" + formOnly + "']";
        conditionSelector2 + "[formOnly='" + formOnly + "']";
        conditionSelector3 + "[formOnly='" + formOnly + "']";
    }

    // 사업자번호 각각의 selector를 구해온다
    var _bizLic1 = $(conditionSelector1); // 사업자번호1
    var _bizLic2 = $(conditionSelector2); // 사업자번호2
    var _bizLic3 = $(conditionSelector3); // 사업자번호3

    _bizLic1.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetBizLicNo1();
    });

    _bizLic2.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetBizLicNo2();
    });

    _bizLic3.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetBizLicNo3();
    });
};

/*
 * User ID 필드 세팅
 */
$.fn.gfSetUserId = function() {
    var _item = this;
    var _noti = $("#" + _item.attr("noti")); // 알림필드
    var _idChk = $("#idChk"); // ID Check Value

    // Input Event
    _item.on("input", function(e, params) {
        var _this = $(this);

        // 숫자 영문자만 입력받게 하기
        _this.val(_this.val().replace(/[^0-9a-zA-Z]/g, ""));

        var len = _this.val().length;

        if(len < 6) {
            if(!$.isEmpty(_noti)){
                _noti.html("* 아이디는 6~20자 사이의 영문으로 시작하는 영문/숫자 조합으로 입력해주세요.");
                _noti.css("color", "#f13221");
            }
        }

        if(len >= 6) _this.trigger("change");

        if(_this.val().length >= 20) { // 20자 이상일 경우 처리
            $.moveTabNext(_item.attr("tabNext"));
            _this.trigger("change");
        }
    });

    // Change Event
    _item.on("change", function(e, params) {
        var _this = $(this);

        if(!$.isEmpty(_idChk)) _idChk.val("N"); // 값이 변했을 경우 idChk값은 "N"

        expr = /^[a-zA-Z]+[a-zA-Z0-9]{5,19}$/g

        // 특수문자 포함
        //var aa = '/^.*(?=^.{6,20}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$/';​

        if(!expr.test(_this.val())) {
            if(!$.isEmpty(_noti)){
                _noti.html("* 아이디는 6~20자 사이의 영문으로 시작하는 영문/숫자 조합으로 입력해주세요.");
                _noti.css("color", "#f13221");
            }
        } else {
            if(!$.isEmpty(_noti)){
                _noti.html("");
                _noti.css("color", "#1ab394");
                if(!$.isEmpty(_idChk)) _idChk.val("Y"); // 정상적인 값을 경우 idChk값은 "Y"
            }
        }
    });
};


/*
 * User ID 필드 초기화
 */
$.gfInitUserId = function(formOnly) {

    var conditionSelector = "input[formType='userid']";

    if(!$.isEmpty(formOnly)) {
        conditionSelector + "[formOnly='" + formOnly + "']";
    }

    // 아이디 필드 selector를 구해온다

    var _userId = $(conditionSelector);

    _userId.each(function(inx, item) {
        var _item = $(item);
        _item.gfSetUserId();
    });
};



/*
 * 공통코드 Select Box 초기화
 */
$.gfInitComCd2ComboBox = function(formOnly) {

    var conditionSelector = "select[formType='comSel']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // Select Box로 세팅될 값들을 찾아온다(formType="comSel")
    var _comSel = $(conditionSelector); // 공통코드 Select 박스 대상들

    _comSel.each(function(inx, item) {
        var _item = $(item);
        // options
        var grpCd = _item.attr("grpCd");
        var isSetNF = _item.attr("isSetNF") == "true" ? true : false;
        var textNF = $.isEmpty(_item.attr("textNF")) ? "" : _item.attr("textNF");
        var useYn = _item.attr("useYn") == "true" ? true : false;
        var setValue = $.isEmpty(_item.attr("setValue")) ? "" : _item.attr("setValue");
        var isDisabled = _item.attr("isDisabled") == "true" ? true : false;
        var grpOpt = $.isEmpty(_item.attr("grpOpt")) ? "" : _item.attr("grpOpt");
        var dnOrdSeq = $.isEmpty(_item.attr("dnOrdSeq")) ? "" : _item.attr("dnOrdSeq");
        var dneOrdSeq = $.isEmpty(_item.attr("dneOrdSeq")) ? "" : _item.attr("dneOrdSeq");
        var upOrdSeq = $.isEmpty(_item.attr("upOrdSeq")) ? "" : _item.attr("upOrdSeq");
        var upeOrdSeq = $.isEmpty(_item.attr("upeOrdSeq")) ? "" : _item.attr("upeOrdSeq");
        var triggerEvent = $.n2s(_item.attr("triggerEvent"));

        _item.gfSetComCd2ComboBox({
            grpCd : grpCd,
            isSetNF : isSetNF,
            textNF : textNF,
            useYn : useYn,
            setValue : setValue,
            isDisabled : isDisabled,
            grpOpt: grpOpt,
            dnOrdSeq: dnOrdSeq,
            dneOrdSeq: dneOrdSeq,
            upOrdSeq: upOrdSeq,
            upeOrdSeq: upeOrdSeq,
            triggerEvent: triggerEvent
        });
    });
};

/*
 * 공통코드 데이터 SelectBox 세팅하기
 */
$.fn.gfSetComCd2ComboBox = function(opts) {
    var _this = this;

    if($.isEmpty(opts)) return false;

    // 옵션
    var grpCd  = opts.grpCd; // 그룹코드(필수)
    var useYn  = opts.useYn; // 사용여부값 적용(true 일경우 useYn = "Y"만 세팅, 기본값 false)
    var grpOpt = opts.grpOpt; // 그룹 옵션
    var dnOrdSeq = opts.dnOrdSeq; // 순서 등급 하위
    var dneOrdSeq = opts.dneOrdSeq; // 순서 등급 하위(=포함)
    var upOrdSeq = opts.upOrdSeq; // 순서 등급 상위
    var upeOrdSeq = opts.upeOrdSeq; // 순서 등급 상위(=포함)

    var isSetNF = $.isEmpty(opts.isSetNF) ? false : opts.isSetNF; // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
    var textNF = $.isEmpty(opts.textNF) ? "" : opts.textNF; // 값이 없는 필드의 Text
    var setValue = opts.setValue; // 선택되어질 값 세팅
    var isDisabled = $.isEmpty(opts.isDisabled) ? false : opts.isDisabled; // 사용불가 세팅 true/false
    var triggerEvent = $.n2s(opts.triggerEvent); // 발생할 이벤트

    var gdComcdF = $.fgGetComCdData({
        grpCd: opts.grpCd,
        useYn: opts.useYn,
        grpOpt: opts.grpOpt,
        dnOrdSeq: opts.dnOrdSeq,
        dneOrdSeq: opts.dneOrdSeq,
        upOrdSeq: opts.upOrdSeq,
        upeOrdSeq: opts.upeOrdSeq,
    });

    // 초기화
    _this.empty();

    // 값이 없는 필드를 가지는 경우
    if(isSetNF) {
        _this.append($("<option/>")
                        .attr("value", "")
                        .text(textNF)
                       );
    }

    // 옵션값 생성
    $.each(gdComcdF, function(i, item) {
        var _option = $("<option/>");

        $.each(item, function(k, v) {
            _option.attr(k, v);
        });
        _option.attr("value", item.comCd);
        _this.append(_option.text(item.comNm));
    });

    // 선택되어질 값 설정
    if(!$.isEmpty(setValue)) {
        _this.val(setValue).prop("selected", true);
    }

    // 이벤트 발생(trigger)
    if(!$.isEmpty(triggerEvent)) _this.trigger(triggerEvent);

    // 사용여부 세팅
     _this.prop("disabled", isDisabled);
};

/*
 * 직원 데이터 SelectBox 초기화
 */
$.gfInitStaff2ComboBox = function(formOnly) {
    var conditionSelector = "select[formType='staffSel']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // Select Box로 세팅될 값들을 찾아온다(formType="staffSel")
    var _staffSel = $(conditionSelector); // 공통코드 Select 박스 대상들

    _staffSel.each(function(inx, item) {
        var _item = $(item);

        var isSetNF = _item.attr("isSetNF") == "true" ? true : false;
        var textNF = $.isEmpty(_item.attr("textNF")) ? "" : _item.attr("textNF");
        var useYn = _item.attr("useYn") == "true" ? true : false;
        var setValue = $.isEmpty(_item.attr("setValue")) ? "" : _item.attr("setValue");
        var isDisabled = _item.attr("isDisabled") == "true" ? true : false;
        var triggerEvent = $.n2s(_item.attr("triggerEvent"));

        _item.gfSetStaff2ComboBox({
            isSetNF : isSetNF,
            textNF : textNF,
            useYn : useYn,
            setValue : setValue,
            isDisabled : isDisabled,
            triggerEvent: triggerEvent
        });
    });
};

/*
 * 직원 데이터 SelectBox 세팅하기
 */
$.fn.gfSetStaff2ComboBox = function(opts) {
    var _this = this;

    // 옵션
    var isSetNF      = false;                             // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
    var textNF       = "";                                // 값이 없는 필드 text
    var useYn        = false;                             // 사용여부값 적용
    var setValue     = "";                                // 선택되어질 값 세팅
    var isDisabled   = false;                             // 사용불가
    var triggerEvent = $.n2s(_this.attr("triggerEvent")); // 발생할 이벤트

    if(!$.isEmpty(opts)) {
        isSetNF      = $.isEmpty(opts.isSetNF) ? false : opts.isSetNF; // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
        textNF       = $.isEmpty(opts.textNF) ? "" : opts.textNF; // 값이 없는 필드 text
        useYn        = $.isEmpty(opts.useYn) ? false : opts.useYn;
        setValue     = opts.setValue;
        isDisabled   = $.isEmpty(opts.isDisabled) ? false : opts.isDisabled;
        triggerEvent = $.n2s(_this.attr("triggerEvent"));
    }

    // 사용여부(useYn) 값에 의한 Filtering
    var gdStaffF = $.grep(GD_SHOP_STAFF, function(el, inx){
        return useYn ? el.useYn == "Y" : true;
    });

    // 초기화
    _this.empty();

    // 값이 없는 필드를 가지는 경우
    if(isSetNF) {
        _this.append($("<option/>")
                        .attr("value", "")
                        .text(textNF)
                       );
    }

    // 옵션값 생성
    $.each(gdStaffF, function(i, item) {
        var _option = $("<option/>");
        $.each(item, function(k, v) {
            _option.attr(k, v);
        });
        _option.attr("value", item.userId);
        _this.append(_option.text(item.userNm + "[" + item.userAuthNm + "]"));
    });

    // 선택되어질 값 설정
    if(!$.isEmpty(setValue)) {
        _this.val(setValue).prop("selected", true);
    }

    // 사용여부 세팅
    _this.prop("disabled", isDisabled);

    // 이벤트 발생(trigger)
    if(!$.isEmpty(triggerEvent)) _this.trigger(triggerEvent);
};

/*
 * Switch 버튼 초기화
 */
$.gfInitSwitchButton = function(formOnly) {

    var _jsSwich = $(".js-switch");

    $.each(_jsSwich, function(i, item){
        new Switchery(item, { color: "#428bca" });
    });
};


/*
 * 매장 데이터 SelectBox 초기화
 */
$.gfInitShop2ComboBox = function(formOnly) {
    var conditionSelector = "select[formType='shopSel']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // Select Box로 세팅될 값들을 찾아온다(formType="shopSel")
    var _shopSel = $(conditionSelector); // 공통코드 Select 박스 대상들

    _shopSel.each(function(inx, item) {
        var _item = $(item);

        var isSetNF = _item.attr("isSetNF") == "true" ? true : false;
        var textNF = $.isEmpty(_item.attr("textNF")) ? "" : _item.attr("textNF");
        var useYn = _item.attr("useYn") == "true" ? true : false;
        var setValue = $.isEmpty(_item.attr("setValue")) ? "" : _item.attr("setValue");
        var isDisabled = _item.attr("isDisabled") == "true" ? true : false;
        var triggerEvent = $.n2s(_item.attr("triggerEvent"));

        _item.gfSetShop2ComboBox({
            isSetNF : isSetNF,
            textNF : textNF,
            useYn : useYn,
            setValue : setValue,
            isDisabled : isDisabled,
            triggerEvent: triggerEvent
        });
    });
};

/*
 * 매장 데이터 SelectBox 세팅하기
 */
$.fn.gfSetShop2ComboBox = function(opts) {
    var _this = this;

    // 옵션
    var isSetNF      = false;                             // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
    var textNF       = "";                                // 값이 없는 필드 text
    var useYn        = false;                             // 사용여부값 적용
    var setValue     = "";                                // 선택되어질 값 세팅
    var isDisabled   = false;                             // 사용불가
    var triggerEvent = $.n2s(_this.attr("triggerEvent")); // 발생할 이벤트

    if(!$.isEmpty(opts)) {
        isSetNF      = $.isEmpty(opts.isSetNF) ? false : opts.isSetNF; // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
        textNF       = $.isEmpty(opts.textNF) ? "" : opts.textNF; // 값이 없는 필드 text
        useYn        = $.isEmpty(opts.useYn) ? false : opts.useYn;
        setValue     = opts.setValue;
        isDisabled   = $.isEmpty(opts.isDisabled) ? false : opts.isDisabled;
        triggerEvent = $.n2s(_this.attr("triggerEvent"));
    }

    // 사용여부(useYn) 값에 의한 Filtering
    var gdShopF = $.grep(GD_SYS_SHOP, function(el, inx){
        return useYn ? el.useYn == "Y" : true;
    });

    // 초기화
    _this.empty();

    // 값이 없는 필드를 가지는 경우
    if(isSetNF) {
        _this.append($("<option/>")
                        .attr("value", "")
                        .text(textNF)
                       );
    }

    // 옵션값 생성
    $.each(gdShopF, function(i, item) {
        var _option = $("<option/>");
        $.each(item, function(k, v) {
            _option.attr(k, v);
        });
        _option.attr("value", item.shopId);
        _this.append(_option.text(item.shopNm));
    });

    // 선택되어질 값 설정
    if(!$.isEmpty(setValue)) {
        _this.val(setValue).prop("selected", true);
    }

    // 사용여부 세팅
    _this.prop("disabled", isDisabled);

    // 이벤트 발생(trigger)
    if(!$.isEmpty(triggerEvent)) _this.trigger(triggerEvent);
};

/*
 * 직원 데이터 SelectBox 세팅하기
 */
$.gfInitAgent2ComboBox = function(formOnly) {
    var conditionSelector = "select[formType='agentSel']";

    if(!$.isEmpty(formOnly)) conditionSelector += "[formOnly='" + formOnly + "']";

    // Select Box로 세팅될 값들을 찾아온다(formType="agentSel")
    var _agentSel = $(conditionSelector); // 공통코드 Select 박스 대상들

    _agentSel.each(function(inx, item) {
        var _item = $(item);

        var isSetNF = _item.attr("isSetNF") == "true" ? true : false;
        var useYn = _item.attr("useYn") == "true" ? true : false;
        var setValue = $.isEmpty(_item.attr("setValue")) ? "" : _item.attr("setValue");
        var isDisabled = _item.attr("isDisabled") == "true" ? true : false;
        var triggerEvent = $.n2s(_item.attr("triggerEvent"));

        _item.gfSetAgent2ComboBox({
            isSetNF : isSetNF,
            useYn : useYn,
            setValue : setValue,
            isDisabled : isDisabled,
            triggerEvent: triggerEvent
        });
    });
};

/*
 * 거래처 데이터 SelectBox 세팅하기
 */
$.fn.gfSetAgent2ComboBox = function(opts) {
    var _this = this;

    // 옵션
    var isSetNF      = false;                             // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
    var useYn        = false;                             // 사용여부값 적용
    var setValue     = "";                                // 선택되어질 값 세팅
    var isDisabled   = false;                             // 사용불가
    var telecomCd    = "";                                // 통신사코드
    var triggerEvent = $.n2s(_this.attr("triggerEvent")); // 발생할 이벤트

    if(!$.isEmpty(opts)) {
        isSetNF      = $.isEmpty(opts.isSetNF) ? false : opts.isSetNF; // 값이 없는 필드를 가지는지 여부 기본값(true일 경우 Null Option 멤버 추가, 기본값 false)
        useYn        = $.isEmpty(opts.useYn) ? false : opts.useYn;
        setValue     = opts.setValue;
        isDisabled   = $.isEmpty(opts.isDisabled) ? false : opts.isDisabled;
        telecomCd    = $.n2s(opts.telecomCd);
        triggerEvent = $.n2s(opts.triggerEvent);
    }

    // 조건에 의한 값에 의한 Filtering
    var gdAgentF = $.grep(GD_AGENT, function(el, inx){
        var arrTelecomCds = el.telecomCd.split(",");

        return (useYn ? el.useYn == "Y" : true)
            && ($.isEmpty(telecomCd) ? true : $.inArray(telecomCd, arrTelecomCds) > -1)
            ;
    });

    // 초기화
    _this.empty();

    // 값이 없는 필드를 가지는 경우
    if(isSetNF) {
        _this.append($("<option/>")
                        .attr("value", "")
                        .text("")
                       );
    }
    // 옵션값 생성
    $.each(gdAgentF, function(i, item) {
        var _option = $("<option/>");
        $.each(item, function(k, v) {
            _option.attr(k, v);
        });
        _this.append(_option.text(item.text));
    });

    // 선택되어질 값 설정
    if(!$.isEmpty(setValue)) {
        _this.val(setValue).prop("selected", true);
    }

    // 사용여부 세팅
    _this.prop("disabled", isDisabled);

    // 이벤트 발생(trigger)
    if(!$.isEmpty(triggerEvent)) _this.trigger(triggerEvent);
};

/*
 * 단말기모델 & 요금제코드로 해당 공시지원금 가져오기
 */
$.gfGetSptAmt = function(opts) {
    var prodCd = opts.prodCd;
    var planCd = opts.planCd;
    var sptAmt = "";

    // 모델코드와 요금제코드 값에 의한 Filtering
    var gdSptAmtF = $.grep(GD_SPT_AMT, function(el, inx){
        // ALL에 대한 처리 필요
        return (el.prodCd == prodCd && el.planCd == planCd);
    });

    $.each(gdSptAmtF, function(i, item) {
        sptAmt = item.sptAmt;
    });

    return sptAmt;
};

/*
 * Chosen Selectbox 데이터 세팅하기(공통사용)
 */
$.fn.gfSetChosenData = function(opts) {
    var _this = this;

    // 옵션이 없거나 Data Key가 없을 경우 처리 안함
    if($.isEmpty(opts) || $.isEmpty(opts.dataKey)) return false;

    // opts 초기화
    var dataKey  = opts.dataKey; // 데이터 Key gv.js gSysGDs 참조
    var optGroup = $.n2s(opts.optGroup); // optGroup 필드 명(있을 경우 grpGroup 처리)
    var filters  = $.isEmpty(opts.filters) ? {} : opts.filters; // 필터조건
    var setValue = $.n2s(opts.setValue); // 세팅될 값
    var disabled = $.isEmpty(opts.disabled) ? false : opts.disabled;

    // Key에 의한 대상 데이터 세팅
    var targetData = disabled ? {} : eval(dataKey);

    // 조건에 의한 값에 의한 Filtering
    var filterData = $.grep(targetData, function(el, inx){
        var flag = true;

        $.each(filters, function(key, value) {
            if(eval("el." + key) !== value) flag = false;
        });

        return flag;
    });

    // select option데이터 제거
    _this.empty();

    // 첫번째 빈값 등록
    _this.append(
                 $("<option/>")
                  .attr("value", "")
                  .text("")
                );

    // option 추가
    if($.isEmpty(optGroup)) { // optGroup 설정이 없을 경우
        $.each(filterData, function(i, item) {
            var _option = $("<option/>");
            $.each(item, function(k, v) {
                _option.attr(k, v);
            });
            _this.append(_option.text(item.text));
        });

    } else { // optGroup 설정이 있을 경우
        // 입고 단말기(개통가능한) 데이터 콤보 생성하기
        var grpOptTmp = "";
        var _optGroup = $("<optGroup/>");

        $.each(filterData, function(i, item) {

            // optGroup에 해당하는 데이터 값 획득
            var grpOpt = eval("item." + optGroup);

            if(grpOptTmp != grpOpt) {
                if(i > 0) {
                    _this.append(_optGroup);
                    _optGroup = $("<optGroup/>");
                    _optGroup.attr("label", grpOpt);
                } else {
                    _optGroup.attr("label", grpOpt);
                }

                grpOptTmp = grpOpt;
            }

            var _option = $("<option/>");
            $.each(item, function(k, v) {
                _option.attr(k, v);
            });
            _optGroup.append(_option.text(item.text));
        });

        // 마지막 그룹 추가
        if(filterData.length > 0) {
            _this.append(_optGroup);
        }

    }

    // 데이터가 없을 경우 disabled
    _this.prop("disabled", filterData.length > 0 ? false : true);

    // 값세팅
    _this.val(setValue);

    _this.trigger("chosen:updated");
    _this.trigger("change");

};


/*
 * 현재 일자 시간 가져오기
 */
$.gfGetNowDateTime = function(opt) {
    opt = $.isEmpty(opt) ? "" : opt.toLowerCase();
    var rtn = "";

    var weekName = new Array('일', '월', '화', '수', '목', '금', '토');
    var fyear = gCurrentDateTime.getFullYear();
    var year  = gCurrentDateTime.getYear();
    var year2 = ("" + fyear).slice(-2);
    var mon   = gCurrentDateTime.getMonth() + 1;
    var mon2  = ("0" + mon).slice(-2);
    var day   = gCurrentDateTime.getDate();
    var day2  = ("0" + day).slice(-2);
    var wk    = gCurrentDateTime.getDay();
    var wn    = weekName[wk];
    var hour  = gCurrentDateTime.getHours();
    var min   = gCurrentDateTime.getMinutes();
    var sec   = gCurrentDateTime.getSeconds();
    var ampm  = (hour < 12) ? "오전" : "오후";

    switch(opt) {
        case "yyyy-mm-dd":
            rtn = fyear + "-" + mon2 + "-" + day2;
            break;
        case "yy-mm-dd":
            rtn = year2 + "-" + mon2 + "-" + day2;
            break;
        default :
//            rtn = fyear + "년 " + mon + "월 " + day + "일 (" + wn + ") " + ampm + " " + hour + ":" + min + ":" + sec;
            break;
    }
    return rtn;
};

/*
 * Date Picker Disable/enable
 */
$.fn.gfDisabledDatePicker = function(flag) {
    var _this = this;
    var _objDateFields = _this.children("span").children("input");

    flag = $.isEmpty(flag) ? false : flag;

    _this.prop("disabled", flag);
    _this.disabledClick(flag);
    _objDateFields.prop("disabled", flag);
    if(flag) {
        _objDateFields.val("");
        _this.datepicker("update", "");
    }
}

/*
 * 클릭 방지용(div, span 등등)
 */
$.fn.disabledClick = function(flag) {
    var _this = this;
    flag = $.isEmpty(flag) ? false : flag;

    // true -> disabled일 경우
    if(flag) {
        _this.addClass("disabled-click");
    } else {
        _this.removeClass("disabled-click");
    }
};

/*
 * 사용자 입력 오류등의 알림 메세지(toaster활용) : javascript 처리
 */
$.gfNotiMsg = function(opts) {
    var msgCd    = "";
    var msgType  = "info";
    var title    = "";
    var msg      = "";
    var focusId  = "";
    var msgFrom  = "G"; // G : GD_SYS_MSG 에서 획득(default)

    if($.isEmpty(opts)) return false;
    else {
        if($.type(opts) === "string") { // 메세지 코드만 입력했을 경우 단일 string parameter
            msgCd = $.n2s(opts);
        } else if($.type(opts) === "object") { // 옵션 object로 입력했을 경우
            msgCd = $.n2s(opts.msgCd);
            msgType = $.isEmpty(opts.msgType) ? "info" : opts.msgType;
            title = $.n2s(opts.title);
            msg = $.n2s(opts.msg);
            focusId = $.n2s(opts.focusId);
            msgFrom   = $.isEmpty(opts.msgFrom) ? "G" : opts.msgFrom;
        } else {
            return false;
        }
    }

    if(msgFrom == "G") {
        // 메세지 코드(msgCd) 값에 의한 Filtering
        var gdSysmsgF = $.grep(GD_SYS_MSG, function(el, inx){
            return el.msgCd == msgCd;
        });

        if(gdSysmsgF.length != 1) {
            console.log("System Message Code is Not Exist or Duplicated!!! Message Count [" + gdSysmsgF.length + "]");
            return false;
        } else {
            msgCd = gdSysmsgF[0].msgCd;
            if($.type(opts) === "string"){
                msgType = gdSysmsgF[0].msgType;
                title = gdSysmsgF[0].title;
                msg = gdSysmsgF[0].msg;
            } else {
                msgType = $.isEmpty(msgType) ? gdSysmsgF[0].msgType : msgType;
                title = $.isEmpty(title) ? gdSysmsgF[0].title : title;
                msg = $.isEmpty(msg) ? gdSysmsgF[0].msg : msg;
            }
        }

        // focus 되어야할 ID가 존재하는 경우
        if(!$.isEmpty(focusId)) {
            _focusTarget = $("#" + focusId);
            _focusTarget.focus();
        }
    }

    toastr.options = {
        "closeButton": true,
        "debug": false, // true일 경우 console.log로 나옴
        "progressBar": true,
        "preventDuplicates": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "showDuration": "400",
        "hideDuration": "1000",
        "timeOut": "3000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    var $toast = toastr[msgType](msg, title);
    $toastlast = $toast;
};

/*
 * 사용자 입력 오류등의 알림 메세지(toaster활용) : 서버 에러코드 및 메시지 처리
 */
$.gfNotiMsgSvr = function(opts) {

    var msgCd    = "";
    var msgType  = "info";
    var title    = "";
    var msg      = "";

    if($.isEmpty(opts)) return false;
    else {
        msgCd = $.n2s(opts.msgCd);
        msgType = $.isEmpty(opts.msgType) ? "info" : opts.msgType;
        title = $.n2s(opts.title);
        msg = $.n2s(opts.msg);
    }

    toastr.options = {
        "closeButton": true,
        "debug": false, // true일 경우 console.log로 나옴
        "progressBar": true,
        "preventDuplicates": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "showDuration": "400",
        "hideDuration": "1000",
        "timeOut": "3000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    var $toast = toastr[msgType](msg, title);
    $toastlast = $toast;
};


/*
 * 그룹코드에 해당하는 공통코드 데이터 값 가져오기
 *  opts.grpCd  : 공통코드의 그룹코드(Default All)
 *  opts.useYn  : 사용여부(Default All, "Y" or "N" else Null)
 *  opts.grpOpt : 그룹옵션(Default All else 해당 옵션)
 */
$.fgGetComCdData = function(opts) {
    var comCdData;

    if($.isEmpty(opts)) return null;

    var grpCd = opts.grpCd; // 그룹코드(필수)
    var useYn = $.n2s(opts.useYn); // 사용여부값 적용(true 일경우 useYn = "Y"만 세팅, 기본값 false)
    var grpOpt = $.n2s(opts.grpOpt); // 그룹옵션
    var dnOrdSeq = $.n2s(opts.dnOrdSeq); // 순서 등급 하위
    var dneOrdSeq = $.n2s(opts.dneOrdSeq); // 순서 등급 하위(=포함)
    var upOrdSeq = $.n2s(opts.upOrdSeq); // 순서 등급 상위
    var upeOrdSeq = $.n2s(opts.upeOrdSeq); // 순서 등급 상위(=포함)
    var sortR = $.isEmpty(opts.sortR) ? false : opts.sortR; // 역정렬 순서 여부(기본 오름차순)

    comCdData = $.grep(GD_SYS_COM_CD, function(el, inx){
        return el.grpCd == grpCd
            && (useYn == "" ? true : el.useYn == useYn)
            && (grpOpt == "" ? true : el.grpOpt.indexOf(grpOpt) > -1)
            && (dnOrdSeq == "" ? true : el.ordSeq > dnOrdSeq)
            && (dneOrdSeq == "" ? true : el.ordSeq >= dneOrdSeq)
            && (upOrdSeq == "" ? true : el.ordSeq < upOrdSeq)
            && (upeOrdSeq == "" ? true : el.ordSeq <= upeOrdSeq)
            ;
    });

    if(sortR){
        comCdData = comCdData.sort(function(a, b){
            return b.ordSeq - a.ordSeq;
        });
    }

    return comCdData;
};

/*
 * Form Field 초기화
 */
$.gfInitFormField = function(formOnly) {

    // 체크박스/라디오버튼  초기화
    $.gfInitCheckbox(formOnly);

    // 직원 필드 초기화
    $.gfInitStaff2ComboBox(formOnly);

    // 딜러/대리점 필드 초기화
    $.gfInitAgent2ComboBox(formOnly);

    // 날짜 입력란 달력피커 초기화
    $.gfInitDatePicker(formOnly);

    // 금액 입력란 초기화
    $.gfInitCurrency(formOnly);

    // 공통 Select Box 값 초기화
    $.gfInitComCd2ComboBox(formOnly);

    // 전화번호 필드 초기화
    $.gfInitTelNo(formOnly);

    // User ID 필드 초기화
    $.gfInitUserId(formOnly);

    // 사업자번호 필드 초기화
    $.gfInitBizLicNo(formOnly);

    // Readonly 텍스트 박스 초기화
    $.gfInitTextReadonly(formOnly);

    // Chosen Select 초기화
    $.gfInitChosen(formOnly);

    // 매장 필드 초기화
    $.gfInitShop2ComboBox(formOnly);

    // Switch 버튼 초기화
    $.gfInitSwitchButton(formOnly);

};

/*
 * 필수부가 서비스의 초기화처리
 */
$.fn.gfInitEasGrp = function(opts) {
    var _target = this;
    var _multiGroup = _target.closest("[eas-area='multi-group']");

    var _areaButton            = _target.children("[eas-area='button']") // 서비스선택 버튼 영역
    var _areaContent           = _target.children("[eas-area='content']") // 필수부가서비스 내용 영역
    var _areaEasAmtCap         = _target.children("[eas-area='eas-amt-cap']") // 금액 Caption영역
    var _areaEasAmt            = _target.children("[eas-area='eas-amt']") // 금액 영역
    var _areaEasCurrency       = _target.children("[eas-area='eas-currency']") // 금액 단위 영역
    var _areaEasKeepDateCap    = _target.children("[eas-area='eas-keep-date-cap']") // 유지일 Caption 영역
    var _areaEasKeepDate       = _target.children("[eas-area='eas-keep-date']") // 유지일 Caption 영역

    var _itemButton            = _areaButton.find("[eas-item='button']"); // 서비스 선택 버튼
    var _itemContent           = _areaContent.children("[eas-item='content']") // 미비서류 내용
    var _itemEasAmt            = _areaEasAmt.children("[eas-item='eas-amt']") // 서비스 금액
    var _itemEasKeepDatePicker = _areaEasKeepDate.find("[eas-item='eas-keep-date-picker']") // 유지일 날짜 Picker
    var _itemEasKeepDateField  = _itemEasKeepDatePicker.find("[eas-item='eas-keep-date-field']") // 유지일 날짜 입력 영역

    // 서비스명 초기화
    _itemContent.gfSetTextReadonly("", "");

    // 금액 초기화
    _itemEasAmt.gfSetCurrency();
    _itemEasAmt.val("").prop("disabled", true);

    // 유지일 초기화
    _itemEasKeepDatePicker.gfSetDatePicker();
    _itemEasKeepDatePicker.gfDisabledDatePicker(true);

    // 서비스 선택 버튼 초기화
    _itemButton.removeClass("on");

    // 필수부가서비스 버튼 이벤트 추가
    _itemButton.off("click").on("click", function(e, params) {
        var _this = $(this);
        var _target = _this.closest("[eas-area='group']");
        var _multiGroup = _target.closest("[eas-area='multi-group']");

        var _areaButton            = _target.children("[eas-area='button']") // 서비스선택 버튼 영역
        var _areaContent           = _target.children("[eas-area='content']") // 필수부가서비스 내용 영역
        var _areaEasAmtCap         = _target.children("[eas-area='eas-amt-cap']") // 금액 Caption영역
        var _areaEasAmt            = _target.children("[eas-area='eas-amt']") // 금액 영역
        var _areaEasCurrency       = _target.children("[eas-area='eas-currency']") // 금액 단위 영역
        var _areaEasKeepDateCap    = _target.children("[eas-area='eas-keep-date-cap']") // 유지일 Caption 영역
        var _areaEasKeepDate       = _target.children("[eas-area='eas-keep-date']") // 유지일 Caption 영역

        var _itemButton            = _areaButton.find("[eas-item='button']"); // 서비스 선택 버튼
        var _itemContent           = _areaContent.children("[eas-item='content']") // 미비서류 내용
        var _itemEasAmt            = _areaEasAmt.children("[eas-item='eas-amt']") // 서비스 금액
        var _itemEasKeepDatePicker = _areaEasKeepDate.find("[eas-item='eas-keep-date-picker']") // 유지일 날짜 Picker
        var _itemEasKeepDateField  = _itemEasKeepDatePicker.find("[eas-item='eas-keep-date-field']") // 유지일 날짜 입력 영역

        // 서비스추가 버튼 사전조건 이벤트 처리
        if(!$.isEmpty(opts) && !$.isEmpty(opts.beforeClickBtn)) {
            if(!opts.beforeClickBtn()) return false;
        }
        var target  = _multiGroup.attr("id");
        var agentCd = _multiGroup.attr("agentCd");
        var agentNm = _multiGroup.attr("agentNm");
        var seqNo   = _target.attr("seqNo");
        var srvcCds = _itemContent.attr("value");

        // 모달 팝업 호출
        $.gfCommonPopUp({
            popUrl: "/static/popup_32_03.html",
            width: "520",
            attrs: {
                target: target,
                seqNo: seqNo,
                agentCd: agentCd,
                agentNm: agentNm,
                srvcCds: srvcCds,
                srvcGb: "A" // 서비스 구분(필수부가서비스 : A)
            }
        });
    });
};

/*
 * 환수 서비스의 초기화처리
 */
$.fn.gfInitDesGrp = function(opts) {
    var _target = this;

    var _areaButton           = _target.children("[des-area='button']") // 서비스선택 버튼 영역
    var _areaContent          = _target.children("[des-area='content']") // 환수서비스 내용 영역
    var _areaDesAmtCap        = _target.children("[des-area='des-amt-cap']") // 금액 Caption영역
    var _areaDesAmt           = _target.children("[des-area='des-amt']") // 금액 영역
    var _areaDesCurrency      = _target.children("[des-area='des-currency']") // 금액 단위 영역

    var _itemButton           = _areaButton.find("[des-item='button']");
    var _itemContent          = _areaContent.children("[des-item='content']") // 미비서류 내용 영역
    var _itemDesAmt           = _areaDesAmt.children("[des-item='des-amt']") // 미비서류 내용 영역

    // 환수서비스명 초기화
    _itemContent.gfSetTextReadonly("", "");

    // 금액 초기화
    _itemDesAmt.val("").prop("disabled", true);

    // 서비스 선택 버튼 초기화
    _itemButton.removeClass("on");

    // 환수서비스 버튼 이벤트 추가
    _itemButton.off("click").on("click", function(e, params) {
        var _this = $(this);
        var _target = _this.closest("[des-area='group']");

        var _areaButton           = _target.children("[des-area='button']") // 서비스선택 버튼 영역
        var _areaContent          = _target.children("[des-area='content']") // 환수서비스 내용 영역
        var _areaDesAmtCap        = _target.children("[des-area='des-amt-cap']") // 금액 Caption영역
        var _areaDesAmt           = _target.children("[des-area='des-amt']") // 금액 영역
        var _areaDesCurrency      = _target.children("[des-area='des-currency']") // 금액 단위 영역

        var _itemContent          = _areaContent.children("[des-item='content']") // 미비서류 내용 영역

        // 서비스추가 버튼 사전조건 이벤트 처리
        if(!$.isEmpty(opts) && !$.isEmpty(opts.beforeClickBtn)) {
            if(!opts.beforeClickBtn()) return false;
        }

        var target  = _target.attr("id");
        var agentCd = _target.attr("agentCd");
        var agentNm = _target.attr("agentNm");
        var srvcCds = _itemContent.attr("value");

        // 모달 팝업 호출
        $.gfCommonPopUp({
            popUrl: "/static/popup_32_04.html",
            width: "520",
            attrs: {
                target: target,
                agentCd: agentCd,
                agentNm: agentNm,
                srvcCds: srvcCds,
                srvcGb: "B" // 서비스 구분(환수서비스 : B)
            }
        });
    });
};



/*
 * 미비서류의 초기화처리
 */
$.fn.gfInitLodGrp = function(opts) {

    var _target = this;
    var _areaButton           = _target.children("[lod-area='button']") // 미비선택 버튼 영역
    var _areaContent          = _target.children("[lod-area='content']") // 미비서류 내용 영역
    var _areaDueDateCap       = _target.children("[lod-area='due-date-cap']") // 예정기일 Caption영역
    var _areaDueDate          = _target.children("[lod-area='due-date']") // 기일 영역

    var _itemButton           = _areaButton.find("[lod-item='button']"); // 미비선택 버튼
    var _itemContent          = _areaContent.children("[lod-item='content']") // 미비서류 내용
    var _itemDueDatePicker    = _areaDueDate.find("[lod-item='due-date-picker']") // 예정기일 Picker
    var _itemDueDateField     = _itemDueDatePicker.find("[lod-item='due-date-field']") // 예정기일

    // 미비서류명 초기화
    _itemContent.gfSetTextReadonly("", "");

    // 예정기일 초기화
    _itemDueDatePicker.gfSetDatePicker();
    _itemDueDatePicker.gfDisabledDatePicker(true);

    // 미비선택 버튼 초기화
    _itemButton.removeClass("on");

    // 미비선택 버튼 이벤트 추가
    _itemButton.off("click").on("click", function(e, params) {
        var _this = $(this);

        // 미비선택 버튼 사전조건 이벤트 처리
        if(!$.isEmpty(opts) && !$.isEmpty(opts.beforeClickBtn)) {
            if(!opts.beforeClickBtn()) return false;
        }

        // 모달 팝업 호출
        $.gfCommonPopUp({
            popUrl: "/static/popup_32_05.html",
            width: "520",
            attrs: {
                target: _target.attr("id"),
                lodCds: _itemContent.attr("value")
            }
        });
    });
};

/*
 * 홈/인터넷 결합 상품의 초기화처리
 */
$.fn.gfInitCcGrp = function(opts) {
    var _target = this;

    var _areaProduct               = _target.children("[cc-area='product']") // 결합 상품 선택 영역
    var _areaMemo                  = _target.children("[cc-area='memo']") // 메모 선택 영역
    var _areaPlanDateCap           = _target.children("[cc-area='plan-date-cap']") // 결합 상품 예정기일 Caption 영역
    var _areaPlanDate              = _target.children("[cc-area='plan-date']") // 결합 상품 예정기일 영역

    var _itemProduct               = _areaProduct.children("[cc-item='product']") // 결합 상품 선택
    var _itemMemo                  = _areaMemo.find("[cc-item='memo']") // 메모
    var _itemPlanDateCap           = _areaPlanDateCap.children("[cc-item='plan-date-cap']") // 결합 상품 예정기일 Caption
    var _itemPlanDatePicker        = _areaPlanDate.find("[cc-item='plan-date-picker']") // 예정기일 날짜 Picker
    var _itemPlanDateField         = _itemPlanDatePicker.find("[cc-item='plan-date-field']") // 예정기일

    var telecomCd = _target.attr("telecomCd");

    // 결합 상품 데이터 세팅
    _itemProduct.gfSetChosenData({
        dataKey: "GD_PROD_CC",
        filters: {
            telecomCd: telecomCd
        }
    });

    // 메모 Clear
    _itemMemo.val("");
    _itemMemo.prop("disabled", true);

    // 예정기일 초기화
    _itemPlanDatePicker.gfDisabledDatePicker(true);

    // 결합 상품 변경 시 이벤트 추가
    _itemProduct.off("change").on("change", function(e, params) {
        var _this                      = $(this);
        var _target                    = _this.closest("[cc-area='group']");

        var _areaProduct               = _target.children("[cc-area='product']") // 결합 상품 선택 영역
        var _areaMemo                  = _target.children("[cc-area='memo']") // 메모 영역
        var _areaPlanDateCap           = _target.children("[cc-area='plan-date-cap']") // 결합 상품 예정기일 Caption 영역
        var _areaPlanDate              = _target.children("[cc-area='plan-date']") // 결합 상품 예정기일 영역

        var _itemProduct               = _areaProduct.children("[cc-item='product']") // 결합 상품 선택
        var _itemMemo                  = _areaMemo.find("[cc-item='memo']") // 메모
        var _itemPlanDateCap           = _areaPlanDateCap.children("[cc-item='plan-date-cap']") // 결합 상품 예정기일 Caption
        var _itemPlanDatePicker        = _areaPlanDate.find("[cc-item='plan-date-picker']") // 예정기일 날짜 Picker
        var _itemPlanDateField         = _itemPlanDatePicker.find("[cc-item='plan-date-field']") // 예정기일

        var telecomCd = _target.attr("telecomCd");

        if($.isEmpty(_this.val())) { // 결합 상품을 선택하지 않았을 경우
            // 예정기일 초기화
            _itemPlanDatePicker.gfDisabledDatePicker(true);

            // 메모 초기화
            _itemMemo.val("");
            _itemMemo.prop("disabled", true);
        } else { // 결합 상품을 선택했을 경우
            // 예정기일 해제
            _itemPlanDatePicker.gfDisabledDatePicker(false);
//            _itemPlanDateField.trigger("focus");

            _itemMemo.val("");
            _itemMemo.prop("disabled", false);
        }

    });

};


/*
 * 인터넷 상품의 초기화처리
 */
$.fn.gfInitProdInternetGrp = function(opts) {
    var _target = this;

    var _areaProduct               = _target.children("[int-area='product']") // 인터넷 상품 선택 영역
    var _areaKeepDateCap           = _target.children("[int-area='keep-date-cap']") // 인터넷 상품 유지일 Caption 영역
    var _areaKeepDate              = _target.children("[int-area='keep-date']") // 인터넷 상품 유지일 영역
    var _areaProductChange         = _target.children("[int-area='product-change']") // 변경예정 인터넷 상품 영역
    var _areaProductChangeComment  = _target.children("[int-area='product-change-comment']") // 변경예정 인터넷 상품 코맨트 영역

    var _itemProduct               = _areaProduct.children("[int-item='product']") // 인터넷 상품 선택
    var _itemKeepDateCap           = _areaKeepDateCap.children("[int-item='keep-date-cap']") // 인터넷 상품 유지일 Caption
    var _itemKeepDatePicker        = _areaKeepDate.find("[int-item='keep-date-picker']") // 유지일 날짜 Picker
    var _itemKeepDateField         = _itemKeepDatePicker.find("[int-item='keep-date-field']") // 유지일 날짜 입력 영역
    var _itemProductChange         = _areaProductChange.children("[int-item='product-change']") // 변경예정 인터넷 상품
    var _itemProductChangeComment  = _areaProductChangeComment.children("[int-item='product-change-comment']") // 변경예정 인터넷 상품 코맨트

    var telecomCd = _target.attr("telecomCd");

    // 인터넷 상품 데이터 세팅
    _itemProduct.gfSetChosenData({
        dataKey: "GD_PROD_HI",
        filters: {
            telecomCd: telecomCd,
            prodGb: "I"
        }
    });

    // 유지일 초기화
    _itemKeepDatePicker.gfDisabledDatePicker(true);

    // 변경예정 상품 Disabled
    _itemProductChange.prop("disabled", true);

    // 변경예정 상품 코맨트 Disabled
    _itemProductChangeComment.val("");
    _itemProductChangeComment.prop("disabled", true);

    // 인터넷 상품 변경 시 이벤트 추가
    _itemProduct.off("change").on("change", function(e, params) {
        var _this                      = $(this);
        var _target                    = _this.closest("[int-area='group']");
        var _areaProduct               = _target.children("[int-area='product']") // 인터넷 상품 선택 영역
        var _areaKeepDateCap           = _target.children("[int-area='keep-date-cap']") // 인터넷 상품 유지일 Caption 영역
        var _areaKeepDate              = _target.children("[int-area='keep-date']") // 인터넷 상품 유지일 영역
        var _areaProductChange         = _target.children("[int-area='product-change']") // 변경예정 인터넷 상품 영역
        var _areaProductChangeComment  = _target.children("[int-area='product-change-comment']") // 변경예정 인터넷 상품 코맨트 영역

        var _itemProduct               = _areaProduct.children("[int-item='product']") // 인터넷 상품 선택
        var _itemKeepDateCap           = _areaKeepDateCap.children("[int-item='keep-date-cap']") // 인터넷 상품 유지일 Caption
        var _itemKeepDatePicker        = _areaKeepDate.find("[int-item='keep-date-picker']") // 유지일 날짜 Picker
        var _itemKeepDateField         = _itemKeepDatePicker.find("[int-item='keep-date-field']") // 유지일 날짜 입력 영역
        var _itemProductChange         = _areaProductChange.children("[int-item='product-change']") // 변경예정 인터넷 상품
        var _itemProductChangeComment  = _areaProductChangeComment.children("[int-item='product-change-comment']") // 변경예정 인터넷 상품 코맨트

        var telecomCd = _target.attr("telecomCd");

        if($.isEmpty(_this.val())) { // 인터넷 상품을 선택하지 않았을 경우
            // 유지일 초기화
//            _itemKeepDateField.val("");
            _itemKeepDatePicker.gfDisabledDatePicker(true);

            // 변경예정 상품 데이터 세팅
            _itemProductChange.gfSetChosenData({
                dataKey: "GD_PROD_HI",
                filters: {
                    telecomCd: telecomCd,
                    prodGb: "I",
                    disabled: true
                }
            });

            // 변경예정 상품 코맨트 Disabled
            _itemProductChangeComment.val("");
            _itemProductChangeComment.prop("disabled", true);
        } else { // 인터넷 상품을 선택했을 경우
            // 유지일 해제
            _itemKeepDatePicker.gfDisabledDatePicker(false);
//            _itemKeepDateField.trigger("focus");

            // 변경예정 상품 데이터 세팅
            _itemProductChange.gfSetChosenData({
                dataKey: "GD_PROD_HI",
                filters: {
                    telecomCd: telecomCd,
                    prodGb: "I"
                }
            });

            // 변경예정 상품 코맨트 Disabled 해제
            _itemProductChangeComment.prop("disabled", false);
        }

    });

};

/*
 * TV 상품의 초기화처리
 */
$.fn.gfInitProdTvGrp = function(opts) {

    var telecomCd = "";

    if(!$.isEmpty(opts)) {
        telecomCd = $.n2s(opts.telecomCd);
    }

    var _target = this;
    var _multiGroup = _target.closest("[tv-area='multi-group']");

    var _areaProduct               = _target.children("[tv-area='product']") // TV 상품 선택 영역
    var _areaKeepDateCap           = _target.children("[tv-area='keep-date-cap']") // TV 상품 유지일 Caption 영역
    var _areaKeepDate              = _target.children("[tv-area='keep-date']") // TV 상품 유지일 영역
    var _areaProductChange         = _target.children("[tv-area='product-change']") // 변경예정 TV 상품 영역
    var _areaProductChangeComment  = _target.children("[tv-area='product-change-comment']") // 변경예정 TV 상품 코맨트 영역

    var _itemProduct               = _areaProduct.children("[tv-item='product']") // TV 상품 선택
    var _itemKeepDateCap           = _areaKeepDateCap.children("[tv-item='keep-date-cap']") // TV 상품 유지일 Caption
    var _itemKeepDatePicker        = _areaKeepDate.find("[tv-item='keep-date-picker']") // 유지일 날짜 Picker
    var _itemKeepDateField         = _itemKeepDatePicker.find("[tv-item='keep-date-field']") // 유지일 날짜 입력 영역
    var _itemProductChange         = _areaProductChange.children("[tv-item='product-change']") // 변경예정 TV 상품
    var _itemProductChangeComment  = _areaProductChangeComment.children("[tv-item='product-change-comment']") // 변경예정 TV 상품 코맨트

    // TV 상품 데이터 세팅
    _itemProduct.gfSetChosenData({
        dataKey: "GD_PROD_HI",
        filters: {
            telecomCd: telecomCd,
            prodGb: "T"
        }
    });

    // 유지일 초기화
    _itemKeepDatePicker.gfDisabledDatePicker(true);

    // 변경예정 상품 Disabled
    _itemProductChange.prop("disabled", true);

    // 변경예정 상품 코맨트 Disabled
    _itemProductChangeComment.val("");
    _itemProductChangeComment.prop("disabled", true);

    // TV 상품 변경 시 이벤트 추가
    _itemProduct.off("change").on("change", function(e, params) {
        var _this                      = $(this);
        var _target                    = _this.closest("[tv-area='group']");
        var _multiGroup                = _target.closest("[tv-area='multi-group']");
        var _areaProduct               = _target.children("[tv-area='product']") // 인터넷 상품 선택 영역
        var _areaKeepDateCap           = _target.children("[tv-area='keep-date-cap']") // 인터넷 상품 유지일 Caption 영역
        var _areaKeepDate              = _target.children("[tv-area='keep-date']") // 인터넷 상품 유지일 영역
        var _areaProductChange         = _target.children("[tv-area='product-change']") // 변경예정 인터넷 상품 영역
        var _areaProductChangeComment  = _target.children("[tv-area='product-change-comment']") // 변경예정 인터넷 상품 코맨트 영역

        var _itemProduct               = _areaProduct.children("[tv-item='product']") // 인터넷 상품 선택
        var _itemKeepDateCap           = _areaKeepDateCap.children("[tv-item='keep-date-cap']") // 인터넷 상품 유지일 Caption
        var _itemKeepDatePicker        = _areaKeepDate.find("[tv-item='keep-date-picker']") // 유지일 날짜 Picker
        var _itemKeepDateField         = _itemKeepDatePicker.find("[tv-item='keep-date-field']") // 유지일 날짜 입력 영역
        var _itemProductChange         = _areaProductChange.children("[tv-item='product-change']") // 변경예정 인터넷 상품
        var _itemProductChangeComment  = _areaProductChangeComment.children("[tv-item='product-change-comment']") // 변경예정 인터넷 상품 코맨트

        var telecomCd = _multiGroup.attr("telecomCd");

        if($.isEmpty(_this.val())) { // 인터넷 상품을 선택하지 않았을 경우
            // 유지일 초기화
            _itemKeepDatePicker.gfDisabledDatePicker(true);

            // 변경예정 상품 데이터 세팅
            _itemProductChange.gfSetChosenData({
                dataKey: "GD_PROD_HI",
                filters: {
                    telecomCd: telecomCd,
                    prodGb: "T",
                    disabled: true
                }
            });

            // 변경예정 상품 코맨트 Disabled
            _itemProductChangeComment.val("");
            _itemProductChangeComment.prop("disabled", true);
        } else { // 인터넷 상품을 선택했을 경우
            // 유지일 해제
            _itemKeepDatePicker.gfDisabledDatePicker(false);
//            _itemKeepDateField.trigger("focus");

            // 변경예정 상품 데이터 세팅
            _itemProductChange.gfSetChosenData({
                dataKey: "GD_PROD_HI",
                filters: {
                    telecomCd: telecomCd,
                    prodGb: "T"
                }
            });

            // 변경예정 상품 코맨트 Disabled 해제
            _itemProductChangeComment.prop("disabled", false);
        }

    });

};

/*
 * TV 상품의 초기화처리
 */
$.fn.gfInitProdItpGrp = function(opts) {

    var telecomCd = "";

    if(!$.isEmpty(opts)) {
        telecomCd = $.n2s(opts.telecomCd);
    }

    var _target = this;
    var _multiGroup = _target.closest("[itp-area='multi-group']");

    var _areaProduct               = _target.children("[itp-area='product']") // 전화 상품 선택 영역

    var _itemProduct               = _areaProduct.children("[itp-item='product']") // TV 상품 선택

    // 전화 상품 데이터 세팅
    _itemProduct.gfSetChosenData({
        dataKey: "GD_PROD_HI",
        filters: {
            telecomCd: telecomCd,
            prodGb: "P"
        }
    });
};

/*
 * 컨텐츠 로딩용 공통 함수
 */
$.gfLoadContents = function(opts) {
    // 옵션 확인
    if($.isEmpty(opts) || $.isEmpty(opts.target)) return false;

    var url      = opts.url;
    var _target  = opts.target; // selector
    var params   = $.isEmpty(opts.params) ? {} : opts.params;

    $.gfAjax({
        type: "POST",
        url: url,
        data: params,
        async: true,
        beforeSendFunc: function(data, textStatus, jqXHR) {
        },
        doneFunc: function(data, textStatus, jqXHR) {
            _target.empty().append(data);
            // 콜백 함수 처리
            if(!$.isEmpty(opts.callback)) {
                opts.callback(data, textStatus, jqXHR);
            }
        },
        failFunc: function(jqXHR, textStatus, errorThrown) {
            _target.empty();

            // Http Error처리
            $.gfHttpErrorPopup({
                jqXHR: jqXHR,
                textStatus: textStatus,
                errorThrown: errorThrown,
                loginRequired: true
            });
        },
        spinTarget: $("#boxContents"),
    });
};


/*
 * 메뉴 데이터를 이용한 메뉴 구성
 */
$.gfSetSysMenu = function() {
    var _sideMenu = $("#side-menu"); // 메뉴가 들어갈 컨텐츠 자리
    _sideMenu.empty();

    var _liMenuGrp,
        _aMenuGrp,
        _iMenuGrp,
        _spanMenuGrpNm,
        _spanMenuGrpArrow,
        _ulMenuGrp,
        _liMenuSub,
        _aMenuSub
        ;

    var tempUpMenuId = "";

    $.each(GD_SYS_MENU, function (i, item) {

        // 상위 메뉴가 다를 경우 새로운 메뉴그룹을 생성
        if(tempUpMenuId != item.upMenuId) {
            // 첫번째 메뉴가 아닐 경우
            if(i != 0) {
                _liMenuGrp.append(_aMenuGrp)
                          .append(_ulMenuGrp);
                _sideMenu.append(_liMenuGrp);
            }

            _liMenuGrp        = $("<li/>");
            _aMenuGrp         = $("<a/>").attr("id", "upmenu_" + item.upMenuId);
            _iMenuGrp         = $("<i/>").addClass(item.upMenuCss);
            _spanMenuGrpNm    = $("<span/>").addClass("nav-label")
                                            .html(item.upMenuNm);
            _spanMenuGrpArrow = $("<span/>").addClass("fa arrow");

            _aMenuGrp.append(_iMenuGrp)
                     .append(_spanMenuGrpNm)
                     .append(_spanMenuGrpArrow)
                     ;

            _ulMenuGrp        = $("<ul/>").addClass("nav nav-second-level");

            tempUpMenuId      = item.upMenuId;
        }

        _liMenuSub = $("<li/>").attr("type", "menu")
        _aMenuSub  = $("<a/>").attr("id", "menu_" + item.menuId)
                              .attr("menuInfo", item.upMenuId + "," + item.menuId)
                              .attr("menuId", item.menuId)
                              .attr("upMenuId", item.upMenuId)
                              .attr("type", "menu")
                              .attr("param", "")
                              .html(item.menuNm)
                              ;

        _liMenuSub.append(_aMenuSub);
        _ulMenuGrp.append(_liMenuSub);


        // 마지막 메뉴일 경우
        if(i == GD_SYS_MENU.length -1) {
            _liMenuGrp.append(_aMenuGrp)
                      .append(_ulMenuGrp);

            _sideMenu.append(_liMenuGrp);
        }
    });

    // 메티스 메뉴 처리
//    $('#side-menu').metisMenu('dispose');
    $('#side-menu').metisMenu();

    // 메뉴 클릭 이벤트 초기화
    $.gfInitEventMenu();

    // 최초 선택 화면 처리(쿠키 이용)
    $.gfLoadInitPage();
};

/*
 * Post 방식의 CSRF Token 쿠키 세팅
 */
$.gfAjaxSetup = function() {
    // CSRF 세팅
    $.ajaxSetup({
        headers: { "X-CSRFToken": $.cookie("csrftoken") }
    });
};

/*
 * 공통 frmCommon에 Csrf Token Set
 */
$.gfSetCsrfToken = function(token) {
    $("#frmCommon [name='csrfmiddlewaretoken']").val(token);
};


/*
 * 공통 frmCommon에서 Csrf Token Get
 */
$.gfGetCsrfToken = function() {
    return $("#frmCommon [name='csrfmiddlewaretoken']").val();
};


/*
 * 공통 Ajax함수
 */
$.gfAjax = function(opts) {

    // 옵션
    var type            = $.isEmpty(opts.type) ? "POST" : opts.type; // 사용할 HTTP 메서드
    var url             = opts.url; // 데이터 URL(필수)
    var dataType        = $.isEmpty(opts.dataType) ? "" : opts.dataType;
    var data            = $.isEmpty(opts.data) ? type == "POST" ? {} : "" : opts.data;
    var async           = $.isEmpty(opts.async) ? true : opts.async;
    var cache           = $.isEmpty(opts.cache) ? false : opts.cache;
    var contentType     = $.isEmpty(opts.contentType) ? 'application/x-www-form-urlencoded; charset=UTF-8' : opts.contentType;
    var beforeSendFunc  = opts.beforeSendFunc; // Ajax 실행전 처리할 함수
    var successFunc     = opts.successFunc;    // Ajax 실행성공 시 처리할 함수(successFunc -> doneFunc 순서로 둘다 호출됨)
    var okFunc          = opts.okFunc;         // ReturnCode가 'OK' 일 경우 처리할 함수
    var ngFunc          = opts.ngFunc;         // ReturnCode가 'OK' 일 경우 처리할 함수
    var doneFunc        = opts.doneFunc;       // Ajax 실행성공 시 처리할 함수
    var failFunc        = opts.failFunc;       // Ajax 실패 시 처리할 함수
    var alwaysFunc      = opts.alwaysFunc;     // Ajax 항상실행 처리할 함수
    var _spinTarget     = opts.spinTarget;     // Ajax 실행시 spinner 처리 대상

    // POST방식일 경우
    if(type == "POST") data.csrfmiddlewaretoken = $.gfGetCsrfToken();

    try {
        // http://api.jquery.com/jquery.ajax/ 참조
        $.ajax({
            type: type, // default: 'POST'
            url: url, // default: The current page
            data: data,
            dataType: dataType,   // default: Intelligent Guess (xml, json, script, or html))
            contentType: contentType,
            cache: cache,
            async: async, // default: true
            beforeSend: function(jqXHR, settings) { // Ajax 실행전 처리
                if(!$.isEmpty(_spinTarget)) {
                    $.gfToggleLoading(_spinTarget, true);
                }
                if(!$.isEmpty(beforeSendFunc)) beforeSendFunc(jqXHR, settings);
            },
            success: function(data, cbFunc) {
                var resultCode = data.resultCode;
                if(resultCode == "OK") {
                    if(!$.isEmpty(okFunc)) okFunc(data, cbFunc);
                } else if(resultCode == "NG") {
                    if(dataType.toLowerCase() == "json") $.gfAjaxSetResult(data);
                    if(!$.isEmpty(ngFunc)) ngFunc(data, cbFunc);
                }
                if(!$.isEmpty(successFunc)) successFunc(data);
            }
        }).done(function(data, textStatus, jqXHR) { // 성공할 경우
            if(!$.isEmpty(doneFunc)) doneFunc(data, textStatus, jqXHR);
        }).fail(function(jqXHR, textStatus, errorThrown) { // 실패할 경우
            if(!$.isEmpty(failFunc)) failFunc(jqXHR, textStatus, errorThrown);
        }).always(function(jqXHR, textStatus, errorThrown) { // 항상 실행
            if(!$.isEmpty(_spinTarget)) {
                $.gfToggleLoading(_spinTarget, false);
            }
            if(!$.isEmpty(alwaysFunc)) alwaysFunc(jqXHR, textStatus, errorThrown);
            $.gfAjaxSetup();
        });

    } catch(err) {
        console.log("gfAjax Occured Exception :");
        console.log(err);
    }
};


/*
 * 메인 화면의 오른쪽 환경 설정 버튼
 */
$.gfSetConfigBtn = function() {
    // Append config box / Only for demo purpose
    // Uncomment on server mode to enable XHR calls
    $.get("/static/js/skin/skin-config.html", function (data) {
        if (!$('body').hasClass('no-skin-config'))
            $('body').append(data);
    });
};

/*
 * Http Error 처리
 */
$.gfHttpErrorPopup = function(opts) {

    if($.isEmpty(opts) || $.isEmpty(opts.jqXHR)) return false;

    var jqXHR = opts.jqXHR;
    var textStatus = opts.textStatus;
    var errorThrown = opts.errorThrown;
    var loginRequired = $.isEmpty(opts.loginRequired) ? false : opts.loginRequired;

    if(!$.isEmpty(jqXHR.status) && jqXHR.status != 200) {
        if(loginRequired && jqXHR.status == 401) { // Login Check 401일 경우 로그인 팝업
            $.gfCommonPopUp({
                popUrl: "/logins/loginpop",
                width: "500",
                attrs: {
                    "data-keyboard": "false"
                }
            });
        } else {
            var status = "";
            var title = "";
            var message = "";

            $.each(GD_SYS_HTTP_STATUS, function(i, item) {
                if(item.status == jqXHR.status) {
                    status = item.status;
                    title = item.title;
                    message = item.message;
                    return;
                }
            });

            $.gfAlert({
                title: title,
                text: message,
                type: "error",
            });
        }
    }
};

/*
 * Ajax 호출 후 결과 처리
 */
$.gfAjaxSetResult = function(data) {
    var resultCode = data["resultCode"];
    var resultMessage = data["resultMessage"];
    var errorItem = data["errorItem"];

    if(resultCode != 'OK') {

        var _errorItem = $.isEmpty(errorItem) ? null : $("#" + errorItem);
        var itemLabel = "";

        if(!$.isEmpty(_errorItem)) {
            itemLabel = _errorItem.attr("label");
            if(!$.isEmpty(itemLabel)) resultMessage = itemLabel + "은(는)" + resultMessage;
            _errorItem.focus();
        }

        $.gfNotiMsg({
            msgCd : "",
            msgType : "warning",
            title : "확인",
            msg : resultMessage,
            msgFrom : "S"
        });

        return false
    }

    return true
};

/*
 * 공통 알럿 처리
 * http://t4t5.github.io/sweetalert/ 참조
 */
$.gfAlert = function(opts) {

    if($.isEmpty(opts)) return false;

    var title = $.isEmpty(opts.title) ? "확인" : opts.title;
    var text = $.isEmpty(opts.text) ? "" : opts.text;

    swal({
        title: title,
        text: text,
        type: "info",
        confirmButtonColor: "#1ab394", // 확인 버튼 색
        confirmButtonText: "OK", // 확인 버튼 문구
        closeOnConfirm: true,
        imageUrl: null,
    },
    function(){
        if(!$.isEmpty(opts.cbFunc)) opts.cbFunc();
    });
}


/*
 * 공통 확인 처리
 * http://t4t5.github.io/sweetalert/ 참조
 */
$.gfComfirm = function(opts) {

    if($.isEmpty(opts)) return false;

    var title = $.isEmpty(opts.title) ? "확인" : opts.title;
    var text = $.isEmpty(opts.text) ? "처리하시겠습니까?" : opts.text;
    var confirmButtonText = $.isEmpty(opts.confirmButtonText) ? "확인" : opts.confirmButtonText;

    swal({
        title: title,
        text: text,
        type: "warning",
        showCancelButton: true,
        cancelButtonText: "취소",
        confirmButtonColor: "#1ab394", // 확인 버튼 색
        confirmButtonText: confirmButtonText, // 확인 버튼 문구
        closeOnCancel: true,
        closeOnConfirm: true,
        imageUrl: null,
    },
    function(isConfirm){
        if(!$.isEmpty(opts.cbFunc)) opts.cbFunc(isConfirm);
    });
};


/*
 *  Json 데이터를 특정 컬럼기준 배열로 획득
 */
$.gfJsonToArray = function(jsonData, colNm){

    var rtnArr = [];

    $.each(jsonData, function(i, item) {
        rtnArr.push(eval("item." + colNm));
    });

    return rtnArr;
};


/*
 * 현재 시간 및 시계 만들기
 * http://momentjs.com/docs/#/parsing/
 */
