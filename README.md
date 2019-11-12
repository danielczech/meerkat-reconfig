A tool to resend the most recent observation configuration information 
to specified hosts (processing nodes).

The messages to be resent are retrieved from the
[`meerkat-backend-interface`](https://github.com/danielczech/meerkat-backend-interface)'s Redis database. Specifically, these messages stored in the Redis database by the `coordinator` process. 

### Usage:
<pre>
positional arguments:
  hosts       List of hosts to resend to. Global messages are always
              published. Host names should be of the form
              "[hostname]/[instance_number]" and separated by spaces. For
              example, "blpn48/0 blpn49/0".

optional arguments:
  -h, --help  show this help message and exit
</pre>
