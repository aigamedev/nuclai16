import pickle
import re

STX = u"\2"
ETX = u"\3"
UNK = u"\4"
MINLEN = 40

def read(filename):
    all_tweets = set()
    text = ""
    count = 0
    with open(filename, 'rb') as f:
        to_serialize = pickle.load(f)
        for t in to_serialize:
            try:
                tweet = t['tweet']['text']
            except:
                tweet = t['tweet'].text

            tweet = tweet.replace("RT ", "", 1).lower()
            if len(tweet) < MINLEN: continue # not a great input - trim it

            tweet = tweet.replace("| rt ", "")
            tweet = re.sub(r"http\S+[\W+]?", '', tweet) # remove links - they are not words
            tweet = re.sub(r"[rt]?@\S+[\W+]?", '', tweet) # remove nicks - not a words either

            tweet = tweet.strip()
            tweet = STX + tweet + ETX
            all_tweets.add(tweet)
            text += tweet
            count +=1
            if count == 100: continue

    chars = set(text)

    # remove extremas
    chars_frequncy = {}
    for c in  chars:
        chars_frequncy[c] = 0

    for c in text:
        chars_frequncy[c] += 1

    threshold = round(len(text) * 0.0005) # 0,05 % ? // why not

    text = ""
    tweets = []

    # replace unusual characters
    for t in all_tweets:
        for c in set(t):
            if chars_frequncy[c] <= threshold:
                t = t.replace(c, UNK)
        tweets.append(t)
        text += t

    chars = set(text)

    return (tweet, text, chars)
