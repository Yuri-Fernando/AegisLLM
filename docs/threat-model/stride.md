# Threat model resumido

| Ativo | Ameaça | Controle |
|---|---|---|
| Dados de tenant | acesso cruzado | tenant isolation + auditoria |
| Prompt/contexto | injection e poisoning | sanitização + policy |
| Ferramentas | excessive agency | allowlist + contexto de usuário |
| Saída | XSS/SQL injection | output validation |
| Provedor | vazamento de dados restritos | classificação + model routing |

