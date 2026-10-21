import json
import os

import litellm
import requests
from langchain.tools import tool
from unstructured.partition.html import partition_html


class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in chunks:
      model = (
          'gemini/gemini-2.0-flash' if os.environ.get('GOOGLE_API_KEY')
          else os.environ.get('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
      )
      result = litellm.completion(
          model=model,
          messages=[{
              "role": "user",
              "content": (
                  "Analyze and summarize the content below, make sure to include "
                  "the most relevant information in the summary, return only the "
                  f"summary nothing else.\n\nCONTENT\n----------\n{chunk}"
              )
          }]
      )
      summaries.append(result.choices[0].message.content)
    return "\n\n".join(summaries)