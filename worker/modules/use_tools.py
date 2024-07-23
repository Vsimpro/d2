import os, shutil, base64

from .send_data import *

from .tools.nmap import main as nmap
from .tools.nuclei import main as nuclei
from .tools.subfinder import main as subfinder
from .tools.feroxbuster import main as feroxbuster

# Global variables
webhook = os.getenv("WEBHOOK")


def run_tool( selection, target ) -> bool:
    """
    Runs the selected tool against the specified target

    Returns:
    * bool: True on success, False if not
    """
    global webhook

    # Tools and their functions / modules
    tools = {
        "nmap"          : nmap,
        "nuclei"        : nuclei,
        "subfinder"     : subfinder,
        "feroxbuster"   : feroxbuster,
    }

    # Call the tools main() function
    success, error = tools[ selection ]( target )

    webhook_message( f"> [✓] { selection } for `{ target }` done ..", webhook )

    # Logging for errors
    if error: 
        print( error )
        webhook_message( f"> [✘] { selection } for `{ target }` ran into an issue!\n Details: { error } ", webhook )
    
    return success


def scan( selection ) -> bool:
    """
    Determine which tools should be used, 
    send out the results and perform cleanup.

    Parameters:
    * selection: a dict( tool : boolean ) that includes the tools selected

    Returns:
    * bool: True on success, False if not
    """
    global webhook

    # Go through the tools
    for tool in selection:
        if tool == "locked" or tool == "message" or tool == "target":
            continue

        # If tool is selected,
        if selection[tool]:

            # Create a dir for outputs if not exist
            directory = "./" + base64.b64encode(bytes(selection["target"], 'utf-8')).decode('utf-8')
            if not os.path.exists( directory ): 
                os.makedirs( directory )
            
            # Run the selected tool
            if not run_tool( tool, selection["target"] ):
                return False

    # Send results back
    send_results( selection["target"], webhook )

    # Cleanup the folders after scanning
    if os.path.exists(directory):
        shutil.rmtree(directory)

    return True
