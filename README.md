# Arvore-Ipv4

Protocolo: **UDP**<br>
Arquitetura: **Cliente-Servidor**<br>
<br>

#### Como Funciona? -
O cliente irá mandar, seu IP ou da rede, máscara e a quantidade de dispositivos que estão/serão alocados.<br>
O servidor criará um arquivo baseado nas informações do cliente. Após a criação do arquivo, o servidor irá mandar
o tamanho do arquivo(os.stat(FILE).st_size) gerado. Após o recebimento do tamanho do arquivo, o cliente irá alocar no
buffer(recvfrom(BUFFER) o tamanho exato do arquivo. Logo depois, o servidor irá mandar o arquivo('_ips.txt_') para que o cliente
possa receber. E finalmente o cliente ira salvar este arquivo, com o nome de '_ips_recebidos.txt_' na mesma janela será printada
todos os ips baseado no arquivo final.
