@startuml
' ERD — Postagem & Curtida
skinparam shadowing false
skinparam roundcorner 12
hide circle

entity "usuario" as Usuario {
  *id : INT <<PK>>
}

entity "postagem" as Postagem {
  *id : INT <<PK>>
  --
  autor_id : INT <<FK>>
  titulo : VARCHAR(255)
  conteudo : TEXT
  imagem : VARCHAR(255)
  created_at : TIMESTAMP
  updated_at : TIMESTAMP
}

entity "curtida" as Curtida {
  *id : INT <<PK>>
  --
  usuario_id : INT <<FK>>
  postagem_id : INT <<FK>>
  created_at : TIMESTAMP
  {unique} (usuario_id, postagem_id)
}

Usuario ||--o{ Postagem : autor_id
Usuario ||--o{ Curtida  : usuario_id
Postagem ||--o{ Curtida : postagem_id

note right of Curtida
  Um usuário não pode curtir
  a mesma postagem mais de uma vez.
end note
@enduml
