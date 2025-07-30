import os
import re
from article import Article
from article import Post


def search_docx_files():
    directory = input("Please input the name of the folder: ")
    for root, directories, files in os.walk(directory):
        if len(files) == 0:
            return
        return [(root + "/" + file) for file in files if file.endswith(".docx")]


def article_list(html_file):
    articles = re.split(r"<p>--+</p>", html_file)
    # articles = re.split(r"\*\*\+", html_file)
    return articles


def multiple():
    docx_files = search_docx_files()
    for file in docx_files:
        print("processing ", file)
        temp = Article.convert_to_html(file)
        html_articles_list = article_list(temp)
        for html_article in html_articles_list:
            current_article = Article(html_file=html_article)
            print(current_article.article["title"])
            current_post = Post(current_article.article)
            current_post.upload_post()
            current_post.show_details()

            # break #uncomment for checking


def single():
    docx_files = search_docx_files()
    for file in docx_files:
        print("processing ", file)
        current_article = Article(filepath=file).article
        current_post = Post(current_article)
        current_post.upload_post()
        current_post.show_details()


def main():
    print("1: Single document for each article")
    print("2: Multiple articles for each document")

    choice = input(
        "Enter the appropriate document-article setup (enter the number only): "
    )

    if choice == "1":
        single()
    elif choice == "2":
        multiple()


main()
