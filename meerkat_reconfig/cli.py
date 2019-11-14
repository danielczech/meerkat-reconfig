#Reconfigurer CLI script

import sys
import argparse
from .reconfigurer import Reconfigurer

def cli(args = sys.argv[0]):
    usage = "{} [options]".format(args)
    description = """Resend configuration messages to specified 
                  hosts (processing nodes)."""
    parser = argparse.ArgumentParser(prog = 'meerkat-reconfigurer', 
        usage = usage, description = description) 
    help_info = """List of hosts to resend to. Global messages are 
               also published, but only to the listed hosts. 
               Host names should be of the form 
               \"[hostname]/[instance_number]\". For example, 
               \"blpn48/0\"."""
    parser.add_argument('hosts', nargs = '+', type = str, help = help_info)
    if(len(sys.argv[1:])==0):
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(hosts = args.hosts)

def main(hosts):
    reconfigurer = Reconfigurer()
    reconfigurer.reconfigure(hosts)

