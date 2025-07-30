import os
import re
import sys
from article import Article
from article import Post


def search_docx_files(path_to_directory):
    directory = path_to_directory
    for root, directories, files in os.walk(directory):
        if len(files) == 0:
            return
        return [(root + "/" + file) for file in files if file.endswith(".docx")]


def article_list(html_file):
    articles = re.split(r"<p>--+</p>", html_file)
    return articles


def multiple(docx_files):
    for file in docx_files:
        temp = Article.convert_to_html(file)
        html_articles_list = article_list(temp)
        for html_article in html_articles_list:
            current_article = Article(html_file=html_article)
            current_post = Post(current_article.article)
            current_post.show_details()
            current_post.upload_post()
            print("*" * 5)
            # break #uncomment for checking


def single(docx_files):
    for file in docx_files:
        print("processing ", file)
        current_article = Article(filepath=file).article
        current_post = Post(current_article)
        current_post.show_details()
        current_post.upload_post()
        print("*" * 5)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python matic.py <path to directory> <article setup>")
        print("Note: article setup can either be 'single' or 'multiple'")
    elif len(sys.argv) == 3:
        doxc_files = search_docx_files(sys.argv[1])
        if (sys.argv[2]) == "single":
            single(doxc_files)
        elif (sys.argv[2]) == "multiple":
            multiple(doxc_files)
