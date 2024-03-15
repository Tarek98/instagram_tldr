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
        uid = ig.user_id_from_username("microsoftteams")

        print("TLDR - latest post from MS Teams account: \n")
        post = ig.user_medias(uid, 1)[0]
        print("\t{\n\t\tPhoto URL: '"+str(post.resources[0].thumbnail_url)+
              "',\n\t\tCaption: '"+post.caption_text+
              "',\n\t\tLikes: '"+str(post.like_count)+"'\n\t}\n")
        
        print("Summary of what the post's photo shows: \n")
        self._openai_summarize_image(str(post.resources[0].thumbnail_url))

        

        pass

    def slack(self):
        pass

    def techcrunch(self):
        pass

    def _openai_summarize_image(self, image_url):
        image_content = requests.get(image_url).content
        encoded_image = base64.b64encode(image_content).decode('ascii')
        payload_messages = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            },
            {
                "type": "text",
                "text": "What does this image show?"
            }
        ]
        result = self._openai_post_request(payload_messages)

        print(result)

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

    def debug(self):
        # TODO: cont
        pass


if __name__ == '__main__':
    ig = Instagram_TLDR()
    ig.start()
