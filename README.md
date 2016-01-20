# Non API Twitter Parser
Small Python utility which helps you to parse and analyse the tweets from Twitter without using twitter API. The API has a restrictions and I wrote this script in order to overcome them.

# Requirements:
- [Firefox](https://www.mozilla.org/en-US/firefox/desktop/);
- [Selenium](https://github.com/SeleniumHQ/selenium/tree/master/py). To install run: ```pip install selenium```

# Usage

First, clone the repository:

```
git clone https://github.com/pycckuu/non-api-twitter-parser.git
```

In command line open the folder and run python. In python shell import the module:

```python
In [1]: import twitter_parser
```

Now, go to the [Twitter advanced search page](https://twitter.com/search-advanced?lang=en) and fill in form's fields in  which you are interested in, hit 'Search' button. When the page is loaded you can adjust the parameters. For instance you may select 'News' tab. When everything is set and the Twitter advanced search page loads the desired result you need to copy the address url from your browser. Now, run the scrapper with the URI:

```python
In [2]: twitter_parser.scrape_page('https://twitter.com/search?f=news&vertical=news&q=water&src=typd&lang=en')
```

It will load Firefox browser and perform scrolling of the page every 0.5 second. After some time, when you fill that it is enough of tweets, you need to interrupt the script. Select all the content in Firefox page (ctrl-A) and copy it (ctrl-C). Save the text into txt file and put it in data folder (you may see as an example txt files already saved there for you, don't forget to delete them before you start scrapping). You can perform this operation several times depending on your needs.

When all tweets of interest are saved into the _data_ folder, you may run the parser:

```python
In [3]: prsd_tweets = twitter_parser.parse_folder('data')
```

By default, the script will search for text files in _data_ folder, but you may specify any folder. The script will output some basic info about found files, total amount of parsed tweets and 50 most common words in all tweets:
```
Found files
Data/dec13-dec6.txt
Data/dec17-dec14.txt
Data/dec30-dec18.txt
Data/dec5-nov30.txt
Total amount of tweets: 28069
Fifty most common words in tweets:
[('water', 30549), ('news', 3557), ('nov', 1703), ('flint', 1041), ('conservation', 958), ('drinking', 896), ('california', 815), ('crisis', 794), ('clean', 771), ('world', 754), ('watkins', 714), ('alyssa', 711), ('city', 710), ('hot', 692), ('climate', 668), ('video', 649), ('state', 624), ('drink', 611), ('drought', 606), ('supply', 602), ('yukohill', 574), ('health', 510), ('us', 508), ('flood', 508), ('energy', 485), ('levels', 481), ('global', 481), ('michigan', 479), ('food', 468), ('india', 452), ('main', 451), ('people', 447), ('wendy', 440), ('epa', 432), ('emergency', 427), ('change', 416), ('break', 416), ('floods', 403), ('air', 389), ('one', 360), ('finds', 359), ('tap', 359), ('power', 354), ('social', 353), ('uk', 350), ('first', 346), ('chennai', 346), ('home', 337), ('media', 335), ('today', 334)]
```

Also, script will return all parsed tweets into the variable _prsd\_tweets_ which is list of python dictionaries. The keys are 
- 'id' = ID of the tweet;
- 'date' = datetime object;
- 'text' = string of the text of tweet;
- 'emo' = sentiment: if '-1' - undefined. The field saved for Deep Learning (soon).

You may estimate daily count of words. You may pass words as a list and in this case the script will return the sum of words in the list as in example with ['world','global']:
```python
In [4]: region = {}
In [5]: region['UK'] = twitter_parser.daily_count_words(['uk'], prsd_tweets)
In [6]: region['US'] = twitter_parser.daily_count_words(['us'], prsd_tweets)
In [7]: region['California'] = twitter_parser.daily_count_words(['california'], prsd_tweets) 
In [8]: region['India'] = twitter_parser.daily_count_words(['india'], prsd_tweets)
In [9]: region['World'] = twitter_parser.daily_count_words(['world','global'], prsd_tweets)
```

It is convenient to save the data as Pandas DataFrame:

```python
In [10]: import pandas as pd
In [11]: df1 = pd.DataFrame(region)
In [12]: df1[-10:]
```

The script will return the data frame (for instance last 10 elements):

|            |California  |India| UK | US  |World|
|------------|-----------:|----:|---:|----:|----:|
| 2015-12-21 |  62        | 7   |  5 | 152 | 35  |
| 2015-12-22 |  60        | 2   |  28| 154 | 27  |
| 2015-12-23 |  18        | 5   |  10| 122 | 10  |
| 2015-12-24 |  7         | 5   |  8 | 94  | 15  |
| 2015-12-25 |  30        | 3   |  3 | 69  | 12  |
| 2015-12-26 |  26        | 12  |  42| 95  | 41  |
| 2015-12-27 |  14        | 25  |  50| 155 | 22  |
| 2015-12-28 |  19        | 13  |  49| 152 | 27  |
| 2015-12-29 |  33        | 6   |  26| 183 | 32  |
| 2015-12-30 |  7         | 1   |  4 | 47  | 8   |


And you can easily plot graphs:

```python
In [12]: df1.plot(kind='area')
```

![alt tag](https://raw.githubusercontent.com/pycckuu/non-api-twitter-parser/master/img/df1.png)

# Notes  
- It doesn't matter how many txt files will be in _data_ folder, the utility will load them all;

# Soon

Deep Learning Recurrent Neural Network algorithms which get sentiment of parsed tweets.
