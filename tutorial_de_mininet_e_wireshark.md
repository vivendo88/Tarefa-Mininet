# Tutorial: Emulação de Redes com Mininet e Análise de Tráfego com Wireshark

Este repositório contém um roteiro prático demonstrando o provisionamento de topologia de rede emulada utilizando **Mininet**, inspeção de interfaces virtuais, testes de conectividade e captura de pacotes em tempo real com **Wireshark**.

---

## 1. Inicializar o Wireshark em Segundo Plano

Abra o terminal com permissão para iniciar ferramentas de captura gráfica e execute o comando abaixo:

```bash
sudo -E wireshark &
```

> **Nota:** O parâmetro `-E` preserva o ambiente do utilizador (incluindo variáveis `$DISPLAY` do servidor X), e o `&` libera o prompt do terminal para continuar comandos.

![Iniciando Wireshark](1%20Iniciando%20wireshark.png)

---

## 2. Iniciar a Topologia Padrão no Mininet

Em uma janela de terminal como root, crie a topologia mínima composta por dois hosts (`h1` e `h2`), um switch OpenFlow (`s1`) e um controlador OpenFlow de referência (`c0`):

```bash
mn
```

![Iniciando Mininet](2%20Iniciando_mininet.png)

---

## 3. Listar os Nós Criados (Nodes)

No prompt interativo do Mininet (`mininet>`), verifique todos os elementos da topologia em execução:

```bash
mininet> nodes
```

![Exibindo os Nodes criados](3%20Exibindo%20os%20Nodes%20criados.png)

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

![Exibindo a configuração da rede](4%20Exibindo%20os%20como%20esta%20configuran%C3%A7%C3%A3o%20da%20rede.png)

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

## 6. Exibir as Configurações de Rede do Host 1

Consulte as propriedades de rede atribuídas ao nó `h1` (endereço IPv4, MAC e status operacional):

```bash
mininet> h1 ifconfig -a
```

![Exibindo configuração do host1](6%20exibindo%20configura%C3%A7%C3%A3o%20do%20host1.png)

---

## 7. Listar Processos em Execução no Namespace do Host 1

Inspecione a tabela de processos em execução dentro do ambiente do nó:

```bash
mininet> h1 ps -a
```

![Exibindo processos rodando no host1](7%20exibindo%20processos%20rodando%20no%20host1.png)

---

## 8. Teste de Conectividade com Ping (ICMP e ARP)

Execute um teste de ping pontual partindo de `h1` em direção a `h2`:

```bash
mininet> h1 ping -c 1 h2
```

![Ping do host 1 para host2](8%20Ping%20do%20host%201%20para%20host2.png)

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

![Iniciando serviço HTTP no host1 e acessando do host2](9%20iniciando%20servi%C3%A7o%20http%20no%20host1%20e%20acessando%20do%20host2.jpg)

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

![Saindo da execução do Mininet](10%20Saindo%20da%20execu%C3%A7%C3%A3o%20do%20mininet.jpg)

> **Comportamento esperado no Wireshark:** Quando o Mininet encerra, a interface virtual de rede (`s1-eth1`) é removida da pilha de rede do Linux. O Wireshark exibirá a mensagem de aviso informando que o adaptador de rede parou de funcionar e encerrou a captura.