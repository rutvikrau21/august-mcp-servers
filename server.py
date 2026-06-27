"""
Amplemarket MCP Server - FastMCP server exposing Amplemarket API as MCP tools.
Setup: pip install mcp[cli] httpx uvicorn
Run: AMPLEMARKET_API_KEY=your_key python server.py
"""
import os, json
from typing import Optional, List
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.amplemarket.com"
API_KEY = os.environ.get("AMPLEMARKET_API_KEY", "")
mcp = FastMCP("Amplemarket")

def _headers():
    if not API_KEY: raise RuntimeError("AMPLEMARKET_API_KEY not set.")
    return {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def _get(path, params=None):
    r = httpx.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=30)
    r.raise_for_status(); return r.json()

def _post(path, body=None):
    r = httpx.post(f"{BASE_URL}{path}", headers=_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json()

def _patch(path, body=None):
    r = httpx.patch(f"{BASE_URL}{path}", headers=_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json() if r.content else {"status": "ok"}

def _delete(path, body=None):
    r = httpx.delete(f"{BASE_URL}{path}", headers=_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json() if r.content else {"status": "deleted"}


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------

@mcp.tool()
def get_account_info() -> str:
    """Get details about the current Amplemarket account."""
    return json.dumps(_get("/account"), indent=2)


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------

@mcp.tool()
def list_contacts(page_size: int = 20) -> str:
    """List contacts with pagination. page_size max 50."""
    return json.dumps(_get("/contacts", {"page[size]": page_size}), indent=2)

@mcp.tool()
def get_contacts(ids: List[str]) -> str:
    """Retrieve up to 20 contacts by their IDs."""
    params = [("ids[]", i) for i in ids]
    r = httpx.get(f"{BASE_URL}/contacts", headers=_headers(), params=params, timeout=30)
    r.raise_for_status(); return json.dumps(r.json(), indent=2)

@mcp.tool()
def get_contact(contact_id: str) -> str:
    """Retrieve a single contact by ID."""
    return json.dumps(_get(f"/contacts/{contact_id}"), indent=2)

@mcp.tool()
def get_contact_by_email(email: str) -> str:
    """Retrieve a contact by email address."""
    return json.dumps(_get(f"/contacts/by_email/{email}"), indent=2)


# ---------------------------------------------------------------------------
# People search & enrichment
# ---------------------------------------------------------------------------

@mcp.tool()
def search_people(
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
    """Search for people with filters: titles, seniority, company, location, industry, size, revenue."""
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
    return json.dumps(_post("/people/search", body), indent=2)

@mcp.tool()
def find_person(
    email: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    name: Optional[str] = None,
    title: Optional[str] = None,
    company_name: Optional[str] = None,
    company_domain: Optional[str] = None,
    reveal_email: bool = False,
    reveal_phone_numbers: bool = False,
) -> str:
    """Look up and enrich a single person. At least one identifier required (email, linkedin_url, or name+company).
    reveal_email costs 1 email credit. reveal_phone_numbers costs 1 phone credit. Each lookup costs 0.5 credits (once per 24h)."""
    params: dict = {}
    if email: params["email"] = email
    if linkedin_url: params["linkedin_url"] = linkedin_url
    if name: params["name"] = name
    if title: params["title"] = title
    if company_name: params["company_name"] = company_name
    if company_domain: params["company_domain"] = company_domain
    if reveal_email: params["reveal_email"] = "true"
    if reveal_phone_numbers: params["reveal_phone_numbers"] = "true"
    return json.dumps(_get("/people/find", params), indent=2)

@mcp.tool()
def enrich_person(linkedin_url: Optional[str] = None, email: Optional[str] = None) -> str:
    """Enrich a single person via the enrichments endpoint (alternative to find_person)."""
    body = {}
    if linkedin_url: body["linkedin_url"] = linkedin_url
    if email: body["email"] = email
    return json.dumps(_post("/people-enrichments/single", body), indent=2)

@mcp.tool()
def start_people_enrichment_batch(
    people: List[dict],
    reveal_email: bool = False,
    reveal_phone_numbers: bool = False,
) -> str:
    """Start a batch people enrichment (up to 100,000 entries).
    Each person dict can include: email, linkedin_url, name, title, company_name, company_domain.
    reveal_email / reveal_phone_numbers trigger credit charges."""
    body: dict = {"people": people}
    if reveal_email: body["reveal_email"] = True
    if reveal_phone_numbers: body["reveal_phone_numbers"] = True
    return json.dumps(_post("/people-enrichments", body), indent=2)

@mcp.tool()
def get_people_enrichment_results(enrichment_id: str) -> str:
    """Poll people enrichment batch results by ID."""
    return json.dumps(_get(f"/people-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def cancel_people_enrichment(enrichment_id: str) -> str:
    """Cancel a running people enrichment batch. Returns partial results gathered so far."""
    return json.dumps(_patch(f"/people/enrichment-requests/{enrichment_id}", {"status": "canceled"}), indent=2)


# ---------------------------------------------------------------------------
# Company search & enrichment
# ---------------------------------------------------------------------------

@mcp.tool()
def search_companies(
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
    """Search for companies with filters."""
    body = {"page": page, "page_size": page_size}
    for k, v in [
        ("company_names", company_names), ("company_domains", company_domains),
        ("company_industries", company_industries), ("company_sizes", company_sizes),
        ("company_locations", company_locations), ("company_types", company_types),
        ("company_focuses", company_focuses), ("company_revenue", company_revenue),
        ("company_keywords", company_keywords),
    ]:
        if v: body[k] = v
    return json.dumps(_post("/companies/search", body), indent=2)

@mcp.tool()
def find_company(
    linkedin_url: Optional[str] = None,
    domain: Optional[str] = None,
) -> str:
    """Look up and enrich a single company by LinkedIn URL or domain. At least one required."""
    params: dict = {}
    if linkedin_url: params["linkedin_url"] = linkedin_url
    if domain: params["domain"] = domain
    return json.dumps(_get("/companies/find", params), indent=2)

@mcp.tool()
def enrich_company(linkedin_url: Optional[str] = None, domain: Optional[str] = None) -> str:
    """Enrich a single company via the enrichments endpoint (alternative to find_company)."""
    body = {}
    if linkedin_url: body["linkedin_url"] = linkedin_url
    if domain: body["domain"] = domain
    return json.dumps(_post("/company-enrichments/single", body), indent=2)

@mcp.tool()
def start_company_enrichment_batch(
    companies: List[dict],
    reveal_email: bool = False,
    reveal_phone_numbers: bool = False,
) -> str:
    """Start a batch company enrichment (up to 10,000 entries).
    Each company dict can include: linkedin_url, domain, name.
    reveal_email / reveal_phone_numbers trigger credit charges."""
    body: dict = {"companies": companies}
    if reveal_email: body["reveal_email"] = True
    if reveal_phone_numbers: body["reveal_phone_numbers"] = True
    return json.dumps(_post("/company-enrichments", body), indent=2)

@mcp.tool()
def get_company_enrichment_results(enrichment_id: str) -> str:
    """Poll company enrichment batch results by ID."""
    return json.dumps(_get(f"/company-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def cancel_company_enrichment(enrichment_id: str) -> str:
    """Cancel a running company enrichment batch. Returns partial results gathered so far."""
    return json.dumps(_patch(f"/companies/enrichment-requests/{enrichment_id}", {"status": "canceled"}), indent=2)


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------

@mcp.tool()
def list_sequences(
    status: Optional[str] = None,
    name: Optional[str] = None,
    created_by_user_id: Optional[str] = None,
    created_by_user_email: Optional[str] = None,
    page_size: int = 20,
) -> str:
    """List sequences. Filters: status (active/draft/paused), name (case-insensitive search),
    created_by_user_id, created_by_user_email."""
    params: dict = {"page[size]": page_size}
    if status: params["status"] = status
    if name: params["name"] = name
    if created_by_user_id: params["created_by_user_id"] = created_by_user_id
    if created_by_user_email: params["created_by_user_email"] = created_by_user_email
    return json.dumps(_get("/sequences", params), indent=2)

@mcp.tool()
def add_leads_to_sequence(
    sequence_id: str,
    leads: List[dict],
    mailboxes: Optional[List[str]] = None,
    leads_distribution: Optional[str] = None,
) -> str:
    """Add leads to a sequence (up to 250 per call). Each lead: {"email": "...", "data": {...}}.
    Use add_lead_to_sequence for a single lead, or import_csv_to_sequence for CSV uploads."""
    body: dict = {"leads": leads}
    settings: dict = {}
    if mailboxes: settings["mailboxes"] = mailboxes
    if leads_distribution: settings["leads_distribution"] = leads_distribution
    if settings: body["settings"] = settings
    return json.dumps(_post(f"/sequences/{sequence_id}/leads", body), indent=2)

@mcp.tool()
def add_lead_to_sequence(
    sequence_id: str,
    email: str,
    fields: Optional[dict] = None,
    mailboxes: Optional[List[str]] = None,
    ignore_recently_contacted: bool = False,
    ignore_exclusion_list: bool = False,
    ignore_duplicate_in_other_active_sequences: bool = False,
) -> str:
    """Add a single lead to a sequence.
    - fields: flat dict of every dynamic variable the sequence requires,
      e.g. {"first_name": "Jane", "company": "Acme", "use_case_1": "...", "city": "NYC"}
    - ignore_* overrides allow bypassing normal skip rules."""
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
    return json.dumps(_post(f"/sequences/{sequence_id}/leads", body), indent=2)

@mcp.tool()
def import_csv_to_sequence(
    sequence_id: str,
    csv_content: str,
    email_column: str = "email",
    mailboxes: Optional[List[str]] = None,
    leads_distribution: Optional[str] = None,
) -> str:
    """Import leads from raw CSV text into a sequence.
    - csv_content: full CSV text including header row (copy-paste the file contents)
    - email_column: name of the column containing email addresses (default: "email")
    - All other columns are automatically passed as sequence dynamic fields
    - Handles batching automatically (20 leads per request)
    Returns a summary of how many leads were added, skipped, or failed per batch."""
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
        return json.dumps({"error": f"No leads found. Check that email_column='{email_column}' matches a column header."})
    settings: dict = {}
    if mailboxes: settings["mailboxes"] = mailboxes
    if leads_distribution: settings["leads_distribution"] = leads_distribution
    results = []
    for i in range(0, len(leads), 20):
        batch = leads[i:i + 20]
        body: dict = {"leads": batch}
        if settings: body["settings"] = settings
        result = _post(f"/sequences/{sequence_id}/leads", body)
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


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

@mcp.tool()
def list_tasks(
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    page: int = 1,
) -> str:
    """List tasks. Use list_task_statuses and list_task_types to see valid filter values."""
    params: dict = {"page": page}
    if status: params["status"] = status
    if task_type: params["task_type"] = task_type
    return json.dumps(_get("/tasks", params), indent=2)

@mcp.tool()
def list_task_statuses() -> str:
    """List all valid task status values (use as filters in list_tasks)."""
    return json.dumps(_get("/tasks/statuses"), indent=2)

@mcp.tool()
def list_task_types() -> str:
    """List all task types."""
    return json.dumps(_get("/tasks/types"), indent=2)

@mcp.tool()
def complete_task(task_id: str, set_lead_to_completed: bool = False) -> str:
    """Mark a task as completed.
    set_lead_to_completed: if True, also marks the associated lead as completed in the sequence."""
    body: dict = {}
    if set_lead_to_completed: body["set_lead_to_completed"] = True
    return json.dumps(_post(f"/tasks/{task_id}/complete", body), indent=2)

@mcp.tool()
def skip_task(task_id: str) -> str:
    """Skip a task."""
    return json.dumps(_post(f"/tasks/{task_id}/skip"), indent=2)


# ---------------------------------------------------------------------------
# Lead Lists
# ---------------------------------------------------------------------------

@mcp.tool()
def list_lead_lists() -> str:
    """List all lead lists."""
    return json.dumps(_get("/lead-lists"), indent=2)

@mcp.tool()
def get_lead_list(lead_list_id: str) -> str:
    """Retrieve a specific lead list and poll its processing status."""
    return json.dumps(_get(f"/lead-lists/{lead_list_id}"), indent=2)

@mcp.tool()
def create_lead_list(
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
    """Create a new lead list.
    - owner: email of an existing Amplemarket user who will own the list
    - shared: True = account-wide, False = user-specific
    - list_type: 'linkedin', 'email', or 'titles_and_company'
    - leads: array of lead objects matching the list_type format
    Returns 202 Accepted. Poll get_lead_list with the returned ID to check status."""
    body: dict = {
        "name": name,
        "owner": owner,
        "shared": shared,
        "type": list_type,
        "leads": leads,
        "visible": visible,
        "options": {
            "reveal_phone_numbers": reveal_phone_numbers,
            "validate_email": validate_email,
            "enrich": enrich,
        },
    }
    return json.dumps(_post("/lead-lists", body), indent=2)

@mcp.tool()
def add_leads_to_list(lead_list_id: str, leads: List[dict]) -> str:
    """Add leads to an existing lead list (max 10,000 per request; 20,000 total per list)."""
    return json.dumps(_post(f"/lead-lists/{lead_list_id}/leads", {"leads": leads}), indent=2)


# ---------------------------------------------------------------------------
# Email Validations
# ---------------------------------------------------------------------------

@mcp.tool()
def start_email_validation(emails: List[str]) -> str:
    """Start a batch email validation job (max 100,000 emails; costs 1 credit each).
    Returns 202 Accepted. Poll get_email_validation_results with the returned ID."""
    return json.dumps(_post("/email-validations", {"emails": emails}), indent=2)

@mcp.tool()
def get_email_validation_results(validation_id: str, page_size: int = 20) -> str:
    """Get email validation results. Status: queued, processing, completed, canceled, error."""
    return json.dumps(_get(f"/email-validations/{validation_id}", {"page[size]": page_size}), indent=2)

@mcp.tool()
def cancel_email_validation(validation_id: str) -> str:
    """Cancel a running email validation job."""
    return json.dumps(_patch(f"/email-validations/{validation_id}", {"status": "canceled"}), indent=2)


# ---------------------------------------------------------------------------
# Calls
# ---------------------------------------------------------------------------

@mcp.tool()
def list_calls(
    page: int = 1,
    user_id: Optional[str] = None,
    from_number: Optional[str] = None,
    to_number: Optional[str] = None,
    start_date_from: Optional[str] = None,
    start_date_to: Optional[str] = None,
) -> str:
    """List logged calls. Date filters are ISO 8601 strings, e.g. '2024-01-15T00:00:00Z'."""
    params: dict = {"page": page}
    if user_id: params["user_id"] = user_id
    if from_number: params["from"] = from_number
    if to_number: params["to"] = to_number
    if start_date_from: params["start_date_from"] = start_date_from
    if start_date_to: params["start_date_to"] = start_date_to
    return json.dumps(_get("/calls", params), indent=2)

@mcp.tool()
def log_call(
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
    """Log an external call (made outside Amplemarket's dialer).
    - from_number / to_number: E.164 phone numbers
    - duration: call length in seconds
    - answered: whether the call was picked up
    - human: True if answered by a person, False if voicemail/machine
    - task_id: UUID of the associated Amplemarket task
    - user_id: UUID of the user who made the call
    - disposition_id: UUID from list_call_dispositions"""
    body: dict = {
        "from": from_number,
        "to": to_number,
        "duration": duration,
        "answered": answered,
        "human": human,
        "task_id": task_id,
        "user_id": user_id,
    }
    if transcription: body["transcription"] = transcription
    if recording_url: body["recording_url"] = recording_url
    if disposition_id: body["disposition_id"] = disposition_id
    return json.dumps(_post("/calls", body), indent=2)

@mcp.tool()
def list_call_dispositions() -> str:
    """List all available call disposition options."""
    return json.dumps(_get("/calls/dispositions"), indent=2)

@mcp.tool()
def get_call_recording(call_id: str) -> str:
    """Get call recording URL for a specific call."""
    return json.dumps(_get(f"/calls/{call_id}/recording"), indent=2)


# ---------------------------------------------------------------------------
# Exclusion Lists
# ---------------------------------------------------------------------------

@mcp.tool()
def list_excluded_emails(page: int = 1) -> str:
    """List all excluded email addresses."""
    return json.dumps(_get("/exclusion-lists/emails", {"page": page}), indent=2)

@mcp.tool()
def create_email_exclusions(emails: List[str]) -> str:
    """Add email addresses to the exclusion list."""
    return json.dumps(_post("/exclusion-lists/emails", {"emails": emails}), indent=2)

@mcp.tool()
def delete_email_exclusions(emails: List[str]) -> str:
    """Remove email addresses from the exclusion list."""
    return json.dumps(_delete("/exclusion-lists/emails", {"emails": emails}), indent=2)

@mcp.tool()
def list_excluded_domains(page: int = 1) -> str:
    """List all excluded domains."""
    return json.dumps(_get("/exclusion-lists/domains", {"page": page}), indent=2)

@mcp.tool()
def create_domain_exclusions(domains: List[str]) -> str:
    """Add domains to the exclusion list."""
    return json.dumps(_post("/exclusion-lists/domains", {"domains": domains}), indent=2)

@mcp.tool()
def delete_domain_exclusions(domains: List[str]) -> str:
    """Remove domains from the exclusion list."""
    return json.dumps(_delete("/exclusion-lists/domains", {"domains": domains}), indent=2)


# ---------------------------------------------------------------------------
# Mailboxes
# ---------------------------------------------------------------------------

@mcp.tool()
def list_mailboxes(
    status: Optional[str] = None,
    email_provider: Optional[str] = None,
    user_email: Optional[str] = None,
    page_size: int = 20,
) -> str:
    """List mailboxes.
    - status: 'active', 'inactive', or 'needs_reconnection'
    - email_provider: 'google', 'outlook', 'other', or 'other_mixed'
    - user_email: filter to a specific user's mailboxes"""
    params: dict = {"page[size]": page_size}
    if status: params["status"] = status
    if email_provider: params["email_provider"] = email_provider
    if user_email: params["user_email"] = user_email
    return json.dumps(_get("/mailboxes", params), indent=2)

@mcp.tool()
def update_mailbox_daily_limit(mailbox_id: str, daily_limit: int) -> str:
    """Update a mailbox's daily email sending limit. Rate-limited to 1/minute and 1/hour per mailbox."""
    return json.dumps(_patch(f"/mailboxes/{mailbox_id}", {"daily_limit": daily_limit}), indent=2)


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

@mcp.tool()
def list_users(
    status: Optional[str] = None,
    role: Optional[str] = None,
    email: Optional[str] = None,
    page_size: int = 20,
) -> str:
    """List team members/users.
    - status: filter by user status (e.g. 'active', 'inactive')
    - role: filter by role (e.g. 'admin', 'sales_rep')
    - email: filter by exact email address"""
    params: dict = {"page[size]": page_size}
    if status: params["status"] = status
    if role: params["role"] = role
    if email: params["email"] = email
    return json.dumps(_get("/users", params), indent=2)


# ---------------------------------------------------------------------------
# CRM Accounts
# ---------------------------------------------------------------------------

@mcp.tool()
def list_accounts(
    page: int = 1,
    name: Optional[str] = None,
    domain: Optional[str] = None,
    owner_email: Optional[str] = None,
    tags: Optional[List[str]] = None,
    page_size: int = 10,
) -> str:
    """List CRM accounts. Filters: name (partial match), domain (exact), owner_email (exact), tags."""
    params: dict = {"page": page, "page[size]": page_size}
    if name: params["name"] = name
    if domain: params["domain"] = domain
    if owner_email: params["owner_email"] = owner_email
    if tags:
        for tag in tags: params.setdefault("tags[]", []).append(tag)
    return json.dumps(_get("/accounts", params), indent=2)

@mcp.tool()
def get_crm_account(account_id: str) -> str:
    """Retrieve a specific CRM account by ID."""
    return json.dumps(_get(f"/accounts/{account_id}"), indent=2)


# ---------------------------------------------------------------------------
# Job Openings
# ---------------------------------------------------------------------------

@mcp.tool()
def list_job_openings(
    company_id: Optional[str] = None,
    domain: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    person_seniorities: Optional[List[str]] = None,
    person_departments: Optional[List[str]] = None,
    person_job_functions: Optional[List[str]] = None,
    only_remote: bool = False,
    page_size: int = 10,
) -> str:
    """List job openings for a company. At least one of company_id, domain, or linkedin_url is required.
    person_seniorities values: Owner, Founder, C-Suite, Partner, VP, Head, Director, Manager, Senior, Entry, Intern, Other."""
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
    return json.dumps(_get("/job-openings", params), indent=2)

@mcp.tool()
def get_job_opening(job_opening_id: str) -> str:
    """Retrieve a specific job opening by ID."""
    return json.dumps(_get(f"/job-openings/{job_opening_id}"), indent=2)


# ---------------------------------------------------------------------------
# Phone Numbers
# ---------------------------------------------------------------------------

@mcp.tool()
def flag_phone_number(phone_number_id: str, user_id: str) -> str:
    """Flag a phone number as wrong/incorrect for review.
    - phone_number_id: ID of the phone number to flag
    - user_id: UUID of the user submitting the report"""
    return json.dumps(_post(f"/phone_numbers/{phone_number_id}/review", {
        "user_id": user_id,
        "reason": "wrong_number",
    }), indent=2)


# ---------------------------------------------------------------------------
# Custom Signals (Duo Copilot)
# ---------------------------------------------------------------------------

@mcp.tool()
def create_custom_signal_entry(token: str, data: dict) -> str:
    """Submit a custom signal entry to Amplemarket's Duo Copilot via webhook.
    - token: your custom signal token (from Amplemarket settings)
    - data: the signal payload as a dict"""
    return json.dumps(_post(f"/custom_signals/{token}/entries", data), indent=2)


# ---------------------------------------------------------------------------
# App entrypoint
# ---------------------------------------------------------------------------

app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
