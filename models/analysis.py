from snownlp import SnowNLP

def analyze_sentiment(posts):
    """
    分析文本情感，返回情感分数
    :param text: 输入文本
    :return: 情感分数，范围从0到1，0表示负面情绪，1表示正面情绪
    """
    for post in posts:
        content = post.get('content', '')
        if not post["content"]:
         post["sentiment"]=0.5  # 如果文本为空，返回中性情感分数
        else:
         s = SnowNLP(post["content"])
         post["sentiment"]=s.sentiments 
    return posts


#分词与高平次提取
def extract_keywords(posts):
    """
    提取文本中的关键词
    :param posts: 帖子列表
    :return: 每个帖子的关键词列表
    """
    for post in posts:
        content = post.get('content', '')
        if content:
            s = SnowNLP(content)
            keywords = s.keywords(5)  # 提取前5个关键词
            post['key_words'] = keywords
        else:
            post['key_words'] = []
    for i, post in enumerate(posts[:5]):  # 只打印前5条
     print(f"[第{i+1}条] 内容: {post['content']}")
     print(f"情感分数: {post['sentiment']}")
     print(f"关键词: {post['key_words']}\n")
    return posts


        
