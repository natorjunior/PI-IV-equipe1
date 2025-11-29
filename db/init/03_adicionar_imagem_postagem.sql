-- Adicionar coluna imagem_url na tabela postagens
ALTER TABLE postagens ADD COLUMN IF NOT EXISTS imagem_url VARCHAR(500);
