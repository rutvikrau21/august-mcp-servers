# August MCP Servers

A monorepo of MCP servers for August Law's internal tooling. Each subdirectory is a self-contained MCP server with its own `Dockerfile`, `requirements.txt`, and `server.py`.

## Servers

| Server | Directory | Description |
|--------|-----------|-------------|
| Amplemarket | `amplemarket/` | Full Amplemarket API — contacts, sequences, enrichment, calls, tasks, exclusions |
| Attio | `attio/` | Full Attio CRM API — objects, records, attributes, notes, tasks, lists, webhooks |

## Adding a New MCP

1. Create a new directory: `mkdir <service-name>`
2. Add `server.py`, `requirements.txt`, `Dockerfile` inside it
3. Deploy on Manufact pointing to `<service-name>/Dockerfile`

## Deployment

The root `Dockerfile` builds the **Amplemarket** MCP by default (used by the existing deployment).

To deploy a different MCP from this repo, configure Manufact to use `<service-name>/Dockerfile` as the build target.

## Running Locally

```bash
cd amplemarket
AMPLEMARKET_API_KEY=your_key python server.py
# Server starts at http://localhost:8000/mcp

cd attio
ATTIO_API_KEY=your_key python server.py
# Server starts at http://localhost:8001/mcp
```
