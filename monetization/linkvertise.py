from linkvertise import LinkvertiseClient

def create_linkvertise_link(original_url, user_id=1131101):
    client = LinkvertiseClient()
    return client.linkvertise(user_id, original_url)
