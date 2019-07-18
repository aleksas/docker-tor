import os
nodes = int(os.environ['NODES'])

tor_port_start = 7050
delegate_port_start = 8050

delegate_version = '9.9.13'

start_sh_body = '''
#!/bin/sh

rm /etc/resolv.conf
echo "nameserver 127.0.0.1" > /etc/resolv.conf
resolvconf -u
ifdown -a
ifup -a

# prepare tor folders
mkdir -p %s
chmod -R 700 /var/db/tor

# launch 10 tors
%s

# launch 10 delegated
DELEGATE_VERSION=9.9.13
%s

# launch haproxy
haproxy -f /etc/default/haproxy.conf -q -db'''

tor_command = '/usr/local/bin/tor --SocksPort %d --PidFile /var/run/tor/%d.pid --RunAsDaemon 1 --DataDirectory /var/db/tor/%d'
delegate_command = '/tmp/delegate%s/src/delegated -P%d SERVER=http SOCKS=localhost:%d PIDFILE=/var/run/delegated/%d.pid OWNER=root/root'
pid_dir = '/var/db/tor/%d'

tor_commands = []
delegate_commands = []
pid_dirs = []

haproxy_conf_body = '''
global
  daemon
  user root
  group root
 
defaults
    mode http
    maxconn 50000
    timeout client 3600s
    timeout connect 1s
    timeout queue 5s
    timeout server 3600s

listen stats
  bind 0.0.0.0:2090
  mode http
  stats enable
  stats uri /
 
listen TOR-in
  bind 0.0.0.0:9100
  default_backend TOR
  balance roundrobin
 
listen Socks-in
  mode tcp
  bind 0.0.0.0:9101
  default_backend Socks 
  balance roundrobin

backend TOR
%s

backend Socks 
%s
'''

backend_tor_command = '  server 127.0.0.1:%d 127.0.0.1:%d check'
backend_socks_command = '  server 127.0.0.1:%d 127.0.0.1:%d check'

backend_tors = []
backend_socks = []

for i in range(1, nodes + 1):
    tor_commands.append( tor_command % (tor_port_start + i, i, i) )
    delegate_commands.append( delegate_command % (delegate_version, delegate_port_start + i, tor_port_start + i, i) )

    backend_tors.append( backend_tor_command % (delegate_port_start + i, delegate_port_start + i) )
    backend_socks.append( backend_socks_command % (tor_port_start + i, tor_port_start + i) )
    pid_dirs.append( pid_dir % i )

with open('/start.sh', 'w') as fh:
  content = start_sh_body % (' '.join(pid_dirs), '\n'.join(tor_commands), '\n'.join(delegate_commands))
  fh.write( content.replace('\r', '') )

with open('/etc/default/haproxy.conf', 'w') as fh:
  fh.write(haproxy_conf_body % ('\n'.join(backend_tors), '\n'.join(backend_socks)))    
