# encoding: utf-8

from const.dict_keys import *

author = u'chenzihang'
email = u'chsc4698@gmail.com'
department = u'school of computer, whu'


VERSION = u'0.0.4a'

switch = {
    'info': True,
    'dbg': True,
    'err': True,
}




PASSWORD_PROMPT = 'pwd? '
ID_PROMPT = 'id? '
GMAIL_PROMPT = 'gmail? '




# note that if you are using linux or any other modern ide which supports unicode,
# please set the following variable to 'utf-8'
CONSOLE_ENCODING = 'utf-8' if switch['dbg'] else 'gbk'

ORIGINAL_HOST = '202.114.74.199'
MAIN_PAGE_URL = r'http://%s' % ORIGINAL_HOST
CAPTCHA_URL = r'http://%s/GenImg' % ORIGINAL_HOST
LOGIN_URL = r'http://%s/servlet/Login' % ORIGINAL_HOST
VIEW_NOTICE_URL = r'http://%s/common/viewNotice.jsp' % ORIGINAL_HOST
# viewing notice will be implemented in next version
PUBLIC_COURSES_LIST_URL = r'http://%s/stu/choose_pubLesson_list.jsp?actionType=query&pageNum=%s'

LOGOUT_URL = r'http://%s/servlet/Logout' % ORIGINAL_HOST
# im getting Method Not Allowed error when logging out using this url, so logging out by this url is blocked now, don't worry, its no big deal

LOGOUT_TRAIT = u'推荐使用IE浏览器，其他浏览器可能存在不兼容情况。'
INVALID_ID_OR_PASSWORD_TRAIT = u'您输入的用户名或密码错误'
WRONG_CAPTCHA_TRAIT = u'您输入的验证码错误'

MY_COURSES_URL = r'http://%s/stu/query_stu_lesson.jsp' % ORIGINAL_HOST

THIS_CALENDAR_TIMEZONE = u'Asia/Shanghai'
THIS_CALENDAR_LOCATION = u'武汉'
SEMESTER_STARTING_DATE = (2012, 2, 12)

DEFAULT_WHUCOURSESHELPER_IDENTIFIER = u'this event was inserted automatically by WhuCoursesHelper'

DAYS_TO_NUMS = {
    MONDAY: 1,
    TUESDAY: 2,
    WEDNESDAY: 3,
    THURSDAY: 4,
    FRIDAY: 5,
    SATURDAY: 6,
    SUNDAY: 7
}

ABBR_DAYS_TO_DAYS = {
    'mon': MONDAY,
    'tue': TUESDAY,
    'wed': WEDNESDAY,
    'thu': THURSDAY,
    'fri': FRIDAY,
    'sat': SATURDAY,
    'sun': SUNDAY
}
