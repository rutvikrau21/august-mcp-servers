"""
Amplemarket MCP Server - FastMCP server exposing Amplemarket API as MCP tools.
Setup: pip install fastmcp httpx
Run: AMPLEMARKET_API_KEY=your_key python server.py
"""
import os, json
from typing import Optional, List
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.amplemarket.com"
API_KEY = os.environ.get("AMPLEMARKET_API_KEY", "")
mcp = FastMCP("Amplemarket", host="0.0.0.0", port=8000)

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
    r.raise_for_status(); return r.json()

def _delete(path, body=None):
    r = httpx.delete(f"{BASE_URL}{path}", headers=_headers(), json=body or {}, timeout=30)
    r.raise_for_status(); return r.json() if r.content else {"status": "deleted"}

@mcp.tool()
def get_account_info() -> str:
    """Get details about the current Amplemarket account."""
    return json.dumps(_get("/account"), indent=2)

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

@mcp.tool()
def search_people(person_name: Optional[str]=None, person_titles: Optional[List[str]]=None,
    person_seniorities: Optional[List[str]]=None, person_departments: Optional[List[str]]=None,
    person_locations: Optional[List[str]]=None, person_keywords: Optional[List[str]]=None,
    company_names: Optional[List[str]]=None, company_domains: Optional[List[str]]=None,
    company_industries: Optional[List[str]]=None, company_sizes: Optional[List[str]]=None,
    company_locations: Optional[List[str]]=None, company_types: Optional[List[str]]=None,
    company_focuses: Optional[List[str]]=None, company_revenue: Optional[List[str]]=None,
    page: int=1, page_size: int=10) -> str:
    """Search for people with filters: titles, seniority, company, location, industry, size, revenue."""
    body = {"page": page, "page_size": page_size}
    for k, v in [("person_name",person_name),("person_titles",person_titles),
        ("person_seniorities",person_seniorities),("person_departments",person_departments),
        ("person_locations",person_locations),("person_keywords",person_keywords),
        ("company_names",company_names),("company_domains",company_domains),
        ("company_industries",company_industries),("company_sizes",company_sizes),
        ("company_locations",company_locations),("company_types",company_types),
        ("company_focuses",company_focuses),("company_revenue",company_revenue)]:
        if v: body[k] = v
    return json.dumps(_post("/people/search", body), indent=2)

@mcp.tool()
def search_companies(company_names: Optional[List[str]]=None, company_domains: Optional[List[str]]=None,
    company_industries: Optional[List[str]]=None, company_sizes: Optional[List[str]]=None,
    company_locations: Optional[List[str]]=None, company_types: Optional[List[str]]=None,
    company_focuses: Optional[List[str]]=None, company_revenue: Optional[List[str]]=None,
    company_keywords: Optional[List[str]]=None, page: int=1, page_size: int=10) -> str:
    """Search for companies with filters."""
    body = {"page": page, "page_size": page_size}
    for k, v in [("company_names",company_names),("company_domains",company_domains),
        ("company_industries",company_industries),("company_sizes",company_sizes),
        ("company_locations",company_locations),("company_types",company_types),
        ("company_focuses",company_focuses),("company_revenue",company_revenue),
        ("company_keywords",company_keywords)]:
        if v: body[k] = v
    return json.dumps(_post("/companies/search", body), indent=2)

@mcp.tool()
def list_sequences() -> str:
    """List all sequences."""
    return json.dumps(_get("/sequences"), indent=2)

@mcp.tool()
def add_leads_to_sequence(sequence_id: str, leads: List[dict], mailboxes: Optional[List[str]]=None, leads_distribution: Optional[str]=None) -> str:
    """Add leads to a sequence. Each lead must be: {"email": "...", "data": {"first_name": "...", "company": "...", ...}}.
    Use add_lead_to_sequence for a single lead with explicit fields, or import_csv_to_sequence to upload a CSV."""
    body = {"leads": leads}
    settings = {}
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
) -> str:
    """Add a single lead to a sequence.
    - fields: flat dict of every dynamic variable the sequence requires,
      e.g. {"first_name": "Jane", "company": "Acme", "use_case_1": "...", "city": "NYC"}
      The required keys depend entirely on the sequence template."""
    lead: dict = {"email": email}
    if fields: lead["data"] = fields
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
    - All other columns are automatically passed as sequence dynamic fields (e.g. first_name, company, use_case_1)
    - Handles batching automatically (20 leads per request)
    Returns a summary of how many leads were added, skipped, or failed per batch."""
    import csv, io
    reader = csv.DictReader(io.StringIO(csv_content.strip()))
    leads = []
    for row in reader:
        email = row.get(email_column, "").strip()
        if not email:
            continue
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

@mcp.tool()
def list_tasks(status: Optional[str]=None, task_type: Optional[str]=None, page: int=1) -> str:
    """List tasks."""
    params = {"page": page}
    if status: params["status"] = status
    if task_type: params["task_type"] = task_type
    return json.dumps(_get("/tasks", params), indent=2)

@mcp.tool()
def list_task_types() -> str:
    """List all task types."""
    return json.dumps(_get("/tasks/types"), indent=2)

@mcp.tool()
def complete_task(task_id: str) -> str:
    """Mark a task as completed."""
    return json.dumps(_post(f"/tasks/{task_id}/complete"), indent=2)

@mcp.tool()
def skip_task(task_id: str) -> str:
    """Skip a task."""
    return json.dumps(_post(f"/tasks/{task_id}/skip"), indent=2)

@mcp.tool()
def list_lead_lists() -> str:
    """List all lead lists."""
    return json.dumps(_get("/lead-lists"), indent=2)

@mcp.tool()
def get_lead_list(lead_list_id: str) -> str:
    """Retrieve a specific lead list."""
    return json.dumps(_get(f"/lead-lists/{lead_list_id}"), indent=2)

@mcp.tool()
def create_lead_list(name: str) -> str:
    """Create a new lead list."""
    return json.dumps(_post("/lead-lists", {"name": name}), indent=2)

@mcp.tool()
def add_leads_to_list(lead_list_id: str, leads: List[dict]) -> str:
    """Add leads to a lead list."""
    return json.dumps(_post(f"/lead-lists/{lead_list_id}/leads", {"leads": leads}), indent=2)

@mcp.tool()
def start_email_validation(emails: List[str]) -> str:
    """Start a batch email validation job."""
    return json.dumps(_post("/email-validations", {"emails": emails}), indent=2)

@mcp.tool()
def get_email_validation_results(validation_id: str) -> str:
    """Get email validation results."""
    return json.dumps(_get(f"/email-validations/{validation_id}"), indent=2)

@mcp.tool()
def cancel_email_validation(validation_id: str) -> str:
    """Cancel an email validation job."""
    return json.dumps(_delete(f"/email-validations/{validation_id}"), indent=2)

@mcp.tool()
def list_calls(page: int=1) -> str:
    """List logged calls."""
    return json.dumps(_get("/calls", {"page": page}), indent=2)

@mcp.tool()
def log_call(contact_email: str, disposition: str, duration_seconds: Optional[int]=None, notes: Optional[str]=None) -> str:
    """Log a call for a contact."""
    body = {"contact_email": contact_email, "disposition": disposition}
    if duration_seconds is not None: body["duration_seconds"] = duration_seconds
    if notes: body["notes"] = notes
    return json.dumps(_post("/calls", body), indent=2)

@mcp.tool()
def list_call_dispositions() -> str:
    """List call dispositions."""
    return json.dumps(_get("/calls/dispositions"), indent=2)

@mcp.tool()
def get_call_recording(call_id: str) -> str:
    """Get call recording URL."""
    return json.dumps(_get(f"/calls/{call_id}/recording"), indent=2)

@mcp.tool()
def list_excluded_emails(page: int=1) -> str:
    """List excluded emails."""
    return json.dumps(_get("/exclusion-lists/emails", {"page": page}), indent=2)

@mcp.tool()
def create_email_exclusions(emails: List[str]) -> str:
    """Add emails to exclusion list."""
    return json.dumps(_post("/exclusion-lists/emails", {"emails": emails}), indent=2)

@mcp.tool()
def delete_email_exclusions(emails: List[str]) -> str:
    """Remove emails from exclusion list."""
    return json.dumps(_delete("/exclusion-lists/emails", {"emails": emails}), indent=2)

@mcp.tool()
def list_excluded_domains(page: int=1) -> str:
    """List excluded domains."""
    return json.dumps(_get("/exclusion-lists/domains", {"page": page}), indent=2)

@mcp.tool()
def create_domain_exclusions(domains: List[str]) -> str:
    """Add domains to exclusion list."""
    return json.dumps(_post("/exclusion-lists/domains", {"domains": domains}), indent=2)

@mcp.tool()
def delete_domain_exclusions(domains: List[str]) -> str:
    """Remove domains from exclusion list."""
    return json.dumps(_delete("/exclusion-lists/domains", {"domains": domains}), indent=2)

@mcp.tool()
def list_mailboxes() -> str:
    """List all mailboxes."""
    return json.dumps(_get("/mailboxes"), indent=2)

@mcp.tool()
def update_mailbox_daily_limit(mailbox_id: str, daily_limit: int) -> str:
    """Update mailbox daily sending limit."""
    return json.dumps(_patch(f"/mailboxes/{mailbox_id}", {"daily_limit": daily_limit}), indent=2)

@mcp.tool()
def list_users() -> str:
    """List all users."""
    return json.dumps(_get("/users"), indent=2)

@mcp.tool()
def list_accounts(page: int=1) -> str:
    """List CRM accounts."""
    return json.dumps(_get("/accounts", {"page": page}), indent=2)

@mcp.tool()
def get_crm_account(account_id: str) -> str:
    """Retrieve a CRM account."""
    return json.dumps(_get(f"/accounts/{account_id}"), indent=2)

@mcp.tool()
def list_job_openings(company_id: Optional[str]=None, page: int=1) -> str:
    """List job openings."""
    params = {"page": page}
    if company_id: params["company_id"] = company_id
    return json.dumps(_get("/job-openings", params), indent=2)

@mcp.tool()
def get_job_opening(job_opening_id: str) -> str:
    """Retrieve a job opening."""
    return json.dumps(_get(f"/job-openings/{job_opening_id}"), indent=2)

@mcp.tool()
def enrich_person(linkedin_url: Optional[str]=None, email: Optional[str]=None) -> str:
    """Enrich a single person."""
    body = {}
    if linkedin_url: body["linkedin_url"] = linkedin_url
    if email: body["email"] = email
    return json.dumps(_post("/people-enrichments/single", body), indent=2)

@mcp.tool()
def start_people_enrichment_batch(people: List[dict]) -> str:
    """Start a batch people enrichment."""
    return json.dumps(_post("/people-enrichments", {"people": people}), indent=2)

@mcp.tool()
def get_people_enrichment_results(enrichment_id: str) -> str:
    """Get people enrichment results."""
    return json.dumps(_get(f"/people-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def cancel_people_enrichment(enrichment_id: str) -> str:
    """Cancel people enrichment."""
    return json.dumps(_delete(f"/people-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def enrich_company(linkedin_url: Optional[str]=None, domain: Optional[str]=None) -> str:
    """Enrich a single company."""
    body = {}
    if linkedin_url: body["linkedin_url"] = linkedin_url
    if domain: body["domain"] = domain
    return json.dumps(_post("/company-enrichments/single", body), indent=2)

@mcp.tool()
def start_company_enrichment_batch(companies: List[dict]) -> str:
    """Start a batch company enrichment."""
    return json.dumps(_post("/company-enrichments", {"companies": companies}), indent=2)

@mcp.tool()
def get_company_enrichment_results(enrichment_id: str) -> str:
    """Get company enrichment results."""
    return json.dumps(_get(f"/company-enrichments/{enrichment_id}"), indent=2)

@mcp.tool()
def cancel_company_enrichment(enrichment_id: str) -> str:
    """Cancel company enrichment."""
    return json.dumps(_delete(f"/company-enrichments/{enrichment_id}"), indent=2)

app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
