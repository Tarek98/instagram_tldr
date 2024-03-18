import os
import requests
import base64

# Configuration

GPT4V_KEY = os.environ.get("GPT4V_KEY")
GPT4V_ENDPOINT = os.environ.get("GPT4V_ENDPOINT")
VISION_API_ENDPOINT = os.environ.get("VISION_API_ENDPOINT")
VISION_API_KEY = os.environ.get("VISION_API_KEY")

# headers = {
#     "Content-Type": "application/json",
#     "api-key": GPT4V_KEY,
# }

# IMAGE_PATH = "/Users/tarek.a/code/FHL_Instagram_TLDR/openai_test/copilot_teams_post.png"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
# # Payload for the request
# payload_one = {
#   "enhancements": {
#     "ocr": {
#       "enabled": True
#     },
#     "grounding": {
#       "enabled": True
#     }
#   },
#   "messages": [
#     {
#       "role": "user",
#       "content": [
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{encoded_image}"
#           }
#         },
#         {
#           "type": "text",
#           "text": "What does this image show?"
#         }
#       ]
#     }
#   ],
#   "temperature": 0.7,
#   "top_p": 0.95,
#   "max_tokens": 800
# }

# comments_like_count_list = '''[('@robertkmackey1987 😄❤️', 3), ('❤🔥❤', 3), ("@0_dd_dd_0 We're really excited about this! 😊", 1), ("Yes, I'm keeping my emails: nightdwellers@hotmail.com ecanus_movie_studio@hotmail.com douglassgibran@hotmail.com", 1), ('Mannnn... You have sooo many bugs in your product. How is your company even leading IT industry!', 0), ("I don't like teams. Seriously I hate it.", 0), ('@tstubs Hi there, Copilot for Teams is not currently available on the Apple Watch.', 0), ('App for Apple Watch???', 0), ("@natattacknelson Hi Nat, thank you for reaching out. Please send us a private message and confirm for us which version of Teams you're using (Business, Education, or Personal)", 0), ('Teams has been a constant letdown over the past couple of weeks. I log on and then 45 minutes later there is a flood of messages I have missed. What is going on?', 0), ('@2amtech Hi there, thanks for reaching out. Yes, Copilot is available on Teams', 0), ('is this already available?', 0), ('Amazing❤️\u200d🔥👏', 0), ('@douglass_gibran_enterprise', 0), ('@clinkitsolutions 💜', 0), ('Nice', 0)]'''
# # Payload for the request
# payload_comments = {
#   "enhancements": {
#     "ocr": {
#       "enabled": True
#     },
#     "grounding": {
#       "enabled": True
#     }
#   },
#   "messages": [
#     {
#       "role": "user",
#       "content": [
#         {
#           "type": "text",
#           "text": f"{comments_like_count_list}"
#         },
#         {
#           "type": "text",
#           "text": "Give me the top 3 negative sentiment comments from this list of comments." # TODO: tweak to add like count
#         },
#         {
#           "type": "text",
#           "text": "Give me the top 3 positive sentiment comments from this list of comments." # TODO: tweak to add like count
#         },
#         {
#           "type": "text",
#           "text": "Categorize each comment as positive or negative sentiment, show it to me, and then give me a percentage of positive vs negative sentiment comments."
#         }
#       ]
#     }
#   ],
#   "temperature": 0.7,
#   "top_p": 0.95,
#   "max_tokens": 800
# }

# # OCR in instagram photo
# # cl.media_info('3321678891070095153').thumbnail_url
# image_url = 'https://scontent-sea1-1.cdninstagram.com/v/t51.2885-15/432473124_692835899469206_6869480885668630288_n.jpg?se=7&stp=dst-jpg_e35&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xMDgweDEzNTAuc2RyIn0&_nc_ht=scontent-sea1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=iE3N_K5fL8oAX9Oe0ia&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=MzMyMTY3ODg5MTA3MDA5NTE1Mw%3D%3D.2-ccb7-5&oh=00_AfB_4QV_8LsK8i_mc1uSumBt0rtgpk5bObpmoh_iHE8CCw&oe=65F76CC3&_nc_sid=fc8dfb'
# response = requests.get(image_url)
# encoded_image = base64.b64encode(response.content).decode('ascii')
# payload_ocr = {
#   "enhancements": {
#     "ocr": {
#       "enabled": True
#     },
#     "grounding": {
#       "enabled": True
#     }
#   },
#   "messages": [
#     {
#       "role": "user",
#       "content": [
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{encoded_image}"
#           }
#         },
#         {
#           "type": "text",
#           "text": "What does this image show?"
#         }
#       ]
#     }
#   ],
#   "temperature": 0.7,
#   "top_p": 0.95,
#   "max_tokens": 800
# }

# # Send request
# try:
#     response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload_ocr)
#     response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
# except requests.RequestException as e:
#     raise SystemExit(f"Failed to make the request. Error: {e}")

def _openai_post_request(payload_messages):
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

# Handle the response as needed (e.g., print or process)
print(response.json())
