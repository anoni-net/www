---
title: Tor relay lookup for AI assistants
description: A Tor relay lookup service the community builds and hosts. Add one URL to a cloud AI assistant and ask, without writing code, how many relays a country runs, how much bandwidth they carry and which networks host them.
lead: Paste one URL into a cloud AI assistant and ask about Tor relays anywhere in plain language.
---

The Tor Project's public data shows how many Tor relays Taiwan is running right now, whether that number has grown or shrunk over the past six months, and which telecoms host them, but getting those answers used to mean writing code to fetch and process the data yourself. Once onionoo MCP is connected to an AI assistant (such as claude.ai), you can type "How many working Tor relays does Taiwan have right now?" and the assistant queries the data, does the arithmetic, and returns a readable report.

The first half of this page is for people who look up data but don't write code, such as journalists, civil-society groups and fact-checkers. The second half, [API access and self-hosting](#API-access-and-self-hosting), is for engineers who want to call the service from code or run their own copy.

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-tw-summary-result-en.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-tw-summary-result-en.png"
            alt="Claude Desktop response from Opus 4.7 summarizing Taiwan's current Tor relays: 13 running relays, total advertised bandwidth ~41.1 MB/s (~329 Mbit/s combined), based on the consensus published 2026-05-16 15:00 UTC, with an ASN breakdown table — AS3462 Chunghwa Telecom (HiNet) 10 relays (77%), AS1659 TANet, AS9416 Hoshin Multimedia, AS18041 Taiwan Digital Streaming each 1 relay (8% each)"
            title="Claude Desktop's summary of Taiwan's current Tor footprint"
            class="shot">
    </a>
    <figcaption>A plain-language question returns a report with the running relay count, total bandwidth and top networks. The numbers come from the Tor Project's public data and are a snapshot taken at query time, so they change as the network does.</figcaption>
</figure>

## Use cases

- **Fact-checking**: when someone claims "Taiwan's Tor capacity is tiny," you can ask on the spot how many relays are running, how much total bandwidth there is, and how that compares to an earlier point in time — numbers you can check and cite.
- **Reporting**: when covering a country's network blocking or circumvention infrastructure, survey how many Tor relays it has and which providers its exit relays (the last hop, where traffic leaves Tor for the ordinary web) cluster in, for a cross-country comparison.
- **Civil society and advocacy**: gauge how concentrated a region's relays are (across how many telecoms — the more spread out, the harder they are to cut off at once) as a digital-resilience indicator.

## Setup in a cloud AI assistant

Without writing code, the simplest route is to connect the service to the cloud AI assistant you already use. There is nothing to install and no config file to edit: add a custom connector in the assistant's settings and paste in this URL:

`https://onionoo.anoni.net/mcp`

Three cloud AI services common across the Asia-Pacific region currently differ in what this takes:

<div class="tbl-names" markdown>

| Cloud AI | URL in the app | How to connect |
|---|---|---|
| **Claude (claude.ai)** | Yes — even on the free plan (1 connector limit) | Settings → Connectors → Add custom connector, paste the URL |
| **ChatGPT** | Yes, but needs a paid plan (Plus or above; not Free) | Settings → Apps → Advanced → turn on Developer Mode → add a custom connector, paste the URL |
| **Google Gemini** | Not yet in the consumer chat app | Goes through Gemini CLI (config file) or Gemini Enterprise (Google Cloud admin) — an engineering or enterprise path; see [API access and self-hosting](#API-access-and-self-hosting) |

</div>

Plan tiers and the exact location of these settings can change; check each vendor's own docs (Claude[^connector], ChatGPT[^chatgpt], Gemini[^gemini]).

The full steps for Claude, which has the lowest barrier of the three:

1. Open [claude.ai](https://claude.ai) (web or desktop) and sign in.
2. Open Settings, find **Connectors**, and click **Add custom connector**.
3. Name it `onionoo`, paste `https://onionoo.anoni.net/mcp` as the URL, and click **Add**.
4. Start a new chat and ask in plain language (examples below).

If you are on a company or team (Team or Enterprise) account, usually only an account Owner can add connectors — ask your admin to add it.

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-claude-desktop.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-claude-desktop.png"
            alt="Claude Desktop Connectors panel showing onionoo as a CUSTOM connector pointed at https://onionoo.anoni.net/mcp, with tools listed: aggregate_as, aggregate_countries, aggregate_flags, get_bandwidth, get_clients, get_details, get_summary, get_uptime, get_weights"
            title="The Connectors panel after pasting the URL"
            class="shot">
    </a>
    <figcaption>Once added, the Connectors panel shows the <code>onionoo</code> custom connector and the query tools it provides. You don't need to name a tool; the assistant chooses one based on your question.</figcaption>
</figure>

## Example questions

Copy any of these three and swap in the country or region you care about.

**Numbers you can cite (fact-checking)**

> How many Tor relays in Taiwan are running right now? Roughly how much total bandwidth? Summarize it as one sentence I can quote.

**Cross-country comparison (reporting)**

> Compare the number of running Tor relays and total bandwidth in Taiwan, Hong Kong, and Japan right now, as a table.

**Relay concentration (civil society)**

> Which telecom networks (ASNs) host Taiwan's Tor relays? What are the top five, and how many relays does each carry?

If the answer looks useful, follow up with "When are these numbers from?" or "What's the source?" to have the assistant state its sources.

??? info "Terms used on this page"

    A rough sense of each is enough, and the assistant can explain any of them on request.

    - **Relay**: a volunteer server in the Tor network that forwards traffic. There are close to ten thousand worldwide, and your traffic passes through several of them in turn.
    - **Bridge**: an unlisted relay, for people who can't reach the ordinary (publicly listed) Tor relays — for example, because they're blocked.
    - **Exit**: the last relay on the path, where traffic leaves the Tor network and connects to the ordinary web.
    - **ASN (Autonomous System Number)**: the number that identifies a telecom or network provider on the internet. Which ASNs the relays sit in tells you which providers carry them.
    - **Consensus weight**: the share of traffic Tor assigns each relay, roughly proportional to how much it can carry. A higher number means the relay is assigned more traffic.

## Reliability and citation

The numbers are citable. They come from the Tor Project's own [Onionoo](https://metrics.torproject.org/onionoo.html) (the public metadata service for Tor relays), and onionoo.anoni.net only reshapes them into a friendlier format without storing or changing any values.

- **Cross-check**: the same relays show up in the Tor Project's own [Relay Search](https://metrics.torproject.org/rs.html), and the figures should line up.
- **Freshness**: the service caches responses for about five minutes, and Onionoo itself updates periodically, so what you get is a point-in-time snapshot, not a live value. Note the time you queried when you cite it.
- **How to cite**: write it as `Source: Tor Project Onionoo (via anoni.net's onionoo service, queried 2026-06-09)`.

---

## API access and self-hosting

`onionoo-fastapi` wraps the Onionoo API in two interfaces that are easier for tooling and AI agents to consume:

- **Semantic HTTP API with OpenAPI / Swagger**: Onionoo's compact field names (`n`, `f`, `a`, `r` and so on) are remapped to readable ones (`nickname`, `fingerprint`, `addresses`, `running`), with a full OpenAPI document on top.
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server**: Claude Desktop, Cursor, Claude Code, and other MCP clients can query relays through tool calls instead of hand-rolling HTTP requests.

The service does **not** store any Onionoo data. It only forwards requests and reshapes responses. The upstream is the Tor Project's [Onionoo service](https://onionoo.torproject.org).

- **Hosted instance**: <https://onionoo.anoni.net>
- **Swagger UI**: <https://onionoo.anoni.net/docs>
- **MCP endpoint**: `https://onionoo.anoni.net/mcp` (Streamable HTTP)
- **Source code**: <https://github.com/anoni-net/onionoo-fastapi> (MIT, currently v1.2.0)

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-swagger.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-swagger.png"
            alt="Swagger UI for onionoo.anoni.net showing Onionoo FastAPI Proxy v1.0.0 with endpoints /healthz, /metrics, /v1/summary, /v1/details, /v1/bandwidth, /v1/weights, /v1/clients"
            title="Swagger UI for onionoo.anoni.net"
            class="shot">
    </a>
    <figcaption>The Swagger UI at <code>onionoo.anoni.net/docs</code>. Every <code>/v1/*</code> endpoint has a full schema and a Try-it-out button for ad-hoc testing.</figcaption>
</figure>

### Motivation

Onionoo's specification is solid, but it ships **without an OpenAPI description**, and its field names are short (optimized for transfer size). That works for a human writing a client by hand, but it is less friendly to AI agents and third-party tooling:

- No OpenAPI means tools like Swagger UI, Postman, or code generators can't introspect it.
- The short field names confuse language models — is `r` a relay or just `running`?
- A single question often needs several endpoints stitched together (`/details` + `/uptime` + `/bandwidth`), and agents that re-derive that orchestration each time make mistakes.

`onionoo-fastapi` fixes all three: it ships an OpenAPI spec, exposes readable field names, and bundles common multi-endpoint tasks into single MCP tools (for example, "give me the health of this relay" is one call).

### API vs MCP

An **API (Application Programming Interface)** is a standard way for programs to query data. Onionoo itself is an API: you send an HTTP request (for example, "give me every running relay in Taiwan") and it returns JSON. The spec is written for engineers, you get raw data back, and it works best when you already know exactly what to ask.

**MCP (Model Context Protocol)** is an open protocol Anthropic introduced in 2024 that defines a standard format for how AI models invoke external tools. Wrapping an existing API as an MCP server means every MCP-capable AI agent or client can connect directly; the model reads the tool list, decides when to call which tool, and you don't redo the integration each time a new client appears.

For early-stage data exploration, MCP means you don't have to learn the dataset's schema before asking questions. The assistant does the first pass of querying and summarizing, and you decide where to dig deeper after reading its report. When some queries need repeating or wiring into a formal analysis, drop back to the API and write a script — the two paths coexist.

### MCP client configuration

If your client connects via a config file (rather than the Connectors UI from the first half), add this to the `mcpServers` block:

```json
{
  "mcpServers": {
    "onionoo": {
      "type": "http",
      "url": "https://onionoo.anoni.net/mcp"
    }
  }
}
```

Save, restart the client, and an `onionoo` tool group appears in the tool list.

To run it locally without depending on the hosted instance, use the stdio transport:

```json
{
  "mcpServers": {
    "onionoo": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/anoni-net/onionoo-fastapi", "onionoo-mcp"]
    }
  }
}
```

You will need [`uv`](https://docs.astral.sh/uv/) installed (`brew install uv` on macOS; see the official docs for Linux).

Gemini CLI also reads an `mcpServers` config (in its settings.json), in a similar shape — drop the same remote URL in. The consumer Gemini chat app doesn't yet have an in-app way to paste a remote MCP URL, so using it there waits on official support.

### HTTP API usage

Every endpoint returns semantic JSON with a `_meta` envelope indicating cache state:

```bash
# Details for moria1 — only return nickname and fingerprint
curl -s 'https://onionoo.anoni.net/v1/details?search=moria&fields=nickname,fingerprint' | jq .

# Taiwan's relays, sorted by consensus weight
curl -s 'https://onionoo.anoni.net/v1/details?country=tw&running=true&order=-consensus_weight&limit=5' | jq .

# Per-country aggregation of currently running relays
curl -s 'https://onionoo.anoni.net/v1/aggregate/countries?running=true' | jq .
```

For the full list of endpoints, parameters, and response fields, see the [Swagger UI](https://onionoo.anoni.net/docs). Query parameters mirror Onionoo's [protocol specification](https://metrics.torproject.org/onionoo.html).

### Docker self-hosting

If you want to run your own copy (for a `.onion` service, an internal network, or experimentation):

```bash
git clone https://github.com/anoni-net/onionoo-fastapi
cd onionoo-fastapi
docker compose up -d --build
```

It listens on port `8000` by default. OpenAPI docs are at `http://localhost:8000/docs`, the MCP endpoint at `http://localhost:8000/mcp`.

Common settings (via environment variables):

| Variable | Purpose | Default |
|---|---|---|
| `ONIONOO_BASE_URL` | Upstream Onionoo URL | `https://onionoo.torproject.org` |
| `CACHE_MAXSIZE` / `CACHE_DEFAULT_TTL_SECONDS` | In-memory cache size and TTL | `128` / `300` s |
| `RATE_LIMIT_ENABLED` / `RATE_LIMIT_PER_MINUTE` | Per-IP rate limiting | `false` / `120` |
| `CORS_ALLOW_ORIGINS` | Allowed CORS origins, comma-separated; an empty string turns CORS off (the 1.0.0 name `CORS_ALLOWED_ORIGINS` is still accepted) | `https://anoni.net`, the docs site's onion mirror and local preview |
| `LOG_FORMAT` | `json` or `console` | `json` |
| `METRICS_ENABLED` | Expose `/metrics` in Prometheus format | `true` |

For the full list, see the [README](https://github.com/anoni-net/onionoo-fastapi#configuration).

### MCP tools at a glance

Task-oriented tools (stdio transport, recommended for agents):

| Tool | Purpose |
|---|---|
| `find_relay(query)` | Free-form lookup; auto-detects whether the query is a 40-character fingerprint, an AS number, an IP, or a nickname substring |
| `get_relay_health(fingerprint)` | A composite health snapshot — details + uptime + bandwidth in one call |
| `top_relays_by_bandwidth(country?, flag?, limit)` | Top-N relays by consensus weight, optionally filtered by country or flag |
| `compare_relays(fingerprints)` | Fetches details for several fingerprints in parallel for side-by-side comparison |
| `country_summary(country)` | Running count, total bandwidth, and flag distribution for one country |
| `aggregate_relays(group_by, running, top)` | Server-side group-by over country / AS / flag |

Both transports also offer low-level pass-through tools over the six native Onionoo endpoints, with different names and arguments. On Streamable HTTP they are `get_summary`, `get_details`, `get_bandwidth`, `get_weights`, `get_clients` and `get_uptime`; each exposes the query parameters as individual tool arguments and returns the semantically renamed JSON. On stdio the same six are `onionoo_summary`, `onionoo_details` and so on; each takes a `params` dict and returns Onionoo's raw response.

> The Streamable HTTP endpoint at `/mcp` exposes the six low-level tools plus three aggregate tools (countries, as, flags); the task-oriented tools and the unified `aggregate_relays` live on the stdio transport. The two transports can run side by side.

### Example agent survey of Taiwan's relays

Once `onionoo` MCP is wired into Claude Desktop or Claude Code, you can ask:

> "Give me a summary of Taiwan's current Tor relays: how many are running, total bandwidth, top 5 ASNs, and pick out the three relays with the highest consensus weight — tell me their nicknames and which AS they're in."

The agent breaks the question into a handful of MCP tool calls and assembles a single report (over the HTTP transport that's typically `aggregate_countries` plus `get_details`; over stdio, the task-oriented tools `country_summary`, `aggregate_relays`, and `top_relays_by_bandwidth` are available too). Queries like this previously meant manually composing Onionoo parameters and merging JSON. Now they are a single sentence.

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-tool-use-detail.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-tool-use-detail.png"
            alt="Claude Opus 4.7 thinking trace: stating it needs Taiwan relay info, listing candidate tools, deciding to call aggregate_countries to find Taiwan's row, then get_details with country=tw to pull AS information, and finally to fetch the top three by consensus weight. The aggregate_countries tool call is shown expanded with a Result chip"
            title="Claude Opus 4.7's expanded tool-use trace"
            class="shot">
    </a>
    <figcaption>The agent narrates its plan — what to query, which tool to pick, what to do with the response — with the actual <code>aggregate_countries</code> and <code>get_details</code> tool calls inlined. The full MCP interaction is visible, which helps with debugging and prompt tuning.</figcaption>
</figure>

### Observability and operations

- `/healthz`: static liveness check, never hits upstream.
- `/healthz/ready`: pings Onionoo (cached) — 200 if reachable, 503 otherwise.
- `/metrics`: Prometheus format. Includes cache hit/miss counters (`onionoo_cache_hits_total` and `_misses_total`), upstream latency (`onionoo_upstream_seconds`), and error rates.
- Every request gets an `X-Request-ID` echoed in the response header and bound into log records — handy for correlating issues.

## Contributing

- **Report bugs or suggest tools**: <https://github.com/anoni-net/onionoo-fastapi/issues>
- **Running a Tor relay**: see the [Tor Relay Setup Guide](/join/setup-tor-relay/). The relay figures we publish for the region are in [Tor Relay Watch](/projects/pulse/).
- **Pre-travel checks**: [Pre-departure digital safety — brief yourself with AI prompts](docs:scenarios/travel-ai-briefing/). Journalists and civil-society groups checking the Tor relay situation at a destination before a trip can connect onionoo MCP to get citable Onionoo figures.
- **Background reading**: [What Is Tor?](docs:tools/what-is-tor/) and [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/).

The current release is v1.2.0, under the MIT license. Issues, PRs, and Matrix discussion on which task-oriented tools to add next are all welcome.

[^connector]: [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) — Claude Help Center (custom connectors work on the Free, Pro, Max, Team, and Enterprise plans; Free is limited to one).

[^chatgpt]: [Developer mode — apps and full MCP connectors in ChatGPT (beta)](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta) — OpenAI Help Center (custom MCP connectors require Developer Mode on the Plus, Pro, Business, Enterprise, or Edu plans; not available on Free).

[^gemini]: [Set up your custom MCP server data store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server) — Gemini Enterprise (Google Cloud). The consumer Gemini chat app does not yet offer an in-app way to connect a remote MCP server by URL; on the developer side, [Gemini CLI](https://geminicli.com/docs/tools/mcp-server/) uses an `mcpServers` config.
