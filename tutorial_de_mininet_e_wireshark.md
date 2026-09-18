# Tutorial: Emulação de Redes com Mininet e Análise de Tráfego com Wireshark

Este repositório contém um roteiro prático demonstrando o provisionamento de topologia de rede emulada utilizando **Mininet**, inspeção de interfaces virtuais, testes de conectividade e captura de pacotes em tempo real com **Wireshark**.

---

## 1. Inicializar o Wireshark em Segundo Plano

Abra o terminal com permissão para iniciar ferramentas de captura gráfica e execute o comando abaixo:

```bash
sudo -E wireshark &
```
<img width="903" height="655" alt="1 Iniciando wireshark" src="https://github.com/user-attachments/assets/32844f5d-1c1b-4d56-b854-6d39fe247ae9" />

> **Nota:** O parâmetro `-E` preserva o ambiente do utilizador (incluindo variáveis `$DISPLAY` do servidor X), e o `&` libera o prompt do terminal para continuar comandos.



---

## 2. Iniciar a Topologia Padrão no Mininet

Em uma janela de terminal como root, crie a topologia mínima composta por dois hosts (`h1` e `h2`), um switch OpenFlow (`s1`) e um controlador OpenFlow de referência (`c0`):

```bash
mn
```

<img width="798" height="578" alt="2 Iniciando_mininet" src="https://github.com/user-attachments/assets/9fa296ea-719c-4acf-b52c-9bef9d722bd4" />




---

## 3. Listar os Nós Criados (Nodes)

No prompt interativo do Mininet (`mininet>`), verifique todos os elementos da topologia em execução:

```bash
mininet> nodes
```

<img width="798" height="578" alt="3 Exibindo os Nodes criados" src="https://github.com/user-attachments/assets/1d3bc798-615e-427c-a511-9dc4f2d4f86b" />



*Saída esperada:*
```text
available nodes are:
c0 h1 h2 s1
```


---

## 4. Inspecionar a Topologia e Conexões de Rede (Links)

Visualize as interfaces de cada elemento e seus respectivos pontos de interconexão física simulada:

```bash
mininet> net
```
<img width="798" height="302" alt="4 Exibindo os como esta configuranção da rede" src="https://github.com/user-attachments/assets/897f6472-db82-4c5c-a6d3-2c86d33774b0" />



*Mapeamento das portas:*
* `h1`: interface `h1-eth0` conectada em `s1-eth1`
* `h2`: interface `h2-eth0` conectada em `s1-eth2`
* `s1`: portas `s1-eth1` e `s1-eth2` ligadas a `h1` e `h2`, respectivamente

---

## 5. Selecionar a Interface para Captura no Wireshark

Retorne à janela do Wireshark iniciada no Passo 1. As interfaces virtuais criadas pelo Mininet estarão visíveis na lista de interfaces ativas:

![Wireshark após iniciar Mininet](5%20wireshark%20ap%C3%B3s%20iniciar%20mininet.png)

* Dê duplo clique sobre a interface **`s1-eth1`** para iniciar a captura do tráfego que entra e sai do host 1.

---

<img width="960" height="757" alt="5 wireshark após iniciar mininet" src="https://github.com/user-attachments/assets/1dcbe4ad-628f-4ac7-82d3-c7144f448cbc" />


## 6. Exibir as Configurações de Rede do Host 1

Consulte as propriedades de rede atribuídas ao nó `h1` (endereço IPv4, MAC e status operacional):

```bash
mininet> h1 ifconfig -a
```
<img width="598" height="260" alt="6 exibindo configuração do host1" src="https://github.com/user-attachments/assets/b03d5c65-cea4-43d5-86f1-6e18c4a93850" />
![Exibindo configuração do host1](6%20exibindo%20configura%C3%A7%C3%A3o%20do%20host1.png)

---

## 7. Listar Processos em Execução no Namespace do Host 1

Inspecione a tabela de processos em execução dentro do ambiente do nó:

```bash
mininet> h1 ps -a
```

<img width="598" height="228" alt="7 exibindo processos rodando no host1" src="https://github.com/user-attachments/assets/920c186a-a17a-421a-ab55-3262017f5317" />


---

## 8. Teste de Conectividade com Ping (ICMP e ARP)

Execute um teste de ping pontual partindo de `h1` em direção a `h2`:

```bash
mininet> h1 ping -c 1 h2
```

<img width="1554" height="517" alt="8 Ping do host 1 para host2" src="https://github.com/user-attachments/assets/3654c655-15d0-4bbb-80d1-a9597eebf45e" />


### O que observar no Wireshark:
1. **Requisição e resposta ARP:** Resolução de endereço físico `MAC` para o IP `10.0.0.2`.
2. **Pacotes ICMP:** Envio de requisição (*Echo Request*) e recebimento da resposta (*Echo Reply*).


---

## 9. Subir Servidor HTTP no Host 1 e Acessar via Host 2

Inicie um servidor web simples com Python no `h1` escutando na porta 80 e execute a requisição HTTP a partir do `h2`:

```bash
mininet> h1 python -m http.server 80 &
mininet> h2 wget -O - h1
```
<img width="1916" height="897" alt="9 iniciando serviço http no host1 e acessando do host2" src="https://github.com/user-attachments/assets/7d9d0e4a-1c03-4112-a7f1-75da8387fd95" />

### O que observar no Wireshark:
* Handshake de 3 vias do TCP (`[SYN]`, `[SYN, ACK]`, `[ACK]`).
* Requisição HTTP `GET / HTTP/1.1`.
* Resposta do servidor `HTTP/1.0 200 OK` e entrega do código HTML via payload TCP.

---

## 10. Finalizar a Execução da Rede

Para derrubar a topologia virtual e liberar os recursos do sistema:

```bash
mininet> exit
```
<img width="1916" height="897" alt="10 Saindo da execução do mininet" src="https://github.com/user-attachments/assets/84d791bf-5dc7-4d61-8893-c70bd90adca8" />


> **Comportamento esperado no Wireshark:** Quando o Mininet encerra, a interface virtual de rede (`s1-eth1`) é removida da pilha de rede do Linux. O Wireshark exibirá a mensagem de aviso informando que o adaptador de rede parou de funcionar e encerrou a captura.

## 11. Teste Dinâmico e Automatizado de Ping (Pingpair)

O Mininet permite subir a topologia, validar a comunicação entre o par de hosts e derrubar o ambiente automaticamente com um único comando:

```bash
mn --test pingpair
```
<img width="961" height="565" alt="11 Comando de teste ping dinamico" src="https://github.com/user-attachments/assets/841104da-8113-49e6-93f4-31476b37e1fa" />



*O Mininet executa o teste ping entre `h1` e `h2`, relata o percentual de pacotes recebidos (`0% dropped`) e desmonta a rede.*

---

## 12. Teste Automatizado de Largura de Banda com Iperf

Avalie a capacidade de transferência TCP do ambiente padrão de switches emulados:

```bash
sudo mn --test iperf
```
<img width="764" height="565" alt="12 comando para gerar trafego na rede" src="https://github.com/user-attachments/assets/b2af162e-0cc5-4a8e-824e-1f2917cce1d4" />


*O teste reporta taxas elevadas (acima de 50 Gbits/sec), demonstrando a ausência de gargalos ou limitações de banda simuladas nos links padrão.*

---

## 13. Simulação de Gargalo de Rede e Atraso (Traffic Control - TC)

É possível emular condições de links reais restringindo largura de banda (`bw`) e inserindo latência (`delay`) através do subsistema `tc` do Linux:

```bash
sudo mn --link tc,bw=10,delay=10ms
```

<img width="923" height="612" alt="13 simulando trafego no ambiente e delay" src="https://github.com/user-attachments/assets/dcb94199-6795-49d9-8c40-07b34bd7cc45" />


Dentro do prompt do Mininet, teste a banda e a latência de ida e volta:

```bash
mininet> iperf
mininet> h1 ping -c10 h2
```



* **Iperf:** Taxa limitada em aproximadamente **9.50 a 11.8 Mbits/sec** (próximo ao teto configurado de 10 Mbps).
* **Ping:** Latência média de ida e volta de cerca de **40 ms** (10 ms por trecho de link: $h1 \leftrightarrow s1$ e $s1 \leftrightarrow h2$, totalizando 20 ms de ida e 20 ms de volta).

---

## 14. Depuração e Logs Detalhados de Inicialização

Para auditar cada chamada interna de sistema, comandos de configuração de IP, interfaces virtuais e inicialização de Open vSwitch:

```bash
mn -v debug
```

<img width="1307" height="878" alt="14 comando para trazer logs de iniciação do codigo" src="https://github.com/user-attachments/assets/7c670106-8c13-413c-8c41-259780da6f0e" />


*Exibe chamadas como `ip link add`, `ovs-vsctl`, migração de interfaces virtuais para namespaces dos hosts e comunicação do controlador OpenFlow.*

---

## 15. Executando uma Topologia Personalizada em Python

Inicie uma topologia escrita em arquivo Python externo (`--custom`) contendo múltiplos switches e nós:

```bash
mn --custom ~/mininet/custom/topo-2sw-2host.py --topo mytopo --test pingall
```

<img width="886" height="612" alt="15 Comando que roda uma topologia personaliza" src="https://github.com/user-attachments/assets/e51fe2ee-357d-4158-ab11-1747f23079ae" />



*A topologia `mytopo` conecta `h1` ao switch `s3`, `h2` ao switch `s4`, e interliga `s3` a `s4`. O teste `pingall` confirma que todos os hosts conseguem se comunicar através dos switches intermediários.*

---

## 16. Endereçamento MAC Padrão vs. MAC Determinístico

Por padrão, o Mininet gera endereços MAC pseudo-aleatórios para as interfaces dos hosts:

```bash
mn
mininet> h1 ifconfig
```

<img width="650" height="612" alt="16 comparando mn ifconfig" src="https://github.com/user-attachments/assets/53f2cc34-cd83-4321-b368-191fd5978f24" />


*O endereço MAC do `h1-eth0` é gerado aleatoriamente (ex: `6a:92:23:14:d7:e4`).*

---

## 17. Utilizando MACs Fáceis de Identificar (`--mac`)

Ao adicionar o parâmetro `--mac`, o Mininet atribui endereços físicos previsíveis baseados no ID do nó:

```bash
mn --mac
mininet> h1 ifconfig
```
<img width="597" height="667" alt="17 comparando mn --mac ifconfig" src="https://github.com/user-attachments/assets/f9f54c71-67de-4629-a9d3-9e7d7abd4f31" />

*O MAC do host 1 passa a ser fixado como `00:00:00:00:00:01`, facilitando inspeção e filtros em capturas de pacotes no Wireshark.*

---

## 18. Abrindo Janelas de Terminal Individuais para Cada Nó (`-x`)

Para depurar e executar comandos simultaneamente em cada elemento da topologia através de instâncias separadas de terminal XTerm:

```bash
sudo -E mn -x
```

<img width="1752" height="717" alt="17 rodando o mininet a abrindo as janelas de cada node" src="https://github.com/user-attachments/assets/1ddc928a-20cf-40e3-a379-5af677adb718" />


*Janelas independentes são iniciadas para o controlador `c0`, o switch `s1`, e os hosts `h1` e `h2`.*

---

## 19. Teste Contínuo de Ping e Inspeção no Wireshark

A partir da janela individual do nó `h1`, inicie um envio contínuo de pings para o IP de `h2`:

```bash
# Na janela do host h1:
ping 10.0.0.2
```

<img width="1901" height="813" alt="18 realizando Ping entres os Hosts" src="https://github.com/user-attachments/assets/ba747d10-0616-4d60-b09a-2ea2c9bd6832" />

*O tráfego de pacotes ICMP em tempo real pode ser inspecionado na interface virtual `s1-eth2` pelo Wireshark.*

---

## 20. Comparação de Desempenho entre Tipos de Switch (User vs. OVS Kernel)

Avalie a diferença de taxa de transferência entre uma implementação de switch no espaço de usuário (*user space*) e no espaço de kernel (*Open vSwitch kernel mode*):

### Switch em User Space:
```bash
sudo mn --switch user --test iperf
```
*Resultados na ordem de **~1.18 Gbits/sec** devido ao overhead de trocas de contexto entre o kernel e o processo de usuário.*

### Switch Open vSwitch em Kernel Mode:
```bash
sudo mn --switch ovsk --test iperf
```
*Resultados na ordem de **~60.1 Gbits/sec**, aproveitando o chaveamento nativo e aceleração dentro do kernel Linux.*

<img width="1901" height="996" alt="19 Comparando test de iperf" src="https://github.com/user-attachments/assets/99c8a419-ebcd-470c-871b-7f9faea441c5" />

## 21. Benchmark de Tempo de Criação e Destruição da Rede

Para medir a latência de inicialização e o tempo que o Mininet leva para subir e desmanchar o ambiente sem rodar testes de rede adicionais, utilize o teste `none`:

```bash
sudo mn --test none
```
<img width="372" height="515" alt="20 comando que tempo de execução da rede" src="https://github.com/user-attachments/assets/a7852c0f-47a8-4ab0-bc2b-da67fc2ed00b" />

*A topologia completa é instanciada e destruída em apenas **0.165 segundos**, evidenciando a leveza dos contêineres e namespaces do Mininet.*

---

## 22. Isolamento Completo com Network Namespaces Próprios (`--innamespace`)

Por padrão, os switches executam no namespace de rede global da máquina host. Com a flag `--innamespace`, o switch em espaço de usuário e a rede de controle passam a rodar em seus próprios namespaces isolados:

```bash
sudo mn --innamespace --switch user
```

Dentro da CLI do Mininet, realize testes de conectividade:

```bash
mininet> h1 ping h2
```

<img width="493" height="359" alt="21 comando como namespace" src="https://github.com/user-attachments/assets/a92c1041-0edb-4520-a3d9-9925acbf7ac1" />


![Comando como namespace](21%20comando%20como%20namespace.png)

*O Mininet testa e valida previamente o canal de controle entre `s1` e `c0` com 0% de perda (`2/2 received`) antes de abrir a linha de comando.*

---

## 23. Abertura Interativa de Terminais XTerm para Hosts Específicos

Em vez de abrir terminais para todos os nós de uma vez só (como ocorre no parâmetro `-x`), você pode chamar janelas interativas sob demanda dentro do próprio prompt do Mininet apenas para os nós necessários:

```bash
mininet> xterm h1 h2
```


<img width="942" height="306" alt="23 comando paara abrir terminal dos hosts(1)" src="https://github.com/user-attachments/assets/89788ead-d343-4f7c-84ca-8b76290bc075" />


*Duas janelas de terminal dedicadas são abertas (`Node: h1` e `Node: h2`), prontas para a execução de serviços, scripts ou ferramentas como tcpdump e htop.*


