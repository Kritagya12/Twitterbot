#______________________________________________________________________________________________________________________#
                                                  #TWITTERBOT#
#______________________________________________________________________________________________________________________#

import tweepy
import re, operator
from paralleldots import set_api_key
from paralleldots import sentiment
import nltk
from nltk.corpus import stopwords

# Authentication
consumer_key='oQ5AdBdNFQw8JsPzte4A3EoID'
consumer_secret='TCRlXF0KKniWnnKbHF0e4C7d6mrBHMR6HrvrKVR37SqF4FgW7p'

# Authentication Access Tokens
access_token='3931823300-2JtkbunsbWs6hPOE8hA5m5jCfU14xUylGsFu9r4'
access_token_secret='ccPH3hF5xXFy5RWlX6tIVfRbs0ubql4gocZgTOruz514t'

oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_token_secret)

api = tweepy.API(oauth)

#--------------------------------------------Function for extracting tweets--------------------------------------------#

def get_search():
    tag_hash = input("\nEnter the word to be searched without # : ")
    tag_hash = "#" + tag_hash
    print(tag_hash)
    tweets = api.search(tag_hash)
    return tweets

#---------------------------------------------Function for top words usage---------------------------------------------#

def top_usage():

    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    dictionary = {}
    tweeted_words = []
    tweet = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for a in tweet:
        b = a.full_text.split(" ")
        for c in b:
            tweeted_words.append(c)
    for word in tweeted_words:
        if word not in stop_words and "http" not in word:
            if word in dictionary.keys():
                dictionary[word] += 1
            else:
                dictionary[word] = 1

    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
    print("The top used words in twitter are: ")
    for i in range(-1, -11, -1):
        print(sorted_dictionary[i][0], " - ", sorted_dictionary[i][1])


#---------------------------------------Function for sentimental analysis----------------------------------------------#

def testing_sentiments():
    sent_list = []
    tweets = get_search()
    set_api_key("5Ilq8t88HXC0EYjVzpCDqqnQSlPJm5mJ9faJTnigwG4")
    for tweet in tweets:
        sent_list.append(sentiment(tweet.text))
    return sent_list

#---------------------------------------Function for comparing the tweets----------------------------------------------#

def tweet_match():
    DT = 0
    tweets = api.user_timeline(screen_name="@realDonaldTrump", count=200, tweet_mode="extended")
    for tweet in tweets:
        # Removing the URLs
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)
        if "india" in tweet_text or "INDIA" in tweet_text or "Hindustan" in tweet_text or "India" in tweet_text:
            DT += 1

    NM = 0
    tweets = api.user_timeline(screen_name="@narendramodi", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)
        if "US" in tweet_text or "USA" in tweet_text or "America" in tweet_text or "United States Of America" in tweet_text or "america" in tweet_text:
            NM += 1

    # Comparison between Narendra Modi and Donald Trump is shown here
    print("Narendra Modi-"+ str(NM))
    print("Donald Trump-"+ str(DT))

#-----------------------------------Function for determining the location and time-------------------------------------#

def determine_location():
    language = {}
    location = {}
    time = {}
    tag_hash = input("Enter the word without #: ")
    tag_hash='#'+ tag_hash
    print(tag_hash)
    tweets = api.search(q=tag_hash, count=200)
    for tweet in tweets:
        if tweet.user.lang in language.keys():
            language[tweet.user.lang] += 1
        else:
            language[tweet.user.lang] = 1
        #for location
        if tweet.user.location in location.keys():
            location[tweet.user.location] += 1
        elif tweet.user.location != '':
            location[tweet.user.location] = 1
        #for time zones
        if tweet.user.time_zone in time.keys():
            time[str(tweet.user.time_zone)] += 1
        else:
            time[str(tweet.user.time_zone)] = 1

    Location = sorted(location, key=location.get, reverse=True)
    Time = sorted(time, key=time.get, reverse=True)
    Language = sorted(language, key=language.get, reverse=True)

    print("Locations for this keyword are:")
    i = 0
    for j in Location[0:5]:
        i += 1
        print(i, j, location[j])

    print("Timezones for this keyword are:")
    i = 0
    for j in Time[0:5]:
        i += 1
        print(i, j, time[j])
    i = 0
    print("Top 5 languages used:")
    for j in Language[0:5]:
        i += 1
        print(i, j, language[j])


#---------------------------------------Function to display the main menu----------------------------------------------#

def main_menu():
    show_menu = True
    menu_choices = "\nEnter your choice: \n1.Retrieval of Tweets\n2.Followers count\n3.Sentimental Analysis  \n4.Determine Location, Language, And Time Zone \n5.Comparison Of Tweets\n6.Top Words Usage\n7.Update a status\n8.Quit"
    while show_menu:
        choice = input(menu_choices)

        # For extracting tweets
        if choice == "1":
            tweets = get_search()
            print("Following tweets have been made by the people \n")
            for tweet in tweets:
                print(tweet.text)
                print("-----------------------------------------------------------------------------------------------")

        # For counting the followers
        elif choice == "2":
            tweets = get_search()
            for tweet in tweets:
                print("User name: %s \t Total followers:%s " % (tweet.user.name, tweet.user.followers_count))
            print("\n")

        # For Determining the sentiments
        elif choice == "3":
            sent_list = testing_sentiments()
            positive = 0
            negative = 0
            neutral = 0
            for x in sent_list:
                if x["sentiment"] == "neutral":
                    neutral += 1
                elif x["sentiment"] == "negative":
                    negative += 1
                elif x["sentiment"] == "positive":
                    positive += 1
            print("Sentimental Analysis Result:\n")
            print("Positive tweets:%d \t Negative tweets:%d \t Neutral tweets:%d" % (positive, negative, neutral))

        # For determining the location
        elif choice == "4":
            determine_location()


        # For comparing the tweets
        elif choice == "5":
            tweet_match()

        # To find the total usage
        elif choice == "6":
            top_usage()

        # For updating a Status
        elif choice == "7":
            status = input("Enter your status: ")
            api.update_status(status)

        # To exit the application
        elif choice == "8":
            show_menu = False
main_menu()

#------------------------------------------------PROJECT ENDS----------------------------------------------------------#