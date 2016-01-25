from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import operator
import re
from dateutil import parser
import glob

often_words = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'anti', 'around', 'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'excepting', 'excluding', 'following', 'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'of', 'off', 'on', 'onto', 'opposite', 'outside', 'over', 'past', 'per', 'the', 'a', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'through', 'to', 'toward', 'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'via', 'with', 'within', 'without', 'account', 'embedded', 'permalink', 'dec', 'jan', 'retweets', 'image', 'hours', '2015', 'reply', 'you', 'is', 'are', 'am', 'was', 'were', 'will',
               'do', 'does', 'did', 'have', 'had', 'has', 'can', 'could', 'should', 'shall', 'may', 'might', 'would', 'likes', 'retweet', 'more', '\xe2\x80\xa6', 'and', 'ago', 'what', 'what', 'when', 'when', 'why', 'why', 'which', 'who', 'how', 'how', 'how', 'whose', 'whom', 'it', 'all', 'your', '21h21', '22h22', 'verified', 'new', 'be', '-', 'that', 'this', '&', 'out', 'not', 'we', 'so', 'no', 'its', '\xe6\x9d\xb1\xe6\x96\xb9\xe7\xa5\x9e\xe8\xb5\xb7', '...', 'retweeted', '|', 'says', 'rt', 'lead', 'an', '', 'httpwwwbbccouknewsuk', 'if', 'year', 'get', 'day', 'times', 'summary', 'our', 'ho', 'i', 'added', 'now', 'york', 'been', 'gov', 'just', 'years', 'green', 'great', 'or', 'daily', 'make', 'giving', 'time', 'view', 'my', 'some', 'need', 'where', 'they', 'watch', 'use', 'high', 'help', 'police', 'seconds', 'their', 'business']


mostcommon = []


def scrape_page(page_url):
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    firefox_profile.set_preference('browser.migration.version', 9001)
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.get(page_url)
    for i in range(1, 100000):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down
        time.sleep(0.5)


def daily_count_words(words, prsd_tweets):
    w_counter = []
    for word in words:
        w_counter.append(count_word_in_tweets(word, prsd_tweets))
    w_counter = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), w_counter)
    return w_counter


def parse_date(tweet):
    last_year_date = re.findall('(\d+\s\D{3}\s2015)', tweet)
    if last_year_date:
        return parser.parse(last_year_date[0])
    this_january_date = re.findall('\sJan\s(\d+)', tweet)
    # TODO: This month searcher could be improved to whole this year searcher like last year one.
    if this_january_date:
        return parser.parse("%s Jan 2016" % (this_january_date[0]))
    if (re.findall('([0-9]+)\shour', tweet)):  # if today?
        return parser.parse('On')
    return None


def parse_tweets(tweets):
    # [{id:, date:, text:}, ...]
    prsd_tweets = []
    for i in range(len(tweets)):
        t = {}
        t['id'] = i
        t['date'] = parse_date(tweets[i])
        t['text'] = clean_tweet(tweets[i])
        t['emo'] = -1
        prsd_tweets.append(t)
    return prsd_tweets


def count_word_in_str(word, string):
    return len(re.findall(word, string.lower()))


def count_word_in_tweets(word, tweets):
    # tweets parsed
    # [{id:, date:, text:}, ...]
    counter = {}
    for t in tweets:
        if not t['date'] in counter:
            counter[t['date']] = count_word_in_str(word, t['text'])
        else:
            counter[t['date']] += count_word_in_str(word, t['text'])
    counter.pop(None, None)
    return counter


def clean_tweet(tweet_text, no_url=False):
    arr = tweet_text.split("\n")
    len_arr = [len(string) for string in arr]
    idx = len_arr.index(max(len_arr))
    txt = arr[idx].strip()
    if no_url:
        txt = re.sub(r'https?:\/\/.*[\r\n]*', '', txt)
    text = ''.join(ch for ch in txt if ch < '\x80')
    return text


def find_files(folder):
    filelist = []
    for counter, files in enumerate(glob.glob(folder + "/*.txt")):
        filelist.append(files)
        print files
    return filelist


def read_files(filelist):
    text = ''
    for fileitem in filelist:
        f = open(fileitem, 'r')
        temp = f.read()
        f.close()
        text += temp
    return text


def split_text_to_tweets(text):
    return re.split('\d\slike', text)


def twitter_wordcount(text, quantity):
    regex = re.compile('[^a-zA-Z]')
    wordcount = {}
    for word in text.split():
        word = word.lower()
        word = regex.sub('', word)
        if word not in often_words and not word.isdigit() and word not in mostcommon:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    return sorted(wordcount.iteritems(), key=operator.itemgetter(1), reverse=True)[:quantity]


def parse_folder(fldr='Data', nltk_lib=False):
    print 'Found files'
    text = read_files(find_files(fldr))
    tweets = split_text_to_tweets(text)
    print 'Total amount of tweets: %s' % len(tweets)
    print 'Fifty most common words in tweets:'
    if nltk_lib:
        import nltk
        fdist = nltk.FreqDist(nltk.corpus.brown.words())
        mostcommon = fdist.most_common(150)
    print twitter_wordcount(text, 50)
    tweets = split_text_to_tweets(text)
    prsd_tweets = parse_tweets(tweets)
    return prsd_tweets
