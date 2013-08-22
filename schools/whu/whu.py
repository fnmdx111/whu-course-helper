# encoding: utf-8

from pyquery import PyQuery as pq
import requests
from mod.exceptions import InvalidIDOrPasswordError, WrongCaptchaError
from mod.fuf import info, verbose
from schools.whu.constants import *
from schools.whu.parsers import my_course_parser
from schools.whu.spiders import get_captcha, grab_courses


def login(session,
          student_id, password, captcha, identification='student'):

    response = session.post(LOGIN_URL,
                            data={'who': identification,
                                  'id': student_id,
                                  'pwd': password,
                                  'yzm': captcha,
                                  'submit': '%C8%B7 %B6%A8'})
    info('retrieving main page')

    d = pq(response.text)

    msg = d('td[height="25"][width="401"]').text()
    if msg:
        if WRONG_CAPTCHA_TRAIT in msg:
            raise WrongCaptchaError
        elif INVALID_ID_OR_PASSWORD_TRAIT in msg:
            raise InvalidIDOrPasswordError

    selectors = ('td.line[height="20"][width="70%"]',
                 'td[height="30"][colspan="6"][align="center"]',
                 'td.line[height="20"][colspan="3"]')
    return map(lambda selector: d(selector).text(),
               selectors)


def load_courses(student_id, password):
    session = requests.Session()

    captcha = get_captcha(session)

    with open('.\captcha.jpg', 'wb') as f:
        f.write(captcha)
        info('captcha saved at %s' % f.name)
        # captcha recognition will be implemented in future versions

    captcha = raw_input('captcha? ')

    student_name, date, semester = login(session,
                                         student_id, password, captcha)
    if student_name:
        info('welcome %s %s %s' % (student_name, date, semester))
    else:
        info('strange, nothing was transmitted,'
             'perhaps wrong password or captcha?')

    return student_name, grab_courses(session,
                                      parser=my_course_parser)


def read_courses(studentID, password):
    student_name, courses = load_courses(studentID, password)

    for item in courses:
        verbose(item)

    return student_name, courses


def logout(session):
    response = session.post(LOGOUT_URL)
    info('logging out')

    if LOGOUT_TRAIT in response.text:
        info('logout succeeded')

