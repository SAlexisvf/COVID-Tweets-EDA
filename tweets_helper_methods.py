import matplotlib.pyplot as plt
import re
from textblob import TextBlob
from wordcloud import WordCloud

def preprocess_dataframe(df):
    # keep only the english tweets
    df = df[df.lang == "en"].reset_index(drop = True)
    # remove links, hashtags, punctuation, mentions, etc (text normalization).
    for i in range(df.shape[0]):
        df['text'][i] = ' '.join(re.sub("(RT @[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(#[A-Za-z0-9]+)", " ", df['text'][i]).split()).lower()
    # since retweets are count as tweets, we need to drop duplicates
    df = df.drop_duplicates(subset='text', keep="first").reset_index()

    return df

def sentiment_analysis(df):
    df['sentiment'] = None
    df['polarity'] = None

    for i, tweet in enumerate(df['text']) :
        blob = TextBlob(tweet)
        df['polarity'][i] = blob.sentiment.polarity
        if blob.sentiment.polarity > 0 :
            df['sentiment'][i] = 'positive'
        elif blob.sentiment.polarity < 0 :
            df['sentiment'][i] = 'negative'
        else :
            df['sentiment'][i] = 'neutral'

    return df

def generate_emotion(df):
    df['emotion'] = None
    for i, polarity in enumerate(df['polarity']):
        if polarity == 1:
            df['emotion'][i] = 'Happy and joy'
        elif polarity >= 0.8 and polarity < 1:
            df['emotion'][i] = 'Confident'
        elif polarity >= 0.6 and polarity < 0.8:
            df['emotion'][i] = 'Optimistic'
        elif polarity >= 0.4 and polarity < 0.6:
            df['emotion'][i] = 'Hopeful'
        elif polarity >= 0.2 and polarity < 0.4:
            df['emotion'][i] = 'Calm and content'
        elif polarity >= -0.2 and polarity < 0:
            df['emotion'][i] = 'Relieved'
        elif polarity >= -0.4 and polarity < -0.2:
            df['emotion'][i] = 'Pessimistic and impatient'
        elif polarity >= -0.6 and polarity < -0.4:
            df['emotion'][i] = 'Worry and boredom'
        elif polarity >= -0.8 and polarity < -0.6:
            df['emotion'][i] = 'Discouraged and difficulty'
        elif polarity == -1:
            df['emotion'][i] = 'Depressed and fear'
        else:
            df['emotion'][i] = 'Neutral and relaxed'
        
    return df


def print_top_five(df, category):
    df = df[[category,'text']].sort_values(category,ascending = False)[:5].reset_index()
    print('Top 5 ' + category)
    for i in range(5):
        print()
        print(category + ': ' + str(df[category][i]))
        print(df['text'][i])

def generate_wordcloud(data):
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(str(data))
    
    fig = plt.figure(1, figsize=(15, 15))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()  