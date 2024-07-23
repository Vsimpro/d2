"""
*   Nuclei scan module.
"""
import base64, subprocess

#
#   Interface
#
def main( target:str, ratelimit:int = 150 ) -> tuple:
    """
    Wrapper for Nuclei

    Parameters:
    * target: target nuclei will scan
    * ratelimit: the ratelimit to scan with
    
    Returns a tuple:
    - 0, bool: if running the command was succesful or not
    - 1, str or None: exception, none if successful  
    """

    # Prepare the command
    target = target.replace("\n", "")
    directory = "./" + base64.b64encode(bytes(target, 'utf-8')).decode('utf-8')
    _command  = f"/root/nuclei -u http://{ target } -silent -nc -rl { ratelimit } -o { directory }/nuclei_{ target }.txt "
    
    # Begin the Nuclei scan.
    try:
        subprocess.run( _command, shell=True, check=True )

    except subprocess.CalledProcessError as e:
        print( e ); return (False, e)

    return ( True, None )
