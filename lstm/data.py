import pickle
import re

STX = u"\2"
ETX = u"\3"
UNK = u"\4"

def read(filename, minlen=40, maxlen=None, padding=None):
    all_tweets = set()
    text = ""
    with open(filename, 'rb') as f:
        to_serialize = pickle.load(f)
        for t in to_serialize:
            try:
                tweet = t['tweet']['text']
            except:
                tweet = t['tweet'].text

            tweet = tweet.replace("RT ", "", 1).lower()
            tweet = tweet.replace("| rt ", "")
            tweet = re.sub(r"http\S+[\W+]?", '', tweet) # remove links - they are not words
            tweet = re.sub(r"[rt]?@\S+[\W+]?", '', tweet) # remove nicks - not a words either
            tweet = tweet.strip()
            tweet = STX + tweet + ETX
            if len(tweet) < minlen: continue # not a great input - trim it
            if maxlen != None and len(tweet) > maxlen: continue # too long
            if padding:
                pad = '{:' + padding + '<' + str(maxlen) + '}'
                tweet = pad.format(tweet)
            all_tweets.add(tweet)
            text += tweet

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

    return (tweets, text, chars)