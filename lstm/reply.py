import pickle
import itertools
import numpy as np

# TODO: Fetch this from a new `data` module.
data = pickle.load(open('test.pkl', 'rb'))


import seq2seq
from seq2seq.models import SimpleSeq2seq

model = SimpleSeq2seq(input_dim=1, hidden_dim=12, output_length=8, output_dim=1, depth=1)
model.compile(loss='mse', optimizer='rmsprop')

X = np.zeros((256, 8, 1), dtype=np.float32)
X[:,:,0] = list(itertools.product([0.0, 1.0], repeat=8))

model.fit(X, X, batch_size=32, nb_epoch=1000, verbose=1)

y = model.predict(X)

# for i in range(256):
#     print(X[i,:,0], y[i,:,0] > 0.5)
