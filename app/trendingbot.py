import openai
import json
from collections import Counter

openai.api_key = 'sk-proj-wxPVT91fhdm62sqn6HwxT3BlbkFJ0WZJhrqshrR9ZyeVyd3J'

class TrendingKeywords:
    def __init__(self):
        pass

    def process_text(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract key phrases from the following text."},
                {"role": "user", "content": text}
            ]
        )
        keywords = response.choices[0].message['content'].strip().split('\n')
        return [kw.strip() for kw in keywords if kw.strip()]

    def get_trending_keywords(self, feed_contents, top_n=10):
        all_keywords = []
        for content in feed_contents:
            keywords = self.process_text(content)
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)
        most_common = keyword_counts.most_common(top_n)

        trending_keywords = {keyword: count for keyword, count in most_common}
        return json.dumps(trending_keywords, indent=4)
