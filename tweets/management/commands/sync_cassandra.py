from cassandra.cluster import Cluster
#from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand
from django.conf import settings

#class Command(NoArgsCommand):
class Command(BaseCommand):

    #def handle_noargs(self, **options):
    def handle(self, *args, **options):
        force_arg = "n"
        if len(args) > 0:
            force_arg = args[0]
        
        print "locate cluster try force:%s "%force_arg
        cluster = Cluster([settings.DATABASE_HOST])
        session = cluster.connect()

        rows = session.execute(
            "SELECT * FROM system.schema_keyspaces WHERE keyspace_name='twissandra'")

        if rows:
            msg = ' It looks like you already have a twissandra keyspace.\nDo you '
            msg += 'want to delete it and recreate it? All current data will '
            msg += 'be deleted! (y/n): '
            print "%s %s"%(msg,force_arg)
#            resp = raw_input(msg)
#            if not resp or resp[0] != 'y':
            if force_arg  != 'y':
                print "Ok, nothing deleted."
                return
            print "Deleting ALL data."
            session.execute("DROP KEYSPACE twissandra")

        session.execute("""
            CREATE KEYSPACE twissandra
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """)

        # create tables
        session.set_keyspace("twissandra")

        session.execute("""
            CREATE TABLE users (
                username text PRIMARY KEY,
                password text
            )
            """)

        session.execute("""
            CREATE TABLE friends (
                username text,
                friend text,
                since timestamp,
                PRIMARY KEY (username, friend)
            )
            """)

        session.execute("""
            CREATE TABLE followers (
                username text,
                follower text,
                since timestamp,
                PRIMARY KEY (username, follower)
            )
            """)

        session.execute("""
            CREATE TABLE tweets (
                tweet_id uuid PRIMARY KEY,
                username text,
                body text
            )
            """)

        session.execute("""
            CREATE TABLE userline (
                username text,
                time timeuuid,
                tweet_id uuid,
                PRIMARY KEY (username, time)
            ) WITH CLUSTERING ORDER BY (time DESC)
            """)

        session.execute("""
            CREATE TABLE timeline (
                username text,
                time timeuuid,
                tweet_id uuid,
                PRIMARY KEY (username, time)
            ) WITH CLUSTERING ORDER BY (time DESC)
            """)

        print 'All done!'
