from pyquery import PyQuery as pq
from mod.fuf import info, dbg
from schools.whu.constants import *

def grab_courses(session,
                 page_url=MY_COURSES_URL,
                 parser=None):
    dbg('pageURL=%s' % page_url)

    info('retrieving course data of url %s' % page_url)
    response = session.get(page_url)

    d = pq(response.text)
    pq_course_data = d('tr.TR_BODY[align="center"]')
    if parser:
        return parser(pq_course_data)
    else:
        return pq_course_data


def get_captcha(session):
    response = session.get(CAPTCHA_URL)

    info('retrieving captcha')
    img_data = response.content

    return img_data


