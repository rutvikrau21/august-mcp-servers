# SDR Training Plan — 90 Days

*Companion to [Good SDR, Bad SDR](./good-sdr-bad-sdr.md) and the [Lead Source Playbook](./lead-source-playbook.md). Extends the existing [BDR Onboarding](https://app.notion.com/p/3569073ab18781f59a1af652c58f5040) page in Notion — that page covers tools, access, and who's who. This one covers company, product, roadmap, and the ramp to full quota.*

---

## Design principles

These are deliberate choices, not boilerplate. Each one exists because of something that already happened here.

**1. Training is the manager's job, not a document's job.**
Horowitz, via Andy Grove: twelve hours of a manager's time across a team returns hundreds of hours of productivity. Every session below has a **named owner**. If the owner can't make it, it moves — it doesn't get skipped or delegated to a Loom.

**2. Training is mandatory, and it's the expectation-setting mechanism.**
Spencer's post-mortem said the role as described didn't match the job week to week. The fix is that the job is written down first (Good SDR / Bad SDR), taught second, and measured third — in that order. Nobody gets held to a standard they were never taught.

**3. Automation is in the job description from day one.**
The other explicit finding from the post-mortem: automation work should have been in the role description or built before the SDR joined. It's in this plan, starting week 2, and it's graded.

**4. Learning and doing run in parallel, not in sequence.**
Four weeks of classroom before touching a phone builds an SDR who is terrified of the phone. Mornings are training, afternoons are reps — shadowing in week 1, live and supervised by week 2, owned by week 4.

**5. Every phase has a gate.**
You don't advance because a calendar week ended. You advance because you passed a specific, demonstrable check.

---

## Before day one — owner: hiring manager

Done *before* the start date, not during week 1. An SDR spending their first three days chasing logins is a manager's failure.

- [ ] All access provisioned and tested: HubSpot, Amplemarket, Salesfinity, Gong, Sales Navigator, Slack, Notion, August Academy (Circle), Attio (read), PostHog (read), Clay
- [ ] `@august.law` email warmed and connected to Amplemarket; sending domain checked
- [ ] Phone number and voicemail live in Salesfinity
- [ ] Laptop, monitor, **headset** shipped and received
- [ ] Territory assigned in writing — which segments, which geographies, which accounts are off-limits because an AE owns them
- [ ] Named onboarding owner + a peer buddy who is not the manager
- [ ] Week 1 calendar sent, fully booked, with owners on every session

---

## Phase 1 — Company and market (Week 1)

**Goal:** They can explain what August is, who buys it, why we win, and why the company exists — to a lawyer, without notes.

| Session | Owner | Content |
|---|---|---|
| Why August exists | Rutvik / Thomas | Founding story, Vecflow → August, the thesis on how AI changes the economics of legal work, why we capture value through outcomes rather than seat expansion |
| The legal market 101 | Julia | Billable hour economics, realization, leverage. Practice areas and the workflows inside each. Firm sizes and how the buying motion differs at 20 lawyers vs. AmLaw 100 |
| Personas and who actually signs | Andrew / Hayden | Managing partner, practice group leader, COO, CIO, KM director, firm administrator. Who is buyer, who is champion, who is blocker at each firm size |
| Competitive landscape | Andrew | Harvey, Legora, Hebbia, Spellbook, Robin AI, GC AI, Vincent/vLex (Clio), Irys. Battlecards. The "Claude for Legal is an orchestration layer, August is a platform" argument |
| How we're organized | Julia | Who does what across sales, marketing, CS, FDE, eng. Where to ask for what. Slack channel map |
| Read + write | Self | Read *Good SDR, Bad SDR* and write a one-page response: which pairs describe you today, which don't |

**Reps this week (afternoons):** Shadow 3 live calls. Watch 5 demos, 5 discovery calls, and 3 closed-won calls in Gong — take notes on the *language customers use*, not the features we mention.

### Gate 1
- [ ] Delivers the 15-second pitch to the manager, cold, and can flex it to a litigator, a corporate associate, and a COO
- [ ] Names the top 5 competitors and gives a one-sentence reason a firm picks August over each
- [ ] Explains how a law firm makes money and what a managing partner is actually optimizing for
- [ ] Submitted the written response to *Good SDR, Bad SDR*

---

## Phase 2 — Product, hands on (Week 2)

**Goal:** They have *used* the product on real work, not watched it. An SDR who has never made August do something surprising cannot describe it credibly.

| Session | Owner | Content |
|---|---|---|
| Assistant + Genius Mode | FDE / CS | Live, on real documents. Run a research task end to end |
| Workflows | Jalaj / CS | Build one from scratch. Then run one of the prebuilt UK/US workflows and read the output critically |
| Playbooks | CS | Run a playbook against a real contract. Understand what "encode the firm's standards" means in practice |
| Tabular Review | CS | Batch a document set into a cited table. This is the demo moment that lands most often — know it cold |
| Integrations, honestly | Dominic / Neil | What ships today vs. what's in dev. Word, Outlook, SharePoint, Google Drive, Dropbox, OneDrive, SOS. iManage phase 1 = pick-and-select, **not** indexing. Clio Manage = in development |
| Security and trust | Neil | SOC 2, data handling, the ethical walls conversation, why this comes up first at white collar and healthcare firms |
| **Automation block** | Harsh | Build one thing: a Claude skill, a Clay enrichment table, or a HubSpot view. It must be published for the team, not kept locally |

**Reps this week:** First live dial block with the manager listening. Two per day, supervised. Goal is not meetings — it's getting comfortable saying the words out loud.

### Gate 2
- [ ] Has personally run: a Workflow, a Playbook, and a Tabular Review, and can narrate what each does and who it's for
- [ ] Can correctly sort a list of 10 capabilities into **live / in development / roadmap** with no errors
- [ ] Shipped one automation and posted it for the team
- [ ] Completed all August Academy videos

---

## Phase 3 — Roadmap and customer proof (Week 3)

**Goal:** They can talk about the future without selling it, and can tell our customer stories from memory.

| Session | Owner | Content |
|---|---|---|
| The roadmap | Rutvik / Josh | Client portals, deposition support, revamped playbooks and workflows, e-discovery, governance and admin controls, DMS integrations (iManage, NetDocuments, SOS, Lawmatics), Clio, desktop app, Zoom/Teams assistant, mobile, autonomous agents |
| **The overpromising rule** | Thomas / Ravi | CS has flagged this directly: overpromising capability is the fastest way to lose a customer at implementation. The rule — you may say *"that's on the roadmap, I'll get you a real timeline from the team."* You may not say *"yes, we do that."* |
| Governance and enterprise readiness | Neil | What Selendy asked for and why it matters: user groups, RBAC, matter-level permissions and ethical walls, external sharing approval, guest access, audit. Where we are honestly |
| Case study deep dive | Vivan / Sharon | Hughes Hubbard, Harrison Drury, Hicksons, Lobo de Rizzo, DVM. For each: firm profile, what changed, named champion, what's public and shareable |
| The FDE model | Jalaj | What a forward-deployed engineer actually does in an account, why it's our structural differentiator, and what it costs — so they don't promise FDE work to an 8-seat firm |
| Pricing and deal shape | Andrew / Hayden | Flat monthly, unlimited queries, no token billing. Typical deal sizes by firm profile. Where the threshold for meaningful FDE work sits |

**Reps this week:** Full call blocks, live, unsupervised. First personalized sequence written and reviewed by Julia before it sends.

### Gate 3
- [ ] Tells the Harrison Drury and Hughes Hubbard stories from memory, including the named champion and what changed
- [ ] Correctly answers three planted "can August do X?" traps — where the right answer is a roadmap deflection, not a yes
- [ ] Knows which reference to use for which prospect profile and why

---

## Phase 4 — Certification and first outbound (Week 4)

**Goal:** Cleared to run their own outbound unsupervised.

| Session | Owner | Content |
|---|---|---|
| Messaging workshop | Julia | Writing personalization that is load-bearing. Rewriting three bad emails into three good ones |
| Objection handling | Andrew / Julia | The five we hear most: *we already use Harvey* · *we're not ready for AI* · *what about privilege and confidentiality* · *we have no budget this year* · *send me something and I'll look*. Drilled, not discussed |
| Handoff standard | Hayden / Myles | What an AE needs in a handoff: pain, trigger, stack, people, objection already heard. Written format, in HubSpot |
| **Certification** | Manager + one AE | Mock call, live. Two attempts allowed |

**Reps this week:** Own the full daily cadence. First sequences live.

### Gate 4 — Certification
- [ ] Passes a live mock: cold open → discovery questions → objection → booked meeting
- [ ] Writes a personalized cold email that Julia would send without edits
- [ ] Produces one handoff that the receiving AE accepts without follow-up questions

**On passing, they are cleared to run live outbound unsupervised and enter ramped quota.**

---

## Phase 5 — Lead engines, one at a time (Weeks 5–8)

Full detail in the [Lead Source Playbook](./lead-source-playbook.md). Sequence matters — warmest first, so early wins come while confidence is still forming.

| Week | Engine | Why this order |
|---|---|---|
| 5 | **Site visitors** | Warmest. They already came to us. Fastest feedback loop, shortest path to a first booked meeting |
| 6 | **Partnership installed base** — iManage, NetDocuments, Lawmatics, Clio | Integration-qualified, and the list-building technique (mining partner sites for firm references) is teachable and repeatable |
| 7 | **Case-study geo expansion** — 10–50 lawyer firms near a reference | Highest craft requirement. Personalization has to be real. Save it for when they can write well |
| 8 | All three, running together | Their own weekly plan, allocating time across engines |

Each week: engine kickoff Monday with the owner, mid-week list review, Friday write-up of what worked in `#sales`.

### Gate 5
- [ ] Has booked qualified meetings from at least two different engines
- [ ] Presents a written 30-minute readout: which engine converts best in their territory, with the numbers behind the claim

---

## Phase 6 — Full ownership (Weeks 9–12)

No new curriculum. The SDR now runs the job and the manager coaches against *Good SDR, Bad SDR*.

- Full quota
- Owns their own territory plan, reviewed monthly
- Weekly 1:1 structured against the Good SDR / Bad SDR pairs — not a status update
- One system improvement shipped per month, published for the team
- Gong self-review: pick one of their own calls each week and critique it before their manager does

### Day 90 review
Structured directly against the document. For each section — ownership, market, product, targeting, messaging, phone, systems, discipline — where are they on the good/bad axis, with evidence.

---

## Ramp targets

Numbers to be set by the manager against current territory data before day one, so the SDR knows them on day one. Suggested shape:

| Period | Expectation | Definition |
|---|---|---|
| Weeks 1–4 | Certification, not volume | Gates 1–4 passed |
| Weeks 5–8 | 40% of full quota | Qualified = sat for a demo **or** moved past discovery |
| Weeks 9–12 | 70% of full quota | Same definition |
| Month 4+ | 100% | Same definition |

**A qualified lead is someone who sits for a demo or moves past discovery.** Booked-and-no-showed is not qualified. This is the same definition used in the SDR offer letter — comp and coaching measure the same thing, deliberately.

---

## What the manager owes the SDR

Reciprocal, and non-negotiable. Horowitz's standard is that you cannot fairly hold someone to expectations you never taught.

- Every session above happens, with the named owner in the room
- Weekly 1:1, never cancelled, structured against this document
- Gong call review with written feedback, weekly through week 8
- Territory and quota in writing before day one
- Say the hard thing on Wednesday, not at the 90-day review

---

## Reading list

- Ben Horowitz — *Good Product Manager, Bad Product Manager*
- Ben Horowitz — *Why Startups Should Train Their People*
- Andy Grove — *High Output Management*, ch. 16, "Why Training is the Boss's Job"
- August battlecards and the Sales Documentation page in Notion
- The last 8 weeks of `#gtm-analytics` — the fastest way to understand where pipeline actually comes from
