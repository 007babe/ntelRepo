# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#def ComCd(request, tab=None):
# Create your views here.
def index(request):
#    return HttpResponse("앗싸... 첫페이지 index")
    return render(request, 'main/main.html', {})

'''
공통코드 데이터 획득
'''
@csrf_exempt
def comCd(request):
    # DB에서 데이터 가져오기
    comCdData = [
            { 'grpCd' : 'G0001', 'comCd' : 'P', 'comNm' : '휴대폰', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'P', 'text' : '휴대폰', 'grpOpt' : 'asdafsdasf' },
            { 'grpCd' : 'G0001', 'comCd' : 'T', 'comNm' : '태블릿', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'T', 'text' : '태블릿', 'grpOpt' : '' },
            { 'grpCd' : 'G0001', 'comCd' : 'W', 'comNm' : '웨어러블', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'W', 'text' : '웨어러블', 'grpOpt' : '' },
            { 'grpCd' : 'G0001', 'comCd' : 'U', 'comNm' : '유심', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : 'U', 'text' : '유심', 'grpOpt' : '' },
            { 'grpCd' : 'G0001', 'comCd' : 'N', 'comNm' : '유선/카드', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : 'N', 'text' : '유선/카드', 'grpOpt' : '' },
            { 'grpCd' : 'G0002', 'comCd' : 'SKT', 'comNm' : 'SKT', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'SKT', 'text' : 'SKT', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0002', 'comCd' : 'KT', 'comNm' : 'KT', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'KT', 'text' : 'KT', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0002', 'comCd' : 'LGT', 'comNm' : 'LGT', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'LGT', 'text' : 'LGT', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0002', 'comCd' : 'sSK', 'comNm' : 'SK-세븐모바일', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : 'sSK', 'text' : 'SK-세븐모바일', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0002', 'comCd' : 'hKT', 'comNm' : 'KT-헬로우모바일', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : 'hKT', 'text' : 'KT-헬로우모바일', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0002', 'comCd' : 'hSK', 'comNm' : 'SK-헬로우모바일', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : 'hSK', 'text' : 'SK-헬로우모바일', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0002', 'comCd' : 'mKT', 'comNm' : 'KT-M모바일', 'useYn' : 'Y', 'ordSeq' : '7', 'value' : 'mKT', 'text' : 'KT-M모바일', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0002', 'comCd' : 'uLG', 'comNm' : 'LG-Umobi', 'useYn' : 'Y', 'ordSeq' : '8', 'value' : 'uLG', 'text' : 'LG-Umobi', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0002', 'comCd' : 'oSK', 'comNm' : 'SK-에스원안심모바일', 'useYn' : 'Y', 'ordSeq' : '9', 'value' : 'oSK', 'text' : 'SK-에스원안심모바일', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0003', 'comCd' : 'S', 'comNm' : 'SKT', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'S', 'text' : 'SKT', 'grpOpt' : '' },
            { 'grpCd' : 'G0003', 'comCd' : 'K', 'comNm' : 'KT', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'K', 'text' : 'KT', 'grpOpt' : '' },
            { 'grpCd' : 'G0003', 'comCd' : 'L', 'comNm' : 'LGT', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'L', 'text' : 'LGT', 'grpOpt' : '' },
            { 'grpCd' : 'G0004', 'comCd' : 'B', 'comNm' : '선결제', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'B', 'text' : '선결제', 'grpOpt' : '' },
            { 'grpCd' : 'G0004', 'comCd' : 'A', 'comNm' : '후결제', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'A', 'text' : '후결제', 'grpOpt' : '' },
            { 'grpCd' : 'G0005', 'comCd' : 'N', 'comNm' : '미구매', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'N', 'text' : '미구매', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0005', 'comCd' : 'A', 'comNm' : '후납', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : 'A', 'text' : '후납', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0005', 'comCd' : 'C', 'comNm' : '완납', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'C', 'text' : '완납', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0005', 'comCd' : 'B', 'comNm' : '대납', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'B', 'text' : '대납', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0006', 'comCd' : '1', 'comNm' : '신규', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '1', 'text' : '신규', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0006', 'comCd' : '2', 'comNm' : 'MNP', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '2', 'text' : 'MNP', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0006', 'comCd' : '3', 'comNm' : '기변/보상', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '3', 'text' : '기변/보상', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0006', 'comCd' : '4', 'comNm' : '에이징', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '4', 'text' : '에이징', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0006', 'comCd' : '5', 'comNm' : '가개통', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '5', 'text' : '가개통', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0006', 'comCd' : '6', 'comNm' : '선불', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : '6', 'text' : '선불', 'grpOpt' : 'AB' },
            { 'grpCd' : 'G0007', 'comCd' : '10', 'comNm' : '할부(개통)', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '10', 'text' : '할부(개통)', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0007', 'comCd' : '20', 'comNm' : '현금(개통)', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '20', 'text' : '현금(개통)', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0008', 'comCd' : '24', 'comNm' : '24개월', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '24', 'text' : '24개월', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0008', 'comCd' : '12', 'comNm' : '12개월', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '12', 'text' : '12개월', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0008', 'comCd' : '30', 'comNm' : '30개월', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '30', 'text' : '30개월', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0008', 'comCd' : '00', 'comNm' : '무약정', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '00', 'text' : '무약정', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0009', 'comCd' : '00', 'comNm' : '해당없음', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '00', 'text' : '해당없음', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0009', 'comCd' : '24', 'comNm' : '24개월', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '24', 'text' : '24개월', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0009', 'comCd' : '30', 'comNm' : '30개월', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '30', 'text' : '30개월', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0009', 'comCd' : '36', 'comNm' : '36개월', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '36', 'text' : '36개월', 'grpOpt' : 'B' },
            { 'grpCd' : 'G0010', 'comCd' : '01', 'comNm' : '필수서비스', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '01', 'text' : '필수서비스', 'grpOpt' : '' },
            { 'grpCd' : 'G0010', 'comCd' : '02', 'comNm' : '환수서비스', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '02', 'text' : '환수서비스', 'grpOpt' : '' },
            { 'grpCd' : 'G0011', 'comCd' : '00', 'comNm' : '없음', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '00', 'text' : '없음', 'grpOpt' : '' },
            { 'grpCd' : 'G0011', 'comCd' : '10', 'comNm' : '미반납', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '10', 'text' : '미반납', 'grpOpt' : '' },
            { 'grpCd' : 'G0011', 'comCd' : '20', 'comNm' : '회수', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '20', 'text' : '회수', 'grpOpt' : '' },
            { 'grpCd' : 'G0011', 'comCd' : '30', 'comNm' : '미회수', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '30', 'text' : '미회수', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '01', 'comNm' : '주민등록증', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '01', 'text' : '주민등록증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '02', 'comNm' : '법대신분증', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '02', 'text' : '법대신분증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '03', 'comNm' : '계좌신분증', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '03', 'text' : '계좌신분증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '04', 'comNm' : '등본', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '04', 'text' : '등본', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '05', 'comNm' : '가족관계증명서', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '05', 'text' : '가족관계증명서', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '06', 'comNm' : '장애인등록증', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : '06', 'text' : '장애인등록증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '07', 'comNm' : '위임장', 'useYn' : 'Y', 'ordSeq' : '7', 'value' : '07', 'text' : '위임장', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '08', 'comNm' : '위임자신분증', 'useYn' : 'Y', 'ordSeq' : '8', 'value' : '08', 'text' : '위임자신분증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '09', 'comNm' : '사업자등록증', 'useYn' : 'Y', 'ordSeq' : '9', 'value' : '09', 'text' : '사업자등록증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '10', 'comNm' : '대표신분증', 'useYn' : 'Y', 'ordSeq' : '10', 'value' : '10', 'text' : '대표신분증', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '11', 'comNm' : '인감증명서', 'useYn' : 'Y', 'ordSeq' : '11', 'value' : '11', 'text' : '인감증명서', 'grpOpt' : '' },
            { 'grpCd' : 'G0012', 'comCd' : '12', 'comNm' : '통장사본', 'useYn' : 'Y', 'ordSeq' : '12', 'value' : '12', 'text' : '통장사본', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '01', 'comNm' : '인터넷', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '01', 'text' : '인터넷', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '02', 'comNm' : 'TV', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '02', 'text' : 'TV', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '03', 'comNm' : '집전화', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '03', 'text' : '집전화', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '04', 'comNm' : '인터넷전화', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '04', 'text' : '인터넷전화', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '05', 'comNm' : '와이파이', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '05', 'text' : '와이파이', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '06', 'comNm' : '신용카드', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : '06', 'text' : '신용카드', 'grpOpt' : '' },
            { 'grpCd' : 'G0013', 'comCd' : '99', 'comNm' : '기타', 'useYn' : 'Y', 'ordSeq' : '7', 'value' : '99', 'text' : '기타', 'grpOpt' : '' },
            { 'grpCd' : 'G0014', 'comCd' : '00', 'comNm' : '없음', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '00', 'text' : '없음', 'grpOpt' : '' },
            { 'grpCd' : 'G0014', 'comCd' : '01', 'comNm' : '장애인', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '01', 'text' : '장애인', 'grpOpt' : '' },
            { 'grpCd' : 'G0014', 'comCd' : '02', 'comNm' : '국가유공자', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '02', 'text' : '국가유공자', 'grpOpt' : '' },
            { 'grpCd' : 'G0014', 'comCd' : '03', 'comNm' : '차상위계층', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '03', 'text' : '차상위계층', 'grpOpt' : '' },
            { 'grpCd' : 'G0014', 'comCd' : '04', 'comNm' : '기초생활수급자', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '04', 'text' : '기초생활수급자', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '01', 'comNm' : '미비서류', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '01', 'text' : '미비서류', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '02', 'comNm' : '할인예정일', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '02', 'text' : '할인예정일', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '03', 'comNm' : '에이징해지', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '03', 'text' : '에이징해지', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '04', 'comNm' : '회수단말기', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '04', 'text' : '회수단말기', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '05', 'comNm' : '미수금', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '05', 'text' : '미수금', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '06', 'comNm' : '요금제유지', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : '06', 'text' : '요금제유지', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '07', 'comNm' : '필수S유지', 'useYn' : 'Y', 'ordSeq' : '7', 'value' : '07', 'text' : '필수S유지', 'grpOpt' : '' },
            { 'grpCd' : 'G0015', 'comCd' : '08', 'comNm' : '일반업무', 'useYn' : 'Y', 'ordSeq' : '8', 'value' : '08', 'text' : '일반업무', 'grpOpt' : '' },
            { 'grpCd' : 'G0016', 'comCd' : '00', 'comNm' : '접수대기', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '00', 'text' : '접수대기', 'grpOpt' : '' },
            { 'grpCd' : 'G0016', 'comCd' : '01', 'comNm' : '해결완료', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '01', 'text' : '해결완료', 'grpOpt' : '' },
            { 'grpCd' : 'G0016', 'comCd' : '99', 'comNm' : '취소', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '99', 'text' : '취소', 'grpOpt' : '' },
            { 'grpCd' : 'G0017', 'comCd' : '01', 'comNm' : '보유', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '01', 'text' : '보유', 'grpOpt' : '' },
            { 'grpCd' : 'G0017', 'comCd' : '02', 'comNm' : '개통', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '02', 'text' : '개통', 'grpOpt' : '' },
            { 'grpCd' : 'G0017', 'comCd' : '03', 'comNm' : '반품', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '03', 'text' : '반품', 'grpOpt' : '' },
            { 'grpCd' : 'G0017', 'comCd' : '04', 'comNm' : '공판', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '04', 'text' : '공판', 'grpOpt' : '' },
            { 'grpCd' : 'G0018', 'comCd' : '01', 'comNm' : '완납', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '01', 'text' : '완납', 'grpOpt' : '' },
            { 'grpCd' : 'G0018', 'comCd' : '02', 'comNm' : '완납/요금', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '02', 'text' : '완납/요금', 'grpOpt' : '' },
            { 'grpCd' : 'G0018', 'comCd' : '03', 'comNm' : '분납', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '03', 'text' : '분납', 'grpOpt' : '' },
            { 'grpCd' : 'G0018', 'comCd' : '00', 'comNm' : '면제', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '00', 'text' : '면제', 'grpOpt' : '' },
            { 'grpCd' : 'G0018', 'comCd' : '11', 'comNm' : '대납', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '11', 'text' : '대납', 'grpOpt' : '' },
            { 'grpCd' : 'G0018', 'comCd' : '12', 'comNm' : '대납/요금', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : '12', 'text' : '대납/요금', 'grpOpt' : '' },
            { 'grpCd' : 'G0019', 'comCd' : '010', 'comNm' : '010', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '010', 'text' : '010', 'grpOpt' : 'A' },
            { 'grpCd' : 'G0019', 'comCd' : '011', 'comNm' : '011', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '011', 'text' : '011', 'grpOpt' : '' },
            { 'grpCd' : 'G0019', 'comCd' : '016', 'comNm' : '016', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '016', 'text' : '016', 'grpOpt' : '' },
            { 'grpCd' : 'G0019', 'comCd' : '017', 'comNm' : '017', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '017', 'text' : '017', 'grpOpt' : '' },
            { 'grpCd' : 'G0019', 'comCd' : '018', 'comNm' : '018', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : '018', 'text' : '018', 'grpOpt' : '' },
            { 'grpCd' : 'G0019', 'comCd' : '019', 'comNm' : '019', 'useYn' : 'Y', 'ordSeq' : '6', 'value' : '019', 'text' : '019', 'grpOpt' : '' },
            { 'grpCd' : 'G0020', 'comCd' : '10', 'comNm' : '단말기', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '10', 'text' : '단말기', 'grpOpt' : '' },
            { 'grpCd' : 'G0020', 'comCd' : '20', 'comNm' : '유심/중고', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '20', 'text' : '유심/중고', 'grpOpt' : '' },
            { 'grpCd' : 'G0020', 'comCd' : '30', 'comNm' : '홈/인터넷', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '30', 'text' : '홈/인터넷', 'grpOpt' : '' },
            { 'grpCd' : 'G0021', 'comCd' : 'A', 'comNm' : '필수부가서비스', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'A', 'text' : '필수부가서비스', 'grpOpt' : '' },
            { 'grpCd' : 'G0021', 'comCd' : 'B', 'comNm' : '환수서비스', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'B', 'text' : '환수서비스', 'grpOpt' : '' },
            { 'grpCd' : 'G0022', 'comCd' : '36', 'comNm' : '36개월', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '36', 'text' : '36개월', 'grpOpt' : '' },
            { 'grpCd' : 'G0022', 'comCd' : '24', 'comNm' : '24개월', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '24', 'text' : '24개월', 'grpOpt' : '' },
            { 'grpCd' : 'G0022', 'comCd' : '12', 'comNm' : '12개월', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : '12', 'text' : '12개월', 'grpOpt' : '' },
            { 'grpCd' : 'G0022', 'comCd' : '00', 'comNm' : '무약정', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : '00', 'text' : '무약정', 'grpOpt' : '' },
            { 'grpCd' : 'G0023', 'comCd' : '10', 'comNm' : '신청일', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : '10', 'text' : '신청일', 'grpOpt' : '' },
            { 'grpCd' : 'G0023', 'comCd' : '20', 'comNm' : '개통일', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : '20', 'text' : '개통일', 'grpOpt' : '' },
            { 'grpCd' : 'G0024', 'comCd' : 'I', 'comNm' : '인터넷', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'I', 'text' : '인터넷', 'grpOpt' : '' },
            { 'grpCd' : 'G0024', 'comCd' : 'T', 'comNm' : 'TV', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'T', 'text' : 'TV', 'grpOpt' : '' },
            { 'grpCd' : 'G0024', 'comCd' : 'P', 'comNm' : '인터넷전화', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'P', 'text' : '인터넷전화', 'grpOpt' : '' },
            { 'grpCd' : 'S0001', 'comCd' : 'C', 'comNm' : '대표', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'C', 'text' : '대표', 'grpOpt' : '' },
            { 'grpCd' : 'S0001', 'comCd' : 'A', 'comNm' : '총괄', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'A', 'text' : '총괄', 'grpOpt' : '' },
            { 'grpCd' : 'S0001', 'comCd' : 'T', 'comNm' : '팀장', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'T', 'text' : '팀장', 'grpOpt' : '' },
            { 'grpCd' : 'S0001', 'comCd' : 'S', 'comNm' : '사원', 'useYn' : 'Y', 'ordSeq' : '4', 'value' : 'S', 'text' : '사원', 'grpOpt' : '' },
            { 'grpCd' : 'S0001', 'comCd' : 'I', 'comNm' : '인턴', 'useYn' : 'Y', 'ordSeq' : '5', 'value' : 'I', 'text' : '인턴', 'grpOpt' : '' },
            { 'grpCd' : 'S0002', 'comCd' : 'P', 'comNm' : 'PC만', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'P', 'text' : 'PC만', 'grpOpt' : '' },
            { 'grpCd' : 'S0002', 'comCd' : 'M', 'comNm' : 'Mobile만', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'M', 'text' : 'Mobile만', 'grpOpt' : '' },
            { 'grpCd' : 'S0002', 'comCd' : 'A', 'comNm' : '전체', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'A', 'text' : '전체', 'grpOpt' : '' },
            { 'grpCd' : 'S0003', 'comCd' : 'C', 'comNm' : '신용카드', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'C', 'text' : '신용카드', 'grpOpt' : '' },
            { 'grpCd' : 'S0003', 'comCd' : 'A', 'comNm' : '무톧장', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'A', 'text' : '무톧장', 'grpOpt' : '' },
            { 'grpCd' : 'S0004', 'comCd' : 'D', 'comNm' : '대리점', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'D', 'text' : '대리점', 'grpOpt' : '' },
            { 'grpCd' : 'S0004', 'comCd' : 'S', 'comNm' : '판매점', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'S', 'text' : '판매점', 'grpOpt' : '' },
            { 'grpCd' : 'S0005', 'comCd' : 'PC', 'comNm' : 'PC', 'useYn' : 'Y', 'ordSeq' : '1', 'value' : 'PC', 'text' : 'PC', 'grpOpt' : '' },
            { 'grpCd' : 'S0005', 'comCd' : 'MO', 'comNm' : '모바일', 'useYn' : 'Y', 'ordSeq' : '2', 'value' : 'MO', 'text' : '모바일', 'grpOpt' : '' },
            { 'grpCd' : 'S0005', 'comCd' : 'ETC', 'comNm' : '기타', 'useYn' : 'Y', 'ordSeq' : '3', 'value' : 'ETC', 'text' : '기타', 'grpOpt' : '' }
    ]
    
    
#    jsonString = json.dumps(comCdData, indent=4, ensure_ascii=False)
#    jsonString = json.dumps(comCdData, indent=4, ensure_ascii=False)
#    print(jsonString)
    
    return HttpResponse(json.dumps(comCdData, indent=4, ensure_ascii=False), content_type="application/json")    
#    return HttpResponse("앗싸... comCd")

    
