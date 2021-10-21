import random, json, codecs, aiohttp

class GIF_And_Text():

    async def create_string(self,*,type,user1,user2):

        """
        Creates a string to be appended to the top of emote embed.
        It loads files/emotes-text.json and retrieves text and random emoji if applicable.
        Then it appends `user1` and `user2` names to string and returns it. 

        args:
            type: str -> Type of string to be requested
            user1: str -> command's author's username
            user2: str -> mentioned user's  username
        
        returns:
            random_text: str -> The generated text
        """

        with open('files/emotes-text.json') as js:
            data = json.load(js)
            js.close()

        if user2 == None:
            people = 'solo'
        else:
            people = 'with'
        
        random_text = random.choice(data['emote'][type][people])

        random_text = random_text.replace('$user1',user1)

        try:
            random_text = random_text.replace('$user2',user2)
        except: pass

        return random_text

    # -------------------------------- #

    async def selector(self,category: str) -> str:
        """
        Selects the function depending on category given.

        args:
            category: str -> category of gif to be returned
        
        returns:
            url: str -> URL of image
        """

        with open('files/emote-url.json', 'r') as f:
            kind = json.load(f)
            f.close()
            lists = []
            for i in kind:
                lists.append(i)

        if category in self.waifu and category in lists:

            if random.randint(1,2) == 1:
                url = await self.listed_gif(category)

            else:
                url = await self.waifu_gif(category)

        elif category in self.waifu and category in self.nekos:

            if random.randint(1,2) == 1:
                url = await self.neko_gif(category)

            else:
                url = await self.waifu_gif(category)

        elif category in self.nekos and category in lists:

            if random.randint(1,2) == 1:
                url = await self.listed_gif(category)

            else:
                url = await self.neko_gif(category)

        elif category in self.waifu:
            url = await self.waifu_gif(category)
        
        elif category in self.nekos:
            url = await self.neko_gif(category)
        
        else:
            url = await self.listed_gif(category)
    
        return url

    # -------------------------------- #

    async def waifu_gif(self,endpoint: str) -> str:
        """
        Generates a random gif from waifu.pics API.
        
        args: 
            endpoint: str -> category of image to get.

        output:
            rq = returns a URL string
        """
        
        url = 'https://waifu.pics/api/sfw/'+endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rq = await response.json()
                await session.close()
        rq = rq["url"]
        return rq

    # -------------------------------- #

    async def neko_gif(self,endpoint: str) -> str:
        """
        Generates a random gif from waifu.pics API.
        
        args: 
            endpoint: str -> category of image to get.

        output:
            rq = returns a URL string
        """
        url = 'https://nekos.best/api/v1/'+endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rq = await response.json()
                await session.close()
        rq = rq['url']
        return rq

    # -------------------------------- #

    async def listed_gif(self,category: str) -> str:
        """
        hmph, dance, sleep, vibe

        Randomly selects an item from list based on category.

        args:
            category: str -> Type of gif to be returned
        returns:
            image: str -> a url of image
        """
        with open('files/emote-url.json', 'r') as f:
            kind = json.load(f)
            f.close()
        image = random.choice(kind[category])
        return image

    # -------------------------------- #

    async def create_string(self,*,type: str, user1: str, user2: str=None) -> str:

        with codecs.open('files/emotes-text.json','r',encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        if user2 == None:
            people = 'solo'
        else:
            people = 'with'
        
        random_text = random.choice(data['emote'][type][people])

        random_text = random_text.replace('$user1',user1)

        try:
            random_text = random_text.replace('$user2',user2)
        except: pass

        emoji_str = data['emote'][type]['emoji']
        if emoji_str == 'none': 
            pass
        else:
            emoji = random.choice(data['emoji'][emoji_str])
            random_text = random_text +" "+ emoji

        return random_text

    # -------------------------------- #


    waifu = [
        'blush',    'kiss',     'smile',    'bite',
        'bully',    'throw',    'nom',      'cringe',
        'wave',     'cuddle',   'happy',    'glomp',
        'hug',      'highfive', 'superhug', 'poke',
        'lick',     'handhold', 'slap',     'wink',
        'pat',      'smug',     'hold',     'kill',
        'cry',      'bonk',     'kick',
        'yeet',     'hungry'
    ]

    lists = [
        'dance','sleep', 'vibe', 'pout', 'hmph', 'run'
    ]

    nekos = [
        'baka', 'bite', 'blush', 'bored', 'cry', 'cuddle',
        'dance', 'facepalmm', 'feed', 'happy', 'hug', 'kiss',
        'laugh', 'pat', 'shrug', 'slap', 'sleep', 'smile',
        'smug', 'stare', 'think', 'thumbsup', 'tickle', 'wave',
        'wink'
    ]
