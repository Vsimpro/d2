"""
*   Module for subfinder
"""
import base64, subprocess

#
#   Interface 
#
def main( target:str ) -> tuple:
    """
    Wrapper for subfinder.

    Parameters:
    * target: target subfinder will scan

    Returns a tuple:
    - 0, bool: if running the command was succesful or not
    - 1, str or None: exception, none if successful  
    """

    # Prepare commands
    directory = "./" + base64.b64encode(bytes(target, 'utf-8')).decode('utf-8')
    _command = f"/root/subfinder -d { target } -o {directory }/subfinder_{ target }.txt" 

    # Run Nmap
    try:
        subprocess.run( _command, shell=True, check=True )
    except subprocess.CalledProcessError as e:
        return ( False, e )

    return ( True, None )
