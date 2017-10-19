import csv
import os
from datetime import datetime as dt

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'


def read_csv(filename):
    with open(filename, 'rt') as f:
        reader = csv.DictReader(f)
        return list(reader)


enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')


############################################
#                 Cleanup                  #
############################################

def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)


for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]

print(daily_engagement[0]['account_key'])

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

############################################
#                 Analysis                 #
############################################

# return the number of rows and unique accounts in each csv file
def get_unique_students(data):
    unique_students = set()
    for student in data:
        unique_students.add(student['account_key'])
    return unique_students


enrollment_num_rows = len(enrollments)
enrollment_num_unique_students = len(get_unique_students(enrollments))

engagement_num_rows = len(daily_engagement)
engagement_num_unique_students = len(get_unique_students(daily_engagement))

submission_num_rows = len(project_submissions)
submission_num_unique_students = len(get_unique_students(project_submissions))

only_enrolled = unique_enrolled_students.difference(unique_engagement_students)
for student in enrollments:
    if student['account_key'] in only_enrolled:
        print(student)
        break
