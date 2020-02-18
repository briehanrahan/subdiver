import os
from collections import namedtuple
from collections import defaultdict
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import praw
from psaw import PushshiftAPI

reddit = praw.Reddit(client_id='Qcv_EIynphFotA',
                     client_secret='FY_uyJWcx6ZsNf6nN_kD5vKEx8A',
                     password='Charlie47!Hotel',
                     user_agent='SubDiver by /u/PavementBlues',
                     username='ChomperBot')
api = PushshiftAPI(reddit)

Post = namedtuple('Post', 'title body score author post_epoch comment_count')
Redditor = namedtuple('Redditor', 'name cakeday')


def collect_posts(subreddit, post_limit):
    post_data = defaultdict(Post)

    for submission in list(api.search_submissions(subreddit='NeutralPolitics', limit=post_limit)):
        post_data[submission.id] = Post(submission.title,
                                        submission.selftext,
                                        submission.score,
                                        submission.author,
                                        submission.created_utc,
                                        submission.num_comments)

    post_data_df = pd.DataFrame.from_dict(data=post_data, orient='index')
    post_data_df['post_datetime'] = pd.to_datetime(post_data_df.post_epoch, unit='s')

    return post_data_df


def write_to_csv(df):
    file_root = 'C:/Users/brie/Documents/SubDiver/exports/post_data__'
    current_date = str(datetime.datetime.now()).replace(' ', '-').replace(':', '-')
    file_name = file_root + current_date + '.csv'

    df.to_csv(file_name, sep='~')


def get_most_recent_csv_name():
    source = 'C:/Users/brie/Documents/SubDiver/exports/'
    files = os.listdir(source)

    return source + str(max(files, key=lambda
        file: datetime.datetime.strptime(file.split('__')[1].split('.csv')[0], '%Y-%m-%d-%H-%M-%S.%f')))


def set_up_metric_variables(df):
    start_date = min(df.post_datetime.dt.date)
    end_date = max(df.post_date.dt.date)
    date_range = pd.date_range(start_date, end_date).tolist()
    date_count = defaultdict(int)

    return (start_date, end_date, date_range, date_count)


def create_metric_columns(df):
    count_df = df.groupby('date').agg(
        post_count=pd.NamedAgg(column='date', aggfunc='count'),
        comment_count_by_post_date=pd.NamedAgg(column='comment_count', aggfunc='sum'),
        post_comment_average = pd.NamedAgg(column='comment_count', aggfunc='mean')
    )

    return count_df


def calculate_metrics_by_day(df):
    start_date, end_date, date_range, date_count = set_up_metric_variables(df)
    df['date'] = pd.DatetimeIndex(post_data_df.post_datetime).date

    return create_metric_columns(df)


def calculate_metrics_by_week(df):
    start_date, end_date, date_range, date_count = set_up_metric_variables(df)
    df['date'] = pd.DatetimeIndex(post_data_df.post_datetime).to_period('W')

    return create_metric_columns(df)


def calculate_metrics_by_month(df):
    start_date, end_date, date_range, date_count = set_up_metric_variables(df)
    df['date'] = pd.DatetimeIndex(post_data_df.post_datetime).to_period('M')

    return create_metric_columns(df)


def calculate_metrics_by_year(df):
    start_date, end_date, date_range, date_count = set_up_metric_variables(df)
    df['date'] = pd.DatetimeIndex(post_data_df.post_datetime).year

    return create_metric_columns(df)



refresh_csv = True
subreddit = 'NeutralPolitics'
post_limit = 1000000

if refresh_csv:
    post_data_df = collect_posts(subreddit, post_limit)
    write_to_csv(post_data_df)
else:
    file_name = get_most_recent_csv_name()
    post_data_df = pd.read_csv(file_name, sep='~')

print(post_data_df.columns)

#metrics_df  = calculate_metrics_by_month(post_data_df)
#metrics_df.plot(y='post_comment_average')
#plt.show()