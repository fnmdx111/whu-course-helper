
import urllib2
import cookielib
from mod.fuf import info
from schools.whu.constants import *

class HeaderHolder(dict):

    def __init__(self, studentID,
                 mainPageURL=MAIN_PAGE_URL):
        dict.__init__(self
)
        self.studentID = studentID
        self.refreshCookie(studentID, mainPageURL)

    @staticmethod
    def _getCookie(url):
        jar = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        info('info', 'retrieving cookie for this session')
        opener.open(url)

        import re

        pattern = re.compile(r'.+Cookie (.+) for .+')
        matches = pattern.search(jar.__str__())

        if matches:
            return matches.group(1)
        else:
            return None

    def refreshCookie(self, studentID,
                      mainPageURL=MAIN_PAGE_URL):
        self['Cookie'] = 'studentid=%s; %s' % (studentID, HeaderHolder._getCookie(mainPageURL))

        return self

