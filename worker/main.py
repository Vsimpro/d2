from dotenv import load_dotenv; load_dotenv()

from .modules.send_data import *
from .modules.use_tools import *

# Global Variables
WEBHOOK = os.getenv("WEBHOOK")
targets = []


def main( data ) -> bool:
    """
    Handle running the tools against the target,
    as per the selections. Basically a wrapper,
    for the wrapper.

    Parameters:
    * data: a dict() with the target & tools selections

    Returns:
    * bool: True if scanning went smoothly, False if not
    """

    global targets
    global WEBHOOK

    target = data["target"]

    if target in targets:
        # Target being worked on or had an error.
        webhook_message( f"> [!] Has been scanned recently, or had an error: \t`{ target }`!", WEBHOOK)
        return False
    
    # Mark job as being worked on & Start analyzing the target
    targets.append( target )
    webhook_message( f"> [+] Starting to work on:\t`{ target }`", WEBHOOK )
    
    if not scan( data ):
        # Upon error, notify the user
        webhook_message( f"> [!] Ran into an error on:\t`{ target }`!", WEBHOOK)
        return False
    
    # Remove from the storage if everything went smooth
    for index in range( len(targets) ):
        if targets[ index ] == target:
            targets.pop( index )

    return True
