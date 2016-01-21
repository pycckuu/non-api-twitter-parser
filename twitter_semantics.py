import csv
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
# from tweets_parser import *
import sys

semantics_max_features = 1600000
sematics_maxlen = 100
semantics_batch_size = 32


def daily_count_semantics(unprsd_tweets):
    s_counter = {}
    s_counter['positive'] = {}
    s_counter['negative'] = {}
    s_counter['tolerant'] = {}
    for t in unprsd_tweets:
        if t['emo'] < 0.33:
            if not t['date'] in s_counter['negative']:
                s_counter['negative'][t['date']] = 1
            else:
                s_counter['negative'][t['date']] += 1
        if t['emo'] > 0.33 and t['emo'] < 0.66:
            if not t['date'] in s_counter['tolerant']:
                s_counter['tolerant'][t['date']] = 1
            else:
                s_counter['tolerant'][t['date']] += 1
        if t['emo'] > 0.66:
            if not t['date'] in s_counter['positive']:
                s_counter['positive'][t['date']] = 1
            else:
                s_counter['positive'][t['date']] += 1
    s_counter.pop(None, None)
    s_counter['positive'].pop(None, None)
    s_counter['negative'].pop(None, None)
    s_counter['tolerant'].pop(None, None)
    return s_counter


def model_compile():
    print 'Compiling Keras model...'
    model = Sequential()
    model.add(Embedding(semantics_max_features, 128, input_length=sematics_maxlen))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  class_mode="binary")
    return model


def model_fit(m, X_train, y_train):
    print 'Fitting the model'
    m.fit(
        X_train, y_train,
        batch_size=semantics_batch_size,
        nb_epoch=1,
        show_accuracy=True
    )
    return m


def create_dict_of_words(w_array):
    print 'Preparing tweets'
    word_dict = {}
    for i, w in enumerate(set(' '.join(w_array).lower().split())):
        word_dict[w] = i + 1
    return word_dict


def replace_words_with_numbers(string, word_dict):
    a = np.zeros(100)
    for i, w in enumerate(string.lower().split()):
        if w in word_dict:
            a[i] = float(word_dict[w])
        else:
            a[i] = 0.0
    return a


def convert_input_string_arr_to_numbers_arr(string_array, word_dict):
    new_array = []
    for string in string_array:
        new_array.append(replace_words_with_numbers(string, word_dict))
    return np.array(new_array)


def update_sentiments(m, parsed_tweets, word_dict):
    print 'Predicting sentiments...'
    for i, t in enumerate(parsed_tweets):
        t['emo'] = m.predict_proba(np.array([replace_words_with_numbers(t['text'], word_dict)]), verbose=0)[0][0]
        print '[{0}\t/{1}]:{2:.2f}%\r'.format(i, len(parsed_tweets), i / float(len(parsed_tweets)) * 100),
        sys.stdout.flush()
    print
    return parsed_tweets


def read_semantics_database():
    x = []
    y = []
    print 'reading Stanford semantics database'
    with open('data/stanford_train_data/training.1600000.processed.noemoticon.csv', 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            y.append(float(row[0]) / 4)
            x.append(row[5])
    y = np.array(y)
    print 'Found {0} entries'.format(len(x))
    return x, y


def read_test_semantics_database():
    x = []
    y = []
    print 'Reading Stanford test Semantics Database'
    with open('data/stanford_train_data/testdata.manual.2009.06.14.csv', 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            y.append(float(row[0]) / 4)
            x.append(row[5])
    y = np.array(y)
    print 'Found {0} entries'.format(len(x))
    return x, y


def semantic_analysis(parsed_tweets):
    x, y = read_test_semantics_database()
    dct = create_dict_of_words(x + [tweet['text'] for tweet in parsed_tweets])
    num_x = convert_input_string_arr_to_numbers_arr(x, dct)
    m = model_compile()
    m = model_fit(m, num_x, y)
    parsed_tweets = update_sentiments(m, parsed_tweets, dct)
    return parsed_tweets
