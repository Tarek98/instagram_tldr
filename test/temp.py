sentiment_values = _openai_post_request([
    {
        "type": "text",
        "text": clt
    },
    {
        "type": "text",
        "text": "Given the following (comment, like_count) list, show a list of (comment, sentiment) where positive sentiment is +1*(like_count+1), neutral is 0, and negative sentiment is -1*(like_count+1)."
    }
])['choices'][0]['message']['content']

sentiment_tally = _openai_post_request([
    {
        "type": "text",
        "text": sentiment_values
    },
    {
        "type": "text",
        "text": "Given the following (comment, sentiment_number) list, give me a list of the sentiment_number values."
    }
])['choices'][0]['message']['content']

sentiment_summary = _openai_post_request([
    {
        "type": "text",
        "text": sentiment_tally
    },
    {
        "type": "text",
        "text": "In the given list, negative numbers are bad, positive numbers are good, and zero is neutral. Give me the sum of each, but for zero give the count & not the sum."
    }
])['choices'][0]['message']['content']