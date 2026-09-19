#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class CustomNetworkTopo( Topo ):
    "Topologia com 4 switches interligados e 12 hosts distribuidos."
    def build( self, n=12 ):
        # a) Criacao de 4 switches
        s1 = self.addSwitch( 's1' )  # Switch central / agregacao
        s2 = self.addSwitch( 's2' )  # Switch de borda 1
        s3 = self.addSwitch( 's3' )  # Switch de borda 2
        s4 = self.addSwitch( 's4' )  # Switch de borda 3

        # Interligacao dos switches (backbone em estrela/arvore)
        self.addLink( s1, s2, bw=100, delay='1ms' )
        self.addLink( s1, s3, bw=100, delay='1ms' )
        self.addLink( s1, s4, bw=100, delay='1ms' )

        # Lista de switches de borda para distribuicao dos hosts
        edge_switches = [ s2, s3, s4 ]

        # Criacao dos hosts (12 hosts, atendendo ao requisito de no minimo 11)
        for h in range( n ):
            host_name = 'h%s' % ( h + 1 )
            host = self.addHost( host_name, cpu=0.5 / n )
            
            # Distribui ciclicamente entre s2, s3 e s4
            selected_switch = edge_switches[ h % len(edge_switches) ]
            
            self.addLink( host, selected_switch, bw=10, delay='5ms', loss=0,
                          max_queue_size=1000, use_htb=True )

def perfTest( net ):
    "b) Testa a largura de banda entre h1 e todos os demais hosts da rede"
    h1 = net.get( 'h1' )
    other_hosts = [ h for h in net.hosts if h != h1 ]

    print("\n*** Running bandwidth tests between h1 and all other hosts ***")
    for other in other_hosts:
        print(f"\n--- Testing bandwidth between {h1.name} and {other.name} ---")
        net.iperf( ( h1, other ) )

if __name__ == '__main__':
    topo = CustomNetworkTopo( n=12 )
    net = Mininet( 
        topo=topo,
        host=CPULimitedHost,
        link=TCLink
    )
    net.start()
    
    print("Dumping host connections")
    dumpNodeConnections( net.hosts )
    
    print("Testing network connectivity")
    net.pingAll()
    
    setLogLevel( 'info' )
    perfTest( net )
    
    net.stop()
