# 5 · How Your Week Runs

*Mirror of the [Notion page](https://app.notion.com/p/3ac9073ab1878151a9b9c0138552efac). Part of [SDR Onboarding](./README.md).*

> **This is the page you actually live in.** The other four tell you what to do and why. This one tells you what to do today.
>
> The test is simple. You should never sit down at your desk and wonder what to work on. If you do, something here is broken and we want to know.

## The shape of the whole thing

**One theme a week. One list of firms behind it. A multi-channel sequence as the backbone, with calls layered on top by you.**

**Rutvik provides the theme and the list.** You build the assets on Monday morning, they're **approved by 11am, and the sequence starts the same day.**

From there the sequence runs itself for six working days across LinkedIn and email. Your hours go into calls and into answering replies, because those are the two things Amplemarket can't do for you. Each list finishes the following Tuesday, so you always have this week's list mid-flight and last week's list closing out.

> **Two things decide whether a week works, and neither of them happens on the phone.**
>
> **The theme.** One segment, one pain, one reference, one angle. Everything you send that week is a different length of the same argument.
>
> **The list.** Fifty firms where that argument is true.
>
> Get those two right and an average week converts. Get them wrong and no amount of dialling saves it. This is why Monday is a build day and why nothing sends until it's been reviewed.

---

## The sequence, and what it already does

The backbone is a single Amplemarket sequence that runs **email and LinkedIn together**, fully automatic, over six working days. This is the shape Shaya already built and it's the right one.

| Stage | Channel | When | What it does |
|---|---|---|---|
| 1 | LinkedIn connect | Day 0 | The connection note. No ask |
| 2 | Email | +1 day | Four paragraphs, fresh subject line |
| 3 | LinkedIn message | +1 day | **The ask lands here** |
| 4 | Email | +2 days | `Re:` threaded on the original |
| 5 | LinkedIn like last post | same day | Free visibility |
| 6 | Email | +2 days | `Re:` threaded, the close |

Six touches, one to two days apart, which is exactly what the audit says works. The ask sits on touch three rather than touch one. The follow-ups thread as `Re:` so they land in the same conversation. LinkedIn steps skip themselves if they go more than three days overdue, so a slow week doesn't produce a message that arrives out of context.

**What the sequence doesn't do is call anybody.** That's the gap, and it matters, because the phone produces the highest interested rate we have.

**So the split is simple. Amplemarket owns email and LinkedIn. You own the phone and every reply.**

Per touch, here's why the phone is worth your hours:

| Channel | Volume, 30 days | Reply / connect | **Interested** |
|---|---|---|---|
| Email | 5,571 sent | 0.37% | **0.13%** |
| LinkedIn | 2,227 tasks | 3.56% | **1.64%** |
| Phone | 908 calls | 10.13% connect | **1.65%** |

Read that correctly. It doesn't mean email is wrong, it means email is cheap automated coverage and your personal time is expensive, so spend it where the rate is highest. A firm that gets the sequence and nothing else is a firm we've reached. A firm that gets the sequence plus two calls is a firm we've actually worked.

---

## Monday: build it and launch it

Everything happens before lunch. The gate is **11am**.

| Time | What | Who |
|---|---|---|
| **By Friday close** | Theme and firm list handed over | Rutvik |
| **9:00–11:00** | Contacts, dedupe, enrichment, write the assets | You |
| **11:00** | Review and sign-off | Rutvik |
| **11:00–12:30** | Load the sequence, load the dialer | You |
| **Afternoon** | **Sequence goes live.** Stage 1 fires | Automatic |

The eleven o'clock gate only works if the theme and list land the Friday before. If they arrive Monday morning you'll lose the day, so chase them on Friday rather than waiting.

### The theme

**Rutvik picks it.** The bank to pick from is in [Outbound Focus](https://app.notion.com/p/3899073ab18780259b1fcaab5589f8d7), which has twenty-one practice segments already written up with the titles to target and the angle for each, plus the location themes for cities and trips we're running.

A theme is good when all fifty firms could receive the same message and it would be specifically true of every one of them.

> **The test.** Swap firm A's name for firm B's on your list. Is the email still true?
>
> **Yes** means it's a real segment theme. Good.
>
> **It would be true of any law firm anywhere** means it's generic. Rewrite it.

The strongest themes carry a trigger, meaning something that changed recently. A merger in the last eighteen months. A new managing partner. A conference they attended. An AI tool bought in 2024 that's up for renewal. Triggers beat demographics every time.

### The list

| | What you do | Where |
|---|---|---|
| **Take the firms** | Roughly **50**, all matching the theme, handed over by Rutvik | Notion |
| **Pick the people** | Two per firm, about 100 contacts. Titles are already written per segment | Sales Navigator |
| **Enrich** | Phone, title, firm size, practice mix, recent news. Harsh helps here | Clay |
| **Dedupe** | Against HubSpot and Attio. Kill anything an AE owns, anything live, any customer, anything touched in ninety days | HubSpot, Attio |

**The list test.** Read any three rows at random. If you can't say in one sentence why that firm belongs to this theme, it doesn't, and it comes off.

### The assets

**You write these.** They're the dynamic fields the sequence fills in, so writing them is the same job as loading the sequence.

| Field | What it is | Level |
|---|---|---|
| `linkedin_connection_message` | Under 300 characters, no ask. The segment noun does the work | Segment |
| `email_subject` | One fresh subject line. Everything after threads `Re:` on it | Segment |
| `email1_para1` | The specific thing about this firm | **Per firm** |
| `email1_para2–4` | The bridge, the reference, the ask | Segment |
| `linkedin_subject`, `linkedin_message` | **The touch that carries the ask.** Short, one offer | Segment, para 1 per firm |
| `email2_para1–4` | A different angle, never a bump of email one | Segment |
| `email3_para1–3` | The graceful close | Segment |

**Write the segment-level fields once.** They're the same for all fifty firms and they're the argument. **Then override paragraph one per firm** on the two touches that carry it, which is email one and the LinkedIn message. That's where the fifteen minutes of research per firm actually goes, and it's the difference between a themed sequence and a mail merge.

Plus one asset that isn't in Amplemarket at all. **The call opener.** Fifteen seconds. Who you are, the specific thing, ask permission to keep going.

> Hi {First}, I'm at August, an AI platform built specifically for law firms. We work with {segment} on {pain point}. Wanted to connect and share what we're seeing across firms like yours.

> **The rules on all of them.** Under 300 characters on the connection note, and verify before sending. No em dashes. Never say "the data" or "our analysis" in anything a prospect reads. Only reference things you actually checked, never an invented post or mutual connection. Soft CTA only on a first touch. **No pricing, no demo ask and no meeting ask in a first cold touch.**

### The brief, and the 11am review

Four lines at the top of the sprint row. If you can't write them, the week isn't ready.

> **Theme.** Insurance defence shops, 20 to 150 attorneys, on flat-rate carrier arrangements.
>
> **Angle.** More output per attorney hour on flat-fee matters without adding headcount.
>
> **Reference.** Hicksons. Never Hughes Hubbard.
>
> **Titles.** Managing Partner, COO, Firm Administrator.

Rutvik signs off at 11am. Nothing sends before that.

**Monday is done when:** 50 firms, 100 contacts, all dynamic fields written, brief approved at 11am, sequence loaded and live, dialer list loaded in Salesfinity.

---

## The week at a glance

| | **Monday** | **Tuesday** | **Wednesday** | **Thursday** | **Friday** |
|---|---|---|---|---|---|
| **Sequence (automatic)** | Build, approve at 11am, **stage 1 live PM** | Stage 2, email | Stage 3, **the LinkedIn ask** | — | Stages 4 and 5 |
| **Last week's list** | — | Stage 6, the close | — | — | — |
| **Phone (you)** | — | **80 dials, this week** | **80 dials, this week** | 60 dials, this week | 40 dials, last week |
| **Replies (you)** | — | All, within the hour | All, within the hour | All, within the hour | All, within the hour |
| **Other** | Build and launch | — | — | — | Sprint row, handoffs, retro, build one thing |

**Call on Tuesday and Wednesday, not Monday.** By Tuesday the connection note and the first email have landed, so you're following up rather than cold calling. That's worth several points of connect rate and it costs nothing to wait a day.

---

## Day by day

### Monday · Build and launch
Contacts, dedupe, enrichment, dynamic fields written. Approved at 11am. Sequence loaded and live in the afternoon, dialer list ready for tomorrow. No cold calls today.

**Done when:** approved at 11am, sequence live, dialer loaded.

### Tuesday · First call day
The connection note landed yesterday and email one lands today, so every call you make is a follow-up rather than a cold open. Mention it: *"I sent you a note yesterday."*

**80 dials on this week's list**, split across two protected blocks, one early and one late. Partners answer before their day starts and after it ends. Nobody picks up mid morning, they're in court or with clients.

Last week's list gets its final email automatically. Nothing for you to do there beyond answering replies.

**Done when:** 80 dials logged, every reply answered inside the hour.

### Wednesday · The ask lands
**Stage three fires, the LinkedIn message carrying the ask.** This is the highest-yield touch in the whole sequence, so watch the inbox and reply fast.

**80 more dials**, second attempt on anyone who didn't pick up Tuesday, at a different hour.

**Done when:** 80 dials logged, every reply answered inside the hour.

### Thursday · Work the responses
**60 dials**, third attempt on the people worth three attempts, meaning the right title at a firm that fits the theme.

Thursday is usually your best booking day, because the LinkedIn ask went out yesterday and people are coming back to it.

**Done when:** 60 dials logged, no reply older than an hour.

### Friday · Close and build
Stages four and five fire automatically. **40 dials on last week's list**, which is the final attempt before it closes.

Then the housekeeping that makes next week work. Update the **sprint row**. Confirm **every booked demo is logged in HubSpot** with clean attribution, because your comp is paid from it. **Hand off** to the AE. **Write the retro**, three lines.

And **build one thing.** A Clay table, a Claude skill, a HubSpot view, a better sequence template. Something that makes next Monday faster, published so the team gets it free.

**Done when:** sprint row complete, every booking logged and handed off, retro posted, one thing shipped.

---

## What each firm actually receives

Across six working days, every firm on the list gets **three emails, a connection request, a LinkedIn message, a post like, and up to three call attempts.** Eight touches, all carrying the same argument.

**Never one and done.** Whether the follow-ups happen is the single biggest lever you control, and the sequence handles five of the eight for you. The three that are yours are the calls.

---

## Your daily scoreboard

Posted in `#sales-standup` at the end of every day. Ninety seconds.

> **Wed 12 Aug**
> Sequence live Mon · 100 in flight · 34 accepted · stage 3 fired today
> Dials 81 · Connects 8 · Conversations 5
> Booked 1 — Bermans, insurance defence, flat-rate carrier work, COO
> Blocked on: need Neil for ten minutes on Muckle's security questions

The blocker line matters more than the numbers. Raised Wednesday it gets solved Wednesday. Raised Friday it's just an explanation.

**Daily targets at full ramp:**

| | Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Assets approved | **11am** | — | — | — | — |
| Sequence live | **by 2pm** | — | — | — | — |
| Dials | — | 80 | 80 | 60 | 40 |
| Replies answered | all | all | all | all | all |

---

## Your weekly numbers

| Every week | Weeks 1–4 | Weeks 5–8 | Month 3+ |
|---|---|---|---|
| Firms on the list | 25 | 40 | 50 |
| Contacts in sequence | 50 | 80 | 100 |
| Connection accept rate | 25%+ | 30%+ | 30%+ |
| Dials | 150 | 220 | 260 |
| Connects | 12 | 18 | 22 |
| Real conversations | 6 | 10 | 13 |
| **Demos booked** | **1** | **1–2** | **2–3** |

**Read the funnel rather than the total.** Accepts red means the connection note is wrong. Accepts fine but replies red means the LinkedIn message is wrong, which is the touch carrying the ask. Dials green and connects red means the phone numbers are bad, so tell Harsh. Conversations green and bookings red means the pitch is wrong. Bookings green and held rate red means you're booking people who didn't understand what they agreed to. Five different problems, five different fixes.

> **Two numbers can be gamed and both matter more than volume.**
>
> **Held rate**, meaning booked demos that actually happen, should sit above 75%. Your comp only pays when the prospect shows, so this is your money as well as our signal.
>
> **Handoff acceptance**, meaning handoffs the AE takes without asking follow-up questions, should sit above 80%.
>
> Somebody chasing dials will quietly destroy both while the activity board looks excellent. If either goes red we stop looking at volume until it recovers.

---

## Friday: close the sprint

Update the row in **SDR Weekly Sprints** and post the retro in `#sales`.

> **Week of 11 Aug · Insurance defence, 20–150 attorneys**
> List 50 firms, 100 contacts · Accepted 34 · Replies 9 · Positive 5 · Demos 3
> **Worked:** the flat-fee angle. Four of five positive replies mentioned carrier rate pressure unprompted.
> **Didn't:** COO titles. Almost no accepts. Managing partners accepted at nearly double the rate.
> **Next:** same theme, managing partners only.

The retro is the part that compounds, and it feeds straight back into theme selection. One specific thing a week, written where the team can read it, is how a segment stops being one person's private knowledge.

---

## Where everything lives

One system owns each thing, and nothing gets recorded twice.

| System | Owns |
|---|---|
| **HubSpot** | Every contact, activity, booked demo and deal. The source of truth. Attribution has to be clean because comp is paid from it |
| **Amplemarket** | The whole sequence. Email and LinkedIn, automatic, six stages over six days |
| **Salesfinity** | The dialer and both call blocks |
| **Sales Navigator** | Picking people, stakeholder mapping |
| **Clay** | Enrichment and list building, with Harsh |
| **SDR Weekly Sprints** | One row per week. The brief, the numbers, the retro |
| **Booked Demos tracker** | The comp ledger. $200 per qualified demo that happens, plus 5% of deal value on close |
| **Slack** | Daily scoreboard in `#sales-standup`, retro in `#sales` |

---

## What's allowed to break the plan

Four things. Everything else waits for its slot.

| Trigger | What you do | How fast |
|---|---|---|
| **Inbound demo request** | Stop and call them | Same hour |
| **A positive reply, any channel** | Reply personally, offer two specific times | Within the hour |
| **A site visitor hitting pricing twice, in segment** | Add to today's dial list | Within 24 hours |
| **An AE asking about your handoff** | Answer now | Same day |

A firm that looked interesting, an idea for a new theme, a competitor's post. Write it down, put it in Monday, carry on with the block you're in.

---

## What your manager runs

Three fixed slots. None of them get cancelled.

- **Monday, 11am.** Review the theme, the list and the assets. Nothing sends before sign-off. This is the highest-leverage half hour in the week, because an unreviewed list burns fifty firms we can't get back.
- **Wednesday, 15 minutes.** Pace check. Off-pace gets said Wednesday while there's still time to act.
- **Friday, 45 minutes.** One to one against [Good SDR, Bad SDR](./good-sdr-bad-sdr.md), plus one recorded call listened to together with written feedback.

---

## Starting from a standing start

**Week one.** Take one theme with real evidence behind it, which right now is insurance defence and workers' compensation, and 25 firms. Run the week exactly as written. Log every day. Add nothing.

**Week two.** Build the second list while the first is finishing. This is the week it feels like too much and it isn't, because a list in its final days needs almost nothing from you.

**Week three.** You're at steady state. From here the only things that change are list size and which theme.

Don't run two themes at once in the first month. One theme, three weeks, then rotate.
