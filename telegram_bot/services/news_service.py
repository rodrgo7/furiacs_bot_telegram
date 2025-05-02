import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser as date_parser
import os
import logging

def get_latest_gnews_news():
    """Fetch latest news from GNews API."""
    try:
        api_key = os.getenv("GNEWS_API_KEY")
        if not api_key:
            return None

        url = f"https://gnews.io/api/v4/search?q=FURIA&lang=pt&token={api_key}"
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        if not articles:
            return None

        for article in articles:
            if "FURIA" in article.get("title", "").upper():
                return {
                    "title": article["title"],
                    "link": article["url"],
                    "date": date_parser.parse(article["publishedAt"])
                }

        return None
    except Exception as e:
        logging.error(f"Erro GNews: {e}")
        return None

def get_latest_hltv_news():
    """Fetch latest news from HLTV."""
    try:
        url = "https://www.hltv.org/team/8297/furia#tab-newsBox"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='newsline article')

        for article in articles:
            title_tag = article.find('a', class_='newsline article-title')
            date_tag = article.find('div', class_='article-time')

            if title_tag and "FURIA" in title_tag.text.upper():
                link = "https://www.hltv.org" + title_tag['href']
                if date_tag:
                    try:
                        date = date_parser.parse(date_tag.text.strip())
                    except:
                        date = datetime.now()
                else:
                    date = datetime.now()
                return {"title": title_tag.text.strip(), "link": link, "date": date}
        return None
    except Exception as e:
        logging.error(f"Erro HLTV: {e}")
        return None

def get_latest_dust2_news():
    """Fetch latest news from Dust2."""
    try:
        url = "https://www.dust2.com.br"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='news-item')

        for article in articles:
            title_tag = article.find('h2', class_='title')
            date_tag = article.find('div', class_='info')

            if title_tag and "FURIA" in title_tag.text.upper():
                link_tag = article.find('a')
                link = "https://dust2.com.br" + link_tag['href']
                raw_date = date_tag.text.strip() if date_tag else ""

                if "há" in raw_date or "atrás" in raw_date:
                    date = datetime.now()
                else:
                    try:
                        date = date_parser.parse(raw_date, dayfirst=True)
                    except:
                        date = datetime.now()
                return {"title": title_tag.text.strip(), "link": link, "date": date}
        return None
    except Exception as e:
        logging.error(f"Erro Dust2: {e}")
        return None

def get_most_recent_news():
    """Get the most recent news from all sources."""
    hltv = get_latest_hltv_news()
    dust2 = get_latest_dust2_news()
    gnews = get_latest_gnews_news()

    sources = [news for news in [hltv, dust2, gnews] if news is not None]

    if not sources:
        return (
            "📰 FURIA, MIBR, ODDIK e paiN conhecem adversários da estreia na PGL Astana 2025\n"
            "🔗 https://draft5.gg/noticia/furia-mibr-oddik-e-pain-conhecem-adversarios-da-estreia-na-pgl-astana-2025"
        )

    sources.sort(key=lambda x: x['date'], reverse=True)
    latest = sources[0]
    return f"📰 {latest['title']} 🔗 {latest['link']}" 