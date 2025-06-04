from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['PingFang SC', 'STHeiti', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def generate_wordcloud(posts):
    """
    从所有帖子中汇总关键词，生成一个长文本
    """
    all_keywords = []
    for post in posts:
        all_keywords.extend(post.get('key_words', []))
    if not all_keywords:
        print("没有关键词可用于生成词云")
        return
    text = ' '.join(all_keywords)
    #创建词云对象
    wordcloud = WordCloud(width=800, height=400, background_color='white',font_path='/System/Library/Fonts/PingFang.ttc').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.title('关键词词云',fontsize=16)
    plt.tight_layout()
    plt.savefig('wordcloud.png')
    print("词云已生成并保存为wordcloud.png")
    plt.close()

def plot_sentiments(posts):
    """
    绘制情感分数的柱状图
    """
    keyword_sentiments = {}
    for post in posts:
        keyword = post.get('keyword', '未知关键词')
        sentiment = post.get('sentiment', 0.5)  # 默认情感分数为0.5
        if keyword not in keyword_sentiments:
            keyword_sentiments[keyword] = []
        keyword_sentiments[keyword].append(sentiment)
    avg_sentiments_by_type = {}
    for t,scores in keyword_sentiments.items():
        avg_sentiments_by_type[t] = sum(scores) / len(scores)
    types = list(avg_sentiments_by_type.keys())
    scores = list(avg_sentiments_by_type.values())

    color=[]
    for score in scores:
        if score < 0.5:
            color.append('red')  # 负面情感
        elif score ==0.5:
            color.append('orange')  # 中性情感
        else:
            color.append('green')  # 正面情感

    # 绘制柱状图
    plt.figure(figsize=(12, 6))
    plt.bar(avg_sentiments_by_type.keys(), avg_sentiments_by_type.values(), color=color)
    plt.xlabel('关键词', fontsize=14)
    plt.ylabel('平均情感分数', fontsize=14)
    plt.title('关键词平均情感分数', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 1)  # 情感分数范围从0到1
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()  # 自动调整布局
    plt.savefig('sentiment_analysis.png')
    print("情感分析柱状图已生成并保存为sentiment_analysis.png")
    plt.close()