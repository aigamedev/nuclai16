import re
import collections

STX = u"\2"
ETX = u"\3"
UNK = u"\4"

def read(filename, minlen=40, maxlen=None, trim_hash=False, shorten=False):
    all_tweets = set()
    text = ""
    with open(filename, 'r', encoding='utf8') as f:
        for t in f.readlines():
            tweet = STX + t.strip() + ETX
            if trim_hash: tweet = re.sub(r"#\S+[\W+]?", '', tweet) # remove hash - not a word
            if shorten and len(tweet) > maxlen:
                i = 1
                tweet_shorten = tweet[:len("".join(tweet.split(".")[:i])) + i]
                while len(tweet[:len("".join(tweet.split(".")[:i + 1])) + i ]) < maxlen:
                    i += 1
                    tweet_shorten = tweet[:len("".join(tweet.split(".")[:i])) + i]
                tweet = tweet_shorten
            if len(tweet) < minlen: continue # not a great input - trim it
            if maxlen != None and len(tweet) > maxlen: continue # too long
            all_tweets.add(tweet)
            text += tweet

    chars = set(text)

    # Remove extremely infrequent characters.
    chars_frequency = collections.Counter(text)
    threshold = round(len(text) * 0.0005) # 0,05%

    text = ""
    tweets = []

    # Replace unusual characters.
    for t in all_tweets:
        for c in set(t):
            if chars_frequency[c] <= threshold:
                t = t.replace(c, UNK)
        tweets.append(t)
        text += t

    chars = sorted(list(set(text)))
    return (tweets, text, chars)
