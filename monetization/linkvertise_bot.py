from linkvertise.client import LinkvertiseClient
import os

my_secret_linkvertise = os.environ['linkvertise']

client = LinkvertiseClient()


def create_linkvertise_link(original_url, user_id=my_secret_linkvertise):

  return client.linkvertise(int(user_id), original_url)
