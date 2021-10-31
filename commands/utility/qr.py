import nextcord
from nextcord.ext import commands
import APIs.color as rang
import loggers.logger as log
import qrcode
from io import BytesIO

class Qr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command(name='qr',aliases=['qrcode'])
    async def qrcode(self, ctx,*, data:str=None):
    
        name = "qr"

        if data is None:
            return await ctx.send("Give me some *D A T A* to encode!")
        try:
            image = qrcode.make(data)
            with BytesIO() as image_binary:
                image.save(image_binary, "PNG")
                image_binary.seek(0)
                await ctx.send('Here is your QR code:',file=nextcord.File(fp=image_binary,filename="qr.png"))
            await log.logger(ctx, name, self.cog_name, 'INFO')
    
        except Exception as error:
            await ctx.send('Some error occured')
            await log.logger(ctx, name, self.cog_name, 'ERROR', error)

def setup(bot):
    bot.add_cog(Qr(bot))
