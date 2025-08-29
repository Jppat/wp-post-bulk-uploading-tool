import os
import re
import sys
from article2 import Article, create_article, convert_to_html


def search_docx_files(directory):
    for root, directories, files in os.walk(directory):
        if len(files) == 0:
            return
        return [(root + "/" + file) for file in files if file.endswith(".docx")]


def article_list(html_file):
    articles = re.split(r"<p>--+</p>", html_file)
    # articles = re.split(r"\*\*\+", html_file)
    return articles


def multiple(docx_files):
    for file in docx_files:
        print("processing ", file)
        html = convert_to_html(file)
        html_articles_list = article_list(html)
        for html_article in html_articles_list:
            current_article = create_article(html_article)
            print(current_article.title)
            response = current_article.upload()
            print(response)


def single(docx_files):
    for file in docx_files:
        print("processing ", file)
        html = convert_to_html(file)
        article = create_article(html)
        # article.categories = [category]
        response = article.upload()
        print(response)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python matic.py <path to directory> <article setup>")
        print("For article setup:")
        print("Single - for one article per .docx file")
        print("Multiple - for multiple articles per .docx file")
    elif len(sys.argv) == 3:
        doxc_files = search_docx_files(sys.argv[1])
        if (sys.argv[2]) == "single":
            single(doxc_files)
        elif (sys.argv[2]) == "multiple":
            multiple(doxc_files)
