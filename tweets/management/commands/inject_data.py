import datetime
import loremipsum
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

	InitDBConnection('twissandra')

        # Oldest account is 10 years
        origin = int(
            time.time() +
            datetime.timedelta(days=365.25 * 10).total_seconds() * 1e6)
        now = int(time.time() * 1e6)

        if len(args) < 4:
            print " "
            print "Usage inject_data <num_users> <max_tweets> <delay_sec> <random_flag>"
            print "   Inserts new <num_users> users * new <max_tweets> tweets"
            print "   with <delay_sec> between each tweet"
            print "   <random_flag> = 0 - Random Distribution Flag"
            print "                 = 1 - Use Random Distribution varies 1-max tweets"
            print " "
            sys.exit(1)

        num_users = int(args[0])
        max_tweets = int(args[1])
        delay_sec = int(args[2])
        random_flag = int(args[3])

        the_ucount = 0
        the_tweet_total = 0

        print "users:",num_users," tw:",max_tweets," sec:",delay_sec," random:",random_flag

        # Generate number of tweets based on a Zipfian distribution
        sample = [random.paretovariate(15) - 1 for x in range(max_tweets)]
        normalizer = 1 / float(max(sample)) * max_tweets
        num_tweets = [int(x * normalizer) for x in sample]

        for i in range(num_users):
            username = self.get_random_string()
            cass.save_user(username, self.get_random_string())
            creation_date = random.randint(origin, now)

            the_tcount = 0

            loop_tweets = max_tweets

            if random_flag == 1:
                loop_tweets = num_tweets[i % max_tweets]

            for _ in range(loop_tweets):
                cass.save_tweet(uuid.uuid1(), username, self.get_tweet(), timestamp=random.randint(creation_date, now))
                the_tcount += 1
                if 0 < delay_sec:
                    time.sleep(delay_sec)

            the_tweet_total += the_tcount
            the_ucount += 1
            print "created user", the_ucount, " tweets:",the_tcount, " total:",the_tweet_total

    def get_tweet(self):
        return loremipsum.get_sentence()

    def get_random_string(self):
        return ''.join(random.sample(string.letters, 10))
