import os, base64
from discord_webhook import DiscordWebhook


#
#  Send the results to the Webhook.
#
def send_results( target, webhook ) -> bool:
    """
    Send results of a target to the specified discord webhook

    Parameters:
    * target : the target that has been scanned
    * webhook : the webhook address of the discord hook
    """

    directory = "./" + base64.b64encode(bytes(target, 'utf-8')).decode('utf-8')

    # Create the Webhook call
    webhook = DiscordWebhook(
        url = webhook, 
        content = f"Finished working on { target }. Here's the results: "
    )

    # Enumarete all files
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Attach all the files
    for file in files:
        with open( directory + "/" + file, "rb" ) as f: 
            webhook.add_file( file = f.read(), filename = f"{ file }")

    # Send away!        
    webhook.execute()
    return True


#
#  Send a msg to the Webhook.
#
def webhook_message( msg, webhook ):
    DiscordWebhook(url=webhook, content=msg).execute()   
    