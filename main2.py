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


def show_details(article):
    print("Title: ", article.title)
    print("Authors: ", article.authors)
    print("Categories: ", article.categories)
    print("Status: ", article.status)


def multiple(docx_files, categories):
    for file in docx_files:
        print("processing ", file)
        html = convert_to_html(file)
        html_articles_list = article_list(html)
        for html_article in html_articles_list:
            current_article = create_article(html_article)
            if categories:
                current_article.categories = categories

            response = current_article.upload()
            if response:
                show_details(current_article)
            print(response.status_code, "\n")


def single(docx_files, categories):
    for file in docx_files:
        print("processing ", file)
        html = convert_to_html(file)
        article = create_article(html)
        if categories:
            article.categories = categories

        response = article.upload()
        if response:
            show_details(article)
        print(response.status_code, "\n")


if __name__ == "__main__":
    default_setup = "single"
    if len(sys.argv) < 2:
        print("Usage: python matic.py <path to directory> [article setup]")
        print("For article setup:")
        print("Single - for one article per .docx file")
        print("Multiple - for multiple articles per .docx file")
    else:
        doxc_files = search_docx_files(sys.argv[1])
        setup = sys.argv[2] if len(sys.argv) > 2 else default_setup
        categories = sys.argv[3:] if len(sys.argv) > 3 else None
        if setup == "single":
            single(doxc_files, categories)
        elif setup == "multiple":
            multiple(doxc_files, categories)
