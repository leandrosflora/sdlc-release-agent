# sdlc-release-agent

Agente `release` do [agentic-sdlc-reference-architecture](https://github.com/leandrosflora/agentic-sdlc-reference-architecture) — implementação operacional do papel `agent_role == "release"` definido em `policies/agent_authorization.rego`.

## Responsabilidade

Publica artefatos via CI e aciona deploys. Deploy não produtivo é livre; deploy em produção exige todos os gates anteriores satisfeitos e aprovação humana independente vinculada ao digest exato do artefato; dono do **Release gate** (mesmo artifact digest aprovado, janela válida, health checks, capacidade de rollback e error budget).

## Autorização (OPA)

- `project.read`: permitido, restrito ao próprio `project_id`.
- `production.deploy`: permitido apenas quando `change.artifact_digest == approval.artifact_digest`, a aprovação é válida, humana e feita por um `actor_id` diferente de `change.author_id`, `change.rollback_verified` é verdadeiro, os gates de segurança e de teste passaram, e `change.risk` está em `{R1, R2, R3}`.
- Publicação de artefato e deploy não produtivo: previstos na matriz de capacidades do governance; ainda não codificados como regra própria em `agent_authorization.rego`.

## Status

Scaffold inicial (Python/.pyproj). Lógica do agente ainda não implementada.

## Referências

- Governança e gates: [docs/governance.md](https://github.com/leandrosflora/agentic-sdlc-reference-architecture/blob/main/docs/governance.md)
- Política: [policies/agent_authorization.rego](https://github.com/leandrosflora/agentic-sdlc-reference-architecture/blob/main/policies/agent_authorization.rego)
