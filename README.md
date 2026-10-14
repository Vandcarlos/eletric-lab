# Eletric Lab

MVP de inspeção assistida de instalações elétricas.

> **Atenção:** fotografias não comprovam conformidade, segurança ou capacidade elétrica. O MVP não executa inferência visual; o relatório é demonstrativo e exige avaliação profissional.

## Estrutura

```text
apps/mobile/                  # Flutter (iOS e Android)
services/agent/
  src/
    api/                      # FastAPI, rotas e contratos HTTP
    service/                  # Regras de negócio e orquestração
    vendor/                   # Integrações externas (futuros providers)
    llm/                      # LangGraph, prompts e estado (futuro)
  tests/
infra/                        # Docker Compose
docs/                         # Arquitetura e roadmap
```

## API local

Requer Python 3.12+ e [uv](https://docs.astral.sh/uv/).

```bash
cd services/agent
uv sync --extra dev
uv run uvicorn src.api.main:app --reload
uv run pytest
```

Documentação OpenAPI: http://127.0.0.1:8000/docs

Alternativamente: `docker compose -f infra/compose.yaml up --build`.

## Flutter

Requer Flutter SDK instalado.

```bash
cd apps/mobile
flutter pub get
flutter run
```

Em emuladores Android, configurar a URL da API para `http://10.0.2.2:8000`; no simulador iOS usar `http://127.0.0.1:8000`. Para dispositivo físico, usar IP local com configuração de rede apropriada.

## MVP

- POST /v1/inspections: recebe JPEG/PNG/WEBP (até 10 MiB), valida assinatura e retorna relatório estruturado.
- GET /health: health check.
- O serviço retorna resultado **sem análise visual**; não há classificação ou identificação de componentes.
- Próxima fase: provedor de visão, bounding boxes, anotações e avaliação; depois LangGraph e RAG com conteúdo normativo licenciado.

## Segurança

Não envie imagens com dados pessoais sensíveis. Nunca use resultados automatizados como autorização para intervenção em circuitos energizados. Normas ABNT devem ser utilizadas respeitando direitos de acesso e licenciamento.
