#Discord
import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook

#Twitter
import tweepy
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Command format
#async def Method(self, ctx, [other parameters])

#Listens and reacts to user-specified accounts
class skyListener(StreamListener):
    def __init__ (self,hook):
        super().__init__()
        self.hook = hook

    def on_status(self, status):
        #Called when tweet data has been received
        try:
            tweetURL = "https://twitter.com/%s/status/%s" % (status.user.screen_name, status.id)
            webhook = DiscordWebhook(url=self.hook, content=tweetURL)
            response = webhook.execute()
            print("Response: %s, Data: %s" % (response, tweetURL))

        except Exception as e:
            print("An error has occurred: %s" % (e))

        return True

    def on_error(self,status):
        #Called if there is an issue with tweet data
        webhook = DiscordWebhook(url=self.hook, content="Error %s; ")
        webhook.execute()
        return False

#TweetCog command class
class TweetCog(commands.Cog):
    def __init__(self, bot, auth, hook):
        self.bot = bot
        self.auth = auth
        self.hook = hook 

    @commands.command(aliases=['tw'])
    async def twitter(self, ctx, option='0', user='0'):

        #Add users to stream listener
        if option == "-a":
            if user == '0': return await ctx.send("Please specify a user to add")
            api = tweepy.API(self.auth)
            try:
                #Attempt to add the user by getting the user's ID from Twitter
                user_to_add = api.get_user(user)
                with open('stream_users.txt', 'a') as fout:
                    fout.write(str(user_to_add.id)+'\n')

                await ctx.send("User **%s** added to Stream" % user_to_add.screen_name)
            except Exception as e:
                print("An error has occurred: %s" % (e))
                await ctx.send("Failed to add the user")


        #Begin streaming tweets            
        elif option == "-s":
            #Open a StreamListener to track tweets from specified users
            with open('stream_users.txt') as f:
                users_to_stream = f.read().splitlines()

            listener = skyListener(self.hook)
            skyStream = Stream(self.auth, listener)
            skyStream.filter(follow=users_to_stream, is_async=True)
            await ctx.send("Now streaming ...")

        else:
            await ctx.send("Options are: -a, -s")    
                                
#Setup function
#Use file name to load the cog, and use class name as the parameter for add_cog
def setup(bot):
    #Get API tokens from file
    #twitter_data is structured as follows: ['consumerToken', 'consumerToken_secret', 'accessToken', 'accessToken_secret', <webhooks>]   
    with open('tToken.txt') as f:
        twitter_data = f.read().splitlines()

    #Setup API access
    auth = tweepy.OAuthHandler(twitter_data[0], twitter_data[1])
    auth.set_access_token(twitter_data[2], twitter_data[3])

    #Setup cog
    bot.add_cog(TweetCog(bot, auth, twitter_data[4]))
