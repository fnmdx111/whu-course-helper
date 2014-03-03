# encoding: utf-8
from const.dict_keys import *

ORIGINAL_HOST = '202.114.74.198'
MAIN_PAGE_URL = r'http://%s' % ORIGINAL_HOST
CAPTCHA_URL = r'http://%s/GenImg' % ORIGINAL_HOST
LOGIN_URL = r'http://%s/servlet/Login' % ORIGINAL_HOST
LOGOUT_URL = r'http://%s/servlet/Logout' % ORIGINAL_HOST

LOGOUT_TRAIT = u'推荐使用IE浏览器，其他浏览器可能存在不兼容情况。'
INVALID_ID_OR_PASSWORD_TRAIT = u'您输入的用户名或密码错误'
WRONG_CAPTCHA_TRAIT = u'您输入的验证码错误'

MY_COURSES_URL = r'http://%s/stu/query_stu_lesson.jsp' % ORIGINAL_HOST

THIS_CALENDAR_TIMEZONE = u'Asia/Shanghai'
THIS_CALENDAR_LOCATION = u'武汉'
SEMESTER_STARTING_DATE = (2014, 2, 16)
# usually a sunday

WEAK_NUMBER = ['', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十',
               u'十一', u'十二', u'十三', u'十四', u'十五', u'十六', u'十七', u'十八', u'十九', u'二十']
STRONG_NUMBER = ['', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖', u'拾',
                 u'拾壹', u'拾贰', u'拾叁', u'拾肆', u'拾伍', u'拾陆', u'拾柒', u'拾捌', u'拾玖', u'贰拾']
GENERAL_NUMBER = range(0, 21)

WEEK_NUMBER = WEAK_NUMBER

