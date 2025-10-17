## TPC3: Analisador Léxico para SPARQL

Criar em Python um analisador léxico (tokenizador) para queries SPARQL básicas.

### Objetivo

Implementar um tokenizador que reconheça os seguintes elementos de uma query SPARQL:

### Tokens a Reconhecer

- **PREFIX**: Palavra-chave `PREFIX`
- **SELECT**: Palavra-chave `SELECT`
- **WHERE**: Palavra-chave `WHERE`
- **OPTIONAL**: Palavra-chave `OPTIONAL`
- **FILTER**: Palavra-chave `FILTER`
- **VAR**: Variáveis que começam com `?` (ex: `?nome`, `?pessoa`)
- **URI**: URIs entre `<` e `>` (ex: `<http://exemplo.com>`)
- **IDENT**: Identificadores prefixados com `:` (ex: `:Pessoa`, `:temIdade`)
- **INT**: Números inteiros
- **STRING**: Strings entre aspas duplas
- **OP**: Operadores de comparação (`=`, `!=`, `<`, `>`, etc.)
- **PUNCT**: Pontuação (`{`, `}`, `.`, `;`, `,`)
- **NEWLINE**: Quebras de linha
- **SKIP**: Espaços e tabs (ignorados)
- **ERROR**: Caracteres não reconhecidos

### Exemplo de Input

```sparql
SELECT ?nome ?desc WHERE { 
    ?s a dbo:MusicalArtist. 
    ?s foaf:name "Chuck Berry"@en . 
    ?w dbo:artist ?s. 
    ?w foaf:name ?nome. 
    ?w dbo:abstract ?desc 
} LIMIT 1000
```

### Exemplo de Output

Cada token reconhecido é retornado como uma tupla:
```python
(TIPO, valor, linha, (início, fim))
```

Por exemplo:
```python
('SELECT', 'SELECT', 1, (0, 6))
('VAR', '?nome', 1, (7, 12))
('VAR', '?desc', 1, (13, 18))
('WHERE', 'WHERE', 1, (19, 24))
...
```
