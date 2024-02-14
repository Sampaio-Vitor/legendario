# 📽 Projeto de Legendas Automáticas de Vídeos com AWS 📽

Este projeto automatiza a adição de legendas a vídeos utilizando serviços da AWS. A automação é desencadeada pelo upload de um vídeo para um bucket do S3, que aciona uma função Lambda. Esta função, então, inicia um container Docker hospedado no Amazon ECR (Elastic Container Registry) executado pelo AWS Fargate para processar o vídeo.

Demonstração de um video legendado utilizando a ferramenta aqui:

https://youtu.be/YiWHUY-Rqsg

# Aplicação

Este projeto pode ser integrado a uma interface de usuário, proporcionando uma experiência onde os usuários fazem upload de seus vídeos e, automaticamente, recebem os vídeos legendados. Essa integração requer um front-end que permita aos usuários selecionar e enviar vídeos para o bucket do S3 designado. Após o upload, o processo automatizado é iniciado, e o vídeo processado com legendas é disponibilizado para o usuário. Esta abordagem simplifica significativamente a adição de legendas a vídeos, tornando-a acessível a uma ampla gama de usuários, desde criadores de conteúdo até empresas que buscam tornar seus vídeos mais inclusivos e acessíveis.

## Arquitetura

- **S3 Bucket**: Armazena os vídeos a serem legendados.
- **Lambda Function**: Detecta uploads de novos vídeos e aciona o processamento.
- **Elastic Container Registry (ECR)**: Armazena a imagem do Docker usada para adicionar legendas aos vídeos.
- **Fargate**: Executa a imagem do Docker sem necessidade de gerenciar servidores ou clusters.

![WhatsApp Image 2024-02-14 at 16 10 58](https://github.com/Sampaio-Vitor/legendario/assets/110466124/e58d5923-ba02-4fb7-8978-28008b3b67e9)


## Pré-requisitos

- AWS CLI configurado com permissões adequadas.
- Docker.
- Conhecimento básico em AWS Lambda, Amazon S3, Amazon ECR, e AWS Fargate.

## Configuração

1. **Prepare o S3 Bucket**: Crie um bucket no S3 para armazenar seus vídeos e os vídeos processados.

2. **Crie a Função Lambda**: Configure uma função Lambda para ser acionada por eventos de `ObjectCreated` no bucket S3. Esta função deve ter permissão para iniciar tarefas no Fargate usando a imagem do Docker armazenada no ECR.

3. **Configure o ECR**: Crie um repositório no ECR e faça push da imagem do Docker que executa a lógica de adicionar legendas ao vídeo.

4. **Configure o Fargate**: Crie uma definição de tarefa no Fargate que utilize a imagem do Docker do seu repositório ECR. A função Lambda deve iniciar esta tarefa quando um vídeo for carregado.

## Uso

Para usar esta automação, basta fazer upload de um vídeo para o bucket S3 configurado. A função Lambda detectará o upload, acionará a tarefa no Fargate que processa o vídeo usando a imagem do Docker, e o vídeo legendado será armazenado conforme definido na lógica de processamento.

## Desenvolvimento

Para modificar a lógica de processamento ou a automação, ajuste o script do Docker, atualize a imagem no ECR e assegure-se de que a função Lambda e a definição de tarefa do Fargate estão configuradas corretamente para usar a nova versão da imagem.


## Contribuições

Contribuições para o projeto são bem-vindas, seja na forma de melhorias no código, na documentação ou na arquitetura de automação.

## Licença

[MIT](LICENSE)
