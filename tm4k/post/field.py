def getPostBlogId(post: dict):
    return post["user"]["blogUrl"]


def getPostId(post: dict):
    return post["id"]


def hasTags(post):
    return post["tags"] != []


def getPostPublishTs(post):
    return post["publishTime"]


def getSubscrLvlName(post: dict) -> str:
    if post.get("subscriptionLevel") is not None:
        return post["subscriptionLevel"]["name"]
    else:
        return "Нет"
