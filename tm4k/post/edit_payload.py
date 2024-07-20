import json


def getPostPayload(post: dict):
    payload = {'title': post['title'],
               'deny_comments': str(post["isCommentsDenied"]).lower(),
               'teaser_data': str(json.dumps(post['teaser'])),
               'data': str(json.dumps(post['data'])),
               }
    if 'advertiserInfo' in post.keys():
        payload['advertiser_info'] = post['advertiserInfo']
    if 'poll' in post.keys():
        payload['poll_id'] = post["poll"]["id"]
    if 'subscriptionLevel' in post.keys():
        payload['subscription_level_id'] = post["subscriptionLevel"]["id"]
    return payload
