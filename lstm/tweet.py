# This code was originally derived from Keras' LSTM examples.

import sys
import json
import random

from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.utils.data_utils import get_file

import h5py
import numpy as np

import data

maxlen = 40

# The tweet length should be above the learned sequence length.
tweets, text, chars = data.read('tweets78k.txt', minlen=maxlen)
print('Number of characters:', len(chars))

char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))


# Cut the text in semi-redundant sequences of maxlen characters.
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('Number of sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1.0
    y[i, char_indices[next_chars[i]]] = 1.0



def build_model(model_in=None, model_out=None):
    if model_in:
        print("Reading model...")
        with open(model_in+'.json', 'r') as model_file:
            model = model_from_json(model_file.read())

    else:
        print('Build model...')
        model = Sequential()
        model.add(LSTM(64, return_sequences=True, input_shape=(maxlen, len(chars))))
        model.add(Dropout(0.2))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(len(chars)))
        model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    if model_out:
        print("Saving model...")
        with open(model_out+'.json', 'w') as model_file:
            model_file.write(model.to_json())

    return model


def sample(a, temperature=1.0):
    # Helper function to sample an index from a probability array.
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1, a, 1))


def generate_tweets(model):
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('----- Diversity:', diversity)

        sentence = random.choice(tweets)[:maxlen-1] + data.STX
        print('----- Generating with seed: "' + sentence + '"')

        for i in range(140):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            sentence = sentence[1:] + next_char
            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()


def train(model):
    # Train the model, output generated text after each iteration.
    try: 

        for iteration in range(1, 50):
            print()
            print('-' * 50)
            print('Iteration', iteration)

            idx = np.random.randint(X.shape[0], size=100000)
            model.fit(X[idx], y[idx], batch_size=128, nb_epoch=1)
            generate_tweets(model)

    except KeyboardInterrupt:
        pass # quit nicely


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='nucl.ai16')
    parser.add_argument('--load', help='The name for model input file', default=None, type=str)
    parser.add_argument('--save', help='The name for model output file', default=None, type=str)
    parser.add_argument('--train', default=False, action='store_true')
    args = parser.parse_args()

    model = build_model(args.load, args.save)

    if args.load:
        print("Reading weights...")
        model.load_weights(args.load+'.h5f')

    if not args.train:
        generate_tweets(model)
        sys.exit(-1)

    train(model)
    if args.save:
        print("Saving weights...")
        model.save_weights(args.save+'.h5f')
