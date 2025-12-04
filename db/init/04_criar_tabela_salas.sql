-- Criar tabela de salas de chat
CREATE TABLE IF NOT EXISTS salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    objective TEXT NOT NULL,
    type VARCHAR(10) NOT NULL,
    password VARCHAR(100),
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Criar índice para melhor performance
CREATE INDEX idx_salas_created_by ON salas(created_by);
CREATE INDEX idx_salas_created_at ON salas(created_at);
