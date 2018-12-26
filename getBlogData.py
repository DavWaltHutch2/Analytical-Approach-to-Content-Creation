from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def get_blog_CNET (pages = 1):

    ##DEFINE LINKS
    url_home = "https://www.cnet.com"
    url_topics = url_home + "/topics/mobile/"

    ##DEFINE PAGE EXTENSIONS
    page_num = []
    for i in range(0,pages):
        num = i + 1
        page_num.append(str(num))


    ##VARIABLES
    blog_titles = []
    blog_links = []
    blog_dates = []
    for i in page_num:
        print(">>>>>  CNET Page: " + str(i))

        ##GET HTML
        url = url_topics + i  + "/"
        req = requests.get(url)
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        ##GET TITLES, LINKS, AND DATE
        assetBodys = soup.find_all("div",{"class":"assetBody"})
        for assetBody in assetBodys:
            blog_titles.append(assetBody.find("h2").get_text().strip())
            blog_links.append(url_home + assetBody.find("a")["href"])

            date = assetBody.find("time").get_text()
            date = date[0:len(date)-4]
            date = datetime.strptime(date, "%B %d, %Y %I:%M %p")
            blog_dates.append(date.strftime("%x"))



    blog_article = []
    for link in blog_links:
        ##article_link = url_home + link
        article_link = link
        print(article_link)

        ##GET HTML
        req = requests.get(article_link)
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        ##GET TITLES
        if (soup.find("div",{"class":"article-main-body"})):
            p = soup.find("div",{"class":"article-main-body"}).find_all("p")
            temp = ""
            for p_tag in p:
                temp = temp + " " + p_tag.get_text().strip()
            blog_article.append(temp)

        elif(soup.find("article", {"id": "cnetReview"})):
            p = soup.find("article", {"id": "cnetReview"}).find_all("p")
            temp = ""
            for p_tag in p:
                temp = temp + " " + p_tag.get_text().strip()
            blog_article.append(temp)

        else:
            print("NO CONTENT TO SCRAPE")
            blog_article.append("")


    blog_df = pd.DataFrame({"Source": "CNET","Title":blog_titles, "Date":blog_dates, "Links": blog_links, "Article": blog_article})
    blog_df = blog_df[blog_df.Article != ""]

    return blog_df


def get_blog_VERGE (pages = 1):

    ##DEFINE LINKS
    url_home = "https://www.theverge.com"
    url_topics = url_home + "/tech/archives/"

    ##DEFINE PAGE EXTENSIONS
    page_num = []
    for i in range(0,pages):
        num = i + 1
        page_num.append(str(num))


    ##VARIABLES
    blog_titles = []
    blog_links = []
    for i in page_num:
        print(">>>>>  Verge Page: " + str(i))

        ##GET HTML
        url = url_topics + i
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")


        ##GET TITLES AND LINKS
        divs = soup.find_all("div",{"class":"c-entry-box--compact__body"})
        for div in divs:
            a= div.find("a")
            blog_titles.append(a.get_text().strip())
            blog_links.append(a.get("href"))


    blog_article = []
    blog_dates = []
    for link in blog_links:
        article_link = link
        print(article_link)
        req = requests.get(article_link, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        ##GET ARTICLE
        if soup.find("div", {"class":"c-entry-content"}):
            div = soup.find("div", {"class":"c-entry-content"})
            ps = div.find_all("p")
            temp = ""
            for p in ps:
                temp = temp + " " + p.get_text()
            blog_article.append(temp)
        else:
            print("NO CONTENT TO SCRAPE")
            blog_article.append("")

        ##GET TIME
        if soup.find("time"):
            date = soup.find("time").get_text().strip()[0:-4]
            date = datetime.strptime(date, "%b %d, %Y, %I:%M%p")
            blog_dates.append(date.strftime("%x"))
        else:
            blog_dates.append(None)

    blog_df = pd.DataFrame({"Source": "VERGE", "Title": blog_titles, "Date":blog_dates, "Links": blog_links, "Article": blog_article})
    blog_df = blog_df[blog_df.Article != ""]
    return blog_df


def get_blog_GADGETS(pages = 1):
    ##DEFINE LINKS
    url_home = "https://gadgets.ndtv.com"
    url_topics = url_home + "/mobiles/news/page-"

    ##DEFINE PAGE EXTENSIONS
    page_nums = []
    for i in range(0,pages):
        num = i + 1
        page_nums.append(str(num))


    ##VARIABLES
    blog_titles = []
    blog_links = []
    blog_dates = []
    for page_num in page_nums:
        print(">>>>>  Gadgets Page: " + page_num)

        ##GET HTML
        url = url_topics + page_num
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        divs = soup.find_all("div", {"class":"caption_box"})
        for div in divs:

            ##GET TITLE AND LINK
            a= div.find("a")
            blog_titles.append(a.get_text().strip())
            blog_links.append(a.get("href"))

            ##GET DATE
            div_dateline = div.find("div", {"class":"dateline"})
            blog_date = div_dateline.get_text().strip()
            blog_date = blog_date.split(",")[1].strip()
            blog_date = datetime.strptime(blog_date, "%d %B %Y")
            blog_dates.append(blog_date.strftime("%x"))


    ##GET ARTICLE
    blog_article = []
    for link in blog_links:
        print(link)
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        story_detail = soup.find("div", {"class","story_detail"})
        ps = story_detail.find_all("p")
        temp = ""
        for p in ps:
            if not p.find("style"):  ##EXCLUDE STYLES
                text = p.get_text() + " "
                temp = temp + text
            else:
                ##print(">> Excluding: " + p.get_text())
                pass
        blog_article.append(temp)


    ##COMBINE DATA TO CREATE DATAFRAME
    blog_df = pd.DataFrame({"Source":"GADGETS","Title": blog_titles, "Date":blog_dates, "Links": blog_links, "Article": blog_article})

    ##RETUNR DATA
    return blog_df


def get_blog_ZDNET(pages = 1):
    ##DEFINE LINKS
    url_home = "https://www.zdnet.com/blog/cell-phones/"
    url_topics = url_home ##FOR SYNTAX PURPOSE

    ##DEFINE PAGE EXTENSIONS
    page_nums = []
    for i in range(0, pages):
        num = i + 1
        page_nums.append(str(num))

    ##VARIABLES
    blog_titles = []
    blog_links = []
    blog_dates = []
    for page_num in page_nums:
        print(">>>>>  ZDNET Page: " + str(i))

        ##GET HTML
        url = url_topics + page_num
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")



        articles = soup.find_all("article", {"class": "item"})
        for article in articles:
            ##GET TITLE
            a = article.find("h3").find("a")
            blog_titles.append(a.get_text().strip())

            ##GET LINK
            site_home = "https://www.zdnet.com"
            blog_links.append(site_home + a.get("href"))

            ##GET DATE
            blog_date = article.find("p", {"class": "meta"}).find("span")["data-date"]
            blog_date = datetime.strptime(blog_date, "%Y-%m-%d %H:%M:%S")
            blog_dates.append(blog_date.strftime("%x"))


    ##GET ARTICLE
    blog_article = []
    for link in blog_links:
        print(link)
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        contents =""
        if soup.find("div", {"class","storyBody"}):
            ##print("Article")
            storyBody = soup.find("div", {"class","storyBody"})
            contents = storyBody.find_all(["p","h3"])
        else:
            ##print("Gallery")
            gallery_data = soup.find("div",{"class", "gallery-data"}).find("div",{"class","galleryBody"})
            contents = gallery_data.find_all("p")

        temp = ""
        for content in contents:
            text = content.get_text().strip() + " "
            temp = temp + text

        blog_article.append(temp)

    ##COMPILE DATA
    blog_df = pd.DataFrame({"Source":"ZDNet", "Title": blog_titles, "Date":blog_dates, "Links": blog_links, "Article": blog_article})


    ##RETUNR DATA
    return blog_df

def get_blog_ANDROIDPOLICE(pages = 1):
    ##DEFINE LINKS
    url_home = "https://www.androidpolice.com/"
    url_topics = url_home ##FOR SYNTAX PURPOSE

    ##DEFINE PAGE EXTENSIONS
    page_nums = []
    for i in range(0, pages):
        num = i + 1
        page_nums.append(str(num))

    ##VARIABLES
    blog_titles = []
    blog_links = []
    blog_dates = []
    for page_num in page_nums:
        print(">>>>>  Android Police Page: " + str(page_num))

        ##GET HTML
        url = url_topics + "/page/"+page_num
        ##print(url)
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        articles = soup.find_all("div", {"class": "post"})
        for article in articles:
            ##GET TITLE
            a = article.find("h2").find("a")
            blog_titles.append(a.get_text().strip())

            ##GET LINK
            blog_links.append(a.get("href"))

            ##GET DATE
            blog_date = article.find("time", {"class": "timeago-hover"}).get_text().strip()
            blog_date = datetime.strptime(blog_date[0:-4], "%Y/%m/%d %I:%M%p")
            blog_dates.append(blog_date.strftime("%x"))


    ##GET ARTICLE
    blog_article = []
    for link in blog_links:
        print(link)
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        contents = ""
        ps =  soup.find("div", {"class", "post-content"}).find_all("p")
        for p in ps:
            contents = contents + " " + p.get_text().strip()

        blog_article.append(contents)

    ##REURN DATA
    blog_df = pd.DataFrame({"Source":"Android Police", "Title": blog_titles, "Date":blog_dates, "Links": blog_links, "Article": blog_article})
    return(blog_df)

def get_blog_APPLEINSIDER(pages = 2):
    ##DEFINE LINKS
    ##http://appleinsider.com/
    url_home = "http://appleinsider.com"
    url_topics = url_home

    ##DEFINE PAGE EXTENSIONS
    page_nums = []
    for i in range(0, pages):
        num = i + 1
        page_nums.append(str(num))

    ##VARIABLES
    blog_titles = []
    blog_links = []
    for page_num in page_nums:
        print(">>>>>  Apple Insider Page: " + str(page_num))

        ##GET HTML
        url = url_topics + "/page/"+page_num
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        ##GET FIRST SET OF TITLES AND LINKS
        articles = soup.find_all("div", {"class": "post"})
        for article in articles:
            ##GET TITLE
            a = article.find("h1").find("a")
            blog_titles.append(a.get_text().strip())

            ##GET LINK
            blog_links.append("https:" + a.get("href"))

        ##GET SECOND SET OF TITLES AND LINKS
        lis = soup.find("ul", {"class": "rel-full"}).find_all("li", {"class":"index_river"})
        for li in lis:
            ##GET TITLE
            a = li.find("a")
            blog_titles.append(a.get_text().strip())

            ##GET LINK
            blog_links.append("https:" +  a["href"])


    ##GET DATES AND ARTICLE
    blog_article = []
    blog_dates =[]
    for link in blog_links:
        ##CREATE SOUP
        print(link)
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        site_html = req.text  ##READING ISSUES TYPE "chcp 65001" IN TERMINAL
        soup = BeautifulSoup(site_html, "html5lib")

        ##GET DATE
        blog_date = soup.find("div", {"class": "article"}).find("span",{"class":"gray"}).get_text().strip()[0:-16].strip()
        blog_date = datetime.strptime(blog_date, "%A, %B %d, %Y, %I:%M %p")
        blog_dates.append(blog_date.strftime("%x"))


        ##GET ARTILCE
        article =  soup.find("div", {"class": "article"})
        [x.extract() for x in article('br')]
        [x.extract() for x in article('div')]
        [x.extract() for x in article('h1')]
        [x.extract() for x in article('p')]
        blog_article.append(article.get_text().strip())


    ##RETURN DATA
    blog_df = pd.DataFrame({"Source":"Apple Insider", "Title": blog_titles, "Date":blog_dates, "Links": blog_links, "Article": blog_article})
    return(blog_df)

def get_blogData():
    CNET = True
    VERGE = True
    GADGET = True
    ZDNET = True
    ANDROIDPOLICE = True
    APPLEINSIDER = True

    data_all = []
    if CNET:
        data_all.append(get_blog_CNET(5))

    if VERGE:
        data_all.append(get_blog_VERGE(2))

    if GADGET:
        data_all.append(get_blog_GADGETS(8))

    if ZDNET:
        data_all.append(get_blog_ZDNET(2))

    if ANDROIDPOLICE:
        data_all.append(get_blog_ANDROIDPOLICE(8))

    if APPLEINSIDER:
        data_all.append(get_blog_APPLEINSIDER(2))

    data = pd.concat(data_all, ignore_index=True)
    return(data)


##READING ISSUES TYPE "chcp 65001" IN TERMINAL
def main():
    data = get_blogData()
    data.to_csv("./data/blogData_delete.csv", index = False)







if __name__ == "__main__":
    main()


