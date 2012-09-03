# encoding: utf-8
from const.dict_keys import *

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
SEMESTER_STARTING_DATE = (2012, 9, 2)


SCHEDULE_PATTERN = u'{0}-{1}周,每{2}周;{3}-{4}节,{5}区,{6}'
SCHEDULE_EXAMPLE = u'周一 1-15周,每1周;3-5节,3区,附1-302 => mon 1 15 1 3 5 3 附1-302'

NECESSARY_FIELDS = (
    COURSE_NAME,
    TEACHER_NAME,
)
OPTIONAL_FIELDS = (
    SCORE_TYPE,
    COURSE_TYPE,
    MAJOR,
    CREDIT,
    PERIOD,
    REMARKS
)