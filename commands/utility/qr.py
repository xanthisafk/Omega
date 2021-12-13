import discord
from discord.ext import commands
import APIs.color as rang
import datetime
import qrcode
from io import BytesIO

class MissingQRData(Exception):
    def __init__(self):
        super().__init__(f"Data is missing for QR code to generate.")

class Qr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command(name='qr',aliases=['qrcode'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def qrcode(self, ctx,*, data:str=None):
    
        name = "qr"

        if data is None:
            raise MissingQRData()
        image = qrcode.make(data)
        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            embed = discord.Embed(description=f"Here is your QR code.", color=await rang.get_color())
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            file=discord.File(fp=image_binary,filename="qr.png")
            embed.set_image(url="attachment://qr.png")
            await ctx.send(embed=embed, file=file)

    @qrcode.error
    async def qrcode_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'You are on cooldown. Try again in {error.retry_after:.2f} seconds.')
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, MissingQRData):
                await ctx.send(f'Missing required argument: *D A T A*')
            else:
                await ctx.send(f'An unexpected error has occured.')
                raise error
        else:
            await ctx.send("Some unexpected error occured")
            raise error

def setup(bot):
    bot.add_cog(Qr(bot))
