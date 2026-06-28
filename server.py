"""
August MCPs — Single FastMCP server exposing four services:
  • Amplemarket  (amplemarket_*) — sales outreach, enrichment, sequences, contacts
  • OrangeSlice  (orangeslice_*) — LinkedIn B2B DB, contact info, web search, Crunchbase, AI gen
  • Attio        (attio_*)       — full CRM: records, notes, tasks, lists, webhooks, SQL, meetings
  • August       (august_*)      — legal AI platform: projects, search, folders, files, Genius Mode queries

All tools are prefixed with their service name so any MCP client or LLM can
route to the right service without ambiguity.
"""
import os, json
from typing import Any, Optional, List
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("August MCPs", host="0.0.0.0")


# ===========================================================================
# AMPLEMARKET
# Base URL: https://api.amplemarket.com  |  Bearer token auth
# ===========================================================================

AM_BASE_URL = "https://api.amplemarket.com"
AM_API_KEY = os.environ.get("AMPLEMARKET_API_KEY", "amp_4b6c21fbe89749796e9d")

def _am_headers():
    if not AM_API_KEY:
        raise RuntimeError("AMPLEMARKET_API_KEY not set.")
    return {"Authorization": f"Bearer {AM_API_KEY}", "Content-Type": "application/json"}

def _am_get(path, params=None):
    r = httpx.get(f"{AM_BASE_URL}{path}", headers=_am_headers(), params=params, timeout=30)
    r.raise_for_status(); return r.json()

def _am_post(path, body=None):
    r = httpx.post(f"{AM_BASE_URL}{path}", headers=_am_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json()

def _am_patch(path, body=None):
    r = httpx.patch(f"{AM_BASE_URL}{path}", headers=_am_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json() if r.content else {"status": "ok"}

def _am_delete(path, body=None):
    r = httpx.delete(f"{AM_BASE_URL}{path}", headers=_am_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json() if r.content else {"status": "deleted"}


# ── Account ──────────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_get_account_info() -> str:
    """[Amplemarket] Get details about the current Amplemarket account."""
    return json.dumps(_am_get("/account"), indent=2)


# ── Contacts ─────────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_contacts(page_size: int = 20) -> str:
    """[Amplemarket] List contacts with pagination. page_size max 50."""
    return json.dumps(_am_get("/contacts", {"page[size]": page_size}), indent=2)

@mcp.tool()
def amplemarket_get_contacts(ids: List[str]) -> str:
    """[Amplemarket] Retrieve up to 20 contacts by their IDs."""
    params = [("ids[]", i) for i in ids]
    r = httpx.get(f"{AM_BASE_URL}/contacts", headers=_am_headers(), params=params, timeout=30)
    r.raise_for_status(); return json.dumps(r.json(), indent=2)

@mcp.tool()
def amplemarket_get_contact(contact_id: str) -> str:
    """[Amplemarket] Retrieve a single contact by ID."""
    return json.dumps(_am_get(f"/contacts/{contact_id}"), indent=2)

@mcp.tool()
def amplemarket_get_contact_by_email(email: str) -> str:
    """[Amplemarket] Retrieve a contact by email address."""
    return json.dumps(_am_get(f"/contacts/by_email/{email}"), indent=2)


# ── People search & enrichment ───────────────────────────────────────────────

@mcp.tool()
def amplemarket_search_people(
    person_name: Optional[str] = None,
    person_titles: Optional[List[str]] = None,
    person_seniorities: Optional[List[str]] = None,
    person_departments: Optional[List[str]] = None,
    person_locations: Optional[List[str]] = None,
    person_keywords: Optional[List[str]] = None,
    company_names: Optional[List[str]] = None,
    company_domains: Optional[List[str]] = None,
    company_industries: Optional[List[str]] = None,
    company_sizes: Optional[List[str]] = None,
    company_locations: Optional[List[str]] = None,
    company_types: Optional[List[str]] = None,
    company_focuses: Optional[List[str]] = None,
    company_revenue: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 10,
) -> str:
    """[Amplemarket] Search for people with filters: titles, seniority, company, location, industry, size, revenue."""
    body = {"page": page, "page_size": page_size}
    for k, v in [
        ("person_name", person_name), ("person_titles", person_titles),
        ("person_seniorities", person_seniorities), ("person_departments", person_departments),
        ("person_locations", person_locations), ("person_keywords", person_keywords),
        ("company_names", company_names), ("company_domains", company_domains),
        ("company_industries", company_industries), ("company_sizes", company_sizes),
        ("company_locations", company_locations), ("company_types", company_types),
        ("company_focuses", company_focuses), ("company_revenue", company_revenue),
    ]:
        if v: body[k] = v
    return json.dumps(_am_post("/people/search", body), indent=2)

@mcp.tool()
def amplemarket_find_person(
    email: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    name: Optional[str] = None,
    title: Optional[str] = None,
    company_name: Optional[str] = None,
    company_domain: Optional[str] = None,
    reveal_email: bool = False,
    reveal_phone_numbers: bool = False,
) -> str:
    """[Amplemarket] Look up and enrich a single person. At least one identifier required
    (email, linkedin_url, or name+company). reveal_email costs 1 email credit.
    reveal_phone_numbers costs 1 phone credit. Each lookup costs 0.5 credits (once per 24h)."""
    params: dict = {}
    if email: params["email"] = email
    if linkedin_url: params["linkedin_url"] = linkedin_url
    if name: params["name"] = name
    if title: params["title"] = title
    if company_name: params["company_name"] = company_name
    if company_domain: params["company_domain"] = company_domain
    if reveal_email: params["reveal_email"] = "true"
    if reveal_phone_numbers: params["reveal_phone_numbers"] = "true"
    return json.dumps(_am_get("/people/find", params), indent=2)

@mcp.tool()
def amplemarket_enrich_person(linkedin_url: Optional[str] = None, email: Optional[str] = None) -> str:
    """[Amplemarket] Enrich a single person via the enrichments endpoint."""
    body = {}
    if linkedin_url: body["linkedin_url"] = linkedin_url
    if email: body["email"] = email
    return json.dumps(_am_post("/people-enrichments/single", body), indent=2)

@mcp.tool()
def amplemarket_start_people_enrichment_batch(
    people: List[dict],
    reveal_email: bool = False,
    reveal_phone_numbers: bool = False,
) -> str:
    """[Amplemarket] Start a batch people enrichment (up to 100,000 entries).
    Each person dict can include: email, linkedin_url, name, title, company_name, company_domain."""
    body: dict = {"people": people}
    if reveal_email: body["reveal_email"] = True
    if reveal_phone_numbers: body["reveal_phone_numbers"] = True
    return json.dumps(_am_post("/people-enrichments", body), indent=2)

@mcp.tool()
def amplemarket_get_people_enrichment_results(enrichment_id: str) -> str:
    """[Amplemarket] Poll people enrichment batch results by ID."""
    return json.dumps(_am_get(f"/people-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def amplemarket_cancel_people_enrichment(enrichment_id: str) -> str:
    """[Amplemarket] Cancel a running people enrichment batch."""
    return json.dumps(_am_patch(f"/people/enrichment-requests/{enrichment_id}", {"status": "canceled"}), indent=2)


# ── Company search & enrichment ──────────────────────────────────────────────

@mcp.tool()
def amplemarket_search_companies(
    company_names: Optional[List[str]] = None,
    company_domains: Optional[List[str]] = None,
    company_industries: Optional[List[str]] = None,
    company_sizes: Optional[List[str]] = None,
    company_locations: Optional[List[str]] = None,
    company_types: Optional[List[str]] = None,
    company_focuses: Optional[List[str]] = None,
    company_revenue: Optional[List[str]] = None,
    company_keywords: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 10,
) -> str:
    """[Amplemarket] Search for companies with filters."""
    body = {"page": page, "page_size": page_size}
    for k, v in [
        ("company_names", company_names), ("company_domains", company_domains),
        ("company_industries", company_industries), ("company_sizes", company_sizes),
        ("company_locations", company_locations), ("company_types", company_types),
        ("company_focuses", company_focuses), ("company_revenue", company_revenue),
        ("company_keywords", company_keywords),
    ]:
        if v: body[k] = v
    return json.dumps(_am_post("/companies/search", body), indent=2)

@mcp.tool()
def amplemarket_find_company(
    linkedin_url: Optional[str] = None,
    domain: Optional[str] = None,
) -> str:
    """[Amplemarket] Look up and enrich a single company by LinkedIn URL or domain."""
    params: dict = {}
    if linkedin_url: params["linkedin_url"] = linkedin_url
    if domain: params["domain"] = domain
    return json.dumps(_am_get("/companies/find", params), indent=2)

@mcp.tool()
def amplemarket_enrich_company(linkedin_url: Optional[str] = None, domain: Optional[str] = None) -> str:
    """[Amplemarket] Enrich a single company via the enrichments endpoint."""
    body = {}
    if linkedin_url: body["linkedin_url"] = linkedin_url
    if domain: body["domain"] = domain
    return json.dumps(_am_post("/company-enrichments/single", body), indent=2)

@mcp.tool()
def amplemarket_start_company_enrichment_batch(
    companies: List[dict],
    reveal_email: bool = False,
    reveal_phone_numbers: bool = False,
) -> str:
    """[Amplemarket] Start a batch company enrichment (up to 10,000 entries).
    Each company dict can include: linkedin_url, domain, name."""
    body: dict = {"companies": companies}
    if reveal_email: body["reveal_email"] = True
    if reveal_phone_numbers: body["reveal_phone_numbers"] = True
    return json.dumps(_am_post("/company-enrichments", body), indent=2)

@mcp.tool()
def amplemarket_get_company_enrichment_results(enrichment_id: str) -> str:
    """[Amplemarket] Poll company enrichment batch results by ID."""
    return json.dumps(_am_get(f"/company-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def amplemarket_cancel_company_enrichment(enrichment_id: str) -> str:
    """[Amplemarket] Cancel a running company enrichment batch."""
    return json.dumps(_am_patch(f"/companies/enrichment-requests/{enrichment_id}", {"status": "canceled"}), indent=2)


# ── Sequences ────────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_sequences(
    status: Optional[str] = None,
    name: Optional[str] = None,
    created_by_user_id: Optional[str] = None,
    created_by_user_email: Optional[str] = None,
    page_size: int = 20,
) -> str:
    """[Amplemarket] List sequences. Filters: status (active/draft/paused), name, created_by_user_id/email."""
    params: dict = {"page[size]": page_size}
    if status: params["status"] = status
    if name: params["name"] = name
    if created_by_user_id: params["created_by_user_id"] = created_by_user_id
    if created_by_user_email: params["created_by_user_email"] = created_by_user_email
    return json.dumps(_am_get("/sequences", params), indent=2)

@mcp.tool()
def amplemarket_add_leads_to_sequence(
    sequence_id: str,
    leads: List[dict],
    mailboxes: Optional[List[str]] = None,
    leads_distribution: Optional[str] = None,
) -> str:
    """[Amplemarket] Add leads to a sequence (up to 250 per call). Each lead: {"email": "...", "data": {...}}."""
    body: dict = {"leads": leads}
    settings: dict = {}
    if mailboxes: settings["mailboxes"] = mailboxes
    if leads_distribution: settings["leads_distribution"] = leads_distribution
    if settings: body["settings"] = settings
    return json.dumps(_am_post(f"/sequences/{sequence_id}/leads", body), indent=2)

@mcp.tool()
def amplemarket_add_lead_to_sequence(
    sequence_id: str,
    email: str,
    fields: Optional[dict] = None,
    mailboxes: Optional[List[str]] = None,
    ignore_recently_contacted: bool = False,
    ignore_exclusion_list: bool = False,
    ignore_duplicate_in_other_active_sequences: bool = False,
) -> str:
    """[Amplemarket] Add a single lead to a sequence.
    fields: flat dict of dynamic variables e.g. {"first_name": "Jane", "company": "Acme"}.
    ignore_* overrides bypass normal skip rules."""
    lead: dict = {"email": email}
    if fields: lead["data"] = fields
    if ignore_recently_contacted or ignore_exclusion_list or ignore_duplicate_in_other_active_sequences:
        lead["overrides"] = {
            "ignore_recently_contacted": ignore_recently_contacted,
            "ignore_exclusion_list": ignore_exclusion_list,
            "ignore_duplicate_leads_in_other_active_sequences": ignore_duplicate_in_other_active_sequences,
        }
    body: dict = {"leads": [lead]}
    if mailboxes: body["settings"] = {"mailboxes": mailboxes}
    return json.dumps(_am_post(f"/sequences/{sequence_id}/leads", body), indent=2)

@mcp.tool()
def amplemarket_import_csv_to_sequence(
    sequence_id: str,
    csv_content: str,
    email_column: str = "email",
    mailboxes: Optional[List[str]] = None,
    leads_distribution: Optional[str] = None,
) -> str:
    """[Amplemarket] Import leads from raw CSV text into a sequence.
    csv_content: full CSV text including header row. email_column: column with email addresses.
    All other columns are passed as sequence dynamic fields. Handles batching automatically."""
    import csv, io
    reader = csv.DictReader(io.StringIO(csv_content.strip()))
    leads = []
    for row in reader:
        email = row.get(email_column, "").strip()
        if not email: continue
        data = {k: v.strip() for k, v in row.items() if k != email_column and v and v.strip()}
        lead: dict = {"email": email}
        if data: lead["data"] = data
        leads.append(lead)
    if not leads:
        return json.dumps({"error": f"No leads found. Check email_column='{email_column}'."})
    settings: dict = {}
    if mailboxes: settings["mailboxes"] = mailboxes
    if leads_distribution: settings["leads_distribution"] = leads_distribution
    results = []
    for i in range(0, len(leads), 20):
        batch = leads[i:i + 20]
        body: dict = {"leads": batch}
        if settings: body["settings"] = settings
        result = _am_post(f"/sequences/{sequence_id}/leads", body)
        results.append({"batch": i // 20 + 1, "sent": len(batch), **result})
    total_added = sum(r.get("total_added_to_sequence", 0) for r in results)
    skipped = sum(
        len(r.get("in_exclusion_list_and_skipped", [])) +
        len(r.get("recently_contacted_and_skipped", [])) +
        len(r.get("already_in_sequence_and_skipped", [])) +
        len(r.get("in_other_active_sequences_and_skipped", []))
        for r in results
    )
    return json.dumps({
        "total_leads_in_csv": len(leads),
        "total_added_to_sequence": total_added,
        "total_skipped": skipped,
        "batches": results,
    }, indent=2)


# ── Tasks (Amplemarket) ──────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_tasks(
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    page: int = 1,
) -> str:
    """[Amplemarket] List tasks. Use amplemarket_list_task_statuses / amplemarket_list_task_types for valid filter values."""
    params: dict = {"page": page}
    if status: params["status"] = status
    if task_type: params["task_type"] = task_type
    return json.dumps(_am_get("/tasks", params), indent=2)

@mcp.tool()
def amplemarket_list_task_statuses() -> str:
    """[Amplemarket] List all valid task status values."""
    return json.dumps(_am_get("/tasks/statuses"), indent=2)

@mcp.tool()
def amplemarket_list_task_types() -> str:
    """[Amplemarket] List all task types."""
    return json.dumps(_am_get("/tasks/types"), indent=2)

@mcp.tool()
def amplemarket_complete_task(task_id: str, set_lead_to_completed: bool = False) -> str:
    """[Amplemarket] Mark a task as completed. set_lead_to_completed also marks the linked lead."""
    body: dict = {}
    if set_lead_to_completed: body["set_lead_to_completed"] = True
    return json.dumps(_am_post(f"/tasks/{task_id}/complete", body), indent=2)

@mcp.tool()
def amplemarket_skip_task(task_id: str) -> str:
    """[Amplemarket] Skip a task."""
    return json.dumps(_am_post(f"/tasks/{task_id}/skip"), indent=2)


# ── Lead Lists ───────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_lead_lists() -> str:
    """[Amplemarket] List all lead lists."""
    return json.dumps(_am_get("/lead-lists"), indent=2)

@mcp.tool()
def amplemarket_get_lead_list(lead_list_id: str) -> str:
    """[Amplemarket] Retrieve a specific lead list and poll its processing status."""
    return json.dumps(_am_get(f"/lead-lists/{lead_list_id}"), indent=2)

@mcp.tool()
def amplemarket_create_lead_list(
    name: str,
    owner: str,
    shared: bool,
    list_type: str,
    leads: List[dict],
    reveal_phone_numbers: bool = False,
    validate_email: bool = False,
    enrich: bool = False,
    visible: bool = True,
) -> str:
    """[Amplemarket] Create a new lead list.
    owner: email of the Amplemarket user who will own it.
    shared: True = account-wide, False = user-specific.
    list_type: 'linkedin', 'email', or 'titles_and_company'."""
    body: dict = {
        "name": name, "owner": owner, "shared": shared, "type": list_type,
        "leads": leads, "visible": visible,
        "options": {"reveal_phone_numbers": reveal_phone_numbers, "validate_email": validate_email, "enrich": enrich},
    }
    return json.dumps(_am_post("/lead-lists", body), indent=2)

@mcp.tool()
def amplemarket_add_leads_to_list(lead_list_id: str, leads: List[dict]) -> str:
    """[Amplemarket] Add leads to an existing lead list (max 10,000 per request)."""
    return json.dumps(_am_post(f"/lead-lists/{lead_list_id}/leads", {"leads": leads}), indent=2)


# ── Email Validations ────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_start_email_validation(emails: List[str]) -> str:
    """[Amplemarket] Start a batch email validation job (max 100,000 emails; costs 1 credit each)."""
    return json.dumps(_am_post("/email-validations", {"emails": emails}), indent=2)

@mcp.tool()
def amplemarket_get_email_validation_results(validation_id: str, page_size: int = 20) -> str:
    """[Amplemarket] Get email validation results. Status: queued, processing, completed, canceled, error."""
    return json.dumps(_am_get(f"/email-validations/{validation_id}", {"page[size]": page_size}), indent=2)

@mcp.tool()
def amplemarket_cancel_email_validation(validation_id: str) -> str:
    """[Amplemarket] Cancel a running email validation job."""
    return json.dumps(_am_patch(f"/email-validations/{validation_id}", {"status": "canceled"}), indent=2)


# ── Calls ────────────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_calls(
    page_size: int = 20,
    page_after: Optional[str] = None,
    user_id: Optional[str] = None,
    from_number: Optional[str] = None,
    to_number: Optional[str] = None,
    start_date_from: Optional[str] = None,
    start_date_to: Optional[str] = None,
) -> str:
    """[Amplemarket] List logged calls. Uses cursor pagination — pass page_after from _links.next."""
    params: dict = {"page[size]": page_size}
    if page_after: params["page[after]"] = page_after
    if user_id: params["user_id"] = user_id
    if from_number: params["from"] = from_number
    if to_number: params["to"] = to_number
    if start_date_from: params["start_date_from"] = start_date_from
    if start_date_to: params["start_date_to"] = start_date_to
    return json.dumps(_am_get("/calls", params), indent=2)

@mcp.tool()
def amplemarket_log_call(
    from_number: str,
    to_number: str,
    duration: int,
    answered: bool,
    human: bool,
    task_id: str,
    user_id: str,
    transcription: Optional[str] = None,
    recording_url: Optional[str] = None,
    disposition_id: Optional[str] = None,
) -> str:
    """[Amplemarket] Log an external call (made outside Amplemarket's dialer).
    from_number/to_number: E.164. duration: seconds. disposition_id from amplemarket_list_call_dispositions."""
    body: dict = {
        "from": from_number, "to": to_number, "duration": duration,
        "answered": answered, "human": human, "task_id": task_id, "user_id": user_id,
    }
    if transcription: body["transcription"] = transcription
    if recording_url: body["recording_url"] = recording_url
    if disposition_id: body["disposition_id"] = disposition_id
    return json.dumps(_am_post("/calls", body), indent=2)

@mcp.tool()
def amplemarket_list_call_dispositions() -> str:
    """[Amplemarket] List all available call disposition options."""
    return json.dumps(_am_get("/calls/dispositions"), indent=2)

@mcp.tool()
def amplemarket_get_call_recording(call_id: str) -> str:
    """[Amplemarket] Get call recording URL for a specific call."""
    return json.dumps(_am_get(f"/calls/{call_id}/recording"), indent=2)


# ── Exclusion Lists ──────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_excluded_emails(page: int = 1) -> str:
    """[Amplemarket] List all excluded email addresses."""
    return json.dumps(_am_get("/exclusion-lists/emails", {"page": page}), indent=2)

@mcp.tool()
def amplemarket_create_email_exclusions(emails: List[str]) -> str:
    """[Amplemarket] Add email addresses to the exclusion list."""
    return json.dumps(_am_post("/exclusion-lists/emails", {"emails": emails}), indent=2)

@mcp.tool()
def amplemarket_delete_email_exclusions(emails: List[str]) -> str:
    """[Amplemarket] Remove email addresses from the exclusion list."""
    return json.dumps(_am_delete("/exclusion-lists/emails", {"emails": emails}), indent=2)

@mcp.tool()
def amplemarket_list_excluded_domains(page: int = 1) -> str:
    """[Amplemarket] List all excluded domains."""
    return json.dumps(_am_get("/exclusion-lists/domains", {"page": page}), indent=2)

@mcp.tool()
def amplemarket_create_domain_exclusions(domains: List[str]) -> str:
    """[Amplemarket] Add domains to the exclusion list."""
    return json.dumps(_am_post("/exclusion-lists/domains", {"domains": domains}), indent=2)

@mcp.tool()
def amplemarket_delete_domain_exclusions(domains: List[str]) -> str:
    """[Amplemarket] Remove domains from the exclusion list."""
    return json.dumps(_am_delete("/exclusion-lists/domains", {"domains": domains}), indent=2)


# ── Mailboxes ─────────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_mailboxes(
    status: Optional[str] = None,
    email_provider: Optional[str] = None,
    user_email: Optional[str] = None,
    page_size: int = 20,
) -> str:
    """[Amplemarket] List mailboxes. status: 'active'|'inactive'|'needs_reconnection'.
    email_provider: 'google'|'outlook'|'other'|'other_mixed'."""
    params: dict = {"page[size]": page_size}
    if status: params["status"] = status
    if email_provider: params["email_provider"] = email_provider
    if user_email: params["user_email"] = user_email
    return json.dumps(_am_get("/mailboxes", params), indent=2)

@mcp.tool()
def amplemarket_update_mailbox_daily_limit(mailbox_id: str, daily_limit: int) -> str:
    """[Amplemarket] Update a mailbox's daily email sending limit."""
    return json.dumps(_am_patch(f"/mailboxes/{mailbox_id}", {"daily_limit": daily_limit}), indent=2)


# ── Users ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_users(
    status: Optional[str] = None,
    role: Optional[str] = None,
    email: Optional[str] = None,
    page_size: int = 20,
) -> str:
    """[Amplemarket] List team members/users. status, role, email filters available."""
    params: dict = {"page[size]": page_size}
    if status: params["status"] = status
    if role: params["role"] = role
    if email: params["email"] = email
    return json.dumps(_am_get("/users", params), indent=2)


# ── CRM Accounts ─────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_accounts(
    page: int = 1,
    name: Optional[str] = None,
    domain: Optional[str] = None,
    owner_email: Optional[str] = None,
    tags: Optional[List[str]] = None,
    page_size: int = 10,
) -> str:
    """[Amplemarket] List CRM accounts. Filters: name (partial), domain (exact), owner_email, tags."""
    params: dict = {"page": page, "page[size]": page_size}
    if name: params["name"] = name
    if domain: params["domain"] = domain
    if owner_email: params["owner_email"] = owner_email
    if tags:
        for tag in tags: params.setdefault("tags[]", []).append(tag)
    return json.dumps(_am_get("/accounts", params), indent=2)

@mcp.tool()
def amplemarket_get_crm_account(account_id: str) -> str:
    """[Amplemarket] Retrieve a specific CRM account by ID."""
    return json.dumps(_am_get(f"/accounts/{account_id}"), indent=2)


# ── Job Openings ──────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_list_job_openings(
    company_id: Optional[str] = None,
    domain: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    person_seniorities: Optional[List[str]] = None,
    person_departments: Optional[List[str]] = None,
    person_job_functions: Optional[List[str]] = None,
    only_remote: bool = False,
    page_size: int = 10,
) -> str:
    """[Amplemarket] List job openings for a company. At least one of company_id, domain, or linkedin_url required."""
    params: dict = {"page[size]": page_size}
    if company_id: params["company_id"] = company_id
    if domain: params["domain"] = domain
    if linkedin_url: params["linkedin_url"] = linkedin_url
    if person_seniorities:
        for s in person_seniorities: params.setdefault("person_seniorities[]", []).append(s)
    if person_departments:
        for d in person_departments: params.setdefault("person_departments[]", []).append(d)
    if person_job_functions:
        for f in person_job_functions: params.setdefault("person_job_functions[]", []).append(f)
    if only_remote: params["only_remote"] = "true"
    return json.dumps(_am_get("/job-openings", params), indent=2)

@mcp.tool()
def amplemarket_get_job_opening(job_opening_id: str) -> str:
    """[Amplemarket] Retrieve a specific job opening by ID."""
    return json.dumps(_am_get(f"/job-openings/{job_opening_id}"), indent=2)


# ── Phone Numbers ─────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_flag_phone_number(phone_number_id: str, user_id: str) -> str:
    """[Amplemarket] Flag a phone number as wrong/incorrect for review."""
    return json.dumps(_am_post(f"/phone_numbers/{phone_number_id}/review", {
        "user_id": user_id, "reason": "wrong_number",
    }), indent=2)


# ── Custom Signals ────────────────────────────────────────────────────────────

@mcp.tool()
def amplemarket_create_custom_signal_entry(token: str, data: dict) -> str:
    """[Amplemarket] Submit a custom signal entry to Duo Copilot via webhook.
    token: your custom signal token. data: the signal payload."""
    return json.dumps(_am_post(f"/custom_signals/{token}/entries", data), indent=2)


# ===========================================================================
# ORANGESLICE
# OrangeSlice is accessed via a Node.js sidecar on port 8002 that uses the
# official `orangeslice` npm package. Tools proxy JSON-RPC calls to the sidecar.
# ===========================================================================

OS_MCP_URL = "http://localhost:8002/mcp"
_os_session_id: Optional[str] = None

def _os_get_session() -> str:
    """Initialize a session with the OrangeSlice sidecar and cache the session ID."""
    global _os_session_id
    if _os_session_id:
        return _os_session_id
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    r = httpx.post(OS_MCP_URL, json={
        "jsonrpc": "2.0", "id": 0, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "august-proxy", "version": "1"}}
    }, headers=headers, timeout=15)
    r.raise_for_status()
    _os_session_id = r.headers.get("mcp-session-id", "")
    return _os_session_id

def _os_call(tool_name: str, arguments: dict) -> str:
    """Call a tool on the local OrangeSlice MCP sidecar and return its text result."""
    clean_args = {k: v for k, v in arguments.items() if v is not None}
    session_id = _os_get_session()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id,
    }
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": tool_name, "arguments": clean_args},
    }
    r = httpx.post(OS_MCP_URL, json=payload, headers=headers, timeout=120)
    r.raise_for_status()
    for line in r.text.splitlines():
        if line.startswith("data:"):
            body = json.loads(line[5:].strip())
            if "result" in body:
                content = body["result"].get("content", [])
                return content[0]["text"] if content else json.dumps(body["result"])
            if "error" in body:
                return f"Error: {body['error']}"
    return r.text


@mcp.tool()
def orangeslice_enrich_person(linkedin_url: Optional[str] = None, username: Optional[str] = None, extended: bool = False) -> str:
    """[OrangeSlice] Enrich a person from the LinkedIn B2B database by LinkedIn URL or username.
    Returns name, title, company, headline, location, skills, and more. Credits: 1."""
    return _os_call("enrich_person", {"url": linkedin_url, "username": username, "extended": extended})

@mcp.tool()
def orangeslice_enrich_company(domain: Optional[str] = None, linkedin_slug: Optional[str] = None, linkedin_url: Optional[str] = None, extended: bool = False) -> str:
    """[OrangeSlice] Enrich a company from the LinkedIn B2B database by domain, LinkedIn slug, or URL.
    Returns name, description, industry, employee count, website, location. Credits: 1."""
    return _os_call("enrich_company", {"domain": domain, "shorthand": linkedin_slug, "url": linkedin_url, "extended": extended})

@mcp.tool()
def orangeslice_search_linkedin_people(sql: str) -> str:
    """[OrangeSlice] Run SQL against the LinkedIn B2B people database (lkd_profile table).
    Use for indexed lookups: person by slug, employees at a company, title/location filters.
    Always include LIMIT. Credits: 1/row.
    Example: SELECT * FROM lkd_profile WHERE company_slug = 'microsoft' LIMIT 25"""
    return _os_call("search_people_linkedin", {"sql": sql})

@mcp.tool()
def orangeslice_search_linkedin_companies(sql: str) -> str:
    """[OrangeSlice] Run SQL against the LinkedIn B2B company database (lkd_company table).
    Use for lookups by domain, slug, industry_code, country_code, employee_count.
    Always include LIMIT. Credits: 1/row.
    Example: SELECT * FROM lkd_company WHERE domain = 'stripe.com' LIMIT 5"""
    return _os_call("search_companies_linkedin", {"sql": sql})

@mcp.tool()
def orangeslice_find_person_linkedin_url(
    name: Optional[str] = None,
    title: Optional[str] = None,
    company: Optional[str] = None,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    email: Optional[str] = None,
) -> str:
    """[OrangeSlice] Find a person's LinkedIn profile URL by name, company, title, or email.
    Credits: 2 (name search) or 50 (reverse email lookup)."""
    return _os_call("find_person_linkedin_url", {k: v for k, v in {
        "name": name, "title": title, "company": company,
        "keyword": keyword, "location": location, "email": email,
    }.items() if v is not None})

@mcp.tool()
def orangeslice_get_contact_info(
    required: List[str],
    linkedin_url: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    company: Optional[str] = None,
    domain: Optional[str] = None,
) -> str:
    """[OrangeSlice] Get verified email and/or phone for a person. Can take up to 10 minutes.
    required: list of 'email', 'phone', and/or 'work_email'.
    Credits: up to 275 (email+phone), 250 (phone only), 25 (email only)."""
    return _os_call("get_contact_info", {k: v for k, v in {
        "required": required, "linkedinUrl": linkedin_url,
        "firstName": first_name, "lastName": last_name,
        "company": company, "domain": domain,
    }.items() if v is not None})

@mcp.tool()
def orangeslice_get_company_employees(
    company_slug: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    search_strategy: str = "database",
    title_variations: Optional[List[str]] = None,
    title_sql_filter: Optional[str] = None,
    limit: int = 25,
    us_only: bool = True,
    min_connections: int = 20,
    offset: int = 0,
) -> str:
    """[OrangeSlice] Find employees at a company using LinkedIn data.
    search_strategy: 'database' (IC/Director, fast) or 'web' (C-Suite/Founders, max 3 title_variations).
    Credits: 1/result."""
    return _os_call("get_company_employees", {k: v for k, v in {
        "companySlug": company_slug, "linkedinUrl": linkedin_url,
        "searchStrategy": search_strategy, "titleVariations": title_variations,
        "titleSqlFilter": title_sql_filter, "limit": limit,
        "usOnly": us_only, "minConnections": min_connections, "offset": offset,
    }.items() if v is not None})

@mcp.tool()
def orangeslice_get_company_revenue(domain: str) -> str:
    """[OrangeSlice] Get company revenue, employee count, HQ, industry, and funding from a domain.
    Credits: 2."""
    return _os_call("get_company_revenue", {"domain": domain})

@mcp.tool()
def orangeslice_web_search(
    query: str,
    domain: Optional[str] = None,
    page: int = 1,
    time_filter: Optional[str] = None,
) -> str:
    """[OrangeSlice] Search Google SERP. Best for prospecting and discovery.
    Supports site:, "exact phrase", OR, -exclude operators.
    time_filter: qdr:h (hour), qdr:d (day), qdr:w (week), qdr:m (month), qdr:y (year).
    Credits: 1."""
    return _os_call("web_search", {k: v for k, v in {
        "query": query, "domain": domain, "page": page, "tbs": time_filter,
    }.items() if v is not None})

@mcp.tool()
def orangeslice_scrape_website(url: str, format: str = "markdown") -> str:
    """[OrangeSlice] Scrape a website URL and return its content.
    format: 'markdown' (default), 'text', or 'html'. Credits: 1."""
    return _os_call("scrape_website", {"url": url, "format": format})

@mcp.tool()
def orangeslice_search_crunchbase(sql: str) -> str:
    """[OrangeSlice] Run SQL against the Crunchbase startup database (public.crunchbase_scraper_lean).
    Filter by operating_status, funding_total_usd, last_funding_type, founded_on, country_code.
    Must include LIMIT (max 100). Credits: 1/row."""
    return _os_call("search_crunchbase", {"sql": sql})

@mcp.tool()
def orangeslice_ai_generate_object(prompt: str, schema: dict) -> str:
    """[OrangeSlice] Use AI to extract or classify data into a structured JSON object.
    prompt: instruction and input text. schema: JSON Schema describing the output structure."""
    return _os_call("ai_generate_object", {"prompt": prompt, "schema": schema})

@mcp.tool()
def orangeslice_google_maps_search(query: str, location: Optional[str] = None, limit: int = 20) -> str:
    """[OrangeSlice] Search businesses via Google Maps. Returns name, address, phone, website, rating.
    Credits: 1."""
    return _os_call("search_google_maps", {k: v for k, v in {
        "query": query, "location": location, "limit": limit,
    }.items() if v is not None})


# ===========================================================================
# ATTIO
# Base URL: https://api.attio.com/v2  |  Bearer token auth
# Full CRM: records, notes, tasks, lists, webhooks, SQL, meetings, and more.
# ===========================================================================

ATTIO_BASE_URL = "https://api.attio.com/v2"
ATTIO_API_KEY = os.environ.get("ATTIO_API_KEY", "a46ef67f2b875c2bd713f5e88b1c71cf9c59fba9a8eac1e9a5169f329d559b40")

def _at_headers() -> dict:
    return {"Authorization": f"Bearer {ATTIO_API_KEY}", "Content-Type": "application/json"}

def _at_get(path: str, params: dict | None = None) -> dict:
    r = httpx.get(ATTIO_BASE_URL + path, headers=_at_headers(), params=params or {}, timeout=30)
    r.raise_for_status(); return r.json()

def _at_post(path: str, body: dict | None = None) -> dict:
    r = httpx.post(ATTIO_BASE_URL + path, headers=_at_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json()

def _at_put(path: str, body: dict | None = None) -> dict:
    r = httpx.put(ATTIO_BASE_URL + path, headers=_at_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json()

def _at_patch(path: str, body: dict | None = None) -> dict:
    r = httpx.patch(ATTIO_BASE_URL + path, headers=_at_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json()

def _at_delete(path: str) -> dict:
    r = httpx.delete(ATTIO_BASE_URL + path, headers=_at_headers(), timeout=30)
    if r.status_code == 204: return {"success": True}
    r.raise_for_status(); return r.json()


# ── Workspace ─────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_get_self() -> str:
    """[Attio] Return information about the current authenticated workspace and user."""
    return json.dumps(_at_get("/self"), indent=2)

@mcp.tool()
def attio_list_workspace_members() -> str:
    """[Attio] List all members of the Attio workspace."""
    return json.dumps(_at_get("/workspace_members"), indent=2)

@mcp.tool()
def attio_get_workspace_member(member_id: str) -> str:
    """[Attio] Get a specific workspace member by ID (UUID)."""
    return json.dumps(_at_get(f"/workspace_members/{member_id}"), indent=2)


# ── Object schema ──────────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_objects() -> str:
    """[Attio] List all object types (people, companies, deals, custom objects) in the workspace."""
    return json.dumps(_at_get("/objects"), indent=2)

@mcp.tool()
def attio_get_object(object_slug: str) -> str:
    """[Attio] Get the schema for a specific object type.
    object_slug: e.g. 'people', 'companies', 'deals', or a custom slug."""
    return json.dumps(_at_get(f"/objects/{object_slug}"), indent=2)

@mcp.tool()
def attio_list_attributes(object_slug: str) -> str:
    """[Attio] List all attributes defined on an object type.
    object_slug: e.g. 'people', 'companies', 'deals'."""
    return json.dumps(_at_get(f"/objects/{object_slug}/attributes"), indent=2)

@mcp.tool()
def attio_get_attribute(object_slug: str, attribute_slug: str) -> str:
    """[Attio] Get a specific attribute definition on an object type."""
    return json.dumps(_at_get(f"/objects/{object_slug}/attributes/{attribute_slug}"), indent=2)

@mcp.tool()
def attio_list_statuses(object_slug: str, attribute_slug: str) -> str:
    """[Attio] List allowed statuses for a status-type attribute (e.g. deals stage)."""
    return json.dumps(_at_get(f"/objects/{object_slug}/attributes/{attribute_slug}/statuses"), indent=2)

@mcp.tool()
def attio_list_select_options(object_slug: str, attribute_slug: str) -> str:
    """[Attio] List allowed options for a select or multi-select attribute."""
    return json.dumps(_at_get(f"/objects/{object_slug}/attributes/{attribute_slug}/options"), indent=2)


# ── Records ────────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_query_records(
    object_slug: str,
    filter_by: Optional[dict] = None,
    sorts: Optional[list] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """[Attio] Query records for any object type with optional filtering and sorting.
    object_slug: e.g. 'people', 'companies', 'deals'.
    filter_by examples:
      {"name": {"$contains": "Acme"}}
      {"email_addresses": {"email_address": {"$eq": "john@example.com"}}}
      {"domains": {"domain": {"$eq": "acme.com"}}}
    Operators: $eq, $not_eq, $contains, $gt, $gte, $lt, $lte, $is_empty, $not_empty.
    sorts: [{"attribute": "name", "direction": "asc"}]
    limit: max 500."""
    body: dict[str, Any] = {"limit": limit, "offset": offset}
    if filter_by: body["filter"] = filter_by
    if sorts: body["sorts"] = sorts
    return json.dumps(_at_post(f"/objects/{object_slug}/records/query", body), indent=2)

@mcp.tool()
def attio_get_record(object_slug: str, record_id: str) -> str:
    """[Attio] Get a single record by ID.
    object_slug: e.g. 'people', 'companies', 'deals'. record_id: UUID."""
    return json.dumps(_at_get(f"/objects/{object_slug}/records/{record_id}"), indent=2)

@mcp.tool()
def attio_create_record(object_slug: str, values: dict) -> str:
    """[Attio] Create a new record with raw attribute values.
    values: dict where each key is an attribute slug and value is a list of value objects.
    Example for person: {"name": [{"first_name": "Jane", "last_name": "Doe", "full_name": "Jane Doe"}],
                         "email_addresses": [{"email_address": "jane@example.com"}]}
    Example for company: {"name": [{"value": "Acme"}], "domains": [{"domain": "acme.com"}]}"""
    return json.dumps(_at_post(f"/objects/{object_slug}/records", {"data": {"values": values}}), indent=2)

@mcp.tool()
def attio_update_record(object_slug: str, record_id: str, values: dict) -> str:
    """[Attio] Update attribute values on an existing record (PATCH — partial update).
    values: same format as attio_create_record values."""
    return json.dumps(_at_patch(f"/objects/{object_slug}/records/{record_id}", {"data": {"values": values}}), indent=2)

@mcp.tool()
def attio_overwrite_record(object_slug: str, record_id: str, values: dict) -> str:
    """[Attio] Overwrite attribute values on a record (PUT — replaces multi-select values entirely).
    Use attio_update_record (PATCH) to append to multi-selects instead."""
    return json.dumps(_at_put(f"/objects/{object_slug}/records/{record_id}", {"data": {"values": values}}), indent=2)

@mcp.tool()
def attio_upsert_record(object_slug: str, matching_attribute: str, values: dict) -> str:
    """[Attio] Create or update a record matched by a unique attribute.
    matching_attribute: e.g. 'email_addresses' for people, 'domains' for companies.
    values: same format as attio_create_record values."""
    return json.dumps(_at_put(f"/objects/{object_slug}/records", {
        "data": {"matching_attribute": matching_attribute, "values": values}
    }), indent=2)

@mcp.tool()
def attio_delete_record(object_slug: str, record_id: str) -> str:
    """[Attio] Permanently delete a record."""
    return json.dumps(_at_delete(f"/objects/{object_slug}/records/{record_id}"), indent=2)

@mcp.tool()
def attio_get_record_list_entries(object_slug: str, record_id: str) -> str:
    """[Attio] Get all list memberships (entries) for a specific record.
    Useful for finding which lists a person or company belongs to."""
    return json.dumps(_at_get(f"/objects/{object_slug}/records/{record_id}/entries"), indent=2)


# ── Attribute values ──────────────────────────────────────────────────────────

@mcp.tool()
def attio_get_attribute_values(object_slug: str, record_id: str, attribute_slug: str) -> str:
    """[Attio] Get all values for a specific attribute on a record.
    attribute_slug: e.g. 'email_addresses', 'phone_numbers', 'name'."""
    return json.dumps(_at_get(
        f"/objects/{object_slug}/records/{record_id}/attributes/{attribute_slug}/values"
    ), indent=2)

@mcp.tool()
def attio_set_attribute_values(object_slug: str, record_id: str, attribute_slug: str, values: list) -> str:
    """[Attio] Replace all values for a specific attribute on a record.
    values: array of value objects, e.g. [{"email_address": "new@example.com"}] for email."""
    return json.dumps(_at_put(
        f"/objects/{object_slug}/records/{record_id}/attributes/{attribute_slug}/values",
        {"data": values}
    ), indent=2)

@mcp.tool()
def attio_delete_attribute_value(object_slug: str, record_id: str, attribute_slug: str, value_id: str) -> str:
    """[Attio] Delete a specific value instance for an attribute on a record.
    value_id: the value UUID returned in attribute value listings."""
    return json.dumps(_at_delete(
        f"/objects/{object_slug}/records/{record_id}/attributes/{attribute_slug}/values/{value_id}"
    ), indent=2)


# ── Convenience: people & companies ──────────────────────────────────────────

@mcp.tool()
def attio_search_people(query: str, limit: int = 20) -> str:
    """[Attio] Search Attio people records by name (partial match)."""
    try:
        return json.dumps(_at_post("/objects/people/records/query", {
            "filter": {"name": {"$contains": query}}, "limit": limit, "offset": 0,
        }), indent=2)
    except httpx.HTTPStatusError:
        return json.dumps(_at_post("/objects/people/records/query", {"limit": limit, "offset": 0}), indent=2)

@mcp.tool()
def attio_search_companies(query: str, limit: int = 20) -> str:
    """[Attio] Search Attio company records by name (partial match)."""
    try:
        return json.dumps(_at_post("/objects/companies/records/query", {
            "filter": {"name": {"$contains": query}}, "limit": limit, "offset": 0,
        }), indent=2)
    except httpx.HTTPStatusError:
        return json.dumps(_at_post("/objects/companies/records/query", {"limit": limit, "offset": 0}), indent=2)

@mcp.tool()
def attio_find_person_by_email(email: str) -> str:
    """[Attio] Look up an Attio person record by exact email address."""
    return json.dumps(_at_post("/objects/people/records/query", {
        "filter": {"email_addresses": {"email_address": {"$eq": email}}},
        "limit": 5, "offset": 0,
    }), indent=2)

@mcp.tool()
def attio_find_company_by_domain(domain: str) -> str:
    """[Attio] Look up an Attio company record by website domain (e.g. 'acme.com')."""
    return json.dumps(_at_post("/objects/companies/records/query", {
        "filter": {"domains": {"domain": {"$eq": domain}}},
        "limit": 5, "offset": 0,
    }), indent=2)

@mcp.tool()
def attio_create_person(
    first_name: str,
    last_name: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    company_id: Optional[str] = None,
    job_title: Optional[str] = None,
    linkedin_url: Optional[str] = None,
) -> str:
    """[Attio] Create a person record in Attio with common fields."""
    values: dict[str, Any] = {
        "name": [{"first_name": first_name, "last_name": last_name, "full_name": f"{first_name} {last_name}"}],
    }
    if email: values["email_addresses"] = [{"email_address": email}]
    if phone: values["phone_numbers"] = [{"phone_number": phone}]
    if company_id: values["company"] = [{"target_object": "companies", "target_record_id": company_id}]
    if job_title: values["job_title"] = [{"value": job_title}]
    if linkedin_url: values["linkedin"] = [{"value": linkedin_url}]
    return json.dumps(_at_post("/objects/people/records", {"data": {"values": values}}), indent=2)

@mcp.tool()
def attio_create_company(
    name: str,
    domain: Optional[str] = None,
    description: Optional[str] = None,
    linkedin_url: Optional[str] = None,
) -> str:
    """[Attio] Create a company record in Attio with common fields."""
    values: dict[str, Any] = {"name": [{"value": name}]}
    if domain: values["domains"] = [{"domain": domain}]
    if description: values["description"] = [{"value": description}]
    if linkedin_url: values["linkedin"] = [{"value": linkedin_url}]
    return json.dumps(_at_post("/objects/companies/records", {"data": {"values": values}}), indent=2)

@mcp.tool()
def attio_list_deals(limit: int = 20, offset: int = 0) -> str:
    """[Attio] List deal records in Attio."""
    return json.dumps(_at_post("/objects/deals/records/query", {"limit": limit, "offset": offset}), indent=2)


# ── Notes ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_notes(
    record_id: Optional[str] = None,
    object_slug: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """[Attio] List notes, optionally filtered to a specific record.
    Provide both record_id and object_slug to filter (e.g. record_id=uuid, object_slug='people')."""
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if record_id and object_slug:
        params["parent_object"] = object_slug
        params["parent_record_id"] = record_id
    return json.dumps(_at_get("/notes", params), indent=2)

@mcp.tool()
def attio_get_note(note_id: str) -> str:
    """[Attio] Get a specific note by ID (UUID)."""
    return json.dumps(_at_get(f"/notes/{note_id}"), indent=2)

@mcp.tool()
def attio_create_note(
    object_slug: str,
    record_id: str,
    title: str,
    content: str,
    format: str = "plaintext",
    created_at: Optional[str] = None,
) -> str:
    """[Attio] Create a note on a record.
    object_slug: e.g. 'people', 'companies'. format: 'plaintext' or 'markdown'.
    created_at: ISO 8601 timestamp (defaults to now)."""
    body: dict[str, Any] = {"data": {
        "parent_object": object_slug, "parent_record_id": record_id,
        "title": title, "content": content, "format": format,
    }}
    if created_at: body["data"]["created_at"] = created_at
    return json.dumps(_at_post("/notes", body), indent=2)

@mcp.tool()
def attio_update_note(note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> str:
    """[Attio] Update a note's title or content."""
    data: dict[str, Any] = {}
    if title is not None: data["title"] = title
    if content is not None: data["content"] = content
    return json.dumps(_at_patch(f"/notes/{note_id}", {"data": data}), indent=2)

@mcp.tool()
def attio_delete_note(note_id: str) -> str:
    """[Attio] Delete a note by ID."""
    return json.dumps(_at_delete(f"/notes/{note_id}"), indent=2)


# ── Tasks ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_tasks(
    linked_record_id: Optional[str] = None,
    linked_object_slug: Optional[str] = None,
    is_completed: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """[Attio] List Attio tasks, optionally filtered by linked record or completion status."""
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if linked_record_id and linked_object_slug:
        params["linked_object"] = linked_object_slug
        params["linked_record_id"] = linked_record_id
    if is_completed is not None:
        params["is_completed"] = str(is_completed).lower()
    return json.dumps(_at_get("/tasks", params), indent=2)

@mcp.tool()
def attio_get_task(task_id: str) -> str:
    """[Attio] Get a specific Attio task by ID."""
    return json.dumps(_at_get(f"/tasks/{task_id}"), indent=2)

@mcp.tool()
def attio_create_task(
    content: str,
    linked_records: Optional[list] = None,
    assignees: Optional[list] = None,
    deadline_at: Optional[str] = None,
    is_completed: bool = False,
) -> str:
    """[Attio] Create a new task in Attio.
    linked_records: [{"target_object": "people", "target_record_id": "<uuid>"}]
    assignees: [{"referenced_actor_type": "workspace-member", "referenced_actor_id": "<uuid>"}]
    deadline_at: ISO 8601 timestamp."""
    return json.dumps(_at_post("/tasks", {"data": {
        "content": content, "format": "plaintext", "is_completed": is_completed,
        "deadline_at": deadline_at, "assignees": assignees or [], "linked_records": linked_records or [],
    }}), indent=2)

@mcp.tool()
def attio_update_task(
    task_id: str,
    content: Optional[str] = None,
    is_completed: Optional[bool] = None,
    deadline_at: Optional[str] = None,
    assignees: Optional[list] = None,
    linked_records: Optional[list] = None,
) -> str:
    """[Attio] Update an existing Attio task."""
    data: dict[str, Any] = {}
    if content is not None: data["content"] = content
    if is_completed is not None: data["is_completed"] = is_completed
    if deadline_at is not None: data["deadline_at"] = deadline_at
    if assignees is not None: data["assignees"] = assignees
    if linked_records is not None: data["linked_records"] = linked_records
    return json.dumps(_at_patch(f"/tasks/{task_id}", {"data": data}), indent=2)

@mcp.tool()
def attio_delete_task(task_id: str) -> str:
    """[Attio] Delete a task from Attio."""
    return json.dumps(_at_delete(f"/tasks/{task_id}"), indent=2)


# ── Lists ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_lists() -> str:
    """[Attio] List all lists in the Attio workspace."""
    return json.dumps(_at_get("/lists"), indent=2)

@mcp.tool()
def attio_get_list(list_id: str) -> str:
    """[Attio] Get a specific Attio list by ID or slug."""
    return json.dumps(_at_get(f"/lists/{list_id}"), indent=2)

@mcp.tool()
def attio_create_list(name: str, object_slug: str) -> str:
    """[Attio] Create a new list for a given object type.
    object_slug: the object type records in this list will be, e.g. 'companies', 'people'."""
    return json.dumps(_at_post("/lists", {"data": {
        "name": name, "api_slug": name.lower().replace(" ", "_"), "object_singular_noun": object_slug,
    }}), indent=2)

@mcp.tool()
def attio_update_list(list_id: str, name: Optional[str] = None) -> str:
    """[Attio] Update a list's display name."""
    data: dict[str, Any] = {}
    if name is not None: data["name"] = name
    return json.dumps(_at_patch(f"/lists/{list_id}", {"data": data}), indent=2)

@mcp.tool()
def attio_delete_list(list_id: str) -> str:
    """[Attio] Delete a list."""
    return json.dumps(_at_delete(f"/lists/{list_id}"), indent=2)

@mcp.tool()
def attio_list_list_attributes(list_id: str) -> str:
    """[Attio] List the attributes (columns) defined on a list."""
    return json.dumps(_at_get(f"/lists/{list_id}/attributes"), indent=2)


# ── List entries ───────────────────────────────────────────────────────────────

@mcp.tool()
def attio_query_list_entries(
    list_id: str,
    filter_by: Optional[dict] = None,
    sorts: Optional[list] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """[Attio] Query entries in a list with optional filtering and sorting.
    Same filter/sort syntax as attio_query_records."""
    body: dict[str, Any] = {"limit": limit, "offset": offset}
    if filter_by: body["filter"] = filter_by
    if sorts: body["sorts"] = sorts
    return json.dumps(_at_post(f"/lists/{list_id}/entries/query", body), indent=2)

@mcp.tool()
def attio_get_list_entry(list_id: str, entry_id: str) -> str:
    """[Attio] Get a specific entry in a list."""
    return json.dumps(_at_get(f"/lists/{list_id}/entries/{entry_id}"), indent=2)

@mcp.tool()
def attio_create_list_entry(
    list_id: str,
    record_id: str,
    object_slug: str,
    entry_values: Optional[dict] = None,
) -> str:
    """[Attio] Add a record to a list as a new entry.
    object_slug: the object type of the record, e.g. 'companies', 'people'.
    entry_values: optional dict of list-level column values."""
    data: dict[str, Any] = {"parent_record_id": record_id, "parent_object": object_slug}
    if entry_values: data["entry_values"] = entry_values
    return json.dumps(_at_post(f"/lists/{list_id}/entries", {"data": data}), indent=2)

@mcp.tool()
def attio_upsert_list_entry(
    list_id: str,
    record_id: str,
    object_slug: str,
    entry_values: Optional[dict] = None,
) -> str:
    """[Attio] Add a record to a list, or update its entry if it already exists."""
    data: dict[str, Any] = {"parent_record_id": record_id, "parent_object": object_slug}
    if entry_values: data["entry_values"] = entry_values
    return json.dumps(_at_put(f"/lists/{list_id}/entries", {"data": data}), indent=2)

@mcp.tool()
def attio_update_list_entry(list_id: str, entry_id: str, entry_values: dict) -> str:
    """[Attio] Update list-entry attribute values for an entry (PATCH — appends to multi-selects)."""
    return json.dumps(_at_patch(f"/lists/{list_id}/entries/{entry_id}", {"data": {"entry_values": entry_values}}), indent=2)

@mcp.tool()
def attio_overwrite_list_entry(list_id: str, entry_id: str, entry_values: dict) -> str:
    """[Attio] Overwrite all values for a list entry (PUT — replaces multi-select values entirely)."""
    return json.dumps(_at_put(f"/lists/{list_id}/entries/{entry_id}", {"data": {"entry_values": entry_values}}), indent=2)

@mcp.tool()
def attio_delete_list_entry(list_id: str, entry_id: str) -> str:
    """[Attio] Remove an entry from a list."""
    return json.dumps(_at_delete(f"/lists/{list_id}/entries/{entry_id}"), indent=2)

@mcp.tool()
def attio_get_list_entry_attribute_values(list_id: str, entry_id: str, attribute_slug: str) -> str:
    """[Attio] Get values for a specific attribute on a list entry."""
    return json.dumps(_at_get(
        f"/lists/{list_id}/entries/{entry_id}/attributes/{attribute_slug}/values"
    ), indent=2)


# ── Comments & threads ────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_threads_for_record(object_slug: str, record_id: str, limit: int = 20) -> str:
    """[Attio] List all comment threads on a specific Attio record."""
    return json.dumps(_at_get("/threads", {
        "object": object_slug, "record_id": record_id, "limit": min(limit, 50),
    }), indent=2)

@mcp.tool()
def attio_list_threads_for_entry(list_id: str, entry_id: str, limit: int = 20) -> str:
    """[Attio] List all comment threads on a specific list entry."""
    return json.dumps(_at_get("/threads", {
        "list": list_id, "entry_id": entry_id, "limit": min(limit, 50),
    }), indent=2)

@mcp.tool()
def attio_get_thread(thread_id: str) -> str:
    """[Attio] Get a comment thread with all its comments."""
    return json.dumps(_at_get(f"/threads/{thread_id}"), indent=2)

@mcp.tool()
def attio_get_comment(comment_id: str) -> str:
    """[Attio] Get a single Attio comment by ID."""
    return json.dumps(_at_get(f"/comments/{comment_id}"), indent=2)

@mcp.tool()
def attio_create_comment(
    object_slug: str,
    record_id: str,
    content: str,
    thread_id: Optional[str] = None,
) -> str:
    """[Attio] Create a comment on a record. Omit thread_id to start a new thread;
    provide thread_id to reply to an existing thread."""
    body: dict[str, Any] = {"data": {
        "record_id": record_id, "record_object": object_slug,
        "content": [{"type": "text", "text": content}],
    }}
    if thread_id: body["data"]["thread_id"] = thread_id
    return json.dumps(_at_post("/comments", body), indent=2)

@mcp.tool()
def attio_delete_comment(comment_id: str) -> str:
    """[Attio] Delete a comment. If it's the first in a thread, the entire thread is deleted."""
    return json.dumps(_at_delete(f"/comments/{comment_id}"), indent=2)


# ── Webhooks ──────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_webhooks() -> str:
    """[Attio] List all webhooks configured in the Attio workspace."""
    return json.dumps(_at_get("/webhooks"), indent=2)

@mcp.tool()
def attio_get_webhook(webhook_id: str) -> str:
    """[Attio] Get a specific webhook by ID."""
    return json.dumps(_at_get(f"/webhooks/{webhook_id}"), indent=2)

@mcp.tool()
def attio_create_webhook(target_url: str, subscriptions: list) -> str:
    """[Attio] Create a new webhook.
    target_url: HTTPS URL Attio will POST events to.
    subscriptions: [{"event_type": "record.created", "object_slug": "people"}, ...]
    Event types: record.created/updated/deleted, note.created/deleted,
    task.created/completed/deleted, attribute-value.created/deleted."""
    return json.dumps(_at_post("/webhooks", {"data": {
        "target_url": target_url, "subscriptions": subscriptions,
    }}), indent=2)

@mcp.tool()
def attio_update_webhook(
    webhook_id: str,
    target_url: Optional[str] = None,
    subscriptions: Optional[list] = None,
) -> str:
    """[Attio] Update a webhook's URL or subscription list (replaces all existing subscriptions)."""
    data: dict[str, Any] = {}
    if target_url is not None: data["target_url"] = target_url
    if subscriptions is not None: data["subscriptions"] = subscriptions
    return json.dumps(_at_patch(f"/webhooks/{webhook_id}", {"data": data}), indent=2)

@mcp.tool()
def attio_delete_webhook(webhook_id: str) -> str:
    """[Attio] Delete a webhook."""
    return json.dumps(_at_delete(f"/webhooks/{webhook_id}"), indent=2)


# ── SQL queries ────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_run_sql(query: str) -> str:
    """[Attio] Execute a read-only SQL SELECT query against your Attio workspace data.
    Extremely powerful — join objects, filter by any attribute, aggregate, alias columns.
    Field names use the format `object.attribute_slug`. Use attio_list_attributes() to find slugs.
    Examples:
      SELECT people.record_id, people.name FROM people LIMIT 10
      SELECT companies.record_id, companies.name FROM companies LIMIT 10
      SELECT tasks.task_id, tasks.content_plaintext, tasks.is_completed FROM tasks WHERE tasks.is_completed = false LIMIT 20"""
    return json.dumps(_at_post("/sql", {"sql": query}), indent=2)


# ── Meetings ──────────────────────────────────────────────────────────────────

@mcp.tool()
def attio_list_meetings(
    limit: int = 20,
    offset: int = 0,
    record_id: Optional[str] = None,
    object_slug: Optional[str] = None,
) -> str:
    """[Attio] List meetings recorded in Attio (Beta). Filter by linked record optionally."""
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if record_id and object_slug:
        params["record_id"] = record_id
        params["object"] = object_slug
    return json.dumps(_at_get("/meetings", params), indent=2)

@mcp.tool()
def attio_get_meeting(meeting_id: str) -> str:
    """[Attio] Get a specific meeting by ID."""
    return json.dumps(_at_get(f"/meetings/{meeting_id}"), indent=2)

@mcp.tool()
def attio_list_call_recordings(meeting_id: str) -> str:
    """[Attio] List call recordings for a meeting."""
    return json.dumps(_at_get(f"/meetings/{meeting_id}/call_recordings"), indent=2)

@mcp.tool()
def attio_get_call_recording(meeting_id: str, recording_id: str) -> str:
    """[Attio] Get a specific call recording from a meeting."""
    return json.dumps(_at_get(f"/meetings/{meeting_id}/call_recordings/{recording_id}"), indent=2)

@mcp.tool()
def attio_get_call_transcript(
    meeting_id: str,
    recording_id: str,
    limit: int = 50,
    cursor: Optional[str] = None,
) -> str:
    """[Attio] Get the transcript for a call recording (cursor-paginated segments)."""
    params: dict[str, Any] = {"limit": limit}
    if cursor: params["cursor"] = cursor
    return json.dumps(_at_get(
        f"/meetings/{meeting_id}/call_recordings/{recording_id}/transcript", params
    ), indent=2)


# ── Object & attribute schema management ─────────────────────────────────────

@mcp.tool()
def attio_create_object(api_slug: str, singular_noun: str, plural_noun: str) -> str:
    """[Attio] Create a custom object type in the workspace.
    api_slug: lowercase with underscores, e.g. 'vendors'.
    singular_noun: 'Vendor'. plural_noun: 'Vendors'."""
    return json.dumps(_at_post("/objects", {"data": {
        "api_slug": api_slug, "singular_noun": singular_noun, "plural_noun": plural_noun,
    }}), indent=2)

@mcp.tool()
def attio_update_object(object_slug: str, singular_noun: Optional[str] = None, plural_noun: Optional[str] = None) -> str:
    """[Attio] Update a custom object's display name."""
    data: dict[str, Any] = {}
    if singular_noun is not None: data["singular_noun"] = singular_noun
    if plural_noun is not None: data["plural_noun"] = plural_noun
    return json.dumps(_at_patch(f"/objects/{object_slug}", {"data": data}), indent=2)

@mcp.tool()
def attio_create_attribute(
    object_slug: str,
    api_slug: str,
    title: str,
    attribute_type: str,
    is_required: bool = False,
    is_unique: bool = False,
    config: Optional[dict] = None,
) -> str:
    """[Attio] Create a new attribute on an object type.
    attribute_type: text, number, checkbox, currency, date, timestamp, location,
    rating, status, select, multi_select, record_reference, actor_reference,
    email_address, phone_number, domain, interaction.
    config examples: {"currency_code": "USD"} or {"relationship": {"target_object": "companies"}}"""
    data: dict[str, Any] = {
        "api_slug": api_slug, "title": title, "type": attribute_type,
        "is_required": is_required, "is_unique": is_unique,
    }
    if config: data.update(config)
    return json.dumps(_at_post(f"/objects/{object_slug}/attributes", {"data": data}), indent=2)

@mcp.tool()
def attio_update_attribute(
    object_slug: str,
    attribute_slug: str,
    title: Optional[str] = None,
    is_required: Optional[bool] = None,
) -> str:
    """[Attio] Update an attribute's title or required flag."""
    data: dict[str, Any] = {}
    if title is not None: data["title"] = title
    if is_required is not None: data["is_required"] = is_required
    return json.dumps(_at_patch(f"/objects/{object_slug}/attributes/{attribute_slug}", {"data": data}), indent=2)

@mcp.tool()
def attio_create_select_option(object_slug: str, attribute_slug: str, title: str, color: Optional[str] = None) -> str:
    """[Attio] Add a new option to a select or multi-select attribute.
    color: 'red', 'green', 'blue', 'yellow', 'purple', etc."""
    data: dict[str, Any] = {"title": title}
    if color: data["color"] = color
    return json.dumps(_at_post(
        f"/objects/{object_slug}/attributes/{attribute_slug}/options", {"data": data}
    ), indent=2)

@mcp.tool()
def attio_create_status(object_slug: str, attribute_slug: str, title: str, color: Optional[str] = None) -> str:
    """[Attio] Add a new status option to a status-type attribute."""
    data: dict[str, Any] = {"title": title}
    if color: data["color"] = color
    return json.dumps(_at_post(
        f"/objects/{object_slug}/attributes/{attribute_slug}/statuses", {"data": data}
    ), indent=2)


# ===========================================================================
# AUGUST PLATFORM
# Base URL: https://api.august.law  |  Bearer token auth
# Legal document intelligence, Genius Mode queries, project & folder management
# ===========================================================================

AUG_BASE_URL = os.environ.get("AUGUST_BASE_URL", "https://api.august.law")
AUG_API_KEY = os.environ.get("AUGUST_API_KEY", "ak_4QJMZSR78ERW16RBEFFC08934J2PR07K")

def _aug_headers():
    if not AUG_API_KEY:
        raise RuntimeError("AUGUST_API_KEY not set.")
    return {"Authorization": f"Bearer {AUG_API_KEY}", "Content-Type": "application/json"}

def _aug_get(path, params=None):
    r = httpx.get(f"{AUG_BASE_URL}{path}", headers=_aug_headers(), params=params, timeout=60)
    r.raise_for_status(); return r.json()

def _aug_post(path, body=None):
    r = httpx.post(f"{AUG_BASE_URL}{path}", headers=_aug_headers(), json=body or {}, timeout=120)
    r.raise_for_status(); return r.json()


# ── Projects ────────────────────────────────────────────────────────────────

@mcp.tool()
def august_list_projects() -> str:
    """[August Platform] List all projects the authenticated user has access to.
    Projects are the top-level organizational unit in August — each represents
    a matter, deal, or workstream containing folders, files, and queries.
    Use this first to discover project IDs needed by other tools."""
    return json.dumps(_aug_get("/api/v1/projects"), indent=2)

@mcp.tool()
def august_list_project_members(project_id: str) -> str:
    """[August Platform] List all members of a specific project.
    Returns each member's id, name, email, and role within the project.
    Useful for understanding who has access and their permissions."""
    return json.dumps(_aug_get(f"/api/v1/projects/{project_id}/members"), indent=2)


# ── Search ──────────────────────────────────────────────────────────────────

@mcp.tool()
def august_global_search(q: str, offset: int = 0, limit: int = 50) -> str:
    """[August Platform] Full-text search across ALL accessible projects.
    Searches file names, document content, and metadata globally.
    Returns matching files, folders, and documents with relevance scores and snippets.
    Use this when you don't know which project contains the information."""
    return json.dumps(_aug_get("/api/v1/search", {"q": q, "offset": offset, "limit": limit}), indent=2)

@mcp.tool()
def august_project_search(project_id: str, q: str, offset: int = 0, limit: int = 50) -> str:
    """[August Platform] Full-text search within a specific project's documents and files.
    More targeted than global search — scoped to a single project.
    Returns matching items with relevance scores, snippets, and folder paths."""
    return json.dumps(_aug_get(f"/api/v1/projects/{project_id}/search", {"q": q, "offset": offset, "limit": limit}), indent=2)


# ── Folders ─────────────────────────────────────────────────────────────────

@mcp.tool()
def august_get_folder_contents(folder_id: str, offset: int = 0, limit: int = 100) -> str:
    """[August Platform] Get the contents (files and subfolders) of a specific folder.
    Returns a paginated list of items with their names, types (file/folder),
    sizes, and timestamps. Use this to browse the folder hierarchy."""
    return json.dumps(_aug_get(f"/api/v1/folders/{folder_id}/contents", {"offset": offset, "limit": limit}), indent=2)

@mcp.tool()
def august_get_folder_tree(folder_id: str) -> str:
    """[August Platform] Get the full recursive folder tree starting from a specific folder.
    Returns the complete hierarchy of subfolders and files as a nested tree structure.
    Useful for understanding the full organizational structure of a project's documents."""
    return json.dumps(_aug_get(f"/api/v1/folders/{folder_id}/tree"), indent=2)


# ── Files ───────────────────────────────────────────────────────────────────

@mcp.tool()
def august_get_file_download_urls(doc_ids: List[str], use_pdf: bool = False, ttl: int = 3600, project_id: Optional[str] = None) -> str:
    """[August Platform] Generate presigned download URLs for one or more files.
    Pass a list of document IDs to get time-limited download links.
    Set use_pdf=True to convert documents to PDF format on download.
    TTL controls how long the URLs remain valid (default 3600 seconds = 1 hour).
    Returns URLs with expiration timestamps and original filenames."""
    body: dict[str, Any] = {"doc_ids": doc_ids, "use_pdf": use_pdf, "ttl": ttl}
    if project_id:
        body["project_id"] = project_id
    return json.dumps(_aug_post("/api/v1/files/download", body), indent=2)


# ── Genius Mode Queries ─────────────────────────────────────────────────────

@mcp.tool()
def august_submit_query(
    query: str,
    project_id: Optional[str] = None,
    folder_ids: Optional[List[str]] = None,
    file_ids: Optional[List[str]] = None,
    mode: str = "research"
) -> str:
    """[August Platform] Submit a Genius Mode query for legal research or document analysis.
    This is August's most powerful capability — it processes natural language questions
    against your documents using AI.

    IMPORTANT: Queries are processed ASYNCHRONOUSLY. This tool returns a query_id
    immediately. You must then poll with august_get_query_status until status is
    'completed', then retrieve results with august_get_query_result.

    Modes:
      - 'research': Deep legal research across documents (default)
      - 'analysis': Structured analysis of specific documents
      - 'draft': Draft new content based on document context
      - 'review': Review and annotate documents

    Scope the query by providing project_id, folder_ids, and/or file_ids.
    Without scope, it searches across all accessible documents."""
    body: dict[str, Any] = {"query": query, "mode": mode}
    if project_id:
        body["project_id"] = project_id
    if folder_ids:
        body["folder_ids"] = folder_ids
    if file_ids:
        body["file_ids"] = file_ids
    return json.dumps(_aug_post("/api/v1/queries", body), indent=2)

@mcp.tool()
def august_get_query_status(query_id: str) -> str:
    """[August Platform] Poll the processing status of a submitted Genius Mode query.
    Status values: 'pending', 'processing', 'completed', 'failed'.
    Also returns a progress indicator (0-1) during processing.
    Call this repeatedly until status is 'completed' before fetching results."""
    return json.dumps(_aug_get(f"/api/v1/queries/{query_id}/status"), indent=2)

@mcp.tool()
def august_get_query_result(query_id: str) -> str:
    """[August Platform] Retrieve the completed result of a Genius Mode query.
    Only call this after august_get_query_status returns 'completed'.
    Returns the AI-generated answer, source documents, and citations
    with references back to specific documents and passages."""
    return json.dumps(_aug_get(f"/api/v1/queries/{query_id}/result"), indent=2)

@mcp.tool()
def august_get_query_files(query_id: str) -> str:
    """[August Platform] Retrieve files generated by a completed Genius Mode query.
    Some query modes produce work products (presentations, spreadsheets, reports).
    This returns the list of generated files with their IDs, names, types, and sizes.
    Use august_get_file_download_urls with the file IDs to download them."""
    return json.dumps(_aug_get(f"/api/v1/queries/{query_id}/files"), indent=2)


# ── Workflows ───────────────────────────────────────────────────────────────

@mcp.tool()
def august_create_workflow(
    prompt: str,
    project_id: Optional[str] = None,
    idempotency_key: Optional[str] = None
) -> str:
    """[August Platform] Create a saved workflow from a natural-language prompt.
    August generates a workflow draft from the prompt and saves it, using the
    same creation flow as the platform chat interface.

    Args:
        prompt: Natural-language description of the workflow (max 20,000 chars).
                Example: "Review all uploaded contracts for liability clauses and
                flag any that exceed $1M exposure"
        project_id: Optional project to scope the workflow to.
        idempotency_key: Optional dedupe key (max 256 chars). Reusing the same
                         key returns the first workflow instead of creating a duplicate.

    Returns workflow_id, name, created status, and any trigger_warnings."""
    body: dict[str, Any] = {"prompt": prompt}
    if project_id:
        body["project_id"] = project_id
    if idempotency_key:
        body["idempotency_key"] = idempotency_key
    return json.dumps(_aug_post("/api/v1/workflows", body), indent=2)


# ── Pre-Share Policies ──────────────────────────────────────────────────────

@mcp.tool()
def august_create_pre_share_policy(
    name: str,
    condition_type: str,
    condition_value: str,
    artifacts: List[dict],
    delivery_mode: str = "share",
    permission_level: str = "viewer",
    backfill_existing_users: bool = False,
    is_enabled: bool = True,
    destination_type: Optional[str] = None,
    target_project_id: Optional[str] = None
) -> str:
    """[August Platform] Create a pre-share policy for mass-sharing projects, folders, or workflows.
    Policies automatically share content with users matching a condition.

    Args:
        name: Policy name (max 200 chars).
        condition_type: Who to share with. One of:
            - 'organization_membership': all members of an org
            - 'email_exact': a specific email address
            - 'email_domain': all users with emails at a domain (e.g. 'acme.com')
        condition_value: The org ID, email, or domain to match against.
        artifacts: List of items to share. Each dict needs:
            - 'artifact_type': one of 'project', 'folder', 'workflow'
            - 'artifact_id': the ID of the artifact
            Example: [{"artifact_type": "workflow", "artifact_id": "abc-123"}]
        delivery_mode: 'share' (give access to original) or 'duplicate' (copy for each user). Default: 'share'.
        permission_level: 'owner', 'editor', or 'viewer'. Default: 'viewer'.
        backfill_existing_users: If True, immediately apply to all existing matching users. Default: False.
        is_enabled: Whether the policy is active. Default: True.
        destination_type: 'personal' or 'project'. Where shared content lands.
        target_project_id: If destination_type is 'project', the target project ID.

    Returns policy details including applied_count, pending_count, and matched_users_count."""
    body: dict[str, Any] = {
        "name": name,
        "condition_type": condition_type,
        "condition_value": condition_value,
        "artifacts": artifacts,
        "delivery_mode": delivery_mode,
        "permission_level": permission_level,
        "backfill_existing_users": backfill_existing_users,
        "is_enabled": is_enabled,
    }
    if destination_type:
        body["destination_type"] = destination_type
    if target_project_id:
        body["target_project_id"] = target_project_id
    return json.dumps(_aug_post("/api/v1/pre-share-policies", body), indent=2)


# ===========================================================================
# App entrypoint
# ===========================================================================

app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
