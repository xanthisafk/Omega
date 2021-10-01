import random,json

class EmbedTextEmote():

    async def create_string(self,*,type,user1,user2):

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

