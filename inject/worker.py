import datetime
import loremipsum
import random
import string
import time
import uuid

import cass

import logging
logger = logging.getLogger(__name__)

import names

class Worker():

    def inject(self, num_users, max_tweets, delay_sec, random_flag):
        # Oldest account is 10 years
        origin = int(
            time.time() +
            datetime.timedelta(days=365.25 * 10).total_seconds() * 1e6)
        now = int(time.time() * 1e6)

        the_ucount = 0
        the_tweet_total = 0

        logger.info( "users: %s tw: %s sec: %s rnd: %s",num_users,max_tweets,delay_sec,random_flag)

        # Generate number of tweets based on a Zipfian distribution
        sample = [random.paretovariate(15) - 1 for x in range(max_tweets)]
        normalizer = 1 / float(max(sample)) * max_tweets
        num_tweets = [int(x * normalizer) for x in sample]

        for i in range(num_users):
            username = self.get_random_name()
            logger.info("NEW USER: %s",username)
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
            logger.info("created user: %s tweets: %s total: %s", the_ucount, the_tcount, the_tweet_total)

    def get_tweet(self):
        return loremipsum.get_sentence()

    def get_random_string(self):
        return ''.join(random.sample(string.letters, 10))

    def get_random_name(self):
        tlist = [ names.get_last_name() ]
        tlist = tlist + random.sample(string.letters, 5)
        return ''.join( tlist )
