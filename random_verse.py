import random
from html.parser import HTMLParser
import requests
import re

link = 'https://wiki.ahlolbait.com/%D8%A2%DB%8C%D9%87_{surah_num}_%D8%B3%D9%88%D8%B1%D9%87_{surah_name}'

class GetDivByTitle(HTMLParser):
    def __init__(self, target_title):
        super().__init__()
        self.target_title = target_title
        self.found_div = False
        self.inner_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for name, value in attrs:
                if name == "title" and value == self.target_title:
                    self.found_div = True

    def handle_data(self, data):
        if self.found_div:
            self.inner_text += data

    def handle_endtag(self, tag):
        if tag == "div" and self.found_div:
            self.found_div = False

    def get_inner_text(self):
        return self.inner_text.strip()

surahs = {
  "\u0641\u0627\u062a\u062d\u0647": 7,
  "\u0628\u0642\u0631\u0647": 286,
  "\u0622\u0644 \u0639\u0645\u0631\u0627\u0646": 200,
  "\u0646\u0633\u0627\u0621": 176,
  "\u0645\u0627\u0626\u062f\u0647": 120,
  "\u0627\u0646\u0639\u0627\u0645": 165,
  "\u0627\u0639\u0631\u0627\u0641": 206,
  "\u0627\u0646\u0641\u0627\u0644": 75,
  "\u062a\u0648\u0628\u0647": 129,
  "\u06cc\u0648\u0646\u0633": 109,
  "\u0647\u0648\u062f": 123,
  "\u06cc\u0648\u0633\u0641": 111,
  "\u0631\u0639\u062f": 43,
  "\u0627\u0628\u0631\u0627\u0647\u06cc\u0645": 52,
  "\u062d\u062c\u0631": 99,
  "\u0646\u062d\u0644": 128,
  "\u0627\u0633\u0631\u0627\u0621": 111,
  "\u06a9\u0647\u0641": 110,
  "\u0645\u0631\u06cc\u0645": 98,
  "\u0637\u0647": 135,
  "\u0627\u0646\u0628\u06cc\u0627\u0621": 112,
  "\u062d\u062c": 78,
  "\u0645\u0624\u0645\u0646\u0648\u0646": 118,
  "\u0646\u0648\u0631": 64,
  "\u0641\u0631\u0642\u0627\u0646": 77,
  "\u0634\u0639\u0631\u0627\u0621": 227,
  "\u0646\u0645\u0644": 93,
  "\u0642\u0635\u0635": 88,
  "\u0639\u0646\u06a9\u0628\u0648\u062a": 69,
  "\u0631\u0648\u0645": 60,
  "\u0644\u0642\u0645\u0627\u0646": 34,
  "\u0633\u062c\u062f\u0629": 30,
  "\u0627\u062d\u0632\u0627\u0628": 73,
  "\u0633\u0628\u0623": 54,
  "\u0641\u0627\u0637\u0631": 45,
  "\u06cc\u0633": 83,
  "\u0635\u0627\u0641\u0627\u062a": 182,
  "\u0635": 88,
  "\u0632\u0645\u0631": 75,
  "\u063a\u0627\u0641\u0631": 85,
  "\u0641\u0635\u0644\u062a": 54,
  "\u0634\u0648\u0631\u06cc": 53,
  "\u0632\u062e\u0631\u0641": 89,
  "\u062f\u062e\u0627\u0646": 59,
  "\u062c\u0627\u062b\u06cc\u0629": 37,
  "\u0627\u062d\u0642\u0627\u0641": 35,
  "\u0645\u062d\u0645\u062f": 38,
  "\u0641\u062a\u062d": 29,
  "\u062d\u062c\u0631\u0627\u062a": 18,
  "\u0642": 45,
  "\u0630\u0627\u0631\u06cc\u0627\u062a": 60,
  "\u0637\u0648\u0631": 49,
  "\u0646\u062c\u0645": 62,
  "\u0642\u0645\u0631": 55,
  "\u0627\u0644\u0631\u062d\u0645\u0646": 78,
  "\u0648\u0627\u0642\u0639\u0647": 96,
  "\u062d\u062f\u06cc\u062f": 29,
  "\u0645\u062c\u0627\u062f\u0644\u0647": 22,
  "\u062d\u0634\u0631": 24,
  "\u0645\u0645\u062a\u062d\u0646\u0647": 13,
  "\u0635\u0641": 14,
  "\u062c\u0645\u0639\u0647": 11,
  "\u0645\u0646\u0627\u0641\u0642\u0648\u0646": 11,
  "\u062a\u063a\u0627\u0628\u0646": 18,
  "\u0637\u0644\u0627\u0642": 12,
  "\u062a\u062d\u0631\u06cc\u0645": 12,
  "\u0645\u0644\u06a9": 30,
  "\u0642\u0644\u0645": 52,
  "\u062d\u0627\u0642\u0647": 52,
  "\u0645\u0639\u0627\u0631\u062c": 44,
  "\u0646\u0648\u062d": 28,
  "\u062c\u0646": 28,
  "\u0645\u0632\u0645\u0644": 20,
  "\u0645\u062f\u062b\u0631": 56,
  "\u0642\u06cc\u0627\u0645\u0647": 40,
  "\u0627\u0646\u0633\u0627\u0646": 31,
  "\u0645\u0631\u0633\u0644\u0627\u062a": 50,
  "\u0646\u0628\u0623": 40,
  "\u0646\u0627\u0632\u0639\u0627\u062a": 46,
  "\u0639\u0628\u0633": 42,
  "\u062a\u06a9\u0648\u06cc\u0631": 29,
  "\u0627\u0646\u0641\u0637\u0627\u0631": 19,
  "\u0645\u0637\u0641\u0641\u06cc\u0646": 36,
  "\u0627\u0646\u0634\u0642\u0627\u0642": 25,
  "\u0628\u0631\u0648\u062c": 22,
  "\u0637\u0627\u0631\u0642": 17,
  "\u0627\u0639\u0644\u06cc": 19,
  "\u063a\u0627\u0634\u06cc\u0647": 26,
  "\u0641\u062c\u0631": 30,
  "\u0628\u0644\u062f": 20,
  "\u0634\u0645\u0633": 15,
  "\u0644\u06cc\u0644": 21,
  "\u0636\u062d\u06cc": 11,
  "\u0634\u0631\u062d": 8,
  "\u062a\u06cc\u0646": 8,
  "\u0639\u0644\u0642": 19,
  "\u0642\u062f\u0631": 5,
  "\u0628\u06cc\u0646\u0647": 8,
  "\u0632\u0644\u0632\u0627\u0644": 8,
  "\u0639\u0627\u062f\u06cc\u0627\u062a": 11,
  "\u0642\u0627\u0631\u0639\u0629": 11,
  "\u062a\u06a9\u0627\u062b\u0631": 8,
  "\u0639\u0635\u0631": 3,
  "\u0647\u0645\u0632\u0647": 9,
  "\u0641\u06cc\u0644": 5,
  "\u0642\u0631\u06cc\u0634": 4,
  "\u0645\u0627\u0639\u0648\u0646": 7,
  "\u06a9\u0648\u062b\u0631": 3,
  "\u06a9\u0627\u0641\u0631\u0648\u0646": 6,
  "\u0646\u0635\u0631": 3,
  "\u0645\u0633\u062f": 5,
  "\u0627\u062e\u0644\u0627\u0635": 4,
  "\u0641\u0644\u0642": 5,
  "\u0646\u0627\u0633": 6
}

def get_random_verse():
    surah_name, verse_count = random.choice(list(surahs.items()))
    random_verse = random.randrange(1,verse_count+1)

    formatted_url = link.format(surah_name=surah_name,surah_num=random_verse)
    
    html_page = requests.get(formatted_url).content.decode()

    parser = GetDivByTitle(target_title="الهی قمشه‌ای")
    parser.feed(html_page)
    random_surah = parser.get_inner_text()

    no_paranthesis = re.sub(r'([\(\[]).*?([\)\]])','\b',random_surah)
    return (no_paranthesis,f"{surah_name}:{random_verse}")


if __name__ == "__main__":
    print(get_random_verse())