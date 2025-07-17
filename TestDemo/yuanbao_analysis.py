import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import jieba
import os

import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 1. 数据加载
def load_data(filepath):
    df = pd.read_excel(filepath)
    return df

# 2. 数据清洗与预处理
def clean_data(df):
    # 去除重复
    df = df.drop_duplicates()
    # 处理缺失值
    df = df.dropna(subset=['评论'])
    # 评分转为数值型
    df['评分'] = pd.to_numeric(df['评分'], errors='coerce')
    # 评论时间格式化
    df['评论时间'] = pd.to_datetime(df['评论时间'], errors='coerce')
    # 去除无效评论（如纯空格、纯表情等）
    df = df[df['评论'].str.strip().astype(bool)]
    return df

# 3. 数据探索（基本信息、唯一值检查、值计数等）
def explore_data(df):
    print('数据基本信息:')
    print(df.info())
    print('\n字段唯一值数量:')
    print(df.nunique())
    print('\n评分分布:')
    print(df['评分'].value_counts())
    print('\n版本分布:')
    print(df['版本号'].value_counts())
    print('\n设备分布:')
    print(df['设备'].value_counts().head(10))
    print('\n评论长度分布:')
    df['评论长度'] = df['评论'].apply(len)
    print(df['评论长度'].describe())

# 4. 数据分析与可视化
def analyze_and_visualize(df, output_dir='analysis_output'):
    os.makedirs(output_dir, exist_ok=True)
    # 评分分布
    plt.figure(figsize=(6,4))
    sns.countplot(x='评分', data=df, order=sorted(df['评分'].dropna().unique()))
    plt.title('评分分布')
    plt.savefig(os.path.join(output_dir, 'score_dist.png'))
    plt.close()
    # 版本分布
    plt.figure(figsize=(8,4))
    df['版本号'].value_counts().head(10).plot(kind='bar')
    plt.title('主流版本分布')
    plt.savefig(os.path.join(output_dir, 'version_dist.png'))
    plt.close()
    # 评论长度分布
    plt.figure(figsize=(6,4))
    df['评论长度'].hist(bins=30)
    plt.title('评论长度分布')
    plt.savefig(os.path.join(output_dir, 'comment_length.png'))
    plt.close()
    # 词云
    text = ' '.join(jieba.cut(' '.join(df['评论'].astype(str))))
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(font_path='msyh.ttc', width=800, height=400, stopwords=stopwords, background_color='white').generate(text)
    wordcloud.to_file(os.path.join(output_dir, 'wordcloud.png'))
    # 时间分布
    plt.figure(figsize=(10,4))
    df['评论时间'].dt.date.value_counts().sort_index().plot()
    plt.title('评论数量随时间变化')
    plt.savefig(os.path.join(output_dir, 'time_trend.png'))
    plt.close()

# 5. 高级分析（情感分析、主题建模等可扩展）
def advanced_analysis(df, output_dir='analysis_output'):
    # 简单情感分析（基于关键词，实际可用snownlp、paddleNLP等中文情感包）
    from snownlp import SnowNLP
    df['情感分'] = df['评论'].apply(lambda x: SnowNLP(str(x)).sentiments)
    plt.figure(figsize=(6,4))
    df['情感分'].hist(bins=30)
    plt.title('评论情感分布')
    plt.savefig(os.path.join(output_dir, 'sentiment_dist.png'))
    plt.close()
    # 输出负面评论高频词
    neg_comments = df[df['情感分'] < 0.4]['评论']
    neg_text = ' '.join(jieba.cut(' '.join(neg_comments.astype(str))))
    neg_wordcloud = WordCloud(font_path='msyh.ttc', width=800, height=400, stopwords=STOPWORDS, background_color='white').generate(neg_text)
    neg_wordcloud.to_file(os.path.join(output_dir, 'neg_wordcloud.png'))

# 6. 自动化报告生成
def generate_report(output_dir='analysis_output'):
    with open(os.path.join(output_dir, 'report.md'), 'w', encoding='utf-8') as f:
        f.write('# 元宝APP用户评论数据分析报告\n')
        f.write('## 评分分布\n![](score_dist.png)\n')
        f.write('## 版本分布\n![](version_dist.png)\n')
        f.write('## 评论长度分布\n![](comment_length.png)\n')
        f.write('## 评论数量随时间变化\n![](time_trend.png)\n')
        f.write('## 评论词云\n![](wordcloud.png)\n')
        f.write('## 评论情感分布\n![](sentiment_dist.png)\n')
        f.write('## 负面评论高频词云\n![](neg_wordcloud.png)\n')
        f.write('\n> 本报告由自动化脚本生成，供产品优化参考。\n')

if __name__ == '__main__':
    # 步骤1：加载数据
    df = load_data('yuanbao.xlsx')
    # 步骤2：清洗预处理
    df = clean_data(df)
    # 步骤3：数据探索
    explore_data(df)
    # 步骤4：分析与可视化
    analyze_and_visualize(df)
    # 步骤5：高级分析
    advanced_analysis(df)
    # 步骤6：自动化报告
    generate_report()
    print('分析完成，报告和图片已输出到 analysis_output 目录。') 