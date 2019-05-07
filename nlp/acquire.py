from requests import get
from bs4 import BeautifulSoup
import json
import os

def get_blog_articles(fresh_take=False):
    if os.path.exists('blog_articles.json') and fresh_take == False:
        with open('blog_articles.json') as f:
            return json.load(f)

    sites = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/', 
             'https://codeup.com/data-science-myths/', 
             'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/', 
             'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/', 
             'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
    articles = []
    for site in sites:
        print(site)
        headers = {'User-Agent':'Codeup Ada Data Science'}
        response = get(site, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', class_='page-title ')
        article = soup.find('div', class_='mk-single-content')
        article_dict = {}
        article_dict['title'] = site.split('/')[-2].replace('-', '_')
        article_dict['body'] = article.text
        articles.append(article_dict) 
    with open('blog_articles.json', 'w') as blog:
        json.dump(articles, blog, indent=4)
    return articles

def get_news_articles(fresh_take=False):

    if os.path.exists('news_articles.json') and fresh_take == False:
        with open('news_articles.json') as f:
            return json.load(f) 
    sites = [
        'https://inshorts.com/en/read/business', 
        'https://inshorts.com/en/read/sports', 
        'https://inshorts.com/en/read/technology', 
        'https://inshorts.com/en/read/entertainment'
    ]
    articles = []
    for site in sites:
        response = get(site)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('span', itemprop='headline')
        content = soup.find_all('div', itemprop='articleBody')
        category = soup.find('li', class_='active-category selected').text
        for i in range(len(title)):
            article = {}
            article['title'] = title[i].text
            article['body'] = content[i].text
            article['category'] = category
            articles.append(article)
    with open('news_articles.json', 'w') as news:
        json.dump(articles, news, indent=4)
    return articles
