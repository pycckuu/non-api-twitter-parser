# Non API Twitter Parser with Semantics Analysis.
Small Python utility which helps you to parse and analyse the tweets from Twitter without using twitter API. The API has a restrictions and I wrote this script in order to overcome them. Moreover, this script contain methods which helps you analyse the statistics of tweets including semantic using Deep Learning Recurrent Neural Network algorithms based on [Keras](http://keras.io/), [Theano](https://github.com/Theano/Theano), and/or [TensorFlow](https://github.com/tensorflow/tensorflow). 

#### Requirements

For parsing:
- [Firefox](https://www.mozilla.org/en-US/firefox/desktop/);
- [Selenium](https://github.com/SeleniumHQ/selenium/tree/master/py). To install run: ```pip install selenium```

For Deep Learning:
- [Keras](http://keras.io/). To install: ```pip install keras```
- [Theano](https://github.com/Theano/Theano). To install ```pip install theano```
- h5py. To install: ```pip install h5py```
- csv. To install: ```pip install csv```
- numpy. To install: ```pip install numpy```


#### Usage

First, clone the repository:

```
git clone https://github.com/pycckuu/non-api-twitter-parser.git
```

In command line open the folder and run python. In python shell import the module:

```python
In [1]: import twitter_parser
```

Now, go to the [Twitter advanced search page](https://twitter.com/search-advanced?lang=en) and fill in form's fields in  which you are interested in, hit 'Search' button. When the page is loaded you can adjust the parameters: for instance, you may select 'News' tab if you  are interested in news relateed tweets. When everything is set and the Twitter advanced search page loads the desired result, you need to copy the address url from your browser. Now, run the scrapper with the URI as a string:

```python
In [2]: twitter_parser.scrape_page('https://twitter.com/search?f=news&vertical=news&q=water&src=typd&lang=en')
```

It will load Firefox browser and perform scrolling of the page every 0.5 second to load new content. After some time, when you think that it is enough information on the Firefox page, you need to interrupt the script, select all the content in Firefox page (```ctrl-A```), copy it (```ctrl-C```) and paste the text (```ctrl-V```) into txt file, save txt-file in data folder (you may see as an example txt-files already saved there for you, don't forget to delete them before you start scrapping). You can perform this operation several times depending on your needs.

When all tweets of interest are saved into the _data_ folder, you may run the parser:

```python
In [3]: prsd_tweets = twitter_parser.parse_folder()
```

By default, the script will search for text files in _data_ folder, but you may specify any folder as input parameter for the method. The script will output some basic info about found files, total amount of parsed tweets and 50 most common words in tweets:
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
- 'date' = date of the tweet as a datetime object;
- 'text' = message of the particular tweet as a string;
- 'emo' = sentiment: if '-1' - undefined. The field saved for Deep Learning (soon).

#### Features

##### Daily count of tweets containing specific word

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

##### Sentiment of parsed tweets

Now, you may perform the semantics analysis. Unzip the [Stanford tweets database](http://help.sentiment140.com/for-students/) _stanford\_train\_data.zip_, which is in the folder of repository. Run the model:

```python
In [13]: prsd_tweets, m = twitter_semantics.semantic_analysis(prsd_tweets)
```

It will perform the training of neural network. If you don't want to wait  long you may use already trained [Keras]() weights. Download them using this [link](https://www.dropbox.com/s/jp443in7mu5i3xr/weights.h5?dl=1) and put file in in the repository root folder. Run the script again:

```python 
In [14]: prsd_tweets, m = twitter_semantics.semantic_analysis(prsd_tweets)
```

The script will update the _emo_ key of dictionaries _prsd\_tweets_ much faster without learning of the model. As the output you will see the following:

```
Found file 'weights.h5' in root folder
Running semantics analysis with preloaded weights
If you want to re-train the model, please, delete 'weights.h5' file and run this method again
For different weight file::: Please, pass the filepath as second argument
Reading Stanford Semantics Database
Found 1600000 entries
Preparing tweets
Compiling Keras model...
Loading Weights from file 'weights.h5'
Updating parsed tweets
Predicting sentiments...
[28068/28068]:100%
```

You may count positive, tolerant and negative sentiment of the tweets containing list of words by:

```python
In [15]: twitter_semantics.daily_count_semantics_for_words(['world','global'],prsd_tweets)
```

It will count sentiment of the tweets containing words _world_ and _global_. Now, you may build graphs of polarity of tweets:

![alt tag](https://raw.githubusercontent.com/pycckuu/non-api-twitter-parser/master/img/df2.png)

#### Notes  
- It doesn't matter how many txt-files will be in _data_ folder, the utility will load them all;
- The code of this example you may find in Jupyter (iPython) notebook _Visualisation.ipynb_.


#### Collaborators are really welcome!

Please, contact me, if you know how to improve or have ideas about some cool features. 
Generally, I expect collaborators to create the pull request with new feature/improvement!

##### The MIT License (MIT)

Copyright (c) 2016 Igor Markelov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
