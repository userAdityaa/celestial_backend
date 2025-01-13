import requests

def get_tweets(screenname):
    url = f"http://127.0.0.1:5000/get_timeline?screenname={screenname}"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        tweet_list = []
        for tweet in data['timeline']:
            tweet_info = {}
            if 'author' in tweet:
                tweet_info['author_name'] = tweet['author']['name']
                tweet_info['author_screen_name'] = tweet['author']['screen_name']
            else:
                tweet_info['author_name'] = 'Unknown'
                tweet_info['author_screen_name'] = 'Unknown'

            tweet_info['tweet_id'] = tweet.get('tweet_id', 'Unknown')
            tweet_info['created_at'] = tweet.get('created_at', 'Unknown')
            tweet_info['text'] = tweet.get('text', '')
            tweet_info['hashtags'] = [hashtag['text'] for hashtag in tweet.get('entities', {}).get('hashtags', [])]
            
            tweet_info['media'] = [media['media_url_https'] for media in tweet.get('media', []) if 'media_url_https' in media]

            tweet_info['favorites'] = tweet.get('favorites', 0)
            tweet_info['views'] = tweet.get('views', 'Unknown')

            tweet_list.append(tweet_info)

        for tweet in tweet_list:
            print(tweet)
    else:
        print("Error fetching data:", response.status_code)

screenname = input("Enter Twitter screen name: ")
get_tweets(screenname)
