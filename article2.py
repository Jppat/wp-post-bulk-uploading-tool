import base64
import requests
import re
import mammoth
import os
from bs4 import BeautifulSoup
from dataclasses import dataclass, field, asdict
from dotenv import load_dotenv

BY = re.compile(
    r"^BY ", re.IGNORECASE
)  # pattern searching for 'by' at the start of a string

# load_dotenv()  # take environment variables from .env.
load_dotenv(dotenv_path="test/local/.env", override=True)


@dataclass
class Article:
    title: str
    authors: list[str] = field(default_factory=list)
    content: str = ""
    categories: list[str] = field(default_factory=list)
    status: str = "draft"
    format: str = "standard"

    def create_auth_header(self):

        def generate_token(user, pwd):
            wp_connection = user + ":" + pwd
            token = base64.b64encode(wp_connection.encode())
            return token

        token = generate_token(os.environ.get("USER"), os.environ.get("APP_PW"))
        headers = {"Authorization": "Basic " + token.decode("utf-8")}

        return headers

    def get_ids(self, resource, value, param):
        url = os.environ.get("URL") + f"/{resource}?{param}]={value}"
        request = requests.get(
            url, headers=self.create_auth_header(), timeout=120, verify=False
        )
        data = request.json()
        ids = [item["id"] for item in data]
        return ids

    def get_author_id(self):
        author_id = self.get_ids("users", self.authors[0], "search")
        return author_id[0]

    # def get_ids(self, attribute):
    #     # author_ids = []
    #     attribute_names = getattr(self, attribute)
    #     for name in attribute_names:
    #         params = {"search": name}
    #         auth = self.create_auth_header()
    #         url = os.environ.get("URL")
    #         response = requests.get(
    #             url + "/users",
    #             headers=auth,
    #             params=params,
    #             timeout=120,
    #             verify=False,
    #         )

    #     for author in response.json():
    #         author_id = author.get("id")

    #         return author_id

    def upload(self):

        url = os.environ.get("URL")
        headers = self.create_auth_header()
        post = asdict(self)
        post["author"] = self.get_ids("users", self.authors[0])
        post["categories"] = []
        for category in self.categories:
            self.get_ids("categories", category)

        wp_request = requests.post(
            url + "/posts",
            headers=headers,
            json=post,
            timeout=120,
            verify=False,
        )

        return wp_request.text


def convert_to_html(filepath, output=False):
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(
            docx_file, style_map="r[style-name='Emphasis'] => em"
        )
        html = result.value
        messages = result.messages  # Any messages, such as warnings during conversion
        print("messages:", messages)

    if output == True:
        with open(
            re.sub(r"\.docx?$", ".html", "output"), "w", encoding="utf-8"
        ) as html_file:
            html_file.write(html)

    return html


def create_article(html_file):
    soup = BeautifulSoup(html_file, "lxml")  # parse the html file
    everything = soup.body.contents
    title = everything[0].get_text(strip=True)

    for content in everything:
        if content.find(string=BY):
            author = re.sub(
                BY, "", content.get_text()
            )  # remove BY in 'By <author name>' to extract author name
            break
        else:
            author = "Panay News"

    string_content = "".join(list(map(str, everything[1:])))
    article = Article(
        title=str(title),
        authors=[author],
        content=string_content,
    )
    return article


def test_show_details(article):
    print(article.title)
    print(article.author)
    print("content: ", type(article.content))
    print(article.status)
    print(article.format)


def test():
    # This function is a placeholder for testing purposes
    html = convert_to_html("test/mai no reason.docx")
    article = create_article(html)
    # test_show_details(article)
    print("author id: ", article.get_author_id())
    # print("categories: ", article.get_ids("categories", "sports"))


test()
