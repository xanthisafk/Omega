import asyncio

import aiohttp

import APIs.color as rang
import discord
import requests
from discord.ext import commands
import loggers.logger as log

class Dog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.group(aliases=['puppy', 'doggo','puper','doggy','pupper'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx, *, breed=None):

        if breed == None:
            url = 'https://dog.ceo/api/breeds/image/random'
            text = f'[Here is a {ctx.invoked_with.capitalize()} photo](https://dog.ceo/)'

        elif breed == 'german shepherd':
            url = 'https://dog.ceo/api/breed/germanshepherd/images/random'
            text = '[Here is a German Shephard photo](https://dog.ceo/)'

        else:
            breed = breed.lower()
            try:
                breed = breed.split(' ')
                breed, type = breed[0], breed[1]
                url = f'https://dog.ceo/api/breed/{type}/{breed}/images/random'
                text = f'[Here you go, a {breed.capitalize()} {type.capitalize()} photo](https://dog.ceo/)'
            except:
                url = f'https://dog.ceo/api/breed/{breed[0]}/images/random'
                text = f'[Here is a {breed[0]} photo](https://dog.ceo/)'
        
        color = await rang.get_color()
        name = 'Dog'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                js = await response.json()
                await session.close()

        if js['status'] == 'error':
            await ctx.send('Breed not found.')
            return
        else:
            url = js['message']

        embed = discord.Embed(description=text,color = color)
        embed.set_image(url=url)
        embed.set_footer(text='Powered by dog.ceo')
        await ctx.send(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')

    @commands.command()
    async def breeds(self,ctx):

        color = await rang.get_color()
        embed = discord.Embed(color=color)

        b1 = '`affenpinscher`, `african`, `airedale`, `akita`, `appenzeller`, `australlian shepherd`, `basenji`, `beagle`, `bluetick`, `borzoi`, `bouvier`, `boxer`, `brabancon`, `braiard`, `norwegian buhund`, `boston bulldog`, `english bulldog`, `french bulldog`, `staffordshire bullterrier`, `australlian cattledog`, `chihuahua`, `chow`, `clumber`, `cockapoo`, `border collie`, `coonhound`, `cardigan corgi`, `cotondetulear`, `dachshund`, `great dane`, `scottish deerhound`, `dhole`, `dingo`, `doberman`, `norwegian elhound`, `entlebucher`, `eskimo`, `lapphund finnish`, `bichon frise`, `german shepherd`, `italian greyhound`, `groenendael`, `havanese`, `afghan hound`, `basset hound`, `blood hound`, `english hound`, `ibizan hound`, `plott hound`, `walker hound`, `husky`, `keeshond`, `kelpie`, `komondor`, `kuvasz`, `labradoodle`, `labrador`, `leonberg`, `lhasa`, `malamute`, `malese`, `bull mastiff`, `tibetan mastiff`, `mexicanhairless`, `mix`, `bernese mountain`, `swiss mountain`, `newfoundland`, `otterhound`'
        b2 = '`caucasian ovcharka`, `papillon`, `perkinese`, `pembroke`, `miniature pinscher`, `pitbull`, `german pointer`, `germanlonghair pointer`, `pomeranian`, `miniature poodle`, `standard poodle`, `toy poodle`, `pug`, `ouggle`, `pyrenees`, `redbone`, `chesapeake retriever`, `curly retriever`, `flatcoated retriever`, `golden retriever`, `rhodesian ridgeback`, `rottwriler`, `saluki`, `samoyed`, `schipperke`, `giant schnauzer`, `miniature schnauzer`, `english setter`, `gordon setter`, `irish setter`, `english sheepdog`, `shetland sheepdog`, `shiba`, `shihtzu`, `blenheim spaniel`, `brittany spaniel`, `cocker spaniel`, `irish spaniel`, `japanese spaniel`, `sussex spaniel`, `welsh spaniel`, `english springer`, `stbernard`, `americal terrier`, `australlian terrier`, `bedlington terrier`, `border terrier`, `cairn terrier`, `irish terrier`, `kerryblue terrier`, `lakeland terrier`, `norfolk terrier`, `norwich terrier`, `patterdale terrier`, `russel terrier`, `scottish terrier`, `sealyham terrier`, `silky terrier`'
        breed = [b1,b2]

        embed.add_field(name='Breeds',value=breed[0])
        embed.set_footer(text='Powered by dog.ceo')

        total = 2
        current = 1
        min=1
        
        message = await ctx.send(embed=embed)

        right_e = self.bot.get_emoji(898963538004021318)
        left_e = self.bot.get_emoji(898963539912437771)

        await message.add_reaction(left_e)
        await message.add_reaction(right_e)

        def check(reaction, user):
                return user == ctx.author and reaction.emoji in [left_e, right_e]
        
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)

                embed.remove_field(0)

                if reaction.emoji == right_e and current != total:
                    current+=1
                    embed.add_field(name='Breeds',value=breed[current-1])
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)

                elif reaction.emoji == left_e and current > min:
                    current-=1
                    embed.add_field(name='Breeds',value=breed[current-1])
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                
                else:
                    await message.remove_reaction(reaction, user)


            except asyncio.TimeoutError:
                await message.edit(content="Message timed out")
                break

    @dog.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'Ask for a dog photo in {round(error.retry_after, 2)} seconds.')
            await log.logger(ctx,'Dog',self.cog_name,'ERROR',message=error)
            return


def setup(bot):
    bot.add_cog(Dog(bot))
