# WhatsApp Sender

O WhatsApp Sender é uma ferramenta Python que permite enviar mensagens em lote para uma lista de transmissão no WhatsApp. Ele é projetado para facilitar o envio de mensagens personalizadas para vários contatos de uma vez.

## Funcionalidades

- Lê uma tabela Excel e extrai os números de telefone da coluna "TELEFONE" e os nomes da coluna "NOME". Se o nome estiver ausente, a mensagem será enviada sem personalização.
- A mensagem a ser enviada é definida no arquivo "message.txt". O nome do destinatário é indicado usando a string "{nome}", que será substituída pelo nome real na mensagem.
- Não possui uma interface gráfica interativa; as interações ocorrem por meio de arquivos e são ativadas executando o arquivo "main.py".
- O arquivo do Excel a ser utilizado é "Pasta.xlsx".
- Utiliza as bibliotecas especificadas no arquivo "requirements.txt" para funcionar corretamente.

## Logs e Limpeza

- Os logs do WhatsApp Sender podem ser encontrados na pasta "logs" (relativa ao diretório do projeto). Eles fornecem informações sobre o status do envio das mensagens.
- Para limpar a lista de transmissão, basta excluir a pasta "cache" (relativa ao diretório do projeto).

## Requisitos

Certifique-se de ter as bibliotecas especificadas no arquivo "requirements.txt" instaladas antes de executar a ferramenta.

### Configuração do Ambiente

1. Clone o repositório do WhatsApp Sender.
2. Instale as dependências especificadas no arquivo "requirements.txt" usando o gerenciador de pacotes de sua escolha (por exemplo, pip).
3. Coloque o arquivo Excel com os dados dos contatos na pasta do projeto e nomeie-o como "Pasta.xlsx".
4. Defina a mensagem a ser enviada no arquivo "message.txt".
5. Execute o arquivo "main.py" para iniciar o envio das mensagens.

Aproveite o WhatsApp Sender para enviar facilmente mensagens personalizadas para sua lista de contatos!
