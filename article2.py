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
# load_dotenv(dotenv_path="test/local/.env", override=True)
load_dotenv(dotenv_path=".env", override=True)


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

    def get_ids(self, resource, params):
        url = os.environ.get("URL") + f"/{resource}?_fields=id&{params}"
        request = requests.get(url, headers=self.create_auth_header(), timeout=120)
        return request.json()

    def get_author_id(self, author_name):
        author_name = author_name.split()
        params_list = [f"search={name}" for name in author_name]
        params = "&".join(params_list)
        author_id = self.get_ids("users", params)
        return [item["id"] for item in author_id]

    def get_category_id(self, category_name):
        params = f"slug={category_name}"
        category_id = self.get_ids("categories", params)
        if category_id:
            return category_id[0]["id"]
        return None

    def upload(self):

        url = os.environ.get("URL")
        headers = self.create_auth_header()
        post = asdict(self)

        if not self.authors:
            post["author"] = 1  # default to admin if author not found
        else:
            author_id = self.get_author_id(self.authors[0])
            if author_id:
                post["author"] = author_id[0]
            else:
                post["author"] = 1  # default to admin if author not found

        category_ids = [self.get_category_id(category) for category in self.categories]
        category_ids = list(filter(lambda id: id != None, category_ids))

        if category_ids:
            post["categories"] = category_ids
        else:
            post.pop("categories")

        wp_request = requests.post(
            url + "/posts",
            headers=headers,
            json=post,
            timeout=120,
            # verify=False,
        )

        return wp_request


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
