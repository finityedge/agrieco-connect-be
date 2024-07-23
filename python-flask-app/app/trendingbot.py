import openai
import json
from collections import Counter
from app.models import Topic
import re
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

class TrendingKeywords:
    def __init__(self):
        pass

    def process_text(self, text):
        topics = Topic.query.all()
        topic_names = [topic.name for topic in topics]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI that analyzes text to extract trending topics. "
                        "Given the following text, return a list of only five items containing any of these keywords: "
                        + ", ".join(topic_names)
                    ),
                },
                {"role": "user", "content": text},
            ],
        )

        response_text = response.choices[0].message['content'].strip()

        keywords = []
        for kw in response_text.split('\n'):
            # Remove any leading numbers and dots
            kw_clean = re.sub(r'^\d+\.\s*', '', kw).strip()
            if kw_clean in topic_names:
                keywords.append(kw_clean)

        return keywords

    def get_trending_keywords(self, feed_contents, top_n=5):
        all_keywords = []
        for content in feed_contents:
            keywords = self.process_text(content)
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)
        most_common = keyword_counts.most_common(top_n)

        trending_keywords = {keyword: count for keyword, count in most_common}
        return trending_keywords
    
    
    def get_random_facts(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that generates random facts about things to do with agriculture, poultry, farming or fishing. Please generate a random fact for me and start the response with the fact directly",
                },
            ],
        )

        response_text = response.choices[0].message['content'].strip()
        return response_text
