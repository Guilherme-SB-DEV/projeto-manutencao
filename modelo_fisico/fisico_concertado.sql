CREATE DATABASE banco_de_dados_manutencao;
USE banco_de_dados_manutencao;

CREATE TABLE Usuario (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Senha VARCHAR(100) NOT NULL,
    Tipo_Perfil VARCHAR(50) NOT NULL,
    Auth VARCHAR(100),
    CONSTRAINT chk_tipo_perfil CHECK (Tipo_Perfil IN ('cliente', 'tecnico', 'admin'))
);

CREATE TABLE Chamado (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Titulo VARCHAR(100) NOT NULL,
    Descricao VARCHAR(255),
    Categoria VARCHAR(50),
    Prioridade VARCHAR(20),
    Status VARCHAR(20) DEFAULT 'aberto',
    Data_Abertura DATETIME NOT NULL,
    Data_Conclusao DATETIME,
    Tempo_Estimado INT,
    CONSTRAINT chk_prioridade CHECK (Prioridade IN ('baixa', 'media', 'alta')),
    CONSTRAINT chk_status CHECK (Status IN ('aberto', 'em andamento', 'concluido', 'cancelado'))
);

CREATE TABLE Mensagem (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Conteudo VARCHAR(255) NOT NULL,
    fk_Chamado_Id INT NOT NULL,
    fk_Usuario_Id INT NOT NULL,
    Tempo_envio DATETIME,
    CONSTRAINT fk_mensagem_chamado FOREIGN KEY (fk_Chamado_Id) REFERENCES Chamado(Id),
    CONSTRAINT fk_mensagem_usuario FOREIGN KEY (fk_Usuario_Id) REFERENCES Usuario(Id)
);

CREATE TABLE Cliente_Abre (

    Id INT PRIMARY KEY AUTO_INCREMENT,
    fk_Usuario_Id INT NOT NULL,
    fk_Chamado_Id INT NOT NULL,
    CONSTRAINT fk_clienteabre_usuario FOREIGN KEY (fk_Usuario_Id) REFERENCES Usuario(Id),
    CONSTRAINT fk_clienteabre_chamado FOREIGN KEY (fk_Chamado_Id) REFERENCES Chamado(Id)
);

CREATE TABLE Tecnico_Atende (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    fk_Usuario_Id INT NOT NULL,
    fk_Chamado_Id INT NOT NULL,
    CONSTRAINT fk_tecnicoatende_usuario FOREIGN KEY (fk_Usuario_Id) REFERENCES Usuario(Id),
    CONSTRAINT fk_tecnicoatende_chamado FOREIGN KEY (fk_Chamado_Id) REFERENCES Chamado(Id)
);

CREATE TABLE Notificacao (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Tipo VARCHAR(50) NOT NULL,
    fk_Chamado_Id INT,
    fk_Usuario_Id INT,
    CONSTRAINT fk_notificacao_chamado FOREIGN KEY (fk_Chamado_Id) REFERENCES Chamado(Id),
    CONSTRAINT fk_notificacao_usuario FOREIGN KEY (fk_Usuario_Id) REFERENCES Usuario(Id),
    CONSTRAINT chk_tipo_notificacao CHECK (Tipo IN ('nova mensagem', 'chamado resolvido', 'atualizacao de status'))
);
