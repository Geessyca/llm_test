# Usa a imagem oficial do MySQL como base
FROM mysql:latest

# Define a variável de ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Copia o script SQL de inicialização para o contêiner
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expondo a porta do MySQL (opcional, já está no compose)
EXPOSE 3306

# Comando padrão para iniciar o MySQL (já está no MySQL oficial)
CMD ["mysqld"]
