---
title: "Implementing Gate Checks – Flashcards"
type: flashcards
source: "[[Implementing Gate Checks]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/implementing-gate-checks

What four outcomes can an implemented gate return?
?
PASS, RETRY (with feedback), REROUTE (to a fallback), STOP (escalate).

What is the validate–retry loop?
?
Run the step, apply the gates, add gate feedback to the prompt on failure, and retry up to N times before escalating.

What usually implements the format gate?
?
A schema validator (a typed data model or JSON Schema), helped by the provider's structured-output mode.

In what order should gates run?
?
Cheapest first: schema, then deterministic content, then logic, then expensive checks (judge model or human).

What makes retry feedback effective?
?
It names the failing field and the rule, and includes the bad value.

Why should gates have no side effects?
?
Retries run them again, so any side effects (writes, emails) would be duplicated.

What is the escalation probability with first-attempt pass rate q and N attempts?
?
(1 − q)^N, assuming the attempts are independent.

Why are real retry gains often smaller than the formula predicts?
?
Failures are correlated: the same prompt tends to repeat the same mistake. Rerouting to a different prompt or model helps.

Name three gate metrics worth logging.
?
First-attempt pass rate per gate, retry success rate, and escalation rate (plus false rejection rate).
