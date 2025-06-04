from playwright.sync_api import sync_playwright
from processor.postsmodel import save_posts_to_db
import re

def clean_posts_message(content):
    #提取所有的话题标签
    tags=re.findall(r"#(.*?)#", content)
    content=re.sub(r"#.*?#", "", content)  #去除话题标签
    content=re.sub(r"展开[cC]?","",content)  #去除展开提示词
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # 表情符
        "\U0001F300-\U0001F5FF"  # 符号 & 图形
        "\U0001F680-\U0001F6FF"  # 交通工具
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\u200b"                 # 零宽空格
        "]+", flags=re.UNICODE
    )
    content = emoji_pattern.sub(r'', content)  # 去除表情符号
    return tags,content


def get_keyword_posts(url,keyword,maxposts=3):
    result=[]
    with sync_playwright() as p:
     browser=p.chromium.launch(headless=True)
     context = browser.new_context(storage_state="storage/weibo_login_state.json")
     page=context.new_page()
     page.goto(url)
 
     while len(result)<maxposts:
        try:
          page.wait_for_selector("[action-type=feed_list_item] div.content [node-type=feed_list_content]")
        except:
           print("页面加载失败")
           page.screenshot(path="debug.png")
           break
        post_elementws=page.query_selector_all("[action-type=feed_list_item] div.content [node-type=feed_list_content]")

        #将爬取的帖子正文存储到result中
        for elem in post_elementws:
           content=elem.inner_text()
           tags,content=clean_posts_message(content)
           if content and content not in result:
              result.append({
                  "keyword": keyword,
                  "content": content,
                  "tags": ",".join(tags)
              })
           if len(result)>=maxposts:
              break
        
        #检测是否存在下一页
        next_btn=page.query_selector("a.next")
        if next_btn and "disabled" not in next_btn.get_attribute("class"):
          next_btn.click()
          page.wait_for_timeout(3000)  # 等页面初步加载

        else:
           break
     browser.close()
     return result
