## meerkat-reconfig

A tool to resend the most recent observation configuration information 
to specified hosts (processing nodes). Useful when developing/debugging
BLUSE processes. 

The messages to be resent are retrieved from the
[`meerkat-backend-interface`](https://github.com/danielczech/meerkat-backend-interface)'s 
Redis database. Specifically, the messages stored in the Redis database 
by the `coordinator` process. 

### Usage:

Resend configuration messages for processing node 48, instance 0:  
`meerkat-reconfig blpn48/0`

Resend configuration messages for instance 0 of processing nodes
in the range 48-63:  
`meerkat-reconfig blpn{48..63}/0`

<pre>
positional arguments:
  hosts       List of hosts to resend to. Global messages are always
              published. Host names should be of the form
              "[hostname]/[instance_number]". For example, "blpn48/0".

optional arguments:
  -h, --help  show this help message and exit
</pre>
