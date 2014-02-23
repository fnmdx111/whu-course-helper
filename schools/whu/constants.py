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


