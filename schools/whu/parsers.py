# encoding: utf-8
import re
from const.dict_keys import *
from mod.course_related import CourseSchedule, MyCourse

from pyquery import PyQuery as pq


def my_course_parser(pq_course_data):
    courses = []

    def process_td(idx, elem):
        return MyCourse.KEYS[idx], pq(elem).text()

    for elem in pq_course_data:
        properties = {key: val if val else ''
                      for key, val in pq(elem).find('td').map(process_td)}
        course = MyCourse(properties)

        for key in MyCourse.KEYS[13:20]:
            val = course.property(key)
            if val:
                course.set_property(key, ''.join(val.split('\n\r')))
                course.append(schedule_parser(CourseSchedule(),
                                              key, val))
            else:
                del course.properties()[key]

        courses.append(course)

    return courses


def gen_location_by_schedule(schedule):
    location = schedule[BUILDING]
    if schedule[BUILDING] != schedule[CLASSROOM]:
        location += '-%s' % schedule[CLASSROOM]

    return location


KEYS_FOR_RE = CourseSchedule.KEYS[1:len(CourseSchedule.KEYS) - 1]
PATTERN = re.compile(ur'^.*'
                     ur'(?P<%s>\d{1,2})\D+(?P<%s>\d{1,2})周'
                     ur'\s*,\s*'
                     ur'每(?P<%s>\d+)周'
                     ur'\s*;\s*'
                     ur'(?P<%s>\d{1,2})\D+(?P<%s>\d{1,2})节'
                     ur'(?:\s*,s*)?'
                     ur'(?:(?P<%s>\d+)区)?'
                     ur'(?:\s*,\s*)?'
                     ur'(?:(?P<%s>.+))?$' % KEYS_FOR_RE)
pattern1 = re.compile(ur'^(\d+)$')
pattern2 = re.compile(ur'^([^\-]+)\s*\-\s*([A-Za-z0-9]+)$')
pattern3 = re.compile(ur'^(.+?)(\d+)$')
def schedule_parser(self, day, raw):
    matches = PATTERN.search(raw)

    self[DAY] = day

    if matches:
        for key in KEYS_FOR_RE:
            self[key] = matches.groupdict()[key]

        if not self[CLASSROOM]:
            self[BUILDING] = None
            return self

        matches1 = pattern1.search(matches.groupdict().get(CLASSROOM, ''))
        matches2 = pattern2.search(matches.groupdict()[CLASSROOM]) or pattern3.search(matches.groupdict()[CLASSROOM])
        if matches1:
            self[BUILDING] = self[CLASSROOM]
        elif matches2:
            self[BUILDING] = matches2.group(1)
            self[CLASSROOM] = matches2.group(2)

    return self


if __name__ == '__main__':
    match = PATTERN.search(u'6-18周,每1周; 3-4节')
    if match:
        print match.groups()


