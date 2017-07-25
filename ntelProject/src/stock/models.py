from django.db import models

# Create your models here.
class StockProdPhone(models.Model):
    '''
    핸드폰 제품 재고 정보
    '''
    prodId = models.CharField(primary_key=True, db_column='prod_id', max_length=14, verbose_name='상품ID')
    serialNo = models.CharField(db_column='user_id', max_length=30, null=False,blank=False, verbose_name='상품Serial번호')
    
    modelNm = models.CharField(db_column='model_nm', max_length=20, default=None, verbose_name='모델명')
    prodInfo = models.CharField(db_column='prod_info', max_length=20, default=None, verbose_name='제품정보')
    prodColor = models.CharField(db_column='prod_color', max_length=20, default=None, verbose_name='제품색상')
    inDt = models.DateTimeField(db_column='in_dt', auto_now_add=True, null=True, blank=True, verbose_name='입고일자')
    inPrice = models.IntegerField(db_column='in_price', null=False, default=0, verbose_name='입고가')

    shopId = models.ForeignKey('system.SysShop', db_column='shop_id', blank=True, null=False, default=None, related_name='r_stock_prod_phone_shop_id', verbose_name='매장ID')
    inStaffId = models.ForeignKey('system.SysUser', db_column='in_staff_id', blank=True, null=False, default=None, related_name='r_stock_prod_phone_in_staff_id', verbose_name='입고직원ID')

    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, verbose_name='등록자ID', related_name='r_stock_prod_phone_reg_id')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=False, verbose_name='수정자ID', related_name='r_stock_prod_phone_mod_id')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "stock_prod_phone"
        
    def __str__(self):
        return self.prodId    
