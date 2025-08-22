import base64
import requests
import re
import mammoth
import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.
load_dotenv(dotenv_path=".env", override=True)

BY = re.compile(
    r"^BY ", re.IGNORECASE
)  # pattern searching for 'by' at the start of a string


def extractAttribute(url, attribute="categories"):
    page = 1
    attb_list = []

    while True:
        json_file = requests.get(
            url + f"/{attribute}?_fields=name,id&page={page}&per_page=100",
            timeout=5,
        )
        result_in_json = json_file.json()
        if len(result_in_json) > 0:
            page += 1
        else:
            break

        for obj in result_in_json:
            attb_list.append(obj)

        with open(f"./{attribute}.json", "w", encoding="utf-8") as file:
            json.dump(attb_list, file, indent=4)


# The Post class accepts an article class to create a wordpress post
class Post:
    def __init__(self, article):
        self.authors = article["author"]
        self.title = article["title"]
        self.body = article["body"]
        self.status = "draft"
        self.format = "standard"

    # gets id of author or category for records in json file
    def _get_ids(self, name_list, file):
        ids = []
        with open(file, encoding="utf-8") as json_file:
            parsed_json = json.load(json_file)
            name_lowercase = list(
                map(str.lower, name_list)
            )  # turn name_list to lowercase for consistency during comparison
            for item in parsed_json:
                if item["name"].lower() in name_lowercase:
                    ids.append(item["id"])

        return ids

    def _get_authors(self):
        authors = self.authors.split(",")
        # print("authors", authors)
        return self._get_ids(authors, "./users.json")

    def _get_categories(self):
        categories = input("enter name of categories, separated by comma: ")
        categories = re.split(
            r',(?=(?:[^"]*"[^"]*")*[^"]*$)', categories
        )  # only split by commas which are not inside quotes
        categories = [element.strip('"') for element in categories]
        # print("categories: ", categories, "type", type(categories))
        return self._get_ids(categories, "./categories.json")

    def _create_post(self):
        post = {
            "title": self.title,
            "author": self._get_authors()[0] if self._get_authors() else 1,
            # "author": self._get_authors()[0],  # only single authors supported at the moment
            "content": self.body,
            "categories": self._get_categories(),
            "status": self.status,
            "format": self.format,
        }
        return post

    def upload_post(self):

        def generate_token(user, pwd):
            wp_connection = user + ":" + pwd
            token = base64.b64encode(wp_connection.encode())
            return token

        post = self._create_post()

        # print("post: ", post)

        # prepare POST request details/requirements
        url = os.environ.get("URL")
        token = generate_token(os.environ.get("USER"), os.environ.get("APP_PW"))
        headers = {"Authorization": "Basic " + token.decode("utf-8")}

        wp_request = requests.post(
            url + "/posts", headers=headers, json=post, timeout=120
        )

        print("status", wp_request)
        print("message", wp_request.text)

        # Print request and response headers
        # print("\nRequest Headers:")
        # print(wp_request.request.headers)

        # print("\nResponse Headers:")
        # print(wp_request.headers)

        # Save the response as an HTML file
        # with open("wp_response.html", "w", encoding="utf-8") as file:
        #     file.write(wp_request.text)

    def show_details(self):
        attributes = vars(self)
        # for att in attributes:
        #     print(att, ":", attributes[att])
        print("title:", attributes["title"])
        print("authors:", attributes["authors"])
        print("format:", attributes["format"])
        print("status:", attributes["status"])


class Article:

    def __init__(self, filepath=None, html_file=None):
        if filepath:
            self.html = self.convert_to_html(filepath)
            self.article = self.create_article(self.html)
        elif html_file:
            self.html = html_file
            self.article = self.create_article(self.html)

    # convert docx file to html
    @staticmethod
    def convert_to_html(filepath, output=False):
        # print(f"converting {filepath} to html")
        with open(filepath, "rb") as docx_file:
            result = mammoth.convert_to_html(
                docx_file, style_map="r[style-name='Emphasis'] => em"
            )
            html = result.value  # The generated HTML
            messages = (
                result.messages
            )  # Any messages, such as warnings during conversion
            print("messages:", messages)

        # output an html file if set to True
        if output == True:
            with open(
                re.sub(r"\.docx?$", ".html", "output"), "w", encoding="utf-8"
            ) as html_file:
                html_file.write(html)

        return html

    # identify the parts of the article from the html file
    @staticmethod
    def create_article(html_file):
        # print("analyzing article")
        soup = BeautifulSoup(html_file, "lxml")  # parse the html file
        title = soup.p.get_text()  # get the title which is the first p element
        body = soup.p.find_next_siblings()
        body_tag_contents = soup.body.contents

        for content in body_tag_contents:
            if content.find(string=BY):
                author = re.sub(
                    BY, "", content.get_text()
                )  # remove BY from byLine to get author name only
                break
            else:
                author = "Panay News"

        string_body = "".join(list(map(str, body)))
        article = {"title": str(title), "author": author, "body": string_body}
        return article


# article1 = Article("./agri-damage.docx").article
# post1 = Post(article1)
# print(post1.article["author"])
# print(post1._get_authors())
# print(post1._get_categories())
# print(post1._create_post())
# post1.upload_post()
# post1.show_details()

# extractAttribute(url="https://panaynews.net/wp-json/wp/v2", attribute="categories")
# extractAttribute(url="https://watchmendailyjournal.com/wp-json/wp/v2")
