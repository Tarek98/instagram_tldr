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

# TODO: check if needed.
# os.environ['PYDEVD_WARN_EVALUATION_TIMEOUT'] = '10000'

class Instagram_TLDR(object):
    def __init__(self) -> None:
        print("\nWelcome to Instagram TLDR!\n")
        self.ig = Client()
        self.ig.login("tarekaadel", getpass("Please enter instagram admin password to proceed: \n"))
        print("Instagram admin login successful.\n")
    
    def help(self):
        # TODO: cont
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
                            "\n 2. Slack - User Engagement Analysis"+
                            "\n 3. Techcrunch - Weekly Newsfeed"+
                            "\n 4. Exit\n\n")
            if command == "0":
                self.help()
            elif command == "1":
                user_id = self.ig.user_id_from_username("microsoftteams")
                medias = cl.user_medias(user_id, 20)
                self.teams()
            
            elif command == "2":
                self.slack()
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
        user_id = ig.user_id_from_username("microsoftteams")

        # 1. Get Latest Post from MS Teams official account
        print("Here is the latest post from Microsoft Teams official account: \n")
        post = ig.user_medias(user_id, 1)[0]

        print(f'''
    "URL": {post.resources[0].thumbnail_url},
    "Caption": {post.caption_text},
    "Likes": {post.like_count}
              ''')

        print("{\nURL: "+str(post.resources[0].thumbnail_url)+
              "\n\tCaption: "+post.caption_text+
              "\n\tLikes: "+str(post.like_count)+"\n}\n")

        # 2. 


        pass

    def slack(self):
        pass

    def techcrunch(self):
        pass

    def _create

    def debug(self):
        # TODO: cont
        pass


if __name__ == '__main__':
    ig = Instagram_TLDR()
    ig.start()
