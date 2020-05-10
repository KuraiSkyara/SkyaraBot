#Discord
import discord
from discord.ext import commands
#Web scraping tools
import requests
from bs4 import BeautifulSoup

#New command format
#@commands.[method]
#async def Method(self, [ctx], [other parameters])

class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Search fn return formatting
    @commands.command()
    async def ws(self,ctx):
        embed = discord.Embed(
            title = 'Seox',
            description = 'Max HP: 1666/1966 | Max ATK: 6666/8666 | Erune | Melee',
        )

        embed.set_footer(text='https://gbf.wiki/Seox')
        embed.set_image(url='https://gbf.wiki/images/thumb/7/76/Npc_zoom_3040035000_01.png/480px-Npc_zoom_3040035000_01.png')
        embed.set_thumbnail(url='https://gbf.wiki/images/thumb/7/73/Npc_m_3040035000_01.jpg/100px-Npc_m_3040035000_01.jpg')

        #Ougis
        embed.add_field(name='Ougi [Void Claws: Terminus]', value='Massive Dark damage to a foe. Gain <:yggWow:541630544253943832> Mirror Image (2 times)', inline=False)
        embed.add_field(name='Ougi [Three Thousand and One Talons]', value='Massive Dark damage to a foe. Gain Mirror Image (2 times) and Other Self (1 time)', inline=False)

        #Skills
        embed.add_field(name='Gate of Sin', value='Gain 20% DMG Amplified. \n[LV95] Buff increased to 30% DMG Amplified\n Also gain 60% Bonus Dark DMG', inline=False)
        embed.add_field(name='Thunderflash', value='Gain Hostility UP and Counters on Dodge (3 times)\n[LV85] Counter upgraded to Counters on Dodge/DMG (6 times)', inline=False)
        embed.add_field(name='Gate of Demons', value='600% Dark damage to all foes (Damage cap: ~700,000). Inflict Petrified\n[LV90] Also inflict Accuracy Lowered', inline=False)
        embed.add_field(name='Six-Ruin\'s Enlightenment', value='Gain Other Self and Double Strike. (Can\'t Recast)', inline=False)

        await ctx.send(embed=embed)

    #Search fn testing
    @commands.command()
    async def srtest(self,ctx,*str):
        seperator = "_"
        term = seperator.join(str)
        term = "https://gbf.wiki/" + term.title()
        sritem = requests.get(term)

        wikiSoup = BeautifulSoup(sritem.content,'html.parser')
        print(wikiSoup.prettify())

        await ctx.send("Webpage stored.\n" + term)

#Setup function
#Use file name to load the cog, and use class name as the parameter for add_cog
def setup(bot):
    bot.add_cog(WikiCog(bot))
