import os
import requests
import base64

# Configuration
GPT4V_KEY = "YOUR_API_KEY"
IMAGE_PATH = "YOUR_IMAGE_PATH"
encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

# Payload for the request
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
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_image}"
          }
        },
        {
          "type": "text",
          "text": "What does the text in this photo say?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The text in the image says:\n\nNo Man's Sky - \"go to the spaceship\"\nValheim - \"chop down a tree\"\nGoat Simulator 3 - \"drive the car\"\nTeardown - \"go through the gate\"\nSatisfactory - \"go to the HUB\"\n\nGoogle Deepmind\ntrained a video\ngame-playing AI\nto be your co-op\ncompanion"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is exciting about this?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The exciting aspect of the information presented in the image is that Google Deepmind has trained an AI to play video games, potentially acting as a cooperative companion for players. This suggests that the AI could understand and perform tasks within various games, providing a more interactive and engaging gaming experience where players can team up with AI entities that can assist in completing objectives or enhancing gameplay. The AI's capability to adapt to different game environments and objectives, such as those listed from No Man's Sky, Valheim, Goat Simulator 3, Teardown, and Satisfactory, indicates a significant advancement in artificial intelligence within the gaming industry."
        }
      ]
    }
  ],
  "temperature": 0.5,
  "top_p": 0.95,
  "max_tokens": 800
}

GPT4V_ENDPOINT = "https://exp-gpt-vision.openai.azure.com/openai/deployments/gpt4-vision/extensions/chat/completions?api-version=2024-02-15-preview"

# Send request
try:
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
print(response.json())