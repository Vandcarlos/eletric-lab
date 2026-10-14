# Architecture

- Flutter app captures images and renders structured inspection reports.
- `src/api`: HTTP transport and Pydantic schemas.
- `src/service`: business rules, input validation and inspection orchestration.
- `src/vendor`: adapters for vision providers, persistence, telemetry and KB.
- `src/llm`: future LangGraph state, nodes, prompts and tool integration.
- The first MVP has no vision model and must not make electrical safety determinations.
- Future KB content must be licensed; deterministic checks must be separate from LLM output.
