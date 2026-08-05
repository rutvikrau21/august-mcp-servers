"""Attio MCP Server — comprehensive wrapper around the Attio REST API v2."""

import os
import json
from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("ATTIO_API_KEY", "a46ef67f2b875c2bd713f5e88b1c71cf9c59fba9a8eac1e9a5169f329d559b40")
BASE_URL = "https://api.attio.com/v2"

mcp = FastMCP("Attio", host="0.0.0.0")
app = mcp.streamable_http_app()


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def _get(path: str, params: dict | None = None) -> dict:
    url = BASE_URL + path
    with httpx.Client(timeout=30) as client:
        r = client.get(url, headers=_headers(), params=params or {})
    r.raise_for_status()
    return r.json()


def _post(path: str, body: dict | None = None) -> dict:
    url = BASE_URL + path
    with httpx.Client(timeout=30) as client:
        r = client.post(url, headers=_headers(), json=body or {})
    r.raise_for_status()
    return r.json()


def _put(path: str, body: dict | None = None) -> dict:
    url = BASE_URL + path
    with httpx.Client(timeout=30) as client:
        r = client.put(url, headers=_headers(), json=body or {})
    r.raise_for_status()
    return r.json()


def _patch(path: str, body: dict | None = None) -> dict:
    url = BASE_URL + path
    with httpx.Client(timeout=30) as client:
        r = client.patch(url, headers=_headers(), json=body or {})
    r.raise_for_status()
    return r.json()


def _delete(path: str) -> dict:
    url = BASE_URL + path
    with httpx.Client(timeout=30) as client:
        r = client.delete(url, headers=_headers())
    if r.status_code == 204:
        return {"success": True}
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Workspace
# ---------------------------------------------------------------------------


@mcp.tool()
def get_self() -> str:
    """Return information about the current authenticated workspace and user."""
    return json.dumps(_get("/self"), indent=2)


@mcp.tool()
def list_workspace_members() -> str:
    """List all members of the workspace."""
    return json.dumps(_get("/workspace_members"), indent=2)


@mcp.tool()
def get_workspace_member(member_id: str) -> str:
    """
    Get a specific workspace member by ID.

    Args:
        member_id: The workspace member ID (UUID).
    """
    return json.dumps(_get(f"/workspace_members/{member_id}"), indent=2)


# ---------------------------------------------------------------------------
# Objects (schema)
# ---------------------------------------------------------------------------


@mcp.tool()
def list_objects() -> str:
    """List all objects (people, companies, deals, custom objects) in the workspace."""
    return json.dumps(_get("/objects"), indent=2)


@mcp.tool()
def get_object(object_slug: str) -> str:
    """
    Get the schema for a specific object type.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals', or a custom slug.
    """
    return json.dumps(_get(f"/objects/{object_slug}"), indent=2)


@mcp.tool()
def list_attributes(object_slug: str) -> str:
    """
    List all attributes defined on an object type.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
    """
    return json.dumps(_get(f"/objects/{object_slug}/attributes"), indent=2)


@mcp.tool()
def get_attribute(object_slug: str, attribute_slug: str) -> str:
    """
    Get a specific attribute definition on an object type.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        attribute_slug: The attribute slug (e.g. 'email_addresses', 'name').
    """
    return json.dumps(_get(f"/objects/{object_slug}/attributes/{attribute_slug}"), indent=2)


@mcp.tool()
def list_statuses(object_slug: str, attribute_slug: str) -> str:
    """
    List the allowed statuses for a status-type attribute.

    Args:
        object_slug: e.g. 'deals'.
        attribute_slug: The status attribute slug (e.g. 'stage').
    """
    return json.dumps(_get(f"/objects/{object_slug}/attributes/{attribute_slug}/statuses"), indent=2)


@mcp.tool()
def list_select_options(object_slug: str, attribute_slug: str) -> str:
    """
    List allowed options for a select-type attribute.

    Args:
        object_slug: e.g. 'people'.
        attribute_slug: The select attribute slug.
    """
    return json.dumps(_get(f"/objects/{object_slug}/attributes/{attribute_slug}/options"), indent=2)


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------


@mcp.tool()
def query_records(
    object_slug: str,
    filter_by: Optional[dict] = None,
    sorts: Optional[list] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """
    Query records for any object type with optional filtering and sorting.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        filter_by: Filter object. Examples:
                   {"name": {"$contains": "Acme"}}
                   {"email_addresses": {"email_address": {"$eq": "john@example.com"}}}
                   {"domains": {"domain": {"$eq": "acme.com"}}}
                   Operators: $eq, $not_eq, $contains, $gt, $gte, $lt, $lte, $is_empty, $not_empty.
                   Note: use $contains for name/text fields, $eq for exact matches.
                   Optional.
        sorts: Array of sort objects, e.g. [{"attribute": "name", "direction": "asc"}]. Optional.
        limit: Max number of records to return (default 20, max 500).
        offset: Number of records to skip for pagination (default 0).
    """
    body: dict[str, Any] = {"limit": limit, "offset": offset}
    if filter_by:
        body["filter"] = filter_by
    if sorts:
        body["sorts"] = sorts
    return json.dumps(_post(f"/objects/{object_slug}/records/query", body), indent=2)


@mcp.tool()
def get_record(object_slug: str, record_id: str) -> str:
    """
    Get a single record by ID.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        record_id: The record UUID.
    """
    return json.dumps(_get(f"/objects/{object_slug}/records/{record_id}"), indent=2)


@mcp.tool()
def create_record(object_slug: str, values: dict) -> str:
    """
    Create a new record with raw attribute values.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        values: Dict of attribute values. Each key is an attribute slug and the value
                is a list of value objects appropriate for that attribute type.
                Example for a person:
                  {"name": [{"first_name": "Jane", "last_name": "Doe", "full_name": "Jane Doe"}],
                   "email_addresses": [{"email_address": "jane@example.com"}]}
                Example for a company:
                  {"name": [{"value": "Acme Corp"}], "domains": [{"domain": "acme.com"}]}
    """
    body = {"data": {"values": values}}
    return json.dumps(_post(f"/objects/{object_slug}/records", body), indent=2)


@mcp.tool()
def update_record(object_slug: str, record_id: str, values: dict) -> str:
    """
    Update attribute values on an existing record (PATCH — partial update).

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        record_id: The record UUID.
        values: Dict of attribute values to update (same format as create_record values).
    """
    body = {"data": {"values": values}}
    return json.dumps(_patch(f"/objects/{object_slug}/records/{record_id}", body), indent=2)


@mcp.tool()
def upsert_record(object_slug: str, matching_attribute: str, values: dict) -> str:
    """
    Create a record or update it if one already exists matching the given attribute.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        matching_attribute: Attribute slug used as the unique key for matching,
                            e.g. 'email_addresses' for people, 'domains' for companies.
        values: Dict of attribute values (same format as create_record values).
    """
    body = {
        "data": {
            "matching_attribute": matching_attribute,
            "values": values,
        }
    }
    return json.dumps(_put(f"/objects/{object_slug}/records", body), indent=2)


@mcp.tool()
def delete_record(object_slug: str, record_id: str) -> str:
    """
    Delete a record permanently.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        record_id: The record UUID.
    """
    return json.dumps(_delete(f"/objects/{object_slug}/records/{record_id}"), indent=2)


# ---------------------------------------------------------------------------
# Attribute values
# ---------------------------------------------------------------------------


@mcp.tool()
def get_attribute_values(object_slug: str, record_id: str, attribute_slug: str) -> str:
    """
    Get all values for a specific attribute on a record.

    Args:
        object_slug: e.g. 'people', 'companies'.
        record_id: The record UUID.
        attribute_slug: e.g. 'email_addresses', 'phone_numbers', 'name'.
    """
    return json.dumps(
        _get(f"/objects/{object_slug}/records/{record_id}/attributes/{attribute_slug}/values"),
        indent=2,
    )


@mcp.tool()
def set_attribute_values(
    object_slug: str, record_id: str, attribute_slug: str, values: list
) -> str:
    """
    Replace all values for a specific attribute on a record.

    Args:
        object_slug: e.g. 'people', 'companies'.
        record_id: The record UUID.
        attribute_slug: e.g. 'email_addresses'.
        values: Array of value objects appropriate for the attribute type.
                Example for email: [{"email_address": "new@example.com"}]
                Example for text: [{"value": "some text"}]
    """
    body = {"data": values}
    return json.dumps(
        _put(f"/objects/{object_slug}/records/{record_id}/attributes/{attribute_slug}/values", body),
        indent=2,
    )


@mcp.tool()
def delete_attribute_value(
    object_slug: str, record_id: str, attribute_slug: str, value_id: str
) -> str:
    """
    Delete a specific value instance for an attribute on a record.

    Args:
        object_slug: e.g. 'people', 'companies'.
        record_id: The record UUID.
        attribute_slug: e.g. 'email_addresses'.
        value_id: The value UUID to delete (returned in attribute value listings).
    """
    return json.dumps(
        _delete(
            f"/objects/{object_slug}/records/{record_id}/attributes/{attribute_slug}/values/{value_id}"
        ),
        indent=2,
    )


# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------


@mcp.tool()
def list_notes(
    record_id: Optional[str] = None,
    object_slug: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """
    List notes, optionally filtered to a specific record.

    Args:
        record_id: Filter to notes attached to this record UUID. Optional.
        object_slug: Required when record_id is provided — e.g. 'people'. Optional.
        limit: Max results (default 20).
        offset: Pagination offset (default 0).
    """
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if record_id and object_slug:
        params["parent_object"] = object_slug
        params["parent_record_id"] = record_id
    return json.dumps(_get("/notes", params), indent=2)


@mcp.tool()
def get_note(note_id: str) -> str:
    """
    Get a specific note by ID.

    Args:
        note_id: The note UUID.
    """
    return json.dumps(_get(f"/notes/{note_id}"), indent=2)


@mcp.tool()
def create_note(
    object_slug: str,
    record_id: str,
    title: str,
    content: str,
    format: str = "plaintext",
    created_at: Optional[str] = None,
) -> str:
    """
    Create a note on a record.

    Args:
        object_slug: The object type the note belongs to, e.g. 'people', 'companies'.
        record_id: The record UUID to attach the note to.
        title: Note title.
        content: Note body text.
        format: Content format — 'plaintext' or 'markdown' (default 'plaintext').
        created_at: ISO 8601 timestamp for the note date (optional, defaults to now).
    """
    body: dict[str, Any] = {
        "data": {
            "parent_object": object_slug,
            "parent_record_id": record_id,
            "title": title,
            "content": content,
            "format": format,
        }
    }
    if created_at:
        body["data"]["created_at"] = created_at
    return json.dumps(_post("/notes", body), indent=2)


@mcp.tool()
def update_note(note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> str:
    """
    Update a note's title or content.

    Args:
        note_id: The note UUID.
        title: New title (optional).
        content: New content body (optional).
    """
    data: dict[str, Any] = {}
    if title is not None:
        data["title"] = title
    if content is not None:
        data["content"] = content
    return json.dumps(_patch(f"/notes/{note_id}", {"data": data}), indent=2)


@mcp.tool()
def delete_note(note_id: str) -> str:
    """
    Delete a note.

    Args:
        note_id: The note UUID.
    """
    return json.dumps(_delete(f"/notes/{note_id}"), indent=2)


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------


@mcp.tool()
def list_tasks(
    linked_record_id: Optional[str] = None,
    linked_object_slug: Optional[str] = None,
    is_completed: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """
    List tasks, optionally filtered by linked record or completion status.

    Args:
        linked_record_id: Filter to tasks linked to this record UUID. Optional.
        linked_object_slug: Required when linked_record_id provided, e.g. 'people'. Optional.
        is_completed: Filter by completion status (true/false). Optional.
        limit: Max results (default 20).
        offset: Pagination offset (default 0).
    """
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if linked_record_id and linked_object_slug:
        params["linked_object"] = linked_object_slug
        params["linked_record_id"] = linked_record_id
    if is_completed is not None:
        params["is_completed"] = str(is_completed).lower()
    return json.dumps(_get("/tasks", params), indent=2)


@mcp.tool()
def get_task(task_id: str) -> str:
    """
    Get a specific task by ID.

    Args:
        task_id: The task UUID.
    """
    return json.dumps(_get(f"/tasks/{task_id}"), indent=2)


@mcp.tool()
def create_task(
    content: str,
    linked_records: Optional[list] = None,
    assignees: Optional[list] = None,
    deadline_at: Optional[str] = None,
    is_completed: bool = False,
) -> str:
    """
    Create a new task.

    Args:
        content: Task description text.
        linked_records: Array of linked record objects, e.g.
                        [{"target_object": "people", "target_record_id": "<uuid>"}]. Optional.
        assignees: Array of assignee objects, e.g.
                   [{"referenced_actor_type": "workspace-member", "referenced_actor_id": "<uuid>"}].
                   Optional.
        deadline_at: ISO 8601 timestamp for the deadline. Optional.
        is_completed: Whether the task starts as completed (default false).
    """
    data: dict[str, Any] = {
        "content": content,
        "format": "plaintext",
        "is_completed": is_completed,
        "deadline_at": deadline_at,
        "assignees": assignees or [],
        "linked_records": linked_records or [],
    }
    return json.dumps(_post("/tasks", {"data": data}), indent=2)


@mcp.tool()
def update_task(
    task_id: str,
    content: Optional[str] = None,
    is_completed: Optional[bool] = None,
    deadline_at: Optional[str] = None,
    assignees: Optional[list] = None,
    linked_records: Optional[list] = None,
) -> str:
    """
    Update an existing task.

    Args:
        task_id: The task UUID.
        content: New task description. Optional.
        is_completed: Mark as completed or not. Optional.
        deadline_at: New deadline ISO 8601 timestamp. Optional.
        assignees: New array of assignee objects (replaces existing). Optional.
        linked_records: New array of linked record objects (replaces existing). Optional.
    """
    data: dict[str, Any] = {}
    if content is not None:
        data["content"] = content
    if is_completed is not None:
        data["is_completed"] = is_completed
    if deadline_at is not None:
        data["deadline_at"] = deadline_at
    if assignees is not None:
        data["assignees"] = assignees
    if linked_records is not None:
        data["linked_records"] = linked_records
    return json.dumps(_patch(f"/tasks/{task_id}", {"data": data}), indent=2)


@mcp.tool()
def delete_task(task_id: str) -> str:
    """
    Delete a task.

    Args:
        task_id: The task UUID.
    """
    return json.dumps(_delete(f"/tasks/{task_id}"), indent=2)


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------


@mcp.tool()
def list_lists() -> str:
    """List all lists in the workspace."""
    return json.dumps(_get("/lists"), indent=2)


@mcp.tool()
def get_list(list_id: str) -> str:
    """
    Get a specific list by ID.

    Args:
        list_id: The list UUID or slug.
    """
    return json.dumps(_get(f"/lists/{list_id}"), indent=2)


@mcp.tool()
def create_list(name: str, object_slug: str) -> str:
    """
    Create a new list for a given object type.

    Args:
        name: Display name for the list.
        object_slug: The object type records in this list will be, e.g. 'companies', 'people'.
    """
    body = {
        "data": {
            "name": name,
            "api_slug": name.lower().replace(" ", "_"),
            "object_singular_noun": object_slug,
        }
    }
    return json.dumps(_post("/lists", body), indent=2)


@mcp.tool()
def update_list(list_id: str, name: Optional[str] = None) -> str:
    """
    Update a list's properties.

    Args:
        list_id: The list UUID.
        name: New display name. Optional.
    """
    data: dict[str, Any] = {}
    if name is not None:
        data["name"] = name
    return json.dumps(_patch(f"/lists/{list_id}", {"data": data}), indent=2)


@mcp.tool()
def delete_list(list_id: str) -> str:
    """
    Delete a list.

    Args:
        list_id: The list UUID.
    """
    return json.dumps(_delete(f"/lists/{list_id}"), indent=2)


@mcp.tool()
def list_list_attributes(list_id: str) -> str:
    """
    List the attributes defined on a list (list-level columns).

    Args:
        list_id: The list UUID.
    """
    return json.dumps(_get(f"/lists/{list_id}/attributes"), indent=2)


# ---------------------------------------------------------------------------
# List entries
# ---------------------------------------------------------------------------


@mcp.tool()
def query_list_entries(
    list_id: str,
    filter_by: Optional[dict] = None,
    sorts: Optional[list] = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """
    Query entries in a list with optional filtering and sorting.

    Args:
        list_id: The list UUID or slug.
        filter_by: Filter object (same structure as query_records filter_by). Optional.
        sorts: Array of sort objects. Optional.
        limit: Max results (default 20, max 500).
        offset: Pagination offset (default 0).
    """
    body: dict[str, Any] = {"limit": limit, "offset": offset}
    if filter_by:
        body["filter"] = filter_by
    if sorts:
        body["sorts"] = sorts
    return json.dumps(_post(f"/lists/{list_id}/entries/query", body), indent=2)


@mcp.tool()
def get_list_entry(list_id: str, entry_id: str) -> str:
    """
    Get a specific list entry.

    Args:
        list_id: The list UUID.
        entry_id: The entry UUID.
    """
    return json.dumps(_get(f"/lists/{list_id}/entries/{entry_id}"), indent=2)


@mcp.tool()
def create_list_entry(
    list_id: str,
    record_id: str,
    object_slug: str,
    entry_values: Optional[dict] = None,
) -> str:
    """
    Add a record to a list as a new entry.

    Args:
        list_id: The list UUID.
        record_id: The record UUID to add to the list.
        object_slug: The object type of the record, e.g. 'companies', 'people'.
        entry_values: Dict of list-entry attribute values (list-level columns). Optional.
    """
    data: dict[str, Any] = {
        "parent_record_id": record_id,
        "parent_object": object_slug,
    }
    if entry_values:
        data["entry_values"] = entry_values
    return json.dumps(_post(f"/lists/{list_id}/entries", {"data": data}), indent=2)


@mcp.tool()
def update_list_entry(list_id: str, entry_id: str, entry_values: dict) -> str:
    """
    Update list-entry attribute values for an entry.

    Args:
        list_id: The list UUID.
        entry_id: The entry UUID.
        entry_values: Dict of list-entry attribute values to update.
    """
    body = {"data": {"entry_values": entry_values}}
    return json.dumps(_patch(f"/lists/{list_id}/entries/{entry_id}", body), indent=2)


@mcp.tool()
def delete_list_entry(list_id: str, entry_id: str) -> str:
    """
    Remove an entry from a list.

    Args:
        list_id: The list UUID.
        entry_id: The entry UUID.
    """
    return json.dumps(_delete(f"/lists/{list_id}/entries/{entry_id}"), indent=2)


@mcp.tool()
def get_list_entry_attribute_values(list_id: str, entry_id: str, attribute_slug: str) -> str:
    """
    Get values for a specific attribute on a list entry.

    Args:
        list_id: The list UUID.
        entry_id: The entry UUID.
        attribute_slug: The attribute slug.
    """
    return json.dumps(
        _get(f"/lists/{list_id}/entries/{entry_id}/attributes/{attribute_slug}/values"),
        indent=2,
    )


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


@mcp.tool()
def list_webhooks() -> str:
    """List all webhooks configured in the workspace."""
    return json.dumps(_get("/webhooks"), indent=2)


@mcp.tool()
def get_webhook(webhook_id: str) -> str:
    """
    Get a specific webhook by ID.

    Args:
        webhook_id: The webhook UUID.
    """
    return json.dumps(_get(f"/webhooks/{webhook_id}"), indent=2)


@mcp.tool()
def create_webhook(target_url: str, subscriptions: list) -> str:
    """
    Create a new webhook.

    Args:
        target_url: The HTTPS URL that Attio will POST events to.
        subscriptions: Array of event subscription objects, e.g.
                       [{"event_type": "record.created", "object_slug": "people"},
                        {"event_type": "note.created"}].
                       Supported event types: record.created, record.updated, record.deleted,
                       note.created, note.deleted, task.created, task.completed, task.deleted,
                       attribute-value.created, attribute-value.deleted.
    """
    body = {
        "data": {
            "target_url": target_url,
            "subscriptions": subscriptions,
        }
    }
    return json.dumps(_post("/webhooks", body), indent=2)


@mcp.tool()
def update_webhook(
    webhook_id: str,
    target_url: Optional[str] = None,
    subscriptions: Optional[list] = None,
) -> str:
    """
    Update a webhook's URL or subscriptions.

    Args:
        webhook_id: The webhook UUID.
        target_url: New target URL. Optional.
        subscriptions: New array of subscription objects (replaces all existing). Optional.
    """
    data: dict[str, Any] = {}
    if target_url is not None:
        data["target_url"] = target_url
    if subscriptions is not None:
        data["subscriptions"] = subscriptions
    return json.dumps(_patch(f"/webhooks/{webhook_id}", {"data": data}), indent=2)


@mcp.tool()
def delete_webhook(webhook_id: str) -> str:
    """
    Delete a webhook.

    Args:
        webhook_id: The webhook UUID.
    """
    return json.dumps(_delete(f"/webhooks/{webhook_id}"), indent=2)


# ---------------------------------------------------------------------------
# Thread comments
# ---------------------------------------------------------------------------


@mcp.tool()
def list_comments(thread_id: str) -> str:
    """
    List all comments in a thread.

    Args:
        thread_id: The thread UUID (returned in record views).
    """
    return json.dumps(_get(f"/threads/{thread_id}/comments"), indent=2)


@mcp.tool()
def create_comment(thread_id: str, content: str) -> str:
    """
    Add a comment to an existing thread.

    Args:
        thread_id: The thread UUID.
        content: Comment text content.
    """
    body = {"data": {"content": content}}
    return json.dumps(_post(f"/threads/{thread_id}/comments", body), indent=2)


@mcp.tool()
def delete_comment(thread_id: str, comment_id: str) -> str:
    """
    Delete a comment from a thread.

    Args:
        thread_id: The thread UUID.
        comment_id: The comment UUID.
    """
    return json.dumps(_delete(f"/threads/{thread_id}/comments/{comment_id}"), indent=2)


# ---------------------------------------------------------------------------
# Convenience: people helpers
# ---------------------------------------------------------------------------


@mcp.tool()
def search_people(query: str, limit: int = 20) -> str:
    """
    Search people records by name (partial match).

    Args:
        query: Name string to search for (partial match).
        limit: Max results (default 20).
    """
    body = {
        "filter": {"name": {"$contains": query}},
        "limit": limit,
        "offset": 0,
    }
    try:
        return json.dumps(_post("/objects/people/records/query", body), indent=2)
    except httpx.HTTPStatusError:
        return json.dumps(_post("/objects/people/records/query", {"limit": limit, "offset": 0}), indent=2)


@mcp.tool()
def search_companies(query: str, limit: int = 20) -> str:
    """
    Search company records by name (partial match).

    Args:
        query: Company name string to search for (partial match).
        limit: Max results (default 20).
    """
    body = {
        "filter": {"name": {"$contains": query}},
        "limit": limit,
        "offset": 0,
    }
    try:
        return json.dumps(_post("/objects/companies/records/query", body), indent=2)
    except httpx.HTTPStatusError:
        return json.dumps(_post("/objects/companies/records/query", {"limit": limit, "offset": 0}), indent=2)


@mcp.tool()
def find_person_by_email(email: str) -> str:
    """
    Look up a person record by exact email address.

    Args:
        email: The email address to search for.
    """
    body = {
        "filter": {"email_addresses": {"email_address": {"$eq": email}}},
        "limit": 5,
        "offset": 0,
    }
    return json.dumps(_post("/objects/people/records/query", body), indent=2)


@mcp.tool()
def find_company_by_domain(domain: str) -> str:
    """
    Look up a company record by website domain.

    Args:
        domain: The domain to search for, e.g. 'acme.com'.
    """
    body = {
        "filter": {"domains": {"domain": {"$eq": domain}}},
        "limit": 5,
        "offset": 0,
    }
    return json.dumps(_post("/objects/companies/records/query", body), indent=2)


# ---------------------------------------------------------------------------
# Deals helpers
# ---------------------------------------------------------------------------


@mcp.tool()
def list_deals(limit: int = 20, offset: int = 0) -> str:
    """
    List deal records.

    Args:
        limit: Max results (default 20).
        offset: Pagination offset (default 0).
    """
    return json.dumps(_post("/objects/deals/records/query", {"limit": limit, "offset": offset}), indent=2)


# ---------------------------------------------------------------------------
# Convenience: create person / company
# ---------------------------------------------------------------------------


@mcp.tool()
def create_person(
    first_name: str,
    last_name: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    company_id: Optional[str] = None,
    job_title: Optional[str] = None,
    linkedin_url: Optional[str] = None,
) -> str:
    """
    Create a person record with common fields.

    Args:
        first_name: Person's first name.
        last_name: Person's last name.
        email: Primary email address. Optional.
        phone: Primary phone number. Optional.
        company_id: UUID of the company record to link. Optional.
        job_title: Job title. Optional.
        linkedin_url: LinkedIn profile URL. Optional.
    """
    values: dict[str, Any] = {
        "name": [{"first_name": first_name, "last_name": last_name, "full_name": f"{first_name} {last_name}"}],
    }
    if email:
        values["email_addresses"] = [{"email_address": email}]
    if phone:
        values["phone_numbers"] = [{"phone_number": phone}]
    if company_id:
        values["company"] = [{"target_object": "companies", "target_record_id": company_id}]
    if job_title:
        values["job_title"] = [{"value": job_title}]
    if linkedin_url:
        values["linkedin"] = [{"value": linkedin_url}]
    body = {"data": {"values": values}}
    return json.dumps(_post("/objects/people/records", body), indent=2)


@mcp.tool()
def create_company(
    name: str,
    domain: Optional[str] = None,
    description: Optional[str] = None,
    linkedin_url: Optional[str] = None,
) -> str:
    """
    Create a company record with common fields.

    Args:
        name: Company name.
        domain: Primary website domain, e.g. 'acme.com'. Optional.
        description: Short description. Optional.
        linkedin_url: LinkedIn company page URL. Optional.
    """
    values: dict[str, Any] = {
        "name": [{"value": name}],
    }
    if domain:
        values["domains"] = [{"domain": domain}]
    if description:
        values["description"] = [{"value": description}]
    if linkedin_url:
        values["linkedin"] = [{"value": linkedin_url}]
    body = {"data": {"values": values}}
    return json.dumps(_post("/objects/companies/records", body), indent=2)


# ---------------------------------------------------------------------------
# Threads (correct comment API)
# ---------------------------------------------------------------------------


@mcp.tool()
def list_threads_for_record(
    object_slug: str,
    record_id: str,
    limit: int = 20,
) -> str:
    """
    List all comment threads on a specific record.

    Args:
        object_slug: Object type, e.g. 'people', 'companies', 'deals'.
        record_id: The record UUID.
        limit: Max results (default 20, max 50).
    """
    params: dict[str, Any] = {
        "object": object_slug,
        "record_id": record_id,
        "limit": min(limit, 50),
    }
    return json.dumps(_get("/threads", params), indent=2)


@mcp.tool()
def list_threads_for_entry(
    list_id: str,
    entry_id: str,
    limit: int = 20,
) -> str:
    """
    List all comment threads on a specific list entry.

    Args:
        list_id: The list UUID.
        entry_id: The list entry UUID.
        limit: Max results (default 20, max 50).
    """
    params: dict[str, Any] = {
        "list": list_id,
        "entry_id": entry_id,
        "limit": min(limit, 50),
    }
    return json.dumps(_get("/threads", params), indent=2)


@mcp.tool()
def get_thread(thread_id: str) -> str:
    """
    Get a thread with all its comments.

    Args:
        thread_id: The thread UUID.
    """
    return json.dumps(_get(f"/threads/{thread_id}"), indent=2)


@mcp.tool()
def get_comment(comment_id: str) -> str:
    """
    Get a single comment by ID.

    Args:
        comment_id: The comment UUID.
    """
    return json.dumps(_get(f"/comments/{comment_id}"), indent=2)


@mcp.tool()
def create_comment_on_record(
    object_slug: str,
    record_id: str,
    content: str,
    thread_id: Optional[str] = None,
) -> str:
    """
    Create a comment on a record (starts a new thread or replies to existing).

    Args:
        object_slug: The object type, e.g. 'people', 'companies'.
        record_id: The record UUID.
        content: Comment text.
        thread_id: Reply to an existing thread UUID. If omitted, starts a new thread. Optional.
    """
    body: dict[str, Any] = {
        "data": {
            "record_id": record_id,
            "record_object": object_slug,
            "content": [{"type": "text", "text": content}],
        }
    }
    if thread_id:
        body["data"]["thread_id"] = thread_id
    return json.dumps(_post("/comments", body), indent=2)


@mcp.tool()
def delete_comment_by_id(comment_id: str) -> str:
    """
    Delete a comment. If it's the first comment in a thread, the entire thread is deleted.

    Args:
        comment_id: The comment UUID.
    """
    return json.dumps(_delete(f"/comments/{comment_id}"), indent=2)


# ---------------------------------------------------------------------------
# SQL queries
# ---------------------------------------------------------------------------


@mcp.tool()
def run_sql(query: str) -> str:
    """
    Execute a read-only SQL query against your Attio workspace data.

    This is extremely powerful — you can join across objects, filter by any attribute,
    aggregate, and alias columns.

    IMPORTANT: Field names must use the format `object.attribute_slug` (not bare column names).
    Use list_attributes() to discover valid attribute slugs for each object.

    Examples:
      SELECT people.record_id, people.name FROM people LIMIT 10
      SELECT companies.record_id, companies.name FROM companies LIMIT 10
      SELECT people.record_id, people.name, people.email_addresses, people.job_title
        FROM people WHERE people.name IS NOT NULL LIMIT 20
      SELECT tasks.task_id, tasks.content_plaintext, tasks.is_completed
        FROM tasks WHERE tasks.is_completed = false LIMIT 20

    Args:
        query: A read-only SQL SELECT statement.
    """
    body = {"sql": query}
    return json.dumps(_post("/sql", body), indent=2)


# ---------------------------------------------------------------------------
# Meetings (Beta)
# ---------------------------------------------------------------------------


@mcp.tool()
def list_meetings(
    limit: int = 20,
    offset: int = 0,
    record_id: Optional[str] = None,
    object_slug: Optional[str] = None,
) -> str:
    """
    List meetings recorded in Attio (Beta feature).

    Args:
        limit: Max results (default 20).
        offset: Pagination offset (default 0).
        record_id: Filter by linked record UUID. Optional.
        object_slug: Object type for record filter, e.g. 'people'. Optional.
    """
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if record_id and object_slug:
        params["record_id"] = record_id
        params["object"] = object_slug
    return json.dumps(_get("/meetings", params), indent=2)


@mcp.tool()
def get_meeting(meeting_id: str) -> str:
    """
    Get a specific meeting by ID.

    Args:
        meeting_id: The meeting UUID.
    """
    return json.dumps(_get(f"/meetings/{meeting_id}"), indent=2)


@mcp.tool()
def list_call_recordings(meeting_id: str) -> str:
    """
    List call recordings for a meeting.

    Args:
        meeting_id: The meeting UUID.
    """
    return json.dumps(_get(f"/meetings/{meeting_id}/call_recordings"), indent=2)


@mcp.tool()
def get_call_recording(meeting_id: str, recording_id: str) -> str:
    """
    Get a specific call recording.

    Args:
        meeting_id: The meeting UUID.
        recording_id: The recording UUID.
    """
    return json.dumps(_get(f"/meetings/{meeting_id}/call_recordings/{recording_id}"), indent=2)


@mcp.tool()
def get_call_transcript(
    meeting_id: str, recording_id: str, limit: int = 50, cursor: Optional[str] = None
) -> str:
    """
    Get the transcript for a call recording (cursor-paginated segments).

    Args:
        meeting_id: The meeting UUID.
        recording_id: The recording UUID.
        limit: Max transcript segments to return (default 50).
        cursor: Pagination cursor from a previous response. Optional.
    """
    params: dict[str, Any] = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    return json.dumps(
        _get(f"/meetings/{meeting_id}/call_recordings/{recording_id}/transcript", params),
        indent=2,
    )


# ---------------------------------------------------------------------------
# Object / attribute schema management
# ---------------------------------------------------------------------------


@mcp.tool()
def create_object(api_slug: str, singular_noun: str, plural_noun: str) -> str:
    """
    Create a custom object type in the workspace.

    Args:
        api_slug: URL-safe identifier, e.g. 'vendors'. Must be lowercase with underscores.
        singular_noun: Human-readable singular name, e.g. 'Vendor'.
        plural_noun: Human-readable plural name, e.g. 'Vendors'.
    """
    body = {
        "data": {
            "api_slug": api_slug,
            "singular_noun": singular_noun,
            "plural_noun": plural_noun,
        }
    }
    return json.dumps(_post("/objects", body), indent=2)


@mcp.tool()
def update_object(object_slug: str, singular_noun: Optional[str] = None, plural_noun: Optional[str] = None) -> str:
    """
    Update a custom object's display name.

    Args:
        object_slug: The object's API slug.
        singular_noun: New singular name. Optional.
        plural_noun: New plural name. Optional.
    """
    data: dict[str, Any] = {}
    if singular_noun is not None:
        data["singular_noun"] = singular_noun
    if plural_noun is not None:
        data["plural_noun"] = plural_noun
    return json.dumps(_patch(f"/objects/{object_slug}", {"data": data}), indent=2)


@mcp.tool()
def create_attribute(
    object_slug: str,
    api_slug: str,
    title: str,
    attribute_type: str,
    is_required: bool = False,
    is_unique: bool = False,
    config: Optional[dict] = None,
) -> str:
    """
    Create a new attribute on an object type.

    Args:
        object_slug: The object to add the attribute to, e.g. 'people'.
        api_slug: URL-safe attribute identifier, e.g. 'contract_value'.
        title: Display name, e.g. 'Contract Value'.
        attribute_type: One of: text, number, checkbox, currency, date, timestamp, location,
                        rating, status, select, multi_select, record_reference, actor_reference,
                        email_address, phone_number, domain, interaction.
        is_required: Whether the attribute is required on all records (default false).
        is_unique: Whether values must be unique across all records (default false).
        config: Additional type-specific config dict. Optional.
                For currency: {"currency_code": "USD"}
                For record_reference: {"relationship": {"target_object": "companies"}}
    """
    data: dict[str, Any] = {
        "api_slug": api_slug,
        "title": title,
        "type": attribute_type,
        "is_required": is_required,
        "is_unique": is_unique,
    }
    if config:
        data.update(config)
    return json.dumps(_post(f"/objects/{object_slug}/attributes", {"data": data}), indent=2)


@mcp.tool()
def update_attribute(
    object_slug: str,
    attribute_slug: str,
    title: Optional[str] = None,
    is_required: Optional[bool] = None,
) -> str:
    """
    Update an attribute's title or required flag.

    Args:
        object_slug: The object the attribute belongs to, e.g. 'people'.
        attribute_slug: The attribute's API slug.
        title: New display name. Optional.
        is_required: New required flag. Optional.
    """
    data: dict[str, Any] = {}
    if title is not None:
        data["title"] = title
    if is_required is not None:
        data["is_required"] = is_required
    return json.dumps(_patch(f"/objects/{object_slug}/attributes/{attribute_slug}", {"data": data}), indent=2)


@mcp.tool()
def create_select_option(object_slug: str, attribute_slug: str, title: str, color: Optional[str] = None) -> str:
    """
    Add a new option to a select or multi-select attribute.

    Args:
        object_slug: The object the attribute belongs to.
        attribute_slug: The select attribute slug.
        title: Option display name.
        color: Optional color name, e.g. 'red', 'green', 'blue', 'yellow', 'purple'.
    """
    data: dict[str, Any] = {"title": title}
    if color:
        data["color"] = color
    return json.dumps(
        _post(f"/objects/{object_slug}/attributes/{attribute_slug}/options", {"data": data}),
        indent=2,
    )


@mcp.tool()
def create_status(object_slug: str, attribute_slug: str, title: str, color: Optional[str] = None) -> str:
    """
    Add a new status option to a status-type attribute.

    Args:
        object_slug: The object the attribute belongs to.
        attribute_slug: The status attribute slug.
        title: Status display name.
        color: Optional color name.
    """
    data: dict[str, Any] = {"title": title}
    if color:
        data["color"] = color
    return json.dumps(
        _post(f"/objects/{object_slug}/attributes/{attribute_slug}/statuses", {"data": data}),
        indent=2,
    )



# ---------------------------------------------------------------------------
# Record entries (list memberships for a given record)
# ---------------------------------------------------------------------------


@mcp.tool()
def get_record_list_entries(object_slug: str, record_id: str) -> str:
    """
    Get all list entries (list memberships) for a specific record.

    Useful for finding which lists a person or company belongs to.

    Args:
        object_slug: The object type, e.g. 'people', 'companies'.
        record_id: The record UUID.
    """
    return json.dumps(_get(f"/objects/{object_slug}/records/{record_id}/entries"), indent=2)


# ---------------------------------------------------------------------------
# List entry upsert
# ---------------------------------------------------------------------------


@mcp.tool()
def upsert_list_entry(list_id: str, record_id: str, object_slug: str, entry_values: Optional[dict] = None) -> str:
    """
    Add a record to a list, or update its entry if it already exists (upsert by parent record).

    Args:
        list_id: The list UUID.
        record_id: The record UUID to add/update.
        object_slug: The object type of the record, e.g. 'companies', 'people'.
        entry_values: Dict of list-entry attribute values. Optional.
    """
    data: dict[str, Any] = {
        "parent_record_id": record_id,
        "parent_object": object_slug,
    }
    if entry_values:
        data["entry_values"] = entry_values
    return json.dumps(_put(f"/lists/{list_id}/entries", {"data": data}), indent=2)


@mcp.tool()
def overwrite_list_entry(list_id: str, entry_id: str, entry_values: dict) -> str:
    """
    Overwrite all values for a list entry (PUT — replaces multi-select values entirely).
    Use update_list_entry (PATCH) to append to multi-selects instead.

    Args:
        list_id: The list UUID.
        entry_id: The entry UUID.
        entry_values: Dict of list-entry attribute values.
    """
    body = {"data": {"entry_values": entry_values}}
    return json.dumps(_put(f"/lists/{list_id}/entries/{entry_id}", body), indent=2)


@mcp.tool()
def overwrite_record(object_slug: str, record_id: str, values: dict) -> str:
    """
    Overwrite attribute values on a record (PUT — replaces multi-select values entirely).
    Use update_record (PATCH) to append to multi-selects instead.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        record_id: The record UUID.
        values: Dict of attribute values (same format as create_record values).
    """
    body = {"data": {"values": values}}
    return json.dumps(_put(f"/objects/{object_slug}/records/{record_id}", body), indent=2)


# ---------------------------------------------------------------------------
# Email-workflow tools
#
# Attio's REST API does NOT expose email bodies or subjects — synced emails
# are only available in-product. What IS available:
#   • interaction attributes on records (last_email_interaction, last_interaction)
#     → gives you timestamp + which workspace member's mailbox was involved
#   • email addresses on person/company records → use these to search Gmail
#
# The three tools below are designed to power the full workflow:
#   1. query_interaction_batch  — last-email metadata for N records in 1 call
#   2. get_deal_contacts        — deal → people + companies with email addresses
#   3. write_email_summary_note — write a Gmail-sourced summary back to a record
# ---------------------------------------------------------------------------


@mcp.tool()
def query_interaction_batch(
    object_slug: str,
    record_ids: list,
) -> str:
    """
    Get last-interaction metadata for a batch of records in a single API call.

    Returns a slim array: [{record_id, name, last_interaction_at, last_interaction_type,
    last_email_interaction_at, owner_actor_id, owner_actor_type}, ...]

    Uses a single POST /records/query with $in filter — collapses N sequential
    get_record() calls into one round-trip.

    Note: Attio's interaction attributes give you WHEN and WHOSE MAILBOX the last
    email ran through, but NOT the email subject or body (those are not exposed by
    the API). Use get_deal_contacts to get email addresses, then search Gmail for
    actual message content.

    Args:
        object_slug: e.g. 'people', 'companies', 'deals'.
        record_ids: List of record UUID strings (up to 500).
    """
    body: dict[str, Any] = {
        "filter": {"record_id": {"$in": record_ids}},
        "limit": min(len(record_ids), 500),
        "offset": 0,
    }
    raw = _post(f"/objects/{object_slug}/records/query", body)

    results = []
    for record in raw.get("data", []):
        rid = record.get("id", {}).get("record_id")
        values = record.get("values", {})

        # Extract name
        name = None
        name_vals = values.get("name", [])
        if name_vals:
            name = name_vals[0].get("full_name") or name_vals[0].get("value")

        # Extract last_interaction (any type)
        last_interaction_at = None
        last_interaction_type = None
        li_vals = values.get("last_interaction", [])
        if li_vals:
            li = li_vals[0]
            last_interaction_at = li.get("interacted_at")
            last_interaction_type = li.get("type")

        # Extract last_email_interaction specifically
        last_email_at = None
        lei_vals = values.get("last_email_interaction", [])
        if lei_vals:
            last_email_at = lei_vals[0].get("interacted_at")

        # Extract owner actor from last_interaction
        owner_actor_id = None
        owner_actor_type = None
        if li_vals:
            actor = li_vals[0].get("owner_actor", {})
            owner_actor_id = actor.get("id")
            owner_actor_type = actor.get("type")

        results.append({
            "record_id": rid,
            "name": name,
            "last_interaction_at": last_interaction_at,
            "last_interaction_type": last_interaction_type,
            "last_email_interaction_at": last_email_at,
            "owner_actor_id": owner_actor_id,
            "owner_actor_type": owner_actor_type,
        })

    return json.dumps(results, indent=2)


@mcp.tool()
def get_deal_contacts(deal_id: str) -> str:
    """
    Given a deal ID, return all associated people and companies with their
    email addresses, phone numbers, and domains.

    This is the bridge between a deal and Gmail: take the returned email
    addresses and use them to search Gmail for email threads.

    Returns:
        {
          "deal": {id, name},
          "people": [{id, name, email_addresses: [...], job_title}],
          "companies": [{id, name, domains: [...], email_addresses: [...]}]
        }

    Args:
        deal_id: The deal record UUID.
    """
    deal = _get(f"/objects/deals/records/{deal_id}")
    deal_values = deal.get("data", deal).get("values", {})

    # Extract deal name
    deal_name = None
    for v in deal_values.get("name", []):
        deal_name = v.get("value") or v.get("full_name")
        if deal_name:
            break

    people_out: list[dict] = []
    companies_out: list[dict] = []

    # Collect referenced person IDs
    person_ids = [
        ref["target_record_id"]
        for ref in deal_values.get("people", [])
        if ref.get("target_record_id")
    ]
    # Collect referenced company IDs
    company_ids = [
        ref["target_record_id"]
        for ref in deal_values.get("associated_company", [])
        if ref.get("target_record_id")
    ]
    # Also check generic 'companies' reference attribute name
    company_ids += [
        ref["target_record_id"]
        for ref in deal_values.get("companies", [])
        if ref.get("target_record_id")
    ]

    # Batch-fetch people
    if person_ids:
        people_resp = _post("/objects/people/records/query", {
            "filter": {"record_id": {"$in": person_ids}},
            "limit": len(person_ids),
        })
        for p in people_resp.get("data", []):
            pid = p.get("id", {}).get("record_id")
            pv = p.get("values", {})
            name = None
            for v in pv.get("name", []):
                name = v.get("full_name") or v.get("value")
                if name:
                    break
            emails = [v.get("email_address") for v in pv.get("email_addresses", []) if v.get("email_address")]
            job_title = next((v.get("value") for v in pv.get("job_title", []) if v.get("value")), None)
            people_out.append({"id": pid, "name": name, "email_addresses": emails, "job_title": job_title})

    # Batch-fetch companies
    seen_company_ids = list(dict.fromkeys(company_ids))  # dedupe
    if seen_company_ids:
        cos_resp = _post("/objects/companies/records/query", {
            "filter": {"record_id": {"$in": seen_company_ids}},
            "limit": len(seen_company_ids),
        })
        for c in cos_resp.get("data", []):
            cid = c.get("id", {}).get("record_id")
            cv = c.get("values", {})
            name = next((v.get("value") for v in cv.get("name", []) if v.get("value")), None)
            domains = [v.get("domain") for v in cv.get("domains", []) if v.get("domain")]
            emails = [v.get("email_address") for v in cv.get("email_addresses", []) if v.get("email_address")]
            companies_out.append({"id": cid, "name": name, "domains": domains, "email_addresses": emails})

    return json.dumps({
        "deal": {"id": deal_id, "name": deal_name},
        "people": people_out,
        "companies": companies_out,
    }, indent=2)


@mcp.tool()
def write_email_summary_note(
    object_slug: str,
    record_id: str,
    summary: str,
    sourced_from: str = "Gmail",
) -> str:
    """
    Write an email-thread summary as a note on a deal, company, or person record.

    Use this after pulling email threads from Gmail and summarising them —
    it writes the summary back to Attio so it's visible on the record.

    The note title is auto-generated as "Email Summary (YYYY-MM-DD)" and the
    content is formatted as markdown.

    Args:
        object_slug: The object type, e.g. 'deals', 'companies', 'people'.
        record_id: The record UUID to attach the note to.
        summary: The email thread summary text (markdown supported).
        sourced_from: Label for where the summary came from (default 'Gmail').
    """
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = f"Email Summary ({today})"
    content = f"*Sourced from {sourced_from} — {today}*\n\n{summary}"
    body: dict[str, Any] = {
        "data": {
            "parent_object": object_slug,
            "parent_record_id": record_id,
            "title": title,
            "content": content,
            "format": "markdown",
        }
    }
    return json.dumps(_post("/notes", body), indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
