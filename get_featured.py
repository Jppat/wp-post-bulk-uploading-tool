import requests
import datetime
from bs4 import BeautifulSoup
from tkinter import Tk


def display_article(article):
    # get body of article
    content = article["content"]["rendered"]

    # select title of article
    title = article["title"]["rendered"]

    # parse html object using beautiful soup
    parsed = BeautifulSoup(content, features="lxml")

    # locate all <p> tag objects
    paragraphs = parsed("p")

    # select only first three paragraphs
    first_three = paragraphs[0:3]

    # remove tags for each <p>
    pars = []
    for p in first_three:
        p = BeautifulSoup(str(p), features="lxml")
        p = p.get_text()
        # display selected body content
        pars.append(p)

    # display article and link
    print(title, "\n")
    print(article["link"], "\n")

    # copy above info to clipboard
    # put text in the right format
    clipboard = f"{title}\n\n" + "\n\n".join(pars) + f"\n\n{article['link']}"

    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(clipboard)
    r.update()  # now it stays on the clipboard after the window is closed
    r.destroy()


# get featured posts from pn
def getPosts(site):

    if site == 1:
        # query for posts under 'featured' cateogry posted on date_now
        url = "https://panaynews.net/wp-json/wp/v2"
        get_posts = requests.get(
            url + "/posts?categories=120&date={date_now}&per_page=30"
        )
    elif site == 2:
        # query latest posts from wdj
        url = "https://watchmendailyjournal.com/wp-json/wp/v2"
        get_posts = requests.get(url + "/posts?date={date_now}&per_page=30")
    elif site == 3:
        url = "https://panaynews.net/wp-json/wp/v2"
        get_posts = requests.get(url + "/posts?categories=43&per_page=10")

    # extract json file from above request
    featured_posts = get_posts.json()
    # print(type(featured_posts))

    current_index = 0

    while True:

        # prompt user with key intsructions
        print("")
        print(
            "Press Enter to proceed; type 'back' to browse back; otherwise type 'q' if you want to quit"
        )
        print("")

        article = featured_posts[current_index]
        display_article(article)

        key = input("Enter input: ")
        if key == "":
            current_index += 1
        elif key == "back":
            if current_index != 0:
                current_index -= 1
        elif key == "q":
            break


# get current date
date_now = datetime.datetime.now()

print("Press 1 for Panay News (featured)")
print("Press 2 for Watchmen")
print("Press 3 for Panay News (opinion)")

site = input("Enter choice: ")
getPosts(int(site))

# get all posts from watchmen issued on current date
# def get_wdj():
#     # query for posts under 'featured' cateogry posted on date_now
#     get_posts = requests.get(url + '/posts?date=date_now')

#     # extract json file from above request
#     featured_posts = get_posts.json()
#     # print(featured_posts)

#     for article in featured_posts:
#         # prompt user with key intsructions
#         print("")
#         print("Press Enter to proceed; otherwise type 'q' if you want to quit")
#         key = input("Enter input: ")
#         print("")

#         if(key==""):
#             # get body of article
#             content = article['content']['rendered']

#             # parse html object using beautiful soup
#             parsed = BeautifulSoup(content,features='lxml')

#             # locate all <p> tag objects
#             paragraphs = parsed("p")

#             # select only first three paragraphs
#             first_three = paragraphs[0:3]

#             # remove tags for each <p>
#             for p in first_three:
#                 p = BeautifulSoup(str(p), features="lxml")
#                 p = p.get_text()
#                 print(p)

#             print("")
#             print("link ", article['link'],"\n")

#         elif(key=='q'):
#             break

# def get_op_pn():
#     # query for posts under 'featured' cateogry posted on date_now
#     get_featured_posts = requests.get(url + '/posts?categories=43&per_page=10')

#     # extract json file from above request
#     featured_posts = get_featured_posts.json()
#     # print(featured_posts)

#     for article in featured_posts:
#         # prompt user with key intsructions
#         print("")
#         print("Press Enter to proceed; otherwise type 'q' if you want to quit")
#         print("Type o to get posts under Op")
#         key = input("Enter input: ")
#         print("")

#         if(key==""):
#             # get body of article
#             content = article['content']['rendered']

#             # parse html object using beautiful soup
#             parsed = BeautifulSoup(content,features='lxml')

#             # locate all <p> tag objects
#             paragraphs = parsed("p")

#             # select only first three paragraphs
#             first_three = paragraphs[0:3]

#             # remove tags for each <p>
#             for p in first_three:
#                 p = BeautifulSoup(str(p), features="lxml")
#                 p = p.get_text()
#                 print(p)

#             print("")
#             print(article['link'],"\n")

#         elif(key=='q'):
#             break
