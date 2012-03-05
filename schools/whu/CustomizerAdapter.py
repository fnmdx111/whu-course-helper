from mod import customize_course
from mod.serialize import createCustomCourse
from schools.whu import parsers, whu
from schools.whu.constants import NECESSARY_FIELDS, OPTIONAL_FIELDS, SCHEDULE_PATTERN, SCHEDULE_EXAMPLE

if __name__ == '__main__':
    def courseGrabber(studentID, studentPwd):
        _, courses = whu.readCourses(studentID, studentPwd, LoadCoursesFromFile=False)
        return courses


    customize_course.main(
        lambda : createCustomCourse(
            parsers.scheduleParser,
            NECESSARY_FIELDS,
            OPTIONAL_FIELDS,
            SCHEDULE_PATTERN,
            SCHEDULE_EXAMPLE,
            8
        ),
        courseGrabber
    )

