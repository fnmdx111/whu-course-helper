# encoding: utf-8

from const.dict_keys import *

author = u'chenzihang'
email = u'chsc4698@gmail.com'
department = u'school of computer, whu'


VERSION = u'0.0.8'

switch = {
    'info': True,
    'dbg': True,
    'err': True,
    'verbose': True
}


def info(channel, msg):
    if switch[channel]:
        print '%s: %s' % (channel, msg)


PASSWORD_PROMPT = 'pwd? '
ID_PROMPT = 'id? '
GMAIL_PROMPT = 'gmail? '

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
