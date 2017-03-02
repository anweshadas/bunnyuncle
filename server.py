# Copyright: 2017 Anwesha Das <anwesha@das.community>
# Licnese: GPLv3

import toml
import tweepy
import json
import os
import time
from mqttclient import send_messages


def get_auth():
    with open("conf.toml") as conffile:
        config = toml.loads(conffile.read())
    return config["consumer_key"], config["consumer_secret"], config["access_token"], config["access_token_secret"]

def get_old_messeges():
    if os.path.exists("old_messages.json"):
        with open("old_messages.json") as fobj:
            data = fobj.read()
        return json.loads(data)

    else:
        return []


def main():
    ckey, csecret, atoken, asecret = get_auth()
    auth = tweepy.OAuthHandler(ckey,csecret)
    auth.set_access_token(atoken,asecret)

    api = tweepy.API(auth)
    mentions = api.mentions_timeline(count=5)
    old_messages = get_old_messeges()


    for mention in mentions:
        msg = "%s:%s" % (mention.user.screen_name,mention.text)
        if not msg in old_messages:
            print(msg)
            send_messages()
            old_messages.insert(0,msg)


    with open("old_messages.json","w") as fobj:
        fobj.write(json.dumps(old_messages))



if __name__ == "__main__":
    while True:
        try:

            main()
        except Exception as e:
            print(e)

        time.sleep(60)
