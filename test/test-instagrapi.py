from getpass import getpass

from instagrapi import Client

from datetime import datetime, timedelta, timezone

cl = Client()
cl.login("tarekaadel", getpass("Enter admin password: "))

print("Instagram Login Successful")

user_id = cl.user_id_from_username("microsoftteams")
# Latest 10 posts from user id
medias = cl.user_medias(user_id, 20)
# ...
test = 1

# media_pk = medias[0].pk
# cl.album_download(media_pk, "/Users/tarek.a/code/FHL_Instagram_TLDR/temp_storage/")
# comments = cl.media_comments(media_pk, 0)
# extract_comment_like = lambda comment: (comment.text, comment.like_count)
# comment_like_list = [extract_comment_like(comment) for comment in comments if not comment.replied_to_comment_id]

# TODO: weight the comment list by likes - gives more weight to positive/negative sentiments.
# comment_like_list = sorted(comment_like_list, key=lambda x: x[1], reverse=True)

# top_hashtag_posts = cl.hashtag_medias_top("microsoftteams", 50)
# cl.hashtag_related_hashtags("microsoftteams")
# TODO: filter out top 5 liked posts from this list that have "#microsoftteams" in the caption & not the comments.
# TODO: Combine all comments from these posts & run sentiment analysis on them. 

# cl.media_info('3321678891070095153').thumbnail_url
# page = cl.user_medias_paginated('198218772')

# end_cursor = None
# page_size = 3
# post_limit = 12
# posts = []
# curr_date = datetime.now(timezone.utc)
# while True:
#     medias, end_cursor = cl.user_medias_paginated('198218772', page_size, end_cursor)
#     posts.extend(medias)
#     print(f"Total posts: {len(posts)}")
#     if (len(posts) >= post_limit) or \
#         (medias[-1].taken_at < curr_date - timedelta(days=7)):
#         break
# for post in posts:
#     # TODO: Do something with the post
#     # Ignore posts older than 7 days
#     if post.taken_at >= curr_date - timedelta(days=7):
#         break

# hash_posts = cl.hashtag_medias_top('microsoftteams', 100)
# top_hash_posts = []

# for hp in hash_posts:
#     if "#microsoftteams" in hp.caption_text.lower():
#         top_hash_posts.append({"id": hp.code, "caption": hp.caption_text, "pic_url": str(hp.thumbnail_url), "comment_count": hp.comment_count, "like_count": hp.like_count})
# TODO: filter out pic_url of None before sorting
# top_5_liked_posts = sorted(top_hash_posts, key=lambda x: x['like_count'], reverse=True)[:5]

def get_media_type_name(media_type_number, product_type):
    if media_type_number == 1:
        return "Photo"
    elif media_type_number == 2 and product_type == "feed":
        return "Video"
    elif media_type_number == 2 and product_type == "igtv":
        return "IGTV"
    elif media_type_number == 2 and product_type == "clips":
        return "Reel"
    elif media_type_number == 8:
        return "Album"
    else:
        raise Exception("Unknown media type")