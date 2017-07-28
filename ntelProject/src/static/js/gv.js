/*
 *
 *   ntel - Global Variables Javascript
 *   version 1.0
 *
 */
 
// System Global Data Info 
var gSysGDs =  [
    { key : "GD_COM_CD", url : "/common/json/comcd", cbFunc : "", useYn : true, desc : "공통코드" },
    { key : "GD_SYS_MENU", url : "/system/json/sysmenu", cbFunc : "$.gfSetSysMenu();", useYn : true, desc : "사용자메뉴" },
    { key : "GD_SYS_MSG", url : "/system/json/sysmsg", cbFunc : "", useYn : true, desc : "시스템메세지 데이터" },

    { key : "GD_STAFF", url : "/static/json/staffInfo.json", cbFunc : "", useYn : true, desc : "직원 데이터" },
    { key : "GD_AGENT", url : "/static/json/agentInfo.json", cbFunc : "", useYn : true, desc : "대리/딜러점 데이터" },
    { key : "GD_PROD_PHONE", url : "/static/json/productPhoneInfo.json", cbFunc : "", useYn : true, desc : "입고 단말기" },
    { key : "GD_PROD_PHONE_USED", url : "/static/json/productPhoneUsedInfo.json", cbFunc : "", useYn : true, desc : "입고 단말기(중고)" },
    { key : "GD_PROD_USIM", url : "/static/json/productUsimInfo.json", cbFunc : "", useYn : true, desc : "입고 유심" },
    { key : "GD_PROD_CC", url : "/static/json/productCc.json", cbFunc : "", useYn : true, desc : "결합상품 데이터" },
    { key : "GD_PROD_HI", url : "/static/json/productHi.json", cbFunc : "", useYn : true, desc : "홈/인터넷 상품 데이터" },
    { key : "GD_TELECOM_CALL_PLAN", url : "/static/json/telecomCallPlanInfo.json", cbFunc : "", useYn : true, desc : "요금제 데이터" },
    { key : "GD_SPT_AMT", url : "/static/json/sptAmtInfo.json", cbFunc : "", useYn : true, desc : "공시지원금 데이터" },
    { key : "GD_SRVC", url : "/static/json/srvcInfo.json", cbFunc : "", useYn : true, desc : "필수부가/환수서비스 데이터" },
];

// 현재 일자용
var gCurrentDateTime = new Date();         

// 전화번호 지역번호
var gArrFirstTelNo = [
 "010" ,"011" ,"016" ,"017" ,"018" ,"019"
,"02"
,"031" ,"032" ,"033" ,"041" ,"042" ,"043" ,"044"
,"051" ,"052" ,"053" ,"054" ,"055"
,"061" ,"062" ,"063" ,"064" 
,"0502" ,"0505" ,"0506"
,"0130" ,"0303"
,"080" ,"070", "060"
];

