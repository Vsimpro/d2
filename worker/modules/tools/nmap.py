"""
*   Module for Nmap
"""
import base64, subprocess

#
#   Interface 
#
def main( target:str, flags:str="-T4" ) -> tuple:
    """
    Wrapper for NMAP.

    Parameters:
    * target: target feroxbuster will scan
    * flags: additional flags as a string
    
    Returns a tuple:
    - 0, bool: if running the command was succesful or not
    - 1, str or None: exception, none if successful  
    """

    # Prepare the command
    directory = "./" + base64.b64encode(bytes(target, 'utf-8')).decode('utf-8')
    _command = f"nmap { target } { flags } -o {directory }/nmap_{ target }.txt" 

    # Run Nmap
    try:
        subprocess.run( _command, shell=True, check=True )

    except subprocess.CalledProcessError as e:
        return ( False, e )

    return ( True, None )
