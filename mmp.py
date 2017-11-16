import tweepy
import MySQLdb

cnx = MySQLdb.connect(host='localhost', user = 'root', password = '123456', database='twitter',charset="utf8")
cur = cnx.cursor()

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

add_status = ("INSERT INTO status"
"(status_id, hashtags, user_id, created_time, retweet_id) "
"VALUES (%s,%s,%s,%s,%s)")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)



class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        created_time = status.created_at
        status_id = status.id_str
        user_id = status.author.id_str
        hashtags = status.entities['hashtags']
        hashtags = [x['text'] for x in hashtags]
        if len(hashtags) == 0:
            return True
        hashtags = ' '.join(hashtags)
        rt_status_id = None
        if hasattr(status, 'retweeted_status'):
            rt_status_id = status.retweeted_status.id_str
            # rt_user_id = status.retweeted_status.author.id_str
            # print('---ret----')

        data_status = (
            status_id,
            hashtags,
            user_id,
            str(created_time),
            rt_status_id
        )
        cur.execute(add_status, data_status)
        cnx.commit()
        
        print('-------')
        
        return True

    def on_error(self, error):
        print(error)
        return True

def main():
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = auth, listener=myStreamListener)
    myStream.filter(languages=['en'], track=['#'])
    
if __name__ == '__main__':
    main()
