import random, json, codecs

class GIF_And_Text():

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

    async def waifu_gif(self,endpoint: str) -> list:
        """
        Generates a random gif from waifu.pics API.
        (Cached on disk for faster search)
        args: 
            endpoint: str -> category of image to get.

        output:
            formed = returns a URL string and attribution
        """

        with open('files/emote-url-waifu.json','r') as f:
            rq = json.load(f)
            f.close()
            rq = random.choice(rq[endpoint])
            ft = "Powered by waifu.pics"
            formed = [rq,ft]
            return formed

    # -------------------------------- #

    async def neko_gif(self,endpoint: str) -> list:
        """
        Generates a random gif from nekos.life API.
        (Cached on disk for faster search)
        args: 
            endpoint: str -> category of image to get.

        output:
            rq = returns a URL string and attribution
        """
        with open('files/emote-url-nekos.json','r') as f:
            rq = json.load(f)
            f.close()
            rq = random.choice(rq[endpoint])
            ft = "Powered by nekos.life"
            formed = [rq,ft]
            return formed

    # -------------------------------- #

    async def listed_gif(self,category: str) -> list:
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
        if 'giphy' in image:
            atr = "Powered by Giphy"
        elif 'tenor' in image:
            atr = "Powered by Tenor"
        else:
            atr = "Powered by Discord"
        image = [image,atr]
        return image

    # -------------------------------- #

    async def create_string(self,*,type: str, user1: str, user2: str=None) -> str:
        """
        Creates a string for given category.\n
        args:
            type: str -> Category of string to be generated\n
            user1: str -> Name of author of command\n
            user2: str -> Name of mentioned user. Can be None if no one was mentioned
        returns:
            random_text: str -> Generated string
        """
        # Open and load the JSON file containing all the strings
        with codecs.open('files/emotes-text.json','r',encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        # Checks if it is solo or not
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
