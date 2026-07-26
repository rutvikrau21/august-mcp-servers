# Lead Source Playbook

*Where this SDR's leads come from. Three engines, in priority order. Built from what's already in Slack, Notion, HubSpot, and the Outbound Focus page — this consolidates and sharpens rather than inventing a new motion.*

---

## Why outbound gets a dedicated person

From `#gtm-analytics`, two numbers justify the hire:

- Outbound has driven the large majority of closed-won revenue, at an average deal size around **$53K**, against roughly **$3K** for self-serve. Roughly **18× upside** per account on the same top-of-funnel.
- Referrals are the single largest attributed source (~$767K, ~31% of attributed closed-won) — and referrals are *worked*, not received.

Meanwhile there were **831 leads sitting in S0** at last count, and press spikes (Bar & Bench, Artificial Lawyer) have driven enormous traffic with almost no attributed conversion. The gap is not lead volume. It is that nobody's whole job is working them.

That is this role.

---

# Engine 1 — Site visitors

**Warmest source. They already came to us. Start here in week 5.**

## What already exists

- **PostHog** tracks website visitors, page-level. Traffic runs ~7K–13K visitors/week depending on press.
- **Clay + Amplemarket** site-visitor segmentation is built — personalized sequences triggered by *which page* a prospect visited, with messaging tailored to that content.
- Demo booking runs through **Cal.com** → HubSpot. Note the known attribution gap: no URL change during booking, so form-fire and GCLID handoff need verifying before trusting the source field.
- **HubSpot** holds the S0 backlog and all prior form fills.

## Sub-sources, in order of warmth

| Sub-source | What it is | How to work it |
|---|---|---|
| **Demo requests / Cal.com bookings** | Highest intent that exists | Same-day follow-up, always. Never let one sit overnight |
| **The S0 backlog** | ~831 leads that entered and stalled | Systematic re-work by cohort — not by date order. Segment first, then sequence |
| **Pricing / product page visitors** | Read as active evaluation | Sequence keyed to the exact page. Tabular Review visitor gets the Tabular Review angle |
| **Solutions page visitors** | Practice-area intent, self-declared | Match to the practice-area segment messaging. Someone on `/solutions/litigation` gets litigation |
| **Guide + ebook downloads** | 20 deals created from the Guides alone | Re-engagement sequence. Warm touchpoint for people who showed early interest and never converted |
| **Landing page conversions** | ROI Calculator, Buyer's Guide, Law Firm of the Future | Use their own inputs as the opener — a completed ROI calculator is a stated pain |
| **Press-driven traffic** | Bar & Bench (India), Artificial Lawyer, ChatGPT referrals | High volume, low intent. Firmographic-filter hard before spending time |
| **Conference + dinner attendees** | 1.5 years of attendee lists | Reactivation angle: what shipped since we met. Genius Mode, new workflows |

## The workflow

1. Pull the visitor list from PostHog / Clay, deduped against HubSpot and Attio.
2. **Firmographic filter first** — is this a law firm we can sell to, at a size we serve? Most press traffic fails here. Spending an hour on unqualifiable traffic is the fastest way to waste this engine.
3. Identify the person, not just the company. A firm's IP visiting `/product/tabular-review` is a signal; find the practice group leader it most likely belongs to.
4. Enroll in the page-matched Amplemarket sequence.
5. Call the same week. Site visit + call is dramatically stronger than either alone.

## What to fix while working it

Real gaps this SDR will hit and should raise, not route around:

- Cal.com → HubSpot deal creation at S0 needs verifying (raised in `#marketing`, unresolved)
- GCLID survival through the homepage → Cal.com → HubSpot handoff
- Press-traffic landing pages have no dedicated capture, so the largest traffic events convert at near zero

---

# Engine 2 — Partnership installed base

**Integration-qualified prospects. Week 6.**

The thesis is simple: a firm already running iManage, NetDocuments, Lawmatics, or Clio has already bought into a document or practice-management spine. August plugs into it. That is a shorter conversation than one that starts from zero.

## Partner status — know this cold before you send anything

| Partner | Where we actually are | What you may claim |
|---|---|---|
| **iManage** | Partnership agreement signed. Partner badge. Integration landing page live. Listed for ConnectLive | Real, named partnership. **Phase 1 is pick-and-select** — browse iManage folders, choose documents, pull them into August. **Not** full indexing or search-across-everything. That's phase 2+, gated on ethical walls |
| **NetDocuments** | Integration + landing page in the rollout sequence; Amplemarket sequence built | DMS integration on the roadmap. Do not describe as shipped |
| **Lawmatics** | In the integration landing page queue; Amplemarket sequence exists | Roadmap. Position as "we're building toward your stack" |
| **Clio** | **Clio Manage integration is in development.** Connect via per-user OAuth, ask about matters in chat, browse and import matter documents, save work product back to a matter, link a project to a matter. Behind a feature flag; built initially for a specific customer | In development, with a demo available. Do **not** sell as GA |

**The iManage security conversation.** This comes up on every serious iManage firm, and Hughes Hubbard raised it directly: *if August indexes everything, do users see documents their firm's ethical walls should have blocked?* The honest answer is that we mirror the DMS's own permissions — so if the firm's iManage is a free-for-all, indexing inherits that. Which is exactly why phase 1 is pick-and-select. **Know this answer before you dial an iManage firm.** Getting it wrong once costs the account.

## The list-building technique

This is the highest-leverage prospecting move available, and it came from Rutvik in `#sales`:

> *"Easy prospecting tip for partnerships is to have Claude look through a company's page for law firm references or mentions and most likely those firms will be a customer. Great for iManage, NetDocs, Lawmatics etc."*

Operationally:

1. Scrape partner sites — customer pages, case studies, press releases, webinar registrations, conference speaker lists, user-conference agendas — for named law firms.
2. Every firm named is almost certainly a customer of that partner. That's your integration-qualified list.
3. Enrich: size, practice mix, geography, existing AI vendor.
4. Filter to fit, dedupe against HubSpot and Attio.
5. Route into the partner-specific Amplemarket sequence.

**Automate this.** It's a Claude skill plus a Clay table, it runs across four partners, and it refreshes. This is exactly the kind of work the training plan grades in week 2 — and exactly the work whose absence was named in the last SDR post-mortem.

## Messaging angles by partner

- **iManage** — *"You've already solved where documents live. August is the layer that reads them."* Lead with the named partnership. Be precise about phase 1.
- **NetDocuments** — Competitive urgency is real here; other legal AI vendors have announced NetDocuments integrations. Position on platform depth, not connector parity.
- **Clio** — Smaller firms, managing-partner buyer, faster cycles. Matter-centric language: *"ask about a matter, pull its documents, file the work product back."* Note that Clio owns Vincent (vLex) — expect it as the incumbent alternative.
- **Lawmatics** — Intake and CRM-led firms. Angle at the intake-to-first-draft handoff.

---

# Engine 3 — Case-study geography

**Highest craft. Highest conversion when done well. Week 7.**

The pattern behind our best closed deal: `harrison_drury` LinkedIn ABM drove ~60 visitors and produced a **$407K** closed deal. Small, precise, reference-anchored targeting beats volume.

The play: take each flagship customer, work outward from it geographically, target firms of **10–50 lawyers** in that region, and make the message genuinely personal — same region, same size, same problems, name the reference.

## The reference map

| Reference | Region to work | Profile to target | The message |
|---|---|---|---|
| **Harrison Drury** (UK, nine offices, ~100 licenses, ~$407K, public video + testimonial reel, Malcolm Ireland) | UK North West — Lancashire, Greater Manchester, Merseyside, Cumbria, Yorkshire | Regional full-service, 10–50 lawyers, multi-office | Strongest asset we have for UK regionals. Public video, named champions, Workflows + FDE outcomes. *"A firm your size, twenty miles from you, is doing this."* |
| **Hughes Hubbard & Reed** (US, firmwide across transactional/litigation/regulatory + business functions, ~$360K, MP Robb Patryk on record, COO Gerard Cruse) | US Northeast day-trip cities — Philadelphia, DC, NYC and upstate, Connecticut, New Jersey | **Use only where the profile matches** — regional full-service, 150–400 lawyers, CIO/COO play | Firmwide simultaneous deployment. Do not use HHR on a 15-lawyer boutique; it reads as a mismatch and kills credibility |
| **Hicksons** (Australia, ~374 active users — our largest by seat count, first-in-region, marketing video) | NSW and Sydney metro, then Melbourne and Brisbane | Insurance defence, litigation, professional services, 10–50 lawyers | Largest deployment by users. First-in-region angle is live for AU/NZ. Warm adjacency via David at Hicksons → Interlaw / Hunt & Hunt |
| **Lobo de Rizzo** (Brazil, ~114 users, launch with press release + video in progress) | São Paulo, Rio, then wider LatAm | Corporate/transactional boutiques, 10–50 lawyers | Press release and video in motion; time outreach to land with the coverage. AB2L network is an adjacent route in |
| **DVM** | Their region and practice peer set | Same size band | Smaller reference — use where profile match beats logo size |
| **Godoy Córdoba** (Colombia), **HDRBB** (NJ), **ELP / Luthra / Quillon** (India) | Respective markets | 10–50 lawyers | Secondary references; check current status with CS before naming |

## Why 10–50 lawyers

It is the sweet spot and the segment brief already says so: the **managing partner is buyer, decision-maker, and daily pain point**. No IT function, no procurement gauntlet, no innovation committee. Deals move in weeks, not quarters. It is also the band where a nearby reference firm carries the most weight — these firms know each other, compete for the same clients, and hire from each other.

## The message formula

Four elements. All four, or it isn't personalized:

1. **Proximity** — same region, named. *"You're twenty minutes from Preston."*
2. **Profile match** — same size, same practice mix, said explicitly.
3. **The reference, with an outcome** — not a logo drop. What changed at that firm.
4. **One specific workflow** for their practice — lease abstraction, demand letters, office actions, dilapidations, s.146 notices. Not "700+ workflows."

Cut any email that would still make sense if you swapped in a different firm's name. That's the test.

## Practice-area overlay

Cross the geography with the segment briefs already written in Outbound Focus — 21 segments with titles and angles defined. The near-term ones that fit the 10–50 band best:

Small corporate boutiques · insurance defence · IP patent prosecution · employment (management-side) · PI and mass tort · estate planning and T&E · construction litigation · commercial real estate leasing · debt collection and creditors' rights · family law · immigration

Two standing cautions from those briefs, worth repeating because they're easy to get wrong: **appellate boutiques** are extremely AI-skeptical — founding partner only, never a firmwide or business-function angle. **White collar defence** requires a warm intro or very targeted outreach, and leads with security.

Our UK legal agent library is unusually deep — statutory demands, dilapidations, s.146 notices, 1954 Act notices, break notices, pre-action debt recovery packages. That is real, specific ammunition for UK regional firms and it is underused in outbound.

---

# Standing sources — always on

Not an engine, but they should never go stale:

| Source | Owner action |
|---|---|
| **Referrals** | #1 attributed revenue source. Ask every happy customer contact, systematically, on a cadence — not opportunistically |
| **Closed-lost in HubSpot / Attio** | Re-engage on a trigger: new capability shipped, new reference in their region, new person in the buying seat |
| **Harvey renewal cohort** | Firms that bought Harvey in 2024 are up for renewal and a real share are unsatisfied. Actively hunt this — it is a stated pattern, not a hope |
| **Merger and roll-up news** | Law360 and LinkedIn. Two siloed precedent libraries and conflicting templates is a genuine trigger event |
| **Job postings** | Firms hiring KM directors, innovation leads, or legal ops are budgeting for exactly this |
| **Intent data** | ZoomInfo intent. BirdDog/WhiteWhale was being wound down — confirm current state before building a motion on it |

---

## Definition of done

**A qualified lead is someone who sits for a demo or moves past discovery.**

Not a booked invite. Not a no-show. Not "send me something." This is the definition in the SDR offer letter, and it is deliberately the same definition used for comp and for coaching.

## Weekly rhythm

| When | What |
|---|---|
| Monday | Territory plan. Which engine gets which hours this week, and why |
| Daily | Two protected call blocks. Sequence tasks. Every activity logged in HubSpot the same day |
| Wednesday | Mid-week honesty check with manager. Off-pace gets said now, not Friday |
| Friday | Number reported, plus one written learning posted to `#sales` — what worked, what didn't, what changes next week |
