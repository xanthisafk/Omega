import redditeasy

async def get_post(sub, i=5, _type='Image'):
        reddit = redditeasy.AsyncSubreddit()
        while i > 0:
            post = await reddit.get_post(sub)
            if post.content_type == _type:
                return post
            else:
                i -= 1
        return None

async def get_post(sub, i=5, _type='Image'):
        reddit = redditeasy.AsyncSubreddit()
        while i > 0:
            post = await reddit.get_top_post(sub)
            if post.content_type == _type:
                return post
            else:
                i -= 1
        return None

async def get_post(sub, i=5, _type='Image'):
        reddit = redditeasy.AsyncSubreddit()
        while i > 0:
            post = await reddit.get_controversial_post(sub)
            if post.content_type == _type:
                return post
            else:
                i -= 1
        return None