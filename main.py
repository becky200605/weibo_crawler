from spiders.hot_search import get_hot_research
from spiders.get_contents import get_keyword_posts
from processor.db import Database
from processor.postsmodel import search_posts_by_keyword,save_keyword_to_db,save_posts_to_db,get_all_posts,insert_sentiment_to_db
from models.analysis import analyze_sentiment, extract_keywords
from models.visualize import plot_sentiments,generate_wordcloud

def main():
    db= Database()
    keywords= get_hot_research()  # 获取热搜关键词
    save_keyword_to_db(db, keywords)  # 保存关键词到数据库
    print("🤖热搜关键词已保存到数据库")

    for item in keywords:
        keyword = item['keyword']
        url = item['url']
        print(f"正在获取关键词 '{keyword}' 的帖子...")
        posts=get_keyword_posts(url, keyword, maxposts=100)
        if posts:
            save_posts_to_db(db, posts)
            print(f"关键词 '{keyword}' 的'{len(posts)}'个帖子已保存到数据库。")
    print("所有关键词的帖子已获取完毕。")
    posts=get_all_posts(db)
    print(posts[:3])
    print(f"🐛现在对{len(posts)}进行情感分析。。。")
    posts= analyze_sentiment(posts)  # 分析情感
    for post in posts:
        insert_sentiment_to_db(db, post['id'], post['sentiment'])
    print("情感分析已完成。")
    posts=extract_keywords(posts)
    print("关键词提取已完成。")
    plot_sentiments(posts)  # 可视化情感分析结果
    generate_wordcloud(posts)  # 可视化关键词提取结果


    db.close()

if __name__ == "__main__":
    main()
