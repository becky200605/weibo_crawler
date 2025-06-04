from playwright.sync_api import sync_playwright
from processor.postsmodel import save_keyword_to_db 


def get_hot_research():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()

        #打开热搜榜
        url="https://s.weibo.com/top/summary"
        page.goto(url)
        page.wait_for_selector("tbody tr")
        rows=page.query_selector_all("tbody tr")[1:16]
        results=[]
        for i,row in enumerate(rows,start=1):
            rank=row.query_selector("td.td-01").inner_text().strip()
            if not rank.isdigit():
                continue
            keyword_element=row.query_selector("td.td-02 a")
            keyword=keyword_element.inner_text().strip()
            hot_url=keyword_element.get_attribute("href")
            full_url="https://s.weibo.com/"+hot_url

            results.append({
                "rank":rank,
                "keyword":keyword,
                "url":full_url
            })
        browser.close()
        return results



