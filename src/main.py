from instagrapi import Client

import os
import requests
import base64
from getpass import getpass
from datetime import datetime, timedelta, timezone

GPT4V_KEY = os.environ.get("GPT4V_KEY")
GPT4V_ENDPOINT = os.environ.get("GPT4V_ENDPOINT")
VISION_API_ENDPOINT = os.environ.get("VISION_API_ENDPOINT")
VISION_API_KEY = os.environ.get("VISION_API_KEY")
os.environ['PYDEVD_WARN_EVALUATION_TIMEOUT'] = '10000'

class Instagram_TLDR(object):
    def __init__(self) -> None:
        print("\nWelcome to Instagram TLDR!\n")
        self.ig = Client()
        self.ig.login("tarekaadel", getpass("Please enter instagram admin password to proceed: "))
        print("Instagram admin login successful.\n")
    
    def help(self):
        help_str = '''
Instagram TLDR is a tool that allows you to analyze user engagement & activity summaries for 
social media accounts on Instagram.\n\nIt uses the OpenAI GPT-4 Vision API to analyze images &
text in posts, and the Instagrapi library to fetch posts, comments, and other user data.
        '''
        print(help_str)

    def start(self):
        while(True):
            print("-------------------------------------------")
            print("Please select a command number from below: ")
            print("-------------------------------------------")
            command = input("\n 0. Help"+
                            "\n 1. MS Teams - User Engagement Analysis"+
                            "\n 2. Discord - User Engagement Analysis"+
                            "\n 3. Techcrunch - Weekly Newsfeed"+
                            "\n 4. Exit\n\n")
            if command == "0":
                self.help()
            elif command == "1":
                self.teams()
            elif command == "2":
                self.discord()
            elif command == "3":
                self.techcrunch()
            elif command == "4":
                print("Exiting Instagram TLDR...\n")
                break
            else:
                print("Invalid command. Please try again.")
                continue

    def teams(self):
        ig = self.ig
        uid = ig.user_id_from_username("microsoftteams")
        print("\nMicrosoft Teams Instagram Account: \n")
        print("---------------------------------- \n")
        self.teams_discord_common(uid)

    def discord(self):
        ig = self.ig
        uid = ig.user_id_from_username("discord")
        print("\nDiscord Instagram Account: \n")
        print("-------------------------- \n")
        self.teams_discord_common(uid)

    def teams_discord_common(self,uid):
        ig = self.ig
        print("Latest post from account: \n")
        print("-------------------------------- \n")
        post = ig.user_medias_v1(uid, 1)[0]
        post_resource = post if post.media_type == 1 else post.resources[0]
        print("\t{\n\t\tPhoto URL: '"+str(post_resource.thumbnail_url)+
              "',\n\t\tCaption: '"+post.caption_text+
              "',\n\t\tLikes: '"+str(post.like_count)+"'\n\t}\n")
        
        print("Summary of what the post's photo shows: \n")
        print("--------------------------------------- \n")
        self._openai_summarize_image(str(post_resource.thumbnail_url))

        print("User comments sentiment for the post: \n")
        print("------------------------------------- \n")
        self._openai_summarize_comments(post.pk)

    def techcrunch(self):
        ig = self.ig
        uid = ig.user_id_from_username("techcrunch")
        posts = ig.user_medias_v1(uid, 6)

        post_timeline = []
        for post in posts:
            post_resource = post if post.media_type == 1 else post.resources[0]
            image_summary = self._openai_summarize_image_helper(post_resource.thumbnail_url)
            
            caption_image_summary = self._openai_post_request([
                {
                    "type": "text",
                    "text": f"Explain these two combined strings in one sentence of at most 10 words: [{post.caption_text}] & [{image_summary}]."
                }
            ])['choices'][0]['message']['content']

            post_timeline.append((post.taken_at, caption_image_summary))

        print("\n")
        for taken_at, summary in post_timeline:
            print(f"Date: {taken_at.strftime('%Y-%m-%d')}, Summary: {summary}")
        print("\n")

    def _openai_summarize_comments(self, media_pk):
        comments = self.ig.media_comments(media_pk, 0)
        extract_comment_like = lambda comment: (comment.text, comment.like_count)
        comment_like_list = [extract_comment_like(comment) for comment in comments if not comment.replied_to_comment_id]
        comment_like_list_str = ', '.join(map(str, comment_like_list))

        sentiment_values = self._openai_post_request([
            {
                "type": "text",
                "text": comment_like_list_str
            },
            {
                "type": "text",
                "text": "Given the following (comment, like_count) list, show a list of (comment, sentiment) where positive sentiment is +1*(like_count+1), neutral is 0, and negative sentiment is -1*(like_count+1)."
            }
        ])['choices'][0]['message']['content']

        sentiment_tally = self._openai_post_request([
            {
                "type": "text",
                "text": sentiment_values
            },
            {
                "type": "text",
                "text": "Given the following (comment, sentiment_number) list, give me a list of the sentiment_number values."
            }
        ])['choices'][0]['message']['content']

        sentiment_summary = self._openai_post_request([
            {
                "type": "text",
                "text": sentiment_tally
            },
            {
                "type": "text",
                "text": "In the given list, negative numbers are bad, positive numbers are good, and zero is neutral. Give me the sum of each, but for zero give the count & not the sum."
            }
        ])['choices'][0]['message']['content']

        print("Sentiment value per comment: \n")
        print("---------------------------- \n")
        print("\t"+sentiment_values+"\n")
        print("Sentiment tally count: \n")
        print("---------------------- \n")
        print("\t"+sentiment_tally+"\n")
        print("Sentiment summary: \n")
        print("------------------ \n")
        print("\t"+sentiment_summary.replace("\n", "\n\t")+"\n")

    def _openai_summarize_image(self, image_url):
        print(self._openai_summarize_image_helper(image_url) + "\n")

    def _openai_summarize_image_helper(self, image_url):
        image_content = requests.get(image_url).content
        encoded_image = base64.b64encode(image_content).decode('ascii')
        result = self._openai_post_request([
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            },
            {
                "type": "text",
                "text": "Explain what this image shows in one sentence."
            }
        ])
        return result['choices'][0]['message']['content']

    def _openai_post_request(self, payload_messages):
        headers = {
            "Content-Type": "application/json",
            "api-key": GPT4V_KEY,
        }

        payload = {
            "enhancements": {
                "ocr": {
                    "enabled": True
                },
                "grounding": {
                    "enabled": True
                }
            },
            "messages": [
                {
                    "role": "user",
                    "content": payload_messages
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        try:
            response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()  
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
        
        return response.json()


if __name__ == '__main__':
    ig = Instagram_TLDR()
    ig.start()
