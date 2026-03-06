# Technical Glossary

Quick reference for core Exahia technical terms.

## Zero Retention
Operational posture where sensitive prompt content is processed in-memory and not stored as persistent conversational data by default.

## Cloud Act
US legal framework that can require US-linked providers to disclose data, including data stored outside the US, under legal process.

## PII Filtering
Pre-inference detection and masking/removal of personally identifiable information (PII) in prompts and documents.

## RAG (Retrieval-Augmented Generation)
Pattern where the model response is grounded with retrieved internal documents (chunks) before generation.

## OpenAI-compatible API
API surface designed to remain interoperable with common OpenAI client SDKs to reduce migration effort.

## Shadow AI
Use of unapproved AI tools by employees outside formal governance, security, and compliance processes.

## Sovereign Hosting
Infrastructure and operational control model ensuring data and execution stay in a chosen jurisdiction (here: France/Europe).

## Dedicated GPU Runtime
Single-tenant or isolated compute allocation where workloads run on customer-assigned GPU resources.

## Multi-tenant Runtime
Shared compute model where multiple tenants consume pooled infrastructure with policy-based isolation.

## Policy Gate
Control layer enforcing security/compliance rules (PII checks, routing constraints, usage restrictions) before inference.

## Prompt Sanitization
Transformation step that removes or redacts unsafe content patterns before sending requests to model runtime.

## Audit Trail
Timestamped evidence records for governance and compliance workflows (policy events, model usage, controls).

## AI Act Readiness
Operational ability to provide documentation, controls, and evidence expected by EU AI Act obligations.

## DPIA (Data Protection Impact Assessment)
Risk-assessment process required by RGPD in high-risk processing contexts, including sensitive AI workflows.
