# encoding: utf-8

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
from const.constants import *
from exceptions import InvalidIDOrPasswordError, WrongCaptchaError
from mod.fuf import eliminateRepeatingCourses, openTxt
from mod.header_holder import HeaderHolder
from mod.parsers import myCoursesParser
from mod.spiders import getCaptchaPic, grabCoursePages
from mod.serialize import deserializeMyCourses
from mod.config import *


def login(studentID, password, captcha, header,
          identification='student',
          loginURL=LOGIN_URL,
          host=ORIGINAL_HOST):
    values = {
        'who': identification,
        'id': studentID,
        'pwd': password,
        'yzm': captcha,
        'submit': '%C8%B7 %B6%A8' # wtf??
    }

    postData = urllib.urlencode(values)

    req = urllib2.Request(loginURL, postData, header, host)
    info('info', 'retrieving main page')
    response = urllib2.urlopen(req)

    studentNameAttrs = {
        'class': 'line',
        'height': '20',
        'width': '70%'
    }
    dateAttrs = {
        'height': '30',
        'colspan': '6',
        'align': 'center',
        'valign': 'middle'
    }
    semesterAttrs = {
        'height': '20',
        'colspan': '3',
        'class': 'line',
        'width': '90%'
    }
    wrongParamAttrs = {
        'height': '25',
        'width': '401'
    }
    def _parseElement(soup, name, attrs):
        element = soup.find(name, attrs)

        if element:
            return element.contents[0].lstrip().rstrip()

    soup = BeautifulSoup(response.read())

    msg = _parseElement(soup, 'td', wrongParamAttrs)
    if msg:
        if WRONG_CAPTCHA_TRAIT in msg:
            raise WrongCaptchaError
        elif INVALID_ID_OR_PASSWORD_TRAIT in msg:
            raise InvalidIDOrPasswordError

    return _parseElement(soup, 'td', studentNameAttrs),\
           _parseElement(soup, 'td', dateAttrs),\
           _parseElement(soup.find(name='td', attrs=semesterAttrs), 'b', {})


def loadCoursesFromWeb(studentID, password):
    header = HeaderHolder(studentID)

    captcha = getCaptchaPic(header)

    with open('captcha.jpg', 'wb') as f:
        f.write(captcha)
        info('info', 'captcha saved at %s' % f.name)
        # captcha recognition will be implemented in future versions

    captchaContent = raw_input('captcha? ')

    studentName, date, semester = login(studentID, password, captchaContent, header)
    if studentName:
        info('info', ('welcome, ' + u'%s %s %s' % (studentName, date, semester)).encode(ConsoleEncoding))
    else:
        info('info', 'strange, nothing was transmitted, perhaps wrong password or captcha?')

    return studentName, grabCoursePages(header, MY_COURSES_URL, parser=myCoursesParser)


def readCourses(studentID, password,
                path=configs[CONFIG_KEY_SERIALIZED_COURSES_PATH],
                LoadCoursesFromWeb=configs[CONFIG_KEY_LOAD_COURSES_FROM_WEB],
                LoadCoursesFromFile=configs[CONFIG_KEY_LOAD_COURSES_FROM_FILE]):
    courses = []
    studentName = studentID
    if LoadCoursesFromWeb:
        studentName, coursesFromWeb = loadCoursesFromWeb(studentID, password)
        courses += coursesFromWeb
    if LoadCoursesFromFile:
        try:
            courses += deserializeMyCourses(openTxt(path))
            courses = eliminateRepeatingCourses(courses)
        except IOError as err:
            if err.errno == 2:
                info('err', '%s not found, skipping loading courses from file' % configs[CONFIG_KEY_SERIALIZED_COURSES_PATH])
                if configs[CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_EXIT]:
                    exit(0)

    for item in courses:
        info('verbose', item.__unicode__().encode(ConsoleEncoding))

    return studentName, courses


def logout(header,
           logoutURL=LOGOUT_URL,
           host=ORIGINAL_HOST):
    req = urllib2.Request(logoutURL, {}, header, host)
    info('info', 'logging out')
    response = urllib2.urlopen(req)

    if LOGOUT_TRAIT in response.read():
        info('info', 'logout succeeded')

