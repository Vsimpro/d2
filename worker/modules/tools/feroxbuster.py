"""
*   Module for FeroxBuster
"""
import base64, subprocess

#
#   Interface 
#
def main( target:str, use_tls:bool=False, ratelimit:int=150 ) -> tuple:
    """
    Wrapper for Feroxbuster.

    Parameters:
    * target: target feroxbuster will scan
    * use_tls: scheme, do we use https or http
    * ratelimit: set the ratelimit
    
    Returns a tuple:
    - 0, bool: if running the command was succesful or not
    - 1, str or None: exception, none if successful  
    """
    
    url = str( str( "http" if not use_tls else "https" ) + "://" + target ) # Use https:// if enabled, else go for http://
    directory = "./" + base64.b64encode(bytes(target, 'utf-8')).decode('utf-8')
    
    # Prepare the command
    _command = f"feroxbuster -u { url } -r --rate-limit { ratelimit } --timeout 10 -o { directory }/feroxbuster_{ target }.txt" 

    # Run FeroxBuster
    try:
        subprocess.run( _command, shell=True, check=True )

    except subprocess.CalledProcessError as e:
        return ( False, e )

    return ( True, None )
