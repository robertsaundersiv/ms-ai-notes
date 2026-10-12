---
title: "MS AI Daily – 2026-10-07"
type: podcast
created: 2026-10-07
duration_min: 32
covers:
  - "[[UdaPlay Agentic AI Project]]"
  - "[[Agent Based RAG]]"
  - "[[Agent Evaluation]]"
  - "[[Agentic RAG]]"
  - "[[Long-Term Agent Memory]]"
  - "[[Retrieval-Augmented Generation]]"
  - "[[Agent State Management]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Prompt Chaining Workflow]]"
  - "[[Tree-of-Thought]]"
  - "[[AI Memory]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-07

![[MS AI Daily - 2026-10-07.mp3]]

> [!abstract] In this episode
> A consolidation episode for the Building Agents capstone. Marcus and Jess climb from passive RAG to agentic RAG, the M08 router, and UdaPlay's two-tier retrieval. They compare the LLM-driven Version A with the state-machine Version B, and treat the web-search cache and long-term preferences as the same risk: a system writing its own knowledge. They finish with how to evaluate the components that make decisions, then review state management and the Wi-Fiber prompt libraries, and link back to prompt chaining, Tree-of-Thought and the AI Memory hub.

## Segments
- **Cold open:** the Mortal Kombat X question that came back as "internal database" ([[UdaPlay Agentic AI Project]])
- **Deep dive: RAG to agentic RAG.** "Most RAG failures are retrieval failures"; Zillow as faithful-but-shallow; why retries aren't independent: [[Retrieval-Augmented Generation]], [[Agentic RAG]]
- **Deep dive: the router level.** RAG as a tool, descriptions as the routing signal, and why returning answers instead of passages blinds reflection: [[Agent Based RAG]]
- **Deep dive: UdaPlay.** LLM judge as gate, Version A vs Version B (a claim vs a record), the web cache as a write path, and structured output as both routing signal and deliverable: [[UdaPlay Agentic AI Project]]
- **Deep dive: memory.** Semantic, episodic and procedural memory; memory vs RAG by origin; owner bound by closure; "long-term in API only"; a preference overriding grounding: [[Long-Term Agent Memory]], [[UdaPlay Agentic AI Project]]
- **Deep dive: evaluation.** Four dimensions, three strategies, four ingredients; what M10's evaluator doesn't check; pass@k vs pass^k; evaluating the judge as a classifier: [[Agent Evaluation]]
- **Rapid review:** the S → S′ contract, traceability vs determinism, and quadratic token growth ([[Agent State Management]]). Scratchpad-not-decider, compute-don't-ask, safety-first gates, closed-list validation: [[Rapid Response Network Operations Manager Prompt Library]], [[Network Operations Engineering Manager Prompt Library]], [[COO Prompt Library]], [[Financial Controller Prompt Library]]
- **Blast from the past:** UdaPlay Version B as a gated prompt chain, and 0.9⁵ ≈ 0.59 showing up twice ([[Prompt Chaining Workflow]]). The evaluator as the ceiling ([[Tree-of-Thought]]). The context window as a budget, and consolidation ([[AI Memory]])

> [!warning] Corrections and ambiguities flagged on air
> - [[Agent Based RAG]] §3 says the client uses an OpenAI embedding function, but the next row says the embedding model is the library default (*unverified*). These conflict. Check `lib/vector_db.py`.
> - The lecture defines semantic memory as facts learned *from the user* ([[Long-Term Agent Memory]]). The wider literature (e.g. CoALA) also counts general world knowledge, so by that definition UdaPlay's web cache is agent-written semantic memory.
> - The retry formula in [[Agentic RAG]] §7.1 assumes independent rounds. The note itself warns that real retries are correlated unless the query, retriever or source changes.

## Think about it
Say you add a time-to-live to UdaPlay's web cache. You could enforce freshness in three places: (1) filter stale entries out at retrieval, (2) tell the judge in its prompt to treat old cached entries as not useful, or (3) add a code router node that checks `CachedOn` before the judge sees the documents. For each placement, what failure mode does it create, and what test cases would show whether the freshness policy actually works?

> [!quote]- Transcript
> **Marcus:** Here's a puzzle to start the day. You build a research agent for the video game industry. On Monday someone asks it, "Was Mortal Kombat X released for the PlayStation 5?" It checks its local database, finds nothing useful, searches the web, and gives a nice answer citing PlayStation dot com and Wikipedia. On Friday someone asks the same question. This time there's no web search. The agent answers from what it calls the "UdaPlay internal database." Nobody re-indexed anything. So what happened?
>
> **Jess:** The agent learned something? It saved the web result somewhere and found it again on Friday.
>
> **Marcus:** Exactly. And here's the part worth chewing on. Is that a feature, or is it a vulnerability?
>
> **Jess:** I'm going to guess the answer is "yes."
>
> **Marcus:** The answer is yes. Welcome to MS AI Daily. It's Wednesday, October seventh, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. And I'm guessing that cache is where we're going today.
>
> **Marcus:** It's where we end up. Today is a big consolidation day. You finished the Building Agents capstone, the UdaPlay project, and a whole cluster of lessons landed with it: agentic RAG, the agent-based RAG exercise, long-term memory, and agent evaluation. So the deep dive builds one picture. We start with plain retrieval-augmented generation, climb up to agentic RAG, look at how UdaPlay actually wired it together, then talk memory, then talk about how you'd know any of it works.
>
> **Jess:** Then a rapid review?
>
> **Marcus:** Then a rapid review of agent state management and the four Wi-Fiber prompt libraries, the COO, the controller, and the two network operations managers. And in Blast from the Past, prompt chaining, Tree-of-Thought, and the AI Memory hub, all of which turn out to explain things we see in the capstone.
>
> **Jess:** Okay. Let's start at the bottom of the stack.
>
> **Marcus:** Retrieval-augmented generation, or RAG. Quick one, Jess. Your notes have a debugging rule in bold in the RAG hub. What is it?
>
> **Jess:** "Most RAG failures are retrieval failures." If the right chunk never makes it into the context, no amount of prompt engineering saves you, because the model can't use what it can't see.
>
> **Marcus:** Right. And what does the model do when the right chunk isn't there?
>
> **Jess:** It guesses. Usually plausibly.
>
> **Marcus:** Plausibly is the dangerous word. Which is why the note says to evaluate retrieval and generation separately. Recall at k for the retriever, faithfulness for the generator. Now, the agentic RAG lecture takes that idea and says passive RAG has a deeper problem. Passive RAG retrieves once, generates, and never asks whether what it retrieved was any good.
>
> **Jess:** That's the Zillow example. Somebody asks why Zillow's home-buying algorithm failed, the system pulls three documents about market volatility and a statement from the CEO, and it answers "unpredictable housing market conditions."
>
> **Marcus:** And is that answer wrong?
>
> **Jess:** No. It's supported by everything it retrieved. It's just shallow.
>
> **Marcus:** This is the part I want you to hold onto. Suppose you ran a faithfulness metric on that answer. What score does it get?
>
> **Jess:** High, actually. Every claim is backed by a retrieved document. So faithfulness would say it's great.
>
> **Marcus:** Faithfulness would give it a gold star. The failure is coverage. None of those documents explained what the pricing model actually did, or the feedback loop where Zillow's own purchases distorted the market data it was learning from. The agentic version notices the gap, reformulates, asking things like "how did Zillow's pricing algorithm affect its own purchases," and comes back with a multi-factor explanation. Faithful and shallow is a real failure mode, and a faithfulness check alone won't catch it.
>
> **Jess:** So the loop is retrieve, reflect, retry. Let me try the math from the note. If one round finds the evidence half the time, then three rounds gets you one minus point five cubed, so eighty-seven and a half percent. So retrying three times is a pretty good deal.
>
> **Marcus:** That's the math in the note, and the note immediately warns you not to believe it. Why?
>
> **Jess:** Because... oh. The rounds aren't independent. If I send the same query to the same index, I get the same three chunks back.
>
> **Marcus:** Same query, same index, same chunks. That formula assumes each round is a fresh coin flip, and a vector search is not a coin flip. It's a very deterministic function wearing a probabilistic hat. Retries only help when something changes: the query gets more specific or gets split into sub-questions, you switch retrievers, say from vectors to SQL for exact figures, or you pivot to a different source like web search.
>
> **Jess:** Which is why the state machine sketch in the note tracks queries tried and tools tried.
>
> **Marcus:** Right, so the router can refuse to repeat itself. And the note puts the budget in code: a round cap, and a "no new evidence last round" check that forces a pivot or an answer with stated gaps.
>
> **Jess:** Okay, so then the M08 exercise. Agent Based RAG. That one felt agentic, but my notes are pretty hard on it.
>
> **Marcus:** Deservedly, but in a friendly way. Describe the architecture.
>
> **Jess:** Two PDFs, the I E A Global EV Outlook and a gaming industry report. Each one gets its own Chroma collection and its own little passive RAG pipeline: retrieve, augment, generate. Then each pipeline is wrapped as a tool, and an agent decides which tool to call, or none.
>
> **Marcus:** Two nested state machines. The whole RAG pipeline runs inside one step of the outer agent's loop. And what decides which tool gets called?
>
> **Jess:** The tool descriptions. Both start with the same generic sentence, "Search the vector database for relevant information," so the only thing that tells them apart is the source block: title, publisher, release date.
>
> **Marcus:** Which means the docstring is doing all the routing. That's the tool descriptions lesson made painfully concrete. Now the runs. Three of them.
>
> **Jess:** The Oscar question, where the agent called no tool and said it didn't have recent information. The Asia Pacific EV exports question, where it rewrote the question into a keyword query before calling the EV tool. And the games-in-education question.
>
> **Marcus:** So: correct abstention, correct routing, query rewriting. Sounds like agentic RAG. So here's my question. Could this agent notice that the EV tool gave it a weak answer and decide to try again with a better query?
>
> **Jess:** I mean, the instructions tell it to reason about the response and retry if needed. So, in principle, yes?
>
> **Marcus:** In principle it can call the tool again. But can it judge whether the evidence was weak?
>
> **Jess:** Hmm. What does the tool return? Oh. It returns the generated answer string. Not the passages.
>
> **Marcus:** That's the crux. The tool hands back a finished answer. The agent never sees the three pages, never sees the distances. So its "reflection" is reflecting on a summary of a summary. It can't tell a well-supported answer from one the inner model padded. Your note calls this the single most important design choice in the exercise, and I agree. If you want real reflection, return passages with page numbers and distances, or an answer plus the passages.
>
> **Jess:** And there's a cost to that, right? Passages are bigger than an answer, so the outer agent's context grows.
>
> **Marcus:** Yes, and that's the trade. Small context and blind, or bigger context and able to inspect and cite. The note's verdict is that M08 is a router on the autonomy spectrum. Passive RAG, router, reflective, planner. M08 is the second rung.
>
> **Jess:** Is that bad?
>
> **Marcus:** No, that's often the right place to start. Cheap, predictable, and every rung above it can be built on that structure. It's also, and I mean this kindly, easy mode. Two collections about electric vehicles and video games. Routing between those is not exactly a Turing test. The real test is two EV reports from different years, or a question that needs both collections.
>
> **Jess:** One thing I noticed rereading it. The indexing table says the vector store manager creates a client with an OpenAI embedding function, and then the next row says the embedding model is the library default, marked unverified.
>
> **Marcus:** Good catch. Those two rows pull in different directions. If the collection really was created with an OpenAI embedding function, then embeddings come from OpenAI's model, not Chroma's built-in default. I wouldn't call the note wrong, because it honestly flags that row as unverified, but it's internally ambiguous. Worth a thirty-second look at the vector D B module to settle it, because if you ever mix embedding functions between indexing and querying, retrieval quietly falls apart.
>
> **Jess:** Which is exactly the "collection does not exist" pitfall in the UdaPlay note. Same path, same collection name, same embedding function in both notebooks.
>
> **Marcus:** Perfect bridge. Let's go to UdaPlay. Give me the one-sentence version.
>
> **Jess:** A video game research agent that answers from a local vector database of fifteen games, has an LLM judge decide whether what it retrieved is good enough, and falls back to Tavily web search when it isn't, citing sources.
>
> **Marcus:** Which is the Corrective RAG pattern from the research literature: grade the retrieved documents, and fall back to web search when they're poor. Notice how much of M08's homework got done here. The metadata is the entire JSON record for each game, so retrieval returns structured fields, exact year, platform, publisher, instead of a page blob. And the judge returns structured output, a report with a boolean called useful and a description.
>
> **Jess:** Why does it matter that useful is a boolean?
>
> **Marcus:** Because the next step branches on it. If the judge writes a paragraph like "these seem mostly fine, I think," you have to parse vibes. A boolean you can route on. That's a gate check with an LLM sitting inside the gate.
>
> **Jess:** Then there are the versions. Version A is the LLM-driven agent, and Version B is the state machine.
>
> **Marcus:** Walk me through A.
>
> **Jess:** The agent gets three tools, retrieve game, evaluate retrieval, and game web search, and its instructions spell out the process. Call retrieve, then call evaluate, if useful answer, if not search the web, then answer in an Answer, Source, Process format.
>
> **Marcus:** And in the recorded runs, did it follow the process?
>
> **Jess:** It did. It even rewrote queries on its own, like turning "When Pokémon Gold and Silver was released?" into "Pokémon Gold and Silver release date."
>
> **Marcus:** So what's the problem?
>
> **Jess:** Nothing enforces it. The order lives in the prompt. And the Process line at the end is written by the model. It's the model describing what it thinks it did.
>
> **Marcus:** Say that again, because it's the whole lesson.
>
> **Jess:** The Process line in Version A is a claim, not a record.
>
> **Marcus:** A claim, not a record. The model is writing its own performance review. In Version B, each tool becomes a fixed node: recall preferences, retrieve, evaluate, then one conditional branch on the useful flag, either straight to answer or through web search to answer. And the Process line is appended by code from the path actually taken. Now it's a fact.
>
> **Jess:** Okay, but here's my hesitation. Version B is strictly less agentic. It can't rewrite queries anymore, it can't improvise a retry. Aren't we taking a step backward? The whole course is called Agentic AI.
>
> **Marcus:** That's a fair challenge, and I want to take it seriously. Look at what B buys. On the database path, A uses three agent turns plus a judge call. B uses one judge call and one answer writer. B can't loop, because the graph is acyclic, so it always terminates, while A's loop had no step cap. Every node in B is a plain function you can unit test. And the process is guaranteed by the graph rather than requested. What did you lose? Query rewriting.
>
> **Jess:** So the question is whether the inputs vary enough to need the autonomy.
>
> **Marcus:** Exactly. UdaPlay's questions all follow one shape: look up, check, maybe search, answer. When the shape doesn't vary, autonomy is mostly a way to pay more for the same path with less certainty. Your note's critical analysis says it well: the right architecture for this problem is the less agentic one. And the natural next step is a hybrid. Keep B's skeleton, and add one LLM-driven node for reformulation with a bounded retry.
>
> **Jess:** So, use the LLM where judgement is needed, grading and writing, and code everywhere else.
>
> **Marcus:** That's the takeaway line from the note, and it's a good one to tattoo somewhere. Metaphorically. Please consult a lawyer before tattooing design principles.
>
> **Jess:** Noted. Okay, the cache. That's the cold open.
>
> **Marcus:** How does it work?
>
> **Jess:** Every web search result gets upserted back into the same persistent collection as the fifteen games. The ID is "web" plus a hash of the normalized question, lowercased, whitespace collapsed, so the same question maps to the same ID and overwrites instead of duplicating. The embedded text starts with the question itself. And the metadata keeps provenance: the source URLs, a cached-on date, a platform field that literally says "Cached web search," and a type tag so you can delete all cache entries without touching the curated games.
>
> **Marcus:** And when the Mortal Kombat question came back?
>
> **Jess:** The cached entry was the top hit, distance point zero eight four, which was actually closer than any direct game match, because the embedded text starts with the question. The judge said useful, no Tavily call, and it cited the original two URLs from the cache.
>
> **Marcus:** So what did caching save?
>
> **Jess:** I assumed tokens, but the note says no. The cached run used about six thousand one hundred twenty-six tokens versus six thousand one hundred and one without the cache.
>
> **Marcus:** Right, and why?
>
> **Jess:** Because the cached description, up to four thousand characters, still goes into the context. You skip the search, not the reading.
>
> **Marcus:** Exactly. It saves the Tavily call: cost, rate limits, latency. And it buys consistency, the same evidence for the same question. What it doesn't do is freshness. There's a cached-on date, and nothing ever checks it.
>
> **Jess:** So if someone asks "What is Rockstar working on right now?" and it's cached, that answer is "right now" forever.
>
> **Marcus:** Forever, with total confidence, cited as internal knowledge. That's the vulnerability half of the cold open. The cache is a write path into the knowledge base. Unvetted web text, including anything injected into a web page, becomes something the agent later cites as its own database. The provenance labels are the right first defense. The missing ones are a time-to-live, or T T L, per question type, so news expires in days and release facts last much longer, plus a quality gate before anything gets written.
>
> **Jess:** And maybe keep the cache in a separate collection from the curated data.
>
> **Marcus:** Or at least always label cache provenance in the answer. Version B partly does that.
>
> **Jess:** One more piece of UdaPlay, structured JSON output.
>
> **Marcus:** Structured output shows up twice in this project, and I want you to name both roles.
>
> **Jess:** The judge's report is a routing signal, and the GameAnswer schema is the final deliverable.
>
> **Marcus:** Good. And one lovely detail in the schema?
>
> **Jess:** Precision-preserving dates. If the source says nineteen ninety-nine, the JSON says nineteen ninety-nine. It never pads it out to January first, nineteen ninety-nine.
>
> **Marcus:** Because January first would be a fabricated fact wearing a very official-looking date format. That's honest schema design. And what does the schema lose?
>
> **Jess:** Sources. The JSON has no source field, so the spec's "cite your source" requirement disappears in structured mode. And yes or no questions don't fit. "Was it released on PS5" becomes a PS4 record, and the nuance, playable but not native, is gone.
>
> **Marcus:** The JSON is cleaner than the text and less informative. Schema design is part of the product spec, not an afterthought.
>
> **Jess:** Okay, that's a good segue into memory, because UdaPlay also had long-term memory. The preferences.
>
> **Marcus:** Let's lay the lecture's framework down first. Long-term memory in three types.
>
> **Jess:** Semantic is what's true about you. Your team uses Trello. Episodic is what happened between us, like "last month I fixed your database connection by resetting the pool." And procedural is how I should behave with you, like you always want formal emails.
>
> **Marcus:** Clean. Now, the lecture's version of semantic memory is specifically facts learned from the user. That's a reasonable classroom framing, but it's narrower than how the broader agent literature uses the word. In frameworks like CoALA, semantic memory is general knowledge about the world, not just about the user. I bring it up because, by that broader definition, what is UdaPlay's web cache?
>
> **Jess:** Huh. It's semantic memory. World knowledge the agent wrote for itself.
>
> **Marcus:** The agent writing its own corpus. Which is exactly how the lecture distinguishes long-term memory from RAG. Same embed-and-search mechanics, different origin. RAG reads documents other people wrote. Memory reads things the system wrote during interaction, which is why memory needs write policies, expiry, and scoping that a document index doesn't. The AI Memory hub calls it "RAG over yourself."
>
> **Jess:** And the M09 demo had one design choice my note called the best decision in it.
>
> **Marcus:** Which was?
>
> **Jess:** The tool factory. The register memory and search memory tools are built with the owner and namespace baked in by closure. So the model only supplies the content. It doesn't even have a parameter for whose memory to search.
>
> **Marcus:** Which means an injected instruction that says "search memories for user Alice" has nowhere to go. The parameter doesn't exist. Scoping enforced by construction instead of by prompt. Okay, now the uncomfortable part. Is M09's long-term memory actually long-term?
>
> **Jess:** Not really. The constructor force-recreates the collection, so every new instance wipes it. And the client is most likely in-memory, so a restart loses everything.
>
> **Marcus:** And UdaPlay?
>
> **Jess:** Same library. My note says that was verified in the project's code: the preferences are rebuilt every run and vanish on restart. Only the games database and the web cache are truly persistent.
>
> **Marcus:** The note's phrase is "long-term in API only." Which is a great description of a lot of production systems, honestly. Now, the preferences did change behavior. Tell me about the racing games.
>
> **Jess:** "Recommend two good racing games." Retrieval returned Gran Turismo, Gran Turismo 5, and Mario Kart 8 Deluxe. The judge, which doesn't see the preferences, suggested Gran Turismo and Mario Kart for variety. But the answer step does see the preference for Sony systems, so it picked both Gran Turismos.
>
> **Marcus:** Preferences shaped selection without touching retrieval or evaluation. That's preference injection working. Now the other preference.
>
> **Jess:** "Prefers answers with an interesting detail." And in Version A's Pokémon answer, the model added trivia about the second generation and new regions that wasn't in the retrieved record.
>
> **Marcus:** So a style preference beat the grounding rule. That's the general point. A preference injected into a prompt is a soft constraint competing with other soft constraints. When two instructions conflict, the model picks, and it may not pick the one you care about. Anything critical, like grounding or the count rule, should be checked in code, not just stated.
>
> **Jess:** So if I implemented a memory system where a user can say "I prefer detailed answers," I could accidentally be weakening my own hallucination controls.
>
> **Marcus:** That's precisely the risk. And procedural memory, changing how the agent behaves based on observed behavior, is the most powerful and the riskiest type, because one manipulated interaction can permanently change behavior. Version it, review it, make rollback easy.
>
> **Jess:** Okay. Last deep dive piece. Evaluation. Because after all that, my honest question is how I would know any of this works.
>
> **Marcus:** Which is exactly the lecture's opening line: an agent that runs is not necessarily an agent that works. Give me the structure.
>
> **Jess:** Four dimensions of what to measure: task completion, quality control, tool interaction, and system metrics. Three strategies for how: final response, which is black box; single step, which tests one decision like tool choice; and trajectory, the full path, which the lecture calls a flight recorder. And every evaluation needs four ingredients: inputs, outputs, reference data, and an evaluator.
>
> **Marcus:** Good. Now the M10 demo. One test case, "What's the best game in the dataset?" All three strategies scored?
>
> **Jess:** One point zero across the board.
>
> **Marcus:** So the agent is great.
>
> **Jess:** Ha. No. It's one easy case, run once. And my note went into the evaluator code and found the checks are shallow. The single-step check only confirms the tool name matched and the arguments were valid JSON. So calling get games with ten games and top equals false for "the best game" would still pass.
>
> **Marcus:** Wrong arguments, perfect score. What else?
>
> **Jess:** Matching uses "any." If a case expects two tools and the agent uses one, it passes. Extra tools are never penalized, so a forbidden tool would slip through. And the trajectory check never looks at whether the final answer is correct.
>
> **Marcus:** So the trajectory evaluator would give a perfect score to an agent that called the right tool, then called a delete tool, then answered wrong. That's the Jane Doe scenario from the lecture, the sales agent that deletes a customer's records instead of re-engaging her, sailing right through. The lesson is: read your evaluator's code. A metric is only as honest as the function that computes it.
>
> **Jess:** And the statistics section. Pass at k versus pass to the k.
>
> **Marcus:** Let me ask you before I explain. A case succeeds ninety percent of the time per run. Your user runs it five times. What's the chance it works all five times?
>
> **Jess:** Point nine to the fifth. That's... around fifty-nine percent?
>
> **Marcus:** Fifty-nine percent. Pass at k asks whether it succeeded at least once, which looks fantastic. Pass to the k asks whether it succeeded every time, which is what a user actually experiences. A ninety percent agent fails a regular user roughly every couple of days.
>
> **Jess:** Hold on, fifty-nine percent. Didn't that number show up somewhere else?
>
> **Marcus:** Hold that thought, it comes back in Blast from the Past. Now, let's connect evaluation to UdaPlay, because the capstone shows trajectories for three queries but doesn't measure anything. What would you assert?
>
> **Jess:** The expected route, database versus web, for each query. Citation present. JSON valid. And on a cache hit, no web call.
>
> **Marcus:** All deterministic checks, all cheap. And the most important one isn't on that list. What's the single point of judgement in UdaPlay?
>
> **Jess:** The judge. Both versions route on its useful flag.
>
> **Marcus:** So evaluate it like a classifier. Build a small labelled set of questions plus retrieved documents, marked should-be-useful or not. Then measure precision and recall. A false "useful" gives a wrong answer from bad evidence. A false "not useful" wastes a web call. Those errors have different costs, so you pick the operating point on purpose. Same goes for the reflector in agentic RAG. Your note says the reflector is the weak link, and it's right.
>
> **Jess:** Evaluate the parts that make decisions.
>
> **Marcus:** And evaluate the environment, not the claim. If an agent says it updated the record, check the record. Which, you'll notice, is Version B's Process line all over again.
>
> **Jess:** Okay, rapid review time?
>
> **Marcus:** Rapid review. Agent State Management first. Jess, give me the step contract.
>
> **Jess:** Every step takes a state object and returns an updated state object, S to S prime. A router function inspects the state and picks the next step. And the state is ephemeral working memory. It's gone at the end of the run unless you persist it on purpose.
>
> **Marcus:** And the gotcha?
>
> **Jess:** The note says the lecture overstates "deterministic." Control flow is deterministic given the state, but the LLM step is still stochastic, so two runs can take different paths. What you really gain is traceability.
>
> **Marcus:** Traceability, not determinism. Quick number. Six LLM calls, a thousand-token initial prompt, each loop adds five hundred tokens, full history resent every call. Total input tokens?
>
> **Jess:** Six thousand from the base, plus five hundred times zero through five, which is fifteen, so seventy-five hundred. Thirteen thousand five hundred.
>
> **Marcus:** And doubling to twelve calls more than triples it, to forty-five thousand. Quadratic growth. State design is a cost lever. And one more: why must the tool step clear pending tool calls?
>
> **Jess:** Otherwise the router sees them again and re-executes the same tools. Duplicate side effects, or an infinite loop.
>
> **Marcus:** Good. Also notice: human-in-the-loop approval forces ephemeral state to become durable, because the run has to pause and resume. Now the four Wi-Fiber prompt libraries. Rather than go one by one, what's the common spine?
>
> **Jess:** The model organizes and drafts, people and tools decide and compute. The rapid response library literally says that during a live incident the model is a scratchpad, not the decision-maker. And all four have some version of "compute, don't ask." Link budgets and subnet math come from engineering tools, the ledger is the source of truth for the controller, and the COO does the math in a spreadsheet or B I tool.
>
> **Marcus:** Why does that matter so much?
>
> **Jess:** Because language models are confidently mediocre at arithmetic, and these are decisions with money and safety attached.
>
> **Marcus:** Confidently mediocre. I'm stealing that. Rapid Response gotcha?
>
> **Jess:** Dispatch gates are applied in a fixed order with safety first, so time pressure can never override a stop-work condition. And restoration verification: an incident doesn't close when the tower is back. It closes when registered customer equipment per sector is at least ninety-eight percent of the pre-outage baseline and stragglers are handled.
>
> **Marcus:** Which is "evaluate the environment, not the claim," applied to a tower. The tower saying "I'm up" is the agent saying "I updated the record." Engineering manager?
>
> **Jess:** Engineering makes failures less frequent and less severe, rapid response makes them shorter. The gotcha is that standards only matter if they're enforced, so the golden config prompt produces compliance checks a script or an agent can run. And the operational readiness review has hard blockers: monitoring, backup power runtime, out-of-band management, and site access info. If any of those is not ready, the site is not ready.
>
> **Marcus:** COO?
>
> **Jess:** Two linked problems: churn is too high and uptime drives churn. The gotcha is in the shared rules: correlation is not causation. Links between outages and churn get labelled as correlations unless there's a controlled comparison. And the Pareto prompt ranks outage causes by subscriber-minutes, not incident count.
>
> **Marcus:** Because ten tiny outages can matter less than one big one. Controller?
>
> **Jess:** The category mapping prompt uses a closed-list validation gate. The model may only map to G L accounts and cost centers from the provided list, never invent one, and anything that might be capital versus operating expense gets flagged for review. And the expense reduction prompt runs every cut through an operations gate, green, yellow, or red, because a savings that causes outages comes back as churn.
>
> **Marcus:** Closed-list validation is one of the most underrated tricks in this whole course. If the output space is finite, make the gate enforce the list. Okay, Blast from the Past.
>
> **Jess:** Prompt chaining first. Each step's output feeds the next, assembly-line style. The risk is error propagation. With per-step success p, an ungated chain of n steps succeeds p to the n.
>
> **Marcus:** Five steps at ninety percent each?
>
> **Jess:** Point nine to the fifth. Fifty-nine percent. There it is.
>
> **Marcus:** There it is. Same number, different axis. Compounding across steps in a chain, and compounding across runs in pass to the k. In both cases a per-unit reliability that sounds great turns into something mediocre once you multiply. The chaining note's remedy is gates. With a ninety percent step, a gate that detects eighty percent of bad outputs, and three attempts, each step gets to about ninety-eight percent, and the five-step chain goes from fifty-nine to about eighty-nine.
>
> **Jess:** And the note's big caveat is that gates only help as much as they detect.
>
> **Marcus:** Which is UdaPlay's judge again. And here's the connection I really want you to see. UdaPlay Version B is a prompt chain. Retrieve, evaluate, maybe search, answer, with one routing gate in the middle. You learned the pattern weeks ago. The capstone is the pattern with a vector database bolted on.
>
> **Jess:** Tree-of-Thought next. Chain-of-thought generalized from one path to a search tree. Generate several candidate thoughts per step, evaluate partial solutions, search with breadth-first, depth-first, or beam, and backtrack from dead ends. The headline result was Game of 24, where GPT-4 went from four percent with chain-of-thought to seventy-four percent with Tree-of-Thought.
>
> **Marcus:** And the weak point?
>
> **Jess:** The evaluator. The search is only as good as its value function.
>
> **Marcus:** Three notes today, one sentence. ToT's evaluator, agentic RAG's reflector, UdaPlay's judge. All three are an LLM grading a partial result, and all three cap the system's quality. Where you can, swap in a programmatic check. And the prompt libraries used ToT sensibly: the mass-event restoration prompt compares three restoration orders, and counting downstream towers can change which site you fix first.
>
> **Jess:** Last one, the AI Memory hub. The idea I'd keep is that the context window is a budget. System prompt, memories, recent turns, tools, and output reserve all compete for the same tokens. Memory management is deciding what earns a place.
>
> **Marcus:** Which explains a UdaPlay number. The memory agent's prompts were longer, Pokémon went from about twenty-nine hundred to about thirty-five hundred tokens, because preferences are injected on every call. And with only two preferences stored and a retrieval limit of two, both are always recalled, even for a plain release-date question. The hub also covers consolidation: "moved to Denver" should replace "lives in Austin," not sit next to it. M09 had no update or dedupe, so changed preferences would just pile up.
>
> **Jess:** Okay. Takeaways?
>
> **Marcus:** Three. First: put control flow in code and judgement in the LLM. Prompts are requests; graphs, closures, gates, and loop caps are guarantees. Version B's Process line is a fact because code wrote it.
>
> **Jess:** Second?
>
> **Marcus:** Second: whenever a system writes to its own knowledge, the write is the critical gate. A web cache and a long-term memory are the same risk wearing different hats. They need provenance, expiry, vetting, and scoping, or one bad write becomes a permanent internal fact.
>
> **Jess:** And third?
>
> **Marcus:** Third: evaluate the components that make decisions, not just the final answer. Judges, reflectors, and evaluators are classifiers, so measure their precision and recall on labelled cases, with enough cases and enough repeated runs that a perfect score actually means something.
>
> **Jess:** And the think-about-it question.
>
> **Marcus:** Here it is. Say you add a time-to-live to UdaPlay's web cache. You could enforce freshness in three places: filter stale entries out at retrieval, tell the judge in its prompt to treat old cached entries as not useful, or add a code router node that checks the cached-on date before the judge ever sees the documents. For each placement, what failure mode does it create, and what test cases would you write to tell whether the freshness policy is actually working?
>
> **Jess:** Ooh. I already have opinions, but I'll sit with it.
>
> **Marcus:** Sit with it. Thanks for listening to MS AI Daily. I'm Marcus.
>
> **Jess:** And I'm Jess. See you tomorrow.

