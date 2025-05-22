CREATE DATABASE banco_de_dados_manutencao;
USE banco_de_dados_manutencao;
CREATE TABLE Usuario (
    Id int PRIMARY KEY AUTO_INCREMENT,
    Senha VARCHAR(100),
    Nome VARCHAR(100),
    Tipo_Perfil VARCHAR(100),
    Email VARCHAR(100)
);

CREATE TABLE Chamado (
    Id int PRIMARY KEY,
    Prioridade VARCHAR(100),
    Data_Conclusao DATE,
    Status VARCHAR(100),
    Descricao VARCHAR(100),
    Data_Abertura DATE,
    Titulo VARCHAR(100),
    fk_Categoria_Id int
);

CREATE TABLE Categoria (
    Id int PRIMARY KEY,
    Nome VARCHAR(100)
);

CREATE TABLE Mensagem (
    Id int PRIMARY KEY,
    Conteudo VARCHAR(100),
    fk_Chamado_Id int,
    fk_Usuario_Id int
);

CREATE TABLE Cliente_abre (
    fk_Usuario_Id int
);

CREATE TABLE Notificacao (
    Id int PRIMARY KEY,
    Tipo VARCHAR(100),
    fk_Chamado_Id int,
    fk_Usuario_Id int
);

CREATE TABLE tecnico_atende (
    fk_Usuario_Id int
);
 
ALTER TABLE Usuario ADD CONSTRAINT FK_Usuario_2
    FOREIGN KEY (Id) -- Aqui deve ser a coluna correta de FK
    REFERENCES ??? (???); -- Favor completar com a tabela e coluna corretas
 
ALTER TABLE Chamado ADD CONSTRAINT FK_Chamado_2
    FOREIGN KEY (fk_Categoria_Id)
    REFERENCES Categoria (Id);
 
ALTER TABLE Mensagem ADD CONSTRAINT FK_Mensagem_2
    FOREIGN KEY (fk_Chamado_Id)
    REFERENCES Chamado (Id);
 
ALTER TABLE Mensagem ADD CONSTRAINT FK_Mensagem_3
    FOREIGN KEY (fk_Usuario_Id)
    REFERENCES Usuario (Id);
 
ALTER TABLE Cliente_abre ADD CONSTRAINT FK_Cliente_abre_1
    FOREIGN KEY (fk_Usuario_Id)
    REFERENCES Usuario (Id);
 
ALTER TABLE Notificacao ADD CONSTRAINT FK_Notificacao_2
    FOREIGN KEY (fk_Chamado_Id)
    REFERENCES Chamado (Id);
 
ALTER TABLE Notificacao ADD CONSTRAINT FK_Notificacao_3
    FOREIGN KEY (fk_Usuario_Id)
    REFERENCES Usuario (Id);
 
ALTER TABLE tecnico_atende ADD CONSTRAINT FK_tecnico_atende_1
    FOREIGN KEY (fk_Usuario_Id)
    REFERENCES Usuario (Id);
