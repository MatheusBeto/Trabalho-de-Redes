Trabalho de Redes

Criar um cliente e servidor http

Para rodar o programa é necessário a biblioteca python-magic
Para instalar use o comando abaixo no terminal do ubuntu 
    pip install python-magic
    
Iniciando o programa
  Primeiro inicie o servidor, no terminal aberto no diretório dos arquivos do programa, digite o seguinte comando 
    python server.py <diretorio> <porta>
      <diretorio> o diretorio que os arquivos que serão servidos estão;
      <porta> a porta que o servidor ficará escutando, se for nulo a porta padrão é a 80
    
  Para iniciar o cliente
    python client.py <dominio> <porta>
      <dominio> por exemplo: localhost
      <porta>, por padrão é a 80
