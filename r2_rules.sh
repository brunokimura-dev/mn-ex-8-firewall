
iptables -F
iptables -t nat -F

iptables -t filter -A FORWARD -d 200.131.132.0/24 -p tcp --dport 80 -j ACCEPT
iptables -t filter -A FORWARD -s 200.131.132.0/24 -p tcp --sport 80 -j ACCEPT

ifconfig r2-eth0:0 200.131.132.15/24

iptables -t nat -A PREROUTING -d 200.131.132.15 -p tcp --dport 80 -m statistic --mode random --probability 0.5 -j DNAT --to-destination 200.131.132.10:80
iptables -t nat -A PREROUTING -d 200.131.132.15 -p tcp --dport 80 -j DNAT --to-destination 200.131.132.20:80

iptables -A FORWARD -j REJECT
#REJECT
