import os, time, dotenv, discord, asyncio
dotenv.load_dotenv()

import worker.main as worker

from discord.ext import commands
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

# Global Variables
storage = {}
TOKEN   = os.getenv( "TOKEN" )
WEBHOOK = os.getenv( "WEBHOOK" )

executor = ThreadPoolExecutor()

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


#
#   Helper functions / Implementation
#

def toggle( message, tool ):
    """
    Toggle a tool to be used or not in the dict().

    Parameters:
    * message: the message object that is reacted to
    * tool: the tool that is toggled on / off 
    """

    global storage
    storage[ message ][tool] = True if not storage[ message ][tool] else False


def ensure_unique( target ) -> bool:
    """
    Make sure the target given to the Queue is already not in Queue

    Parameters: 
    * target: the user given target

    Returns:
    * bool: False if not unique, True if it is
    """
    global storage
    
    for message in storage:
        if storage[message] == None:
            continue
        
        if storage[message]["target"] == target:
            return False
        
    return True


# Bit poorly named
def check_target( target:str ):
    """
    Takes the given target and creates a properly formed domain. 
    Returns "" if malformed.

    Parameters:
    * target: the user given target

    Returns:
    * target: but formatted. Empty if unsuccesful
    """
    result = urlparse( target )
    return result.path + result.netloc


async def add_reactions( message, list_of_reactions:list ):
    """
    Add multiple reactions into one message object

    Parameters:
    * message: the message object reactions should be added to
    * list_of_reactions: a list of reactiosn that are to be added
    """
    for reaction in list_of_reactions:
        while 1:
            try:
                await message.add_reaction( reaction ); break
            except discord.errors.HTTPException as e:
                print( e ); time.sleep( 1 )


#
#   Bot interactions
#
@bot.command(name='add')
async def add(ctx, target):
    """
    The command 'add':
    Should add create a new prompt and begin the process
    for scanning the 'target' with selected tools.

    Targets and their progress is monitored in the global
    variable dict:'storage'.
    """

    global storage

    # Ensure target is properly formed
    target = check_target( target )    
    if target == "" or "." not in target:
        
        # Notify user target is not in the form of a domain
        message = await ctx.send(
            f"", 
            embed=discord.Embed(
                title = "",
                url="", 
                description = f"""
                The desired target: " { target } "
                does not match the format of a Domain. The target should look something like this (without defangs, [:]):\n- example.com\n- sub.example.com\n- http[:]//sub.example.com\n- https[:]//example.com/resource\n\t- (<resource> will be stripped)\n- http[:]//sub.example.com:8000
                """, 
                color = discord.Color.blue()
            )
        )   
        return

    # Ensure the target is not in selection right now. 
    if not ensure_unique( target ):
        # Notify the user target is in queue
        message = await ctx.send(
            f"", 
            embed=discord.Embed(
                title = "",
                url="", 
                description = f"""
                The desired target: `{ target }`
                is already in the queue!
                """, 
                color = discord.Color.blue()
            )
        )   
        return

    # Begin the selection process via the prompt
    message = await ctx.send(
        f"", 
        embed=discord.Embed(
            title = "",
            url="", 
            description = f"""
            Adding a domain target: `{ target }`
            Select all the tools you want to use:
            
            >    🤖\t `subfinder`
            >    🔥\t `feroxbuster`
            >    🐉\t `nuclei`
            >    👓\t `nmap`
            
            and select :white_check_mark: once you're ready to launch!
            """, 
            color = discord.Color.blue()
        )
    )   

    # Store the states
    storage[message] = {
        "target"      : str(target),
        "nmap"        : False,
        "nuclei"      : False,
        "feroxbuster" : False,
        "subfinder"   : False,
        "locked"      : False
    }

    # Repeat glasses as a timeout.
    await add_reactions(message, ["🤖","🔥","🐉", "👓", "👓", "👓",  "✅" ])


@bot.event
async def on_reaction_add(reaction, user):
    """
    Monitors the reacts to the prompts. 
    Reacts are being used as selection for the tools in use.
    'white_check_mark' should lock in the selection, and
    send the job into RabbitMQueue.
    """
    
    global storage
    
    message = reaction.message 
    emoji = reaction.emoji.encode()
    emoji_actions = {
        b"\xe2\x9c\x85":     "locked",
        b"\xf0\x9f\x91\x93": "nmap",
        b"\xf0\x9f\x90\x89": "nuclei",
        b"\xf0\x9f\x94\xa5": "feroxbuster", 
        b"\xf0\x9f\xa4\x96": "subfinder" ,
    }

    # Make sure the prompt has pre-requisites, and bot is not the one reacting.
    if not (reaction.message in storage) or not (user != bot.user):
        return
    
    # If prompt is locked, do not continue.
    if storage[ reaction.message  ]["locked"]:
        return

    # Reacting with a non-defined emoji.
    if not emoji in emoji_actions:
        return 

    # Toggle selections.    
    toggle( message, emoji_actions[ emoji ] )

    # User has selected tools, continue to scanning.
    if storage[ message ]["locked"]:
        await reaction.message.clear_reactions()
        await reaction.message.add_reaction("📫")
        
        # Start the worker
        result = await asyncio.to_thread( worker.main, storage[ reaction.message ] )

        if result:
            await reaction.message.clear_reactions()
            await reaction.message.add_reaction("☑️")

            # Delete target from Queue
            storage[ reaction.message ] = None

        if not result:
            await reaction.message.clear_reactions()
            await reaction.message.add_reaction("❌")


if __name__ == "__main__":
    env_variables_exist = True
    if TOKEN == None or TOKEN == "":
        print( "! Ensure the Discord bot token exists in the .env variable, as TOKEN." )
        env_variables_exist = False

    if WEBHOOK == None or WEBHOOK == "":
        print( "! Ensure the Discord webhook exists in the .env variable, as WEBHOOK." )
        env_variables_exist = False

    if not env_variables_exist:
        exit( 2 )

    # Start the bot
    bot.run(TOKEN)
