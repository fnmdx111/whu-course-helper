# encoding: utf-8
import __init__
from const.constants import   PASSWORD_PROMPT, ID_PROMPT, DAYS_TO_NUMS

from const.dict_keys import *
from BeautifulSoup import BeautifulSoup
from mod.fuf import getAccountInfo
from mod.config import *
from schools.whu import whu
from schools.whu.parsers import genLocationByCourseSchedule


mainHtml = u'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<style type="text/css">
    td {{
        text-align: center;
    }}
</style>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>{student_name}的课表</title>
</head>

<body>
{table_content}
</body>
</html>
'''

tableContent = u'''
<table width="{table_width}" height="{table_height}" border="{table_border}>
{table_header_content}
{table_rows_contents}
</table>
'''

tableRowContent = u'''\t<tr>'''

tableHeaderContent = u'''
\t\t<th class="%s" %s scope="%s">%s</th>
'''

clsNumberTableHeaderClassContent = u'headerofclass%s'
clsNumberTableHeaderText = u'第%s节'

dayNumberTableHeaderClassContent = u'headerofday%s'
dayNumberTableHeaderText = u'星期%s'

tdContent= u'\t\t<td class="day%sclass%s" rowspan="%s">&nbsp;</td>\n'


def genRow(clsNumber):
    content = tableRowContent

    content += tableHeaderContent % (
        clsNumberTableHeaderClassContent % clsNumber,
        u'',
        u'row',
        clsNumberTableHeaderText % clsNumber
    )

    for day in range(1, 8):
        content += tdContent % (day, clsNumber, 1)

    content += u'</tr>'

    return content


def genBlankRow():
    content = u'''<tr>
    <th scope="row" colspan="8">&nbsp;</th>
</tr>'''

    return content


def genRows():
    content = u''
    for i in range(1, 6):
        content += genRow(i)

    content += genBlankRow()

    for i in range(6, 12):
        content += genRow(i)

    content += genBlankRow()

    for i in range(12, 15):
        content += genRow(i)

    return content


def genDays():
    content = tableRowContent

    content += tableHeaderContent % (
        dayNumberTableHeaderClassContent % 0,
        u'width="222"',
        u'col',
        u'&nbsp;'
    )

    for enum, day in enumerate((u'一', u'二', u'三', u'四', u'五', u'六', u'天')):
        content += tableHeaderContent % (
            dayNumberTableHeaderClassContent % (enum + 1),
            u'width="213"',
            u'col',
            dayNumberTableHeaderText % day
        )

    content += u'</tr>'

    return content


def genTable(tableWidth=1748, tableHeight=537, tableBorder=1):
    table_params = {
        u'table_width': tableWidth,
        u'table_height': tableHeight,
        u'table_border': tableBorder,
        u'table_header_content': genDays(),
        u'table_rows_contents': genRows()
    }

    content = tableContent.format(**table_params)

    return content


def genHTML(studentName):
    htmlParams = {
        u'student_name': studentName,
        u'table_content': genTable()
    }

    content = mainHtml.format(**htmlParams)

    return content


def genCourseInfoInTableElem(course, currentSchedule, showClsNum=False):
    content = u'{course_name} {teacher_name}<br />{district}区, {classroom_and_building}, {class_number}<br />{starting_week}-{ending_week}周, 每{frequency}周'

    classNumber = u''
    if showClsNum:
        startingClassNum = int(currentSchedule[STARTING_CLASS_NUMBER])
        endingClassNum = int(currentSchedule[ENDING_CLASS_NUMBER])
        classNumber = u'%s-%s节' % (startingClassNum, endingClassNum)

    params = {
        COURSE_NAME: course.getProperty(COURSE_NAME),
        TEACHER_NAME: course.getProperty(TEACHER_NAME),
        DISTRICT: currentSchedule[DISTRICT],
        u'classroom_and_building': genLocationByCourseSchedule(currentSchedule),
        STARTING_WEEK: currentSchedule[STARTING_WEEK],
        ENDING_WEEK: currentSchedule[ENDING_WEEK],
        FREQUENCY: currentSchedule[FREQUENCY],
        u'class_number': classNumber
    }

    return content.format(**params)


def pourCourseIntoSoup(soup, course):
    def _findElemBy(dayNum, clsNum):
        return soup.find(
            name='td',
            attrs={
                'class': u'day%sclass%s' % (dayNum, clsNum)
            }
        )

    for schedule in course:
        dayNum = DAYS_TO_NUMS[schedule[DAY]]
        startingClassNum = int(schedule[STARTING_CLASS_NUMBER])
        endingClassNum = int(schedule[ENDING_CLASS_NUMBER])

        period = endingClassNum - startingClassNum + 1

        for i in range(startingClassNum + 1, endingClassNum + 1):
            elem = _findElemBy(dayNum, i)
            if elem:
                elem.extract()

        td = _findElemBy(dayNum, startingClassNum)

        td['rowspan'] = period if int(td['rowspan']) < period else td['rowspan']

        contents = genCourseInfoInTableElem(course, schedule)
        if td.contents[0] != u'&nbsp;':
            contents = td.contents[0] + u'<br />' * 2 + genCourseInfoInTableElem(course, schedule, showClsNum=True)
        td.contents[0].replaceWith(contents)


def createMyCourseTable(soup, courses):
    for course in courses:
        pourCourseIntoSoup(soup, course)

    return soup

def genTimetable(studentID, password):
    student_name, courses = whu.readCourses(studentID, password)

    with open('%s.html' % student_name, 'w') as f:
        print >> f, genHTML(student_name).encode('utf-8')

    with open('%s.html' % student_name, 'r') as f:
        soup = BeautifulSoup(f.read())

        createMyCourseTable(soup, courses)

    with open('%s.html' % student_name, 'w') as f:
        f.write(str(soup))

    return True

if __name__ == '__main__':
    try:
        studentID = getAccountInfo(configs[CONFIG_KEY_STUDENT_ID], ID_PROMPT)
        password = getAccountInfo(configs[CONFIG_KEY_STUDENT_PWD], PASSWORD_PROMPT, True)

        if genTimetable(studentID, password):
            info('info', 'task has been done successfully')
    except StopIteration as err:
        info('err', 'got fatal error: %s' % err )
        exit(0)

