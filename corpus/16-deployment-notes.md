Source: LangGraph documentation - Deployment concepts (docs.langchain.com/langsmith/deployment)
License: see corpus/ATTRIBUTION.md

# Deployment Concepts for Agent Applications

Deploying an agent application means running the compiled graph behind a service that other systems can call, with configuration supplied through environment variables rather than hard-coded values.

API keys and other secrets belong in the environment or a secret manager, never in source code. An application should also start and answer health checks without any optional provider key, falling back to a safe default path when a key is absent.

Containerization packages the application and its dependencies into one image so the same build runs locally, in staging, and in production. A pinned requirements file is what makes that build reproducible.

Observability matters more for agents than for simple request handlers. Logging the plan, the retrieved sources, and the verification result for each run makes failures debuggable after the fact, because the interesting failure is usually a wrong retrieval or an unsupported claim, not a crash.
