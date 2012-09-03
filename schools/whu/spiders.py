from BeautifulSoup import BeautifulSoup
import urllib2
from mod.fuf import info
from schools.whu.constants import *
from schools.whu.parsers import publicCoursesParser

def grabCoursePages(header, pageURL,
                    parser=None,
                    host=ORIGINAL_HOST):
    info('dbg', 'pageURL=%s' % pageURL)

    req = urllib2.Request(pageURL, None, header, host)
    info('info', 'retrieving course data of url %s' % pageURL)
    response = urllib2.urlopen(req)

    soup = BeautifulSoup(response.read())
    rawCourseData = soup.findAll(
        name='tr',
        attrs={
            'align': 'center',
            'class': 'TR_BODY'
        }
    )
    if parser:
        return parser(rawCourseData)
    else:
        return rawCourseData


def getCaptchaPic(header,
                  captchaURL=CAPTCHA_URL,
                  host=ORIGINAL_HOST):

    req = urllib2.Request(
        url=captchaURL,
        headers=header,
        origin_req_host=host)

    info('info', 'retrieving captcha')
    imgdata = urllib2.urlopen(req)

    return imgdata.read()


def grabAllPublicCoursePages(header):
    allPublicCourses = []
    for i in range(1,11):
        info('info', 'retrieving course data of page %s' % i)
        data = grabCoursePages(header, PUBLIC_COURSES_LIST_URL % (ORIGINAL_HOST, i), publicCoursesParser)
        for item in data:
            info('verbose', item)
            allPublicCourses.append(item)
    info('info', 'grabbing completed, %s courses caught' % len(allPublicCourses))

    return allPublicCourses
