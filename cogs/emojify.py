import discord
from discord.ext import commands
from emojifier import Emojifier
import json
import loggers.logger as log

class Emoji(commands.Cog):
    cog_name = 'Emoji'
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def emojify(self,ctx,*,text=None):
        name = 'Emojify'
        
        try:
            # Loads the emoji-mappings.json file
            with open("files/emoji-mappings.json", "r", encoding="utf8") as f:
                mapping = json.load(f)
            emoji = Emojifier.of_custom_mappings(mapping)
            
            # Checks if no text was given
            if text == None:
                temp = '❌ You need to have some text. Where text?'
                temp = emoji.generate_emojipasta(temp)
                await ctx.send(temp)
                await log.event_logger(ctx,name,self.cog_name)
                return

            # Checks if length of given text is less than 1500
            elif len(text) > 1500:
                temp = '❌ Maximum 1500 characters allowed. One you have is too big for me!'
                temp = emoji.generate_emojipasta(temp)
                await ctx.send(temp)
                await log.event_logger(ctx,name,self.cog_name)
                return

            # Runs the actual code if both test cases pass
            else:
                text = emoji.generate_emojipasta(text)
                await ctx.send(text)
                await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

def setup(client):
    client.add_cog(Emoji(client))