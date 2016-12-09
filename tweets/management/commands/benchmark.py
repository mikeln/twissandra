import datetime
import random
import string
import time
import uuid

import cass

from django.core.management.base import BaseCommand
#
# based on fake_data.py
#
class Command(BaseCommand):

    def handle(self, *args, **options):

        session = cass.initDBConnection('twissandra')

        # Oldest account is 10 years
        origin = int(
            time.time() +
            datetime.timedelta(days=365.25 * 10).total_seconds() * 1e6)
        now = int(time.time() * 1e6)

        if len(args) < 2:
            print " "
            print "Usage benchmard <num_users> <max_tweets>"
            print "   Inserts new <num_users> users * new <max_tweets> tweets"
            print " "
            sys.exit(1)

        num_users = int(args[0])
        max_tweets = int(args[1])

        the_ucount = 0
        the_tweet_total = 0

        print "users:",num_users," tw:",max_tweets

        for i in range(num_users):
            username = self.get_random_string()
            cass.save_user(username, self.get_random_string())
            creation_date = random.randint(origin, now)

            the_tcount = 0

            loop_tweets = max_tweets

            for _ in range(loop_tweets):
                cass.save_tweet(uuid.uuid1(), username, self.get_tweet(), timestamp=random.randint(creation_date, now))
                the_tcount += 1

            the_tweet_total += the_tcount
            the_ucount += 1
            print "created user", the_ucount, " tweets:",the_tcount, " total:",the_tweet_total

    def get_tweet(self):
        return ''.join(random.sample((string.letters)*5, 80))

    def get_random_string(self):
        return ''.join(random.sample(string.letters, 10))
