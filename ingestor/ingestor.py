from collections import namedtuple
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt
import praw
from psaw import PushshiftAPI

reddit = praw.Reddit(client_id='Qcv_EIynphFotA',
                     client_secret='FY_uyJWcx6ZsNf6nN_kD5vKEx8A',
                     password='Charlie47!Hotel',
                     user_agent='SubDiver by /u/PavementBlues',
                     username='ChomperBot')
api = PushshiftAPI(reddit)

Post = namedtuple('Post', 'title score author post_epoch comment_count')
Redditor = namedtuple('Redditor', 'name cakeday')

def collect_posts_with_praw(subreddit, post_limit):
    post_data = defaultdict(Post)

    for submission in reddit.subreddit('NeutralPolitics').new(limit=post_limit):
        post_data[submission.id] = Post(submission.title,
                                        submission.score,
                                        submission.author,
                                        submission.created_utc,
                                        submission.num_comments)

    post_data_df = pd.DataFrame.from_dict(data=post_data, orient='index')
    post_data_df['post_datetime'] = pd.to_datetime(post_data_df['post_epoch'], unit='s')
    post_data_df['post_date'] = post_data_df['post_datetime'].dt.date

    return post_data_df

def collect_posts_with_psaw(subreddit, post_limit):
    post_data = defaultdict(Post)

    for submission in list(api.search_submissions(subreddit='NeutralPolitics', limit=post_limit)):
        post_data[submission.id] = Post(submission.title,
                                        submission.score,
                                        submission.author,
                                        submission.created_utc,
                                        submission.num_comments)

    post_data_df = pd.DataFrame.from_dict(data=post_data, orient='index')
    post_data_df['post_datetime'] = pd.to_datetime(post_data_df['post_epoch'], unit='s')
    post_data_df['post_date'] = post_data_df['post_datetime'].dt.date

    return post_data_df

'''
def count_posts_by_day(post_data_df):
    column_names = ['date', 'post_count']
    count_by_day_df = pd.DataFrame(columns=column_names)

    for post_date in post_data_df['post_date'].values:
        current_count = count_by_day_df.get(post_date, default=0)
        count_by_day_df['date'] = current_count + 1

    return count_by_day_df
'''

post_data_df = collect_posts_with_psaw('NeutralPolitics', 1000000)

post_data_df.to_csv('C:/Users/brie/Documents/SubDiver/post_data_full', sep='~')

'''count_by_day_df = count_posts_by_day(post_data_df)
print(count_by_day_df.info())
print(count_by_day_df.head())
'''

#plt.subplot(2, 2, 1)

#x_axis = count_by_day_df.keys
#y_axis = count_by_day_df.values

#plt.plot(x_axis, y_axis)
#plt.show()