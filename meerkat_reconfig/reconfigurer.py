import redis
import sys

class Reconfigurer(object):
    """Read most recent observation config information 
    from Redis and publish the information to the 
    corresponding processing nodes.
    """

    def __init__(self, redis_host = '127.0.0.1', redis_port = '6379', hpgdomain = 'bluse'):
        """Connect to Redis server.
        """
        self.redis_host = redis_host
        self.port = redis_port
        self.hpgdomain = hpgdomain
        self.redis_server = redis.StrictRedis(redis_host, redis_port)

    def read_obs_info(self, host):
        """Read in the most recent stored configuration 
        information for an observation.
        """
        host_channel = '{}://{}/set'.format(self.hpgdomain, host)
        host_msgs = self.redis_server.hgetall(host_channel)
        msg_list = []
        for key in host_msgs:
            val = host_msgs[key]
            msg_list = msg_list + ['{}={}'.format(key, val)]
        return msg_list

    def republish(self, host_channel, msg_list):
        """Sequentially republish messages for a host.
        """
        for msg in msg_list:
            self.redis_server.publish(host_channel, msg)

    def reconfigure(self, hosts):
        """Republish the relevant messages to the 
        specified hosts. 
        """
        # Global host redis channels
        global_channel = '{}:///set'.format(self.hpgdomain)
        try:
            global_msgs = self.read_obs_info('')
        except:
            print('Could not find messages for channel {}.'.format(global_channel))
            sys.exit(0)
        self.republish(global_channel, global_msgs)
        # Host-specific redis channels
        # Sequentially publish each message to each host channel
        if(hosts != 'global'):
            for host in hosts.split():
                host_channel = '{}://{}/set'.format(self.hpgdomain, host)
                try:
                    msg_list = self.read_obs_info(host)
                except:
                    print('Could not find messages for channel {}.'.format(host_channel))
                    continue       
                self.republish(host_channel, msg_list)            
        
