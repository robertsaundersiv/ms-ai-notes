---
title: "Model Context Protocol – Flashcards"
type: flashcards
source: "[[Model Context Protocol]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/mcp

What is the Model Context Protocol (MCP)?
?
An open JSON-RPC-based client–server standard for connecting AI applications to external tools, data and prompts.

What problem does MCP solve?
?
The M×N integration problem: M apps × N services connectors become M clients + N servers.

What are the MCP roles?
?
Host (AI app), client (one connection per server), server (exposes capabilities), transport.

What are the three MCP server primitives, and who controls each?
?
Tools (model-controlled), resources (application-controlled), prompts (user-controlled).

What transports does MCP use?
?
stdio for local servers, and Streamable HTTP for remote servers.

What is MCP sampling?
?
A server asks the host's LLM for a completion, with user approval. It is deprecated in the 2026-07-28 spec; servers should call LLM provider APIs directly.

What is tool poisoning?
?
Malicious instructions hidden in a tool's description or metadata, which the model reads and may follow.

What is an MCP rug pull?
?
A server changes its tools' behavior or descriptions after the user approved it.

Does MCP make tools safe?
?
No. It standardizes connectivity, not trust. You still need vetting, least privilege, confirmation and logging.
