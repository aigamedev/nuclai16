import pickle
import itertools
import numpy as np
import data

import seq2seq
from seq2seq.models import SimpleSeq2seq

MAXLEN = 40

tweets, text, chars = data.read('tweets75k.pickle', minlen=20, maxlen=MAXLEN, padding=" ", trim_hash=True, shorten=True)
chars_number = len(chars)
tweets_number = len(tweets)

model =  SimpleSeq2seq(input_dim=1, hidden_dim=12, output_length=8, output_dim=1, depth=1)
model.compile(loss='mse', optimizer='rmsprop')
X = np.zeros((tweets_number, MAXLEN, chars_number), dtype=np.float32)


model.fit(X, X, batch_size=32, nb_epoch=1000, verbose=1)

y = model.predict(X)

for i in range(0, 256, 9):
    print(X[i,:,0], y[i,:,0] > 0.5)
