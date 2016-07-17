import sys
import itertools

import numpy as np
from seq2seq.models import SimpleSeq2seq

import data

MAXLEN = 40

tweets, text, chars = data.read('tweets78k.txt', minlen=20, maxlen=MAXLEN, trim_hash=True, shorten=True)
num_chars = len(chars)
num_tweets = len(tweets)

print('Number of characters:', len(chars))
print('Number of sequences:', len(tweets))


model =  SimpleSeq2seq(input_dim=num_chars, hidden_dim=256, output_length=MAXLEN, output_dim=num_chars, depth=1)
model.compile(loss='mse', optimizer='rmsprop')


char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))


print('Vectorization...')
X = np.zeros((num_tweets, MAXLEN, num_chars), dtype=np.float32)
for i, tweet in enumerate(tweets):
    sentence = list(itertools.chain(*itertools.repeat(tweet.replace('\4', '').replace('\2', '').replace('\3', ''), times=2)))[:MAXLEN]
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1.0

model.fit(X, X, batch_size=1024, nb_epoch=20, verbose=1)

y = model.predict(X[:8])

def sample(a, temperature=1.0):
    # Helper function to sample an index from a probability array.
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1, a, 1))

for i in range(8):
    print(y[i].shape)
    for t, a in enumerate(y[i]):
        j = sample(a+a.min(), temperature=1.0)
        # print(j, end=' ')
        print(ord(indices_char[j]), end=' ')
        sys.stdout.write(indices_char[j])
    sys.stdout.write('<END>\n')
    sys.stdout.flush()

