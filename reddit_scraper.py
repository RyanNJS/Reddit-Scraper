import praw
import pandas as pd
from praw.models import MoreComments
import datetime
import time

reddit = praw.Reddit(client_id="hidden", client_secret="hidden", user_agent="hidden", username='hidden', password='hidden')

subreddit = reddit.subreddit("SGExams")
# for post in subreddit.search(query='teach', limit=10)

# Display the name of the Subreddit
print("Display Name: r/" + str(subreddit.display_name))
# Display the title of the Subreddit
print("Title:", subreddit.title)


def get_recent_posts():
    posts_dict = {"Title": [], "Post Text": [], "ID": [], "Post Score": [], "Total Comments": [], "Link": [], "Post URL": [], "Date": []}
    comments_dict = {"Title": [], "Comment Text": [], "Comment Score": [], "Sneak Peek Bot": [], "Additional Replies": [], "Reply Score": []}
    post_count = 1
    for post in subreddit.top(time_filter='year', limit=10):
        post.comments.replace_more(limit=None)
        print('Post ' + str(post_count) + ':', post.title)

        if len(post.title) == 0:
            posts_dict["Title"].append('No title')
        else:
            posts_dict["Title"].append(post.title)

        if len(post.selftext) == 0:
            posts_dict["Post Text"].append('NIL')
        else:
            posts_dict["Post Text"].append(post.selftext)

        posts_dict["ID"].append(post.id)
        posts_dict["Post Score"].append(post.score)
        posts_dict["Total Comments"].append(post.num_comments)
        posts_dict["Link"].append('https://www.reddit.com' + str(post.permalink))
        posts_dict["Post URL"].append(post.url)

        # print('Time:', post.created_utc)
        time_in_datetime = datetime.datetime.utcfromtimestamp(post.created_utc)
        str_time = datetime.datetime.strftime(time_in_datetime, '%b %d %Y')
        posts_dict["Date"].append(str_time)

        submission = reddit.submission(post.id)
        count = 0

        if post.num_comments > 0:
            for top_level_comment in submission.comments:
                if count >= 5:
                    break
                if top_level_comment.author == None:
                    pass
                elif isinstance(top_level_comment, MoreComments):
                    pass
                else:
                    if len(post.title) == 0:
                        comments_dict["Title"].append('No title')
                    else:
                        comments_dict["Title"].append(post.title)
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    elif top_level_comment.author.name == 'sneakpeek_bot':
                        comments_dict["Sneak Peek Bot"].append('SneakPeekPost')
                        comments_dict["Comment Text"].append(top_level_comment.body)
                        comments_dict["Comment Score"].append(top_level_comment.score)
                        comments_dict["Additional Replies"].append('NIL')
                        comments_dict["Reply Score"].append('NIL')
                    else:
                        # print(top_level_comment.author.name, 'made: ---', top_level_comment.body, '----- with score of', top_level_comment.score)
                        comments_dict["Sneak Peek Bot"].append('NIL')
                        comments_dict["Comment Text"].append(top_level_comment.body)
                        comments_dict["Comment Score"].append(top_level_comment.score)

                        second_level_count = 0
                        if len(top_level_comment.replies) == 0:
                            comments_dict["Additional Replies"].append('NIL')
                            comments_dict["Reply Score"].append('NIL')
                        else:
                            for second_level_comment in top_level_comment.replies:
                                if second_level_count == 1:
                                    break
                                elif isinstance(second_level_comment, MoreComments):
                                    comments_dict["Additional Replies"].append('NIL')
                                    comments_dict["Reply Score"].append('NIL')
                                    second_level_count += 1
                                else:
                                    comments_dict["Additional Replies"].append(second_level_comment.body)
                                    comments_dict["Reply Score"].append(second_level_comment.score)
                                    second_level_count += 1
                count += 1
            else:
                pass
        post_count += 1
        time.sleep(2)

    post_df = pd.DataFrame(posts_dict)

    with pd.ExcelWriter('redditdata_sgexams.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        post_df.to_excel(writer, sheet_name='PostsData')

    comment_df = pd.DataFrame(comments_dict)

    with pd.ExcelWriter('redditdata_sgexams.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        comment_df.to_excel(writer, sheet_name='CommentsAndReplies')

