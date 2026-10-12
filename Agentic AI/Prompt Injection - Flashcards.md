---
title: "Prompt Injection – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Prompt Injection]]"
created: 2026-09-23
---

#flashcards/agentic-ai/prompt-injection

Flashcards for [[Prompt Injection]].

What is prompt injection?
?
An attack where adversarial input makes an LLM application follow the attacker's instructions instead of the developer's or user's. It is OWASP LLM01.

What is the root cause of prompt injection?
?
LLMs read instructions and data as one token stream. There is no enforced boundary, so data can be interpreted as instructions.

What is indirect prompt injection?
?
Instructions planted in content the system later reads (web pages, emails, documents, tool outputs), which then affect a legitimate user's agent.

How does jailbreaking differ from prompt injection?
?
Jailbreaking bypasses the model's safety training. Prompt injection hijacks the application's instructions to make the system act against its owner or user.

What are the three legs of the lethal trifecta?
?
Access to private data, exposure to untrusted content, and a way to communicate externally. Remove one leg to break the exfiltration path.

Why are prompt-level defenses like delimiters insufficient on their own?
?
They are probabilistic conventions the model was trained to follow, not enforced boundaries. They lower the attack success rate but don't eliminate it.

What is the dual-LLM (quarantined LLM) pattern?
?
A tool-less quarantined model processes untrusted content and returns structured data. A privileged model with tools never sees the raw untrusted text.

Name four deterministic defenses against prompt injection in agents.
?
Least-privilege tool scoping, privilege separation, human confirmation for irreversible actions, and output controls such as disabling remote image or link rendering and allow-listing destinations.

What is tool poisoning?
?
Hiding instructions in a tool's description or metadata, so any agent that loads the tool is influenced. It is a supply-chain risk for tool ecosystems like MCP.

Why does multiplying per-layer miss rates overstate layered defense?
?
The layers are correlated. An attack that fools one LLM-based filter often fools the others, so the failures are not independent.

What two metrics should a prompt-injection defense evaluation report?
?
Attack success rate against adaptive attacks, and the utility loss on legitimate tasks.
