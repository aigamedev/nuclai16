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

# the minlen for tweet must be >= then maxlen defined for subsequences, otherwise we won't be able to build them.
tweets, text, chars = data.read('tweets78k.txt', minlen=maxlen)

print('total chars:', len(chars))

char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

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
        with open(model_in, 'r') as model_file:
            model = model_from_json(model_file.read())

    else:
        # build the model: 2 stacked LSTM
        print('Build model...')
        model = Sequential()
        model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, len(chars))))
        model.add(Dropout(0.2))
        model.add(LSTM(512, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(len(chars)))
        model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    if model_out:
        print("Saving model...")
        with open(model_out, 'w') as model_file:
            model_file.write(model.to_json())

    return model

def train(model, weights_in=None, weights_out=None):

    def sample(a, temperature=1.0):
        # helper function to sample an index from a probability array
        a = np.log(a) / temperature
        a = np.exp(a) / np.sum(np.exp(a))
        return np.argmax(np.random.multinomial(1, a, 1))

    if weights_in:
        print("Reading weights...")
        model.load_weights(weights_in)

    # train the model, output generated text after each iteration
    try: 

        for iteration in range(1, 60):
            print()
            print('-' * 50)
            print('Iteration', iteration)
            model.fit(X, y, batch_size=128, nb_epoch=1)

            start_index = random.randint(0, len(text) - maxlen - 1)

            for diversity in [0.2, 0.5, 1.0, 1.2]:
                print()
                print('----- diversity:', diversity)

                generated = ''

                sentence = random.choice(tweets)[:maxlen-1] + data.STX
                #generated += sentence
                print('----- Generating with seed: "' + sentence + '"')
                sys.stdout.write(generated)

                for i in range(140):
                    x = np.zeros((1, maxlen, len(chars)))
                    for t, char in enumerate(sentence):
                        x[0, t, char_indices[char]] = 1.

                    preds = model.predict(x, verbose=0)[0]
                    next_index = sample(preds, diversity)
                    next_char = indices_char[next_index]

                    generated += next_char
                    sentence = sentence[1:] + next_char

                    sys.stdout.write(next_char)
                    sys.stdout.flush()
                print()

    except KeyboardInterrupt:
        pass # quit nicely

    if weights_out:
        print("Saving weights...")
        model.save_weights(weights_out)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='nucl.ai16')
    parser.add_argument('--model-in', help='The name for model input file', default=None, type=str)
    parser.add_argument('--model-out', help='The name for model output file', default=None, type=str)
    parser.add_argument('--weights-in', help='The name for model weights input file', default=None, type=str)
    parser.add_argument('--weights-out', help='The name for model weights output file', default=None, type=str)
    args = parser.parse_args()

    model = build_model(args.model_in, args.model_out)
    train(model, args.weights_in, args.weights_out)

