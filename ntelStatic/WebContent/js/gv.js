/*
 *
 *   ntel - Global Variables Javascript
 *   version 1.0
 *
 */
 
// System Global Data Info 
var gSysGDs =  [
    { key : "GD_COMCD", url : "json/comCdInfo.json", useYn : true, desc : "공통코드용(TB_COM_CD)" },
    { key : "GD_STAFF", url : "json/staffInfo.json", useYn : true, desc : "직원 데이터" },
    { key : "GD_AGENT", url : "json/agentInfo.json", useYn : true, desc : "대리/딜러점 데이터" },
    { key : "GD_PROD_PHONE", url : "json/productPhoneInfo.json", useYn : true, desc : "입고 단말기" },
    { key : "GD_PROD_PHONE_USED", url : "json/productPhoneUsedInfo.json", useYn : true, desc : "입고 단말기(중고)" },
    { key : "GD_PROD_USIM", url : "json/productUsimInfo.json", useYn : true, desc : "입고 유심" },
    { key : "GD_PROD_CC", url : "json/productCc.json", useYn : true, desc : "결합상품 데이터" },
    { key : "GD_PROD_HI", url : "json/productHi.json", useYn : true, desc : "홈/인터넷 상품 데이터" },
    { key : "GD_TELECOM_CALL_PLAN", url : "json/telecomCallPlanInfo.json", useYn : true, desc : "요금제 데이터" },
    { key : "GD_SPT_AMT", url : "json/sptAmtInfo.json", useYn : true, desc : "공시지원금 데이터" },
    { key : "GD_SRVC", url : "json/srvcInfo.json", useYn : true, desc : "필수부가/환수서비스 데이터" },
    { key : "GD_SYS_MSG", url : "json/sysMsg.json", useYn : true, desc : "시스템메세지 데이터" }
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

