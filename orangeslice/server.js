/**
 * OrangeSlice MCP Server
 * Exposes 30+ data provider enrichment capabilities via MCP tools.
 * Covers: person enrichment, contact info, company data, LinkedIn B2B DB,
 * Crunchbase, web search, website scraping, and AI structured output.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { configure, services } from "orangeslice";
import { createServer } from "http";
import { z } from "zod";

const API_KEY = process.env.ORANGESLICE_API_KEY;
if (!API_KEY) {
  console.error("ORANGESLICE_API_KEY env var is required");
  process.exit(1);
}

configure({ apiKey: API_KEY });

const server = new McpServer({
  name: "OrangeSlice",
  version: "1.0.0",
});

// ─── PERSON ────────────────────────────────────────────────────────────────────

server.tool(
  "enrich_person",
  "Enrich a person from the LinkedIn B2B database by LinkedIn URL or username. Returns name, title, company, headline, location, and more. Fast (~300-500ms). Credits: 1.",
  {
    url: z.string().optional().describe("LinkedIn profile URL (e.g. https://www.linkedin.com/in/satyanadella)"),
    username: z.string().optional().describe("LinkedIn username/slug (e.g. satyanadella)"),
    extended: z.boolean().optional().describe("Include full experience, education, certifications (default: false)"),
  },
  async ({ url, username, extended }) => {
    try {
      const result = await services.person.linkedin.enrich({ url, username, extended });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "find_person_linkedin_url",
  "Find a person's LinkedIn profile URL by name, company, title, or email. Credits: 2 (name search) or 50 (reverse email lookup). Returns URL string or null.",
  {
    name: z.string().optional().describe("Full name"),
    title: z.string().optional().describe("Job title"),
    company: z.string().optional().describe("Company name"),
    keyword: z.string().optional().describe("Additional keyword, industry, etc."),
    location: z.string().optional().describe("Location (city, state, country)"),
    email: z.string().optional().describe("Email address for reverse lookup"),
  },
  async (params) => {
    try {
      const result = await services.person.linkedin.findUrl(params);
      return { content: [{ type: "text", text: result || "No LinkedIn URL found" }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "get_contact_info",
  "Get verified email and/or phone number for a person via LinkedIn URL or name+company. Slow (up to 10 min). Returns work emails, personal emails, work phones, personal phones. Credits: up to 275 (email+phone), 250 (phone only), 25 (email only).",
  {
    linkedinUrl: z.string().optional().describe("LinkedIn profile URL"),
    firstName: z.string().optional().describe("First name"),
    lastName: z.string().optional().describe("Last name"),
    company: z.string().optional().describe("Company name"),
    domain: z.string().optional().describe("Work email domain to target (e.g. stripe.com)"),
    required: z.array(z.enum(["email", "phone", "work_email"])).describe("What to fetch: email, phone, and/or work_email"),
  },
  async ({ linkedinUrl, firstName, lastName, company, domain, required }) => {
    try {
      const result = await services.person.contact.get({ linkedinUrl, firstName, lastName, company, domain, required });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "search_people_linkedin",
  "Run SQL against the LinkedIn B2B people database (linkedin_profile, linkedin_profile_position3). Use for lookup by slug/ID or listing employees at a known company. NOT for prospecting — use web_search for discovery. Credits: 1/result.",
  {
    sql: z.string().describe("SQL query against linkedin_profile / linkedin_profile_position3 tables. Always include LIMIT. Example: SELECT name, title FROM linkedin_profile WHERE slug = 'satyanadella' LIMIT 1"),
  },
  async ({ sql }) => {
    try {
      const result = await services.person.linkedin.search({ sql });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

// ─── COMPANY ───────────────────────────────────────────────────────────────────

server.tool(
  "enrich_company",
  "Enrich a company from the LinkedIn B2B database by LinkedIn slug, URL, or domain. Returns name, description, industry, employee count, website, location, funding, and more. Credits: 1.",
  {
    shorthand: z.string().optional().describe("LinkedIn company slug (e.g. stripe)"),
    url: z.string().optional().describe("LinkedIn company URL (e.g. https://www.linkedin.com/company/stripe)"),
    domain: z.string().optional().describe("Company website domain (e.g. stripe.com)"),
    extended: z.boolean().optional().describe("Include growth metrics and funding data (default: false)"),
  },
  async ({ shorthand, url, domain, extended }) => {
    try {
      const result = await services.company.linkedin.enrich({ shorthand, url, domain, extended });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "get_company_employees",
  "Find employees at a company using LinkedIn data. Supports database strategy (IC/VP/Director roles, fast) and web strategy (C-Suite/Founders only). Credits: 1/result.",
  {
    companySlug: z.string().optional().describe("LinkedIn company slug (e.g. stripe)"),
    linkedinUrl: z.string().optional().describe("LinkedIn company URL"),
    searchStrategy: z.enum(["database", "web"]).optional().describe("database=fast for IC/Director roles; web=C-Suite/Founders only (default: database)"),
    titleVariations: z.array(z.string()).optional().describe("Title keywords to filter by. Required for web strategy (max 3). E.g. ['engineer', 'developer']"),
    titleSqlFilter: z.string().optional().describe("Raw SQL filter for title (database strategy only). E.g. \"title ILIKE '%engineer%'\""),
    limit: z.number().optional().describe("Max results (default: 25, max: 100)"),
    usOnly: z.boolean().optional().describe("Filter to US-based only (default: true)"),
    minConnections: z.number().optional().describe("Minimum connection count (default: 20)"),
    offset: z.number().optional().describe("Pagination offset (database only)"),
  },
  async (params) => {
    try {
      const result = await services.company.getEmployeesFromLinkedin(params);
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "get_company_revenue",
  "Get company revenue, employee count, headquarters, industry, and funding from a domain. Credits: 2.",
  {
    domain: z.string().describe("Company website domain (e.g. stripe.com or https://stripe.com)"),
  },
  async ({ domain }) => {
    try {
      const result = await services.company.revenue({ domain });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "search_companies_linkedin",
  "Run SQL against the LinkedIn B2B company database (linkedin_company). Use for lookups by domain, slug, industry_code, country_code, employee_count, etc. NOT for prospecting by name/description — use web_search. Credits: 1/result.",
  {
    sql: z.string().describe("SQL query against linkedin_company table. Always include LIMIT (max 2000). Avoid ORDER BY on large columns (causes timeout). Example: SELECT name, domain, employee_count FROM linkedin_company WHERE domain = 'stripe.com' LIMIT 1"),
  },
  async ({ sql }) => {
    try {
      const result = await services.company.linkedin.search({ sql });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

// ─── WEB & SCRAPE ──────────────────────────────────────────────────────────────

server.tool(
  "web_search",
  "Search Google SERP. Default tool for prospecting and discovery. Supports site: operator, time filters, and pagination. Credits: 1.",
  {
    query: z.string().describe("Search query. Supports operators: site:, \"exact\", OR, -exclude"),
    domain: z.string().optional().describe("Restrict results to this domain (e.g. linkedin.com/in)"),
    advance_search: z.boolean().optional().describe("Enable knowledge graph results"),
    page: z.number().optional().describe("Page number (1-indexed, default: 1)"),
    tbs: z.string().optional().describe("Time filter: qdr:h (hour), qdr:d (day), qdr:w (week), qdr:m (month), qdr:y (year)"),
  },
  async (params) => {
    try {
      const result = await services.web.search(params);
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

server.tool(
  "scrape_website",
  "Scrape a website URL and return its content as clean text or HTML. Good for extracting structured info from a known page. Credits: 1.",
  {
    url: z.string().describe("URL to scrape"),
    format: z.enum(["text", "html", "markdown"]).optional().describe("Output format (default: text)"),
  },
  async ({ url, format }) => {
    try {
      const result = await services.scrape.website({ url, format });
      return { content: [{ type: "text", text: typeof result === "string" ? result : JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

// ─── CRUNCHBASE ─────────────────────────────────────────────────────────────────

server.tool(
  "search_crunchbase",
  "Run SQL against Crunchbase startup database (public.crunchbase_scraper_lean) for funding-stage prospecting. Filter by operating_status, funding_total_usd, last_funding_type, founded_on, country_code. Credits: 1/row.",
  {
    sql: z.string().describe("SQL SELECT query against public.crunchbase_scraper_lean. Must include LIMIT (max 100). Example: SELECT name, website_url, funding_total_usd, last_funding_type FROM public.crunchbase_scraper_lean WHERE operating_status = 'active' AND last_funding_type = 'series_a' LIMIT 25"),
  },
  async ({ sql }) => {
    try {
      const rows = await services.crunchbase.search({ sql });
      return { content: [{ type: "text", text: JSON.stringify(rows, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

// ─── AI ────────────────────────────────────────────────────────────────────────

server.tool(
  "ai_generate_object",
  "Use AI to extract or classify data from text into a structured JSON object matching a schema. Useful for enrichment, scoring, and classification tasks.",
  {
    prompt: z.string().describe("Instruction and input text for the AI"),
    schema: z.record(z.unknown()).describe("JSON Schema object describing the output structure"),
  },
  async ({ prompt, schema }) => {
    try {
      const result = await services.ai.generateObject({ prompt, schema });
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

// ─── GOOGLE MAPS ───────────────────────────────────────────────────────────────

server.tool(
  "search_google_maps",
  "Search businesses via Google Maps by query and optional location. Returns business name, address, phone, website, rating. Credits: 1.",
  {
    query: z.string().describe("Search query (e.g. 'law firms in Austin TX')"),
    location: z.string().optional().describe("Location to center search (e.g. 'Austin, TX')"),
    limit: z.number().optional().describe("Max results (default: 20)"),
  },
  async (params) => {
    try {
      const result = await services.googleMaps.search(params);
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  }
);

// ─── HTTP SERVER ───────────────────────────────────────────────────────────────

const PORT = parseInt(process.env.PORT || "8002");

const httpServer = createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", server: "OrangeSlice MCP" }));
    return;
  }

  if (!req.url?.startsWith("/mcp")) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
  });

  res.on("close", () => transport.close());

  await server.connect(transport);

  // Parse body as JSON for POST requests
  let parsedBody;
  if (req.method === "POST") {
    const raw = await new Promise((resolve) => {
      const chunks = [];
      req.on("data", (c) => chunks.push(c));
      req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    });
    try {
      parsedBody = JSON.parse(raw);
    } catch {
      parsedBody = undefined;
    }
  }

  await transport.handleRequest(req, res, parsedBody);
});

httpServer.listen(PORT, "0.0.0.0", () => {
  console.log(`OrangeSlice MCP server running on http://0.0.0.0:${PORT}/mcp`);
});
