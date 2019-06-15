import tweepy
import time

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt' #Stores the last user replied in order to don't reply him anymore

def retrieve_last_seen(file_name):
    f_read = open(file_name, 'r')
    last_seen = int(f_read.read().strip())
    f_read.close()
    return last_seen

def store_last_seen(last_seen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen))
    f_write.close()
    return

def replying_tweets():
    print('Replying to tweets...')
    last_seen = retrieve_last_seen(FILE_NAME)    
    mentions = api.mentions_timeline(last_seen, tweet_mode='extended')
    for mention in reversed(mentions): #Starts replying from old tweets first
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen = mention.id
        store_last_seen(last_seen, FILE_NAME)

        if '#whatsapptip' in mention.full_text.lower():
            print('Found Whatsapp asking for tip. Replying back...')
            api.update_status('@' + mention.user.screen_name + ' Do you know your WhatsApp conversations are end-to-end encrypted?', mention.id)
        if '#facebooktip' in mention.full_text.lower():
            print('Found Facebook asking for tip. Replying back...')
            api.update_status('@' + mention.user.screen_name + ' It is recommended that you change your Facebook password regularly.', mention.id)
        if '#twittertip' in mention.full_text.lower():
            print('Found Twitter asking for tip. Replying back...')
            api.update_status('@' + mention.user.screen_name + ' If you do not want to non-followers reads your tweets, you can protect them!', mention.id)
        if '#instagramtip' in mention.full_text.lower():
            print('Found Instagram asking for tip. Replying back...')
            api.update_status('@' + mention.user.screen_name + ' You can also turn your Instagram account to private, so that only your followers can see your photos', mention.id)

while True:
    replying_tweets()
    time.sleep(5)
