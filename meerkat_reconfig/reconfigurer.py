# Reconfigurer class for accessing and republishing messages to 
# processing nodes. 

import redis
import sys

class Reconfigurer(object):
    """Reads the most recent observation config information 
    from Redis and publishes the information to the 
    corresponding processing nodes.
    """

    def __init__(self, redis_host = '127.0.0.1', redis_port = '6379', 
        hpgdomain = 'bluse'):
        """Initialise and connect to Redis server.

        Args:
            redis_host (str): IP address of Redis host. 
            redis_port (str): IP address of Redis port.
            hpgdomain (str): Hashpipe-Redis Gateway domain name.   

        Returns:
            None
        """
        self.redis_host = redis_host
        self.port = redis_port
        self.hpgdomain = hpgdomain
        self.redis_server = redis.StrictRedis(redis_host, redis_port)

    def read_obs_info(self, host):
        """Read in the most recent stored observation configuration 
        information for one host.

        Args:
            host (str): Name of specified host (including instance
            number) of the form [host_name]/[instanc_number].
            eg: blpn48/0

        Returns:
            msg_list (list): A list (of strings), of which each item 
            is a Hashpipe-Redis gateway message. These messages
            were published to this particular host at the most
            recent time a subarray was configured.   
        """
        host_channel = '{}://{}/set'.format(self.hpgdomain, host)
        host_msgs = self.redis_server.hgetall(host_channel)
        msg_list = []
        for key in host_msgs:
            val = host_msgs[key]
            msg_list = msg_list + ['{}={}'.format(key, val)]
        return msg_list

    def republish(self, host_channel, msg_list):
        """Sequentially republish messages for a particular host.
           
        Args:
            host_channel (str): Full name of the Redis channel for 
            a particular host (eg bluse://blpn48/0/set).
            msg_list (list): List of messages (str) to be published
            to the host Redis channel.

        Returns:
            None
        """
        for msg in msg_list:
            self.redis_server.publish(host_channel, msg)

    def gen_host_names(self, firsthost, lasthost, prefix, inst_num):
        """Generate a list of host names according to a range of
        host numbers and the host naming convention. 
        """
        host_names = []
        for i in range(firsthost, lasthost + 1):
            host_names = host_names + ['{}{}/{}'.format(prefix, i, inst_num)]
        return host_names 

    def reconfigure(self, hosts):
        """Republish the relevant messages to the 
        specified hosts. Also publishes global messages, but only to 
        the hosts listed.

        Args:
            hosts (list): List containing all user-entered hosts (str)
            to publish to.
   
        Returns:
            None
        """
        # Global host redis channels
        global_channel = '{}:///set'.format(self.hpgdomain)
        global_msg_list = self.read_obs_info('')
        if(len(global_msgs) == 0):
            print('Could not find messages for global channel: {}.'.format(global_channel))
        # Host-specific redis channels
        # Sequentially publish each message to each host channel
        for host in hosts:
            host_channel = '{}://{}/set'.format(self.hpgdomain, host)
            msg_list = self.read_obs_info(host)
            if(len(msg_list) == 0):
                print('Could not find messages for channel: {}.'.format(host_channel))
                continue       
            self.republish(host_channel, global_msg_list)
            self.republish(host_channel, msg_list)            
        
