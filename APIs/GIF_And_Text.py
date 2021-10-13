import random, requests, json, codecs

class GIF_And_Text():

    async def selector(self,category: str) -> str:
        """
        Selects the function depending on category given. Temp solution until I get my own API working.

        args:
            category: str -> category of gif to be returned
        
        returns;
            url = 
        """

        if category in self.waifu and category in self.lists:

            if random.randint(1,2) == 1:
                url = await self.listed_gif(category)

            else:
                url = await self.waifu_gif(category)

        elif category in self.waifu and category in self.nekos:

            if random.randint(1,2) == 1:
                url = await self.neko_gif(category)

            else:
                url = await self.waifu_gif(category)

        elif category in self.nekos and category in self.lists:

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



    async def waifu_gif(self,endpoint: str) -> str:
        """
        Generates a random gif from waifu.pics API.
        
        args: 
            endpoint: str -> category of image to get.

        output:
            rq = returns a URL string
        """
        url = 'https://api.waifu.pics/sfw/'+endpoint
        rq = requests.get(url).json()
        rq = rq["url"]
        return rq



    async def neko_gif(self,endpoint: str) -> str:
        """
        Generates a random gif from waifu.pics API.
        
        args: 
            endpoint: str -> category of image to get.

        output:
            rq = returns a URL string
        """
        url = 'https://nekos.best/api/v1/'+endpoint
        rq = requests.get(url).json()
        rq = rq["url"]
        return rq



    async def listed_gif(self,category: str) -> str:
        """
        hmph, dance, sleep, vibe

        Randomly selects an item from list based on category.

        args:
            category: str -> Type of gif to be returned
        returns:
            image: str -> a url of image
        """
        image = random.choice(self.kind[category])
        return image




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

    kind = {

        'hmph' : [
            'https://media.giphy.com/media/v1YqHOqVYnlaJd6N9b/giphy.gif',
            'https://media.giphy.com/media/W6WLbzsxEqBN6IY9Ut/giphy.gif',
            'https://media.giphy.com/media/XkkHaXnkh55bK3rkLw/giphy.gif',
            'https://media.giphy.com/media/JGcpukTlRlkf7YAJ0B/giphy.gif',
            'https://media.giphy.com/media/HHTybEwS97uRoifAHR/giphy.gif',
            'https://media.giphy.com/media/xKC5e6kJjdV4TrE1rd/giphy.gif',
            'https://media.giphy.com/media/ujQxQVlHyMnhWuMS9m/giphy.gif',
            'https://media.giphy.com/media/HQmFvNg8btasrpqSbf/giphy.gif',
            'https://media.giphy.com/media/sPSKOQGn41AM8bpcqN/giphy.gif'
        ],

        "dance" : [
            'https://media.discordapp.net/attachments/799689564092104738/885485414905970708/tenor_7.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485407746261013/tenor_5.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485407784026162/tenor_6.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485406299238490/tenor_4.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485396622995466/tenor_2.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485394345467944/tenor_3.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485389240991764/tenor_1.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/885485378491015168/tenor_8.gif',
            'https://cdn.discordapp.com/attachments/703316133717213285/885486321081139210/ByHK_IQPb.gif',
            'https://media.discordapp.net/attachments/703316133717213285/885488989568663622/kermit-dance.gif',
            'https://media.discordapp.net/attachments/703316133717213285/886125451163107368/anime-dance_1.gif',
            'https://media.discordapp.net/attachments/703316133717213285/886162194365026354/ByhduIQP-.gif',
            'https://media.discordapp.net/attachments/703272258990374973/886448324159344720/crab-rave-mmd.gif',
            'https://tenor.com/view/yay-yeah-happy-dance-gif-14866505'
        
        ],

        'sleep' : [
            'https://cdn.discordapp.com/attachments/799689564092104738/886127225836015616/tenor_11.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127210912706560/tenor_8.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127200728911882/tenor_10.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127190016675840/tenor_9.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127186472480808/tenor_7.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127176842346496/tenor_6.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127176385183785/tenor_5.gif',
            'https://media.discordapp.net/attachments/799689564092104738/886127174590021632/tenor_4.gif',
            'https://media.discordapp.net/attachments/799689564092104738/886127173587599390/tenor_3.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127158978818108/tenor_1.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127158647488542/tenor_2.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127155107463198/tenor.gif',
            'https://cdn.discordapp.com/attachments/799689564092104738/886127151181594644/tenor_12.gif',
            'https://media.discordapp.net/attachments/703316133717213285/886135952127430676/umaru-umaru-chan.gif'
        ],

        'pout' : [
            'https://cdn.discordapp.com/attachments/843508777177186334/887299073009414144/tenor_1.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299073428840458/tenor.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299078470393937/tenor_3.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299079741243402/tenor_2.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299087743995955/tenor_4.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299092043161610/tenor_5.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299099139911681/tenor_6.gif',
            'https://cdn.discordapp.com/attachments/843508777177186334/887299103409733632/tenor_7.gif'
        ],

        'vibe' :[
            'https://media.giphy.com/media/bZuUnCvOSv3CTKleRz/giphy.gif',
            'https://media.giphy.com/media/5JhiUPPbmmk25J5dPy/giphy.gif',
            'https://media.giphy.com/media/vCheMEtFNI1MoUuJsK/giphy.gif',
            'https://media.giphy.com/media/k8yxkQ9HzUDldZmqpv/giphy.gif',
            'https://media.giphy.com/media/b7Fq9oXDOPgsNLOMgF/giphy.gif',
            'https://media.giphy.com/media/TbrNlFwvkSNfLH023C/giphy.gif',
            'https://media.giphy.com/media/4klUaetpUNmkeTkeoH/giphy.gif',
            'https://media.giphy.com/media/9q1AR4VnNahfgNaKsS/giphy.gif',
            'https://media.giphy.com/media/lApANmHzBQdNsSGXOy/giphy.gif',
        ]


    }

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
        'dance','sleep', 'vibe', 'pout', 'hmph'
    ]

    nekos = [
        'baka', 'bite', 'blush', 'bored', 'cry', 'cuddle',
        'dance', 'facepalmm', 'feed', 'happy', 'hug', 'kiss',
        'laugh', 'pat', 'shrug', 'slap', 'sleep', 'smile',
        'smug', 'stare', 'think', 'thumbsup', 'tickle', 'wave',
        'wink'
    ]

    aliases = {
        "throw":"yeet",
        "hold":"handhold",
        "eat":"nom",
        "hungry":"nom",
        "nom":"bite",
        "superhug":"glomp",
        "thonk":"think",
    }