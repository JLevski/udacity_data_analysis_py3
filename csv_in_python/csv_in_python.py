import csv
from datetime import datetime as dt
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

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

# print(daily_engagement[0]['account_key'])

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

num_prob_records = 0
for enrollment in enrollments:
    if (enrollment['account_key'] not in get_unique_students(daily_engagement)
            and enrollment['join_date'] != enrollment['cancel_date']):
        # print(enrollment)
        num_prob_records += 1

# Create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])


def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data


# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

# Dictionary of students not cancelled yet, or lasted > 7 days
paid_students = {}
for enrollment in non_udacity_enrollments:
    if (enrollment['days_to_cancel'] is None or
            enrollment['days_to_cancel'] > 7):
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        if (account_key not in paid_students or enrollment_date >
                paid_students[account_key]):
            paid_students[account_key] = enrollment_date

# print(len(paid_students))


# engagement records for paid students in their first week
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days >= 0 and time_delta.days < 7


def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data


paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

# create field to track whether student visited that day
for engagement_record in paid_engagement:
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited'] = 1
    else:
        engagement_record['has_visited'] = 0

paid_engagement_in_first_week = []
for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)

# print(len(paid_engagement_in_first_week))


# Create a dictionary grouped by studenta key (e.g. a student).
def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data


# Aggregate different variables (minutes, lessons) by key (e.g. a student)
def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data in grouped_data.items():
        sum_data = 0
        for data_point in data:
            sum_data += data_point[field_name]
        summed_data[key] = sum_data
    return summed_data


# Output mean, standard deviation, max, min and length (count) for a data set
def stat_outputs(data):
    grouped_data = list(data.values())
    print("Mean: ", np.mean(grouped_data))
    print("Standard Deviation: ", np.std(grouped_data))
    print("Maximum: ", np.max(grouped_data))
    print("Minimum: ", np.min(grouped_data))
    print("Length: ", len(grouped_data))


def histogram(*args):
    if args is not None:
        n_rows = math.ceil(math.sqrt(len(args)))
        n_cols = math.ceil(len(args) / n_rows)
        sub_plot_count = 1
        plt.figure()
        for data in args:
            grouped_data = list(data.values())
            plt.hist(grouped_data)
            plt.subplot(n_rows, n_cols, sub_plot_count)
            sub_plot_count += 1
        plt.show()
    else:
        print('please provide a dataset')


# engagement_by_account = group_data(paid_engagement_in_first_week,
#                                    'account_key')
# total_lessons_by_account = sum_grouped_items(engagement_by_account,
#                                              'lessons_completed')
# print("Statistical outputs for total_lessons_by_account")
# print(stat_outputs(total_lessons_by_account))
#
# total_minutes_by_account = sum_grouped_items(engagement_by_account,
#                                              'total_minutes_visited')
# print("Statistical outputs for total_minutes_by_account")
# print(stat_outputs(total_minutes_by_account))
#
# days_visited_by_account = sum_grouped_items(engagement_by_account,
#                                             'has_visited')
# print("Statistical outputs for days_visited_by_account")
# print(stat_outputs(days_visited_by_account))

# Create two lists of engagement data for paid students in the first week.
# The first list should contain data for students who eventually pass the
# subway project, and the second list should contain data for students
# who do not.

subway_project_lesson_keys = ['746169184', '3176718735']
passing_grades = ['PASSED', 'DISTINCTION']

pass_subway_project = set()
passing_engagement = []
non_passing_engagement = []

for submission in paid_submissions:
    if submission['lesson_key'] in subway_project_lesson_keys:
        if submission['assigned_rating'] in passing_grades:
            pass_subway_project.add(submission['account_key'])

# print(len(pass_subway_project))

for engagement in paid_engagement_in_first_week:
    if engagement['account_key'] in pass_subway_project:
        passing_engagement.append(engagement)
    else:
        non_passing_engagement.append(engagement)

# print(len(passing_engagement))
# print(len(non_passing_engagement))

passing_engagement_by_account = group_data(passing_engagement, 'account_key')
non_passing_engagement_by_account = group_data(non_passing_engagement,
                                               'account_key')

total_pass_projects_by_account = sum_grouped_items(
    passing_engagement_by_account, 'projects_completed')
total_pass_minutes_by_account = sum_grouped_items(
    passing_engagement_by_account, 'total_minutes_visited')
total_pass_lessons_by_account = sum_grouped_items(
    passing_engagement_by_account, 'lessons_completed')
pass_days_visited_by_account = sum_grouped_items(
    passing_engagement_by_account, 'has_visited')

total_non_pass_projects_by_account = sum_grouped_items(
    non_passing_engagement_by_account, 'projects_completed')
total_non_pass_minutes_by_account = sum_grouped_items(
    non_passing_engagement_by_account, 'total_minutes_visited')
total_non_pass_lessons_by_account = sum_grouped_items(
    non_passing_engagement_by_account, 'lessons_completed')
non_pass_days_visited_by_account = sum_grouped_items(
    non_passing_engagement_by_account, 'has_visited')

# print("Statistical outputs for total_pass_projects_by_account")
# print(stat_outputs(total_pass_projects_by_account))
# print("Statistical outputs for total_non_pass_projects_by_account")
# print(stat_outputs(total_non_pass_projects_by_account))
#
# print("Statistical outputs for total_pass_minutes_by_account")
# print(stat_outputs(total_pass_minutes_by_account))
# print("Statistical outputs for total_non_pass_minutes_by_account")
# print(stat_outputs(total_non_pass_minutes_by_account))
#
# print("Statistical outputs for total_pass_lessons_by_account")
# print(stat_outputs(total_pass_lessons_by_account))
# print("Statistical outputs for total_non_pass_lessons_by_account")
# print(stat_outputs(total_non_pass_lessons_by_account))
#
# print("Statistical outputs for pass_days_visited_by_account")
# print(stat_outputs(pass_days_visited_by_account))
# print("Statistical outputs for non_pass_days_visited_by_account")
# print(stat_outputs(non_pass_days_visited_by_account))

# print(stat_outputs(total_non_pass_minutes_by_account))
# plt.figure()
# grouped_data = list(total_non_pass_minutes_by_account.values())
# plt.hist(grouped_data, bins=20)
# plt.xlabel('Number of minutes')
# plt.title('Distribution of minutes spent in the first week for students who ' +
#           'failed the subway project')
# plt.show()
# histogram(total_non_pass_minutes_by_account)
histogram(total_pass_minutes_by_account, total_non_pass_minutes_by_account,
          total_pass_lessons_by_account, total_non_pass_lessons_by_account,
          pass_days_visited_by_account, non_pass_days_visited_by_account)



# understand why max minutes is so high
# student_with_max_minutes = None
# max_minutes = 0
#
# for student, total_minutes in total_minutes_by_account.items():
#     if total_minutes > max_minutes:
#         max_minutes = total_minutes
#         student_with_max_minutes = student
#
# for engagement_record in paid_engagement_in_first_week:
#     if engagement_record['account_key'] == student_with_max_minutes:
#         print(engagement_record)
