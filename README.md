# August MCP Servers

A monorepo of MCP servers for August Law's internal tooling. Each subdirectory is a self-contained MCP server with its own `Dockerfile`, `requirements.txt`, and `server.py`.

## Servers

| Server | Directory | Description |
|--------|-----------|-------------|
| August MCPs (all four) | `.` (root) | Amplemarket + OrangeSlice + Attio + August in one server, tools prefixed by service |
| Amplemarket | `amplemarket/` | Full Amplemarket API — contacts, sequences, enrichment, calls, tasks, exclusions |
| Attio | `attio/` | Full Attio CRM API — objects, records, attributes, notes, tasks, lists, webhooks |
| OrangeSlice | `orangeslice/` | Node.js sidecar — LinkedIn B2B DB, contact info, web search, Crunchbase |

## API keys are per connection

No keys are baked into these servers. Whoever connects supplies their own, so
several people can share one deployment and each spends their own credits.

A key is resolved fresh on every tool call, in this order:

1. **HTTP header** on the MCP request — `X-Amplemarket-Api-Key: amp_...`
2. **Query string** on the MCP server URL — `https://<host>/mcp?amplemarket_key=amp_...`
3. **Environment variable** on the server — `AMPLEMARKET_API_KEY=amp_...` (shared fallback)

| Service | Header | URL query param | Env var | Key looks like |
|---------|--------|-----------------|---------|----------------|
| Amplemarket | `X-Amplemarket-Api-Key` | `amplemarket_key` | `AMPLEMARKET_API_KEY` | `amp_...` |
| OrangeSlice | `X-Orangeslice-Api-Key` | `orangeslice_key` | `ORANGESLICE_API_KEY` | `osk_...` |
| Attio | `X-Attio-Api-Key` | `attio_key` | `ATTIO_API_KEY` | access token |
| August | `X-August-Api-Key` | `august_key` | `AUGUST_API_KEY` | `ak_...` |

You only need keys for the services you plan to use. Tools for a service with no
key return a message explaining how to add one; the other services keep working.
Call the **`connection_auth_status`** tool to see what the current connection is
authenticated for and where each key came from.

### Connecting from Claude (claude.ai / desktop / mobile)

Custom connectors are set up by pasting a URL, so put your keys in the query string:

```
https://<your-deployment>/mcp?amplemarket_key=amp_YOURKEY&attio_key=YOURTOKEN&august_key=ak_YOURKEY&orangeslice_key=osk_YOURKEY
```

Settings → Connectors → Add custom connector → paste the URL above.

### Connecting from Claude Code

Headers keep the keys out of the URL — prefer this where the client supports it:

```bash
claude mcp add --transport http august-mcps https://<your-deployment>/mcp \
  --header "X-Amplemarket-Api-Key: amp_YOURKEY" \
  --header "X-Attio-Api-Key: YOURTOKEN" \
  --header "X-August-Api-Key: ak_YOURKEY" \
  --header "X-Orangeslice-Api-Key: osk_YOURKEY"
```

### A note on keys in URLs

The query-string option exists because some clients only accept a URL. URLs land
in proxy logs, browser history, and screen shares more readily than headers do,
so use the header form when you have the choice, and treat a key pasted into a
URL as one to rotate if that URL is ever shared.

### Single-tenant deployments

To run this for one team with one set of credentials, set the environment
variables on the deployment instead. Connections that supply their own key still
override the server default, so both models can coexist.

## Adding a New MCP

1. Create a new directory: `mkdir <service-name>`
2. Add `server.py`, `requirements.txt`, `Dockerfile` inside it
3. Resolve the API key per request (copy the `_api_key()` helper from an existing
   `server.py`) rather than reading a module-level constant at import time
4. Deploy on Manufact pointing to `<service-name>/Dockerfile`

## Deployment

The root `Dockerfile` builds the combined **August MCPs** server (Amplemarket +
Attio + August in Python, with the OrangeSlice Node sidecar on port 8002).

To deploy a single-service MCP from this repo, configure Manufact to use
`<service-name>/Dockerfile` as the build target.

`requirements.txt` pins `mcp[cli]>=1.9,<2`: mcp 2.0 removed `mcp.server.fastmcp`,
which every server here is built on.

## Running Locally

```bash
# Combined server (all four services)
python -m uvicorn server:app --host 0.0.0.0 --port 8000
# then connect to http://localhost:8000/mcp?attio_key=...&august_key=...

# Single service, key supplied by the server
cd amplemarket && AMPLEMARKET_API_KEY=your_key python server.py   # :8000/mcp
cd attio       && ATTIO_API_KEY=your_key       python server.py   # :8000/mcp
```
