---
title: ASN Observation Data Retrieval and Analysis
description: Setup and use of the OONI Coverage command-line tool, covering OONI's three data sources, the S3 path layout, CSV output and the coverage formula.
---

[OONI Coverage](/projects/asn-coverage/) (ASN Coverage) has a command-line tool, [`anoni-net/asn-coverage`](https://github.com/anoni-net/asn-coverage), that pulls public data from OONI (Open Observatory of Network Interference) and computes the observation coverage of a region's autonomous system numbers (ASNs). This page is the technical companion to [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/), with the setup and usage of the tool.

Before starting, set up a development environment following [Development Environment Setup](/join/dev-setup/).

!!! tip "Working directory"

    Every command below runs from a clone of [`anoni-net/asn-coverage`](https://github.com/anoni-net/asn-coverage). On first use, clone the repository, `cd` into it, run `uv sync` to install dependencies, then follow the examples below using `uv run python ooni.py ...`.

## Three entry points

OONI's observation data has three entry points with quite different uses, so pick one before starting:

| Entry point | Suits | Limitation |
|---|---|---|
| [AWS S3 public dataset](https://registry.opendata.aws/ooni/) | Bulk analysis, full-population statistics, comparison over time | You parse it yourself, and downloads run to gigabytes |
| [OONI API](https://api.ooni.org/api/v1/measurements) | Filtering by criteria, fetching one complete measurement | A cap on results per request |
| [OONI Explorer](https://explorer.ooni.org/) | Looking things up by hand, checking individual measurements | Not suited to programmatic access |

ASN Coverage takes the S3 route, since its purpose is coverage statistics rather than single lookups. For API usage with single measurements or small-scale filtering, see [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/).

## Scope of the scripts

`ooni.py` currently produces coverage and verdict-distribution statistics, within three limits on what it retrieves:

- **The `webconnectivity` directory only**: the dozen-plus other nettests (OONI's individual test types) in the same hour are not included, so observations from `tor`, `telegram`, `signal` and the rest never reach the statistics. For what each nettest measures, see [OONI Nettest Quick Reference](/projects/asn-coverage/ooni-nettests-map/).
- **Three fields per measurement**: `probe_asn`, `annotations.network_type` and `test_keys.blocking`. The scripts never read the evidence layer (`queries`, `tcp_connect`, `requests`), so the output covers which ASNs have someone measuring, how often, and how the verdicts break down, but not what the evidence for a single measurement looks like.
- **`.jsonl.gz` only**: the `.tar.gz` files in the same directory are skipped.

`blocking` is the boolean `false` when no interference was observed and a string when there was. The tool normalises both into one key space before counting and records measurements with no verdict as `none`, so each ASN's verdict counts always add up to its measurement count. For how to read those verdicts, see [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/).

Analysing the evidence layer means pulling its fields and comparing measurements one by one. That needs a storage design of its own, since plain counters cannot hold the data.

## S3 dataset layout

The bucket is `ooni-data-eu-fra` in `eu-central-1`, and public reads need no credentials. Paths nest four levels deep by date, hour, country code and nettest:

```text title="Path structure"
raw/{YYYYMMDD}/{HH}/{country}/{nettest}/{YYYYMMDDHH}_{country}_{nettest}.n{batch}.{seq}.jsonl.gz
```

!!! warning "UTC dates and hours"

    The `{YYYYMMDD}` and `{HH}` in the path, along with the `date` and `hour` fields in the CSV output further down, are all UTC. The scripts get the time from `arrow.Arrow.utcnow()` throughout. When analysing the observation distribution during a given local time window, convert for your own offset first, or the whole chart shifts.

The `.n{batch}.{seq}` at the end of the filename is OONI's internal batch numbering and can be ignored when parsing.

You can check what is in a directory before installing anything:

```bash title="Every nettest for one hour in Taiwan"
curl -s "https://ooni-data-eu-fra.s3.eu-central-1.amazonaws.com/?list-type=2&prefix=raw/20260804/00/TW/&delimiter=/" \
  | grep -oE '<Prefix>raw/[^<]+</Prefix>'
```

The response is XML on a single line, so the `grep` above pulls out just the directory names. Taiwan usually has a dozen-plus nettest directories within a single hour, with `webconnectivity` only one of them, alongside `tor`, `telegram`, `signal`, `whatsapp`, `dnscheck`, `echcheck`, `openvpn`, `psiphon`, `ndt` and `dash`.

Within each nettest directory, the same batch comes in two packages, `.jsonl.gz` and `.tar.gz`. Unpacked, `.jsonl.gz` gives one measurement per line, which suits line-by-line parsing, and it is what the scripts read. Taiwan's `webconnectivity` data on 2026-08-04, for example, runs to around 10 MB per file. A full month of national data adds up to a substantial volume, so estimate bandwidth and runtime before a real run. The scripts process the data as a stream, so raw files are never written to disk and the only output is the CSV.

For how to read each line's fields, see [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/). For what the verdict fields mean, see [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/).

## Retrieval and analysis commands

### Lookback over recent data

```bash title="The last 36 hours"
uv run python ooni.py lookback --units=36 --loc=TW --frame=hours
```

All three arguments are optional, and the defaults match the example above. `--frame` sets the unit for the total lookback span and accepts `hours`, `days`, `weeks` and so on. Whatever you pass, the data is always split by hour. Output filename format:

- `lookback_{loc}_{YYYYMMDD}_{units}_{frame}.csv`

The `{YYYYMMDD}` in the filename is the UTC date the script ran, not the range the data covers, so check the file contents for the actual range. The file is written to the current working directory.

### Data for a date range

```bash title="A specified range"
uv run python ooni.py span --start=2026/08/01 --end=2026/08/03 --loc=TW --chunk=40
```

Give a start time (`start`) and end time (`end`) to retrieve hourly data across that period. `--chunk` controls how many hours are processed concurrently and defaults to `40`. Lower it when network or memory is tight. Output filename format:

- `span_{loc}_{startYYYYMMDD}_{endYYYYMMDD}.csv`

### Spreadsheet rows

```bash title="Spreadsheet format"
uv run python ooni.py sheetrow --path=./span_TW_20260801_20260803.csv
```

`sheetrow` expands data you have already retrieved so it can be worked with in a spreadsheet. The output filename is the original prefixed with `rows_`, which for the example above is `rows_span_TW_20260801_20260803.csv`.

## CSV output format

Files produced by `lookback` and `span` have four fields, one row per hour:

| Field | Contents |
|---|---|
| `loc` | Country code, for example `TW` |
| `date` | Date as `YYYY/MM/DD`, UTC |
| `hour` | Hour as `HH`, UTC |
| `statistics` | That hour's statistics, held as a JSON string |

`statistics` holds three counts: `counts` tallies measurements per ASN, `network_type` tallies by connection type, and `blocking` tallies the verdict distribution per ASN. Here is real data from hour `00` in Taiwan on 2026-08-04, which had 551 measurements:

```json title="The statistics field expanded"
{"counts": {"AS3462": 300, "AS17716": 100, "AS18419": 100, "AS24158": 51},
 "network_type": {"mobile": 44, "no_internet": 7},
 "blocking": {"AS3462": {"false": 294, "dns": 1, "tcp_ip": 1, "none": 4},
              "AS17716": {"false": 94, "none": 6},
              "AS18419": {"false": 99, "none": 1},
              "AS24158": {"false": 51}}}
```

`counts` and `blocking` reconcile per ASN, while `network_type` does not, and that is normal. The annotation comes from the Probe (OONI's measurement app) itself: mobile apps generally write it, and CLI and desktop versions mostly do not. Only 51 of the 551 measurements above carry the annotation, and the scripts skip measurements without one. Within that, `no_internet` means the Probe detected it was offline at measurement time. With annotation coverage below ten percent, the field is useful for trends but not as the basis for a mobile-versus-fixed-line ratio.

`none` inside `blocking` means no verdict was recorded, covering both a missing `test_keys` and a `null` blocking. Eleven of the 551 measurements above fall into it. The share is small but it shows up in every ASN, so decide whether those measurements belong in the denominator before calculating an anomaly rate.

Nested JSON is awkward to work with in a spreadsheet, so `sheetrow` flattens it into one row per ASN:

| `loc` | `date` | `hour` | `asn` | `count` | `anomaly` | `blocking_false` | `blocking_dns` | `blocking_tcp_ip` |
|---|---|---|---|---|---|---|---|---|
| `TW` | `2026/08/04` | `00` | `AS3462` | `300` | `2` | `294` | `1` | `1` |
| `TW` | `2026/08/04` | `00` | `AS17716` | `100` | `0` | `94` | `0` | `0` |

The remaining columns are `blocking_http_failure`, `blocking_http_diff`, `blocking_none` and `blocking_other`, trimmed from the table above for width. `anomaly` sums the four interference types and can serve directly as the numerator in a spreadsheet. `blocking_other` catches values `ts-017` does not define yet and should normally be `0`. Any other value means upstream has added a verdict type.

A worked example of the resulting spreadsheet (2023-09 to 2023-12):

[<i data-icon="google-spreadsheet"></i> 20230901-20231204-TW](https://docs.google.com/spreadsheets/d/1lMDsqX8Oa3GKW68y8TuFeKQW2nKM7X0u4z-RopfJIaA/){ .btn .solid }

## ASN coverage calculation

Coverage needs two numbers: the count of distinct ASNs appearing in the observation data, and the total ASNs registered to that region. Get the first from the flattened CSV in the previous section with a pivot table, and the second from RIPE NCC via `ripe.py`:

```bash title="Full ASN list for a region"
uv run python ripe.py save --loc=TW
```

The output filename is `asns_{YYYYMMDDTHH}.csv`, with six fields: `no`, `location`, `org_id`, `registrar`, `reserved` and `name`.

!!! warning "Differing ASN formats"

    The `no` field `ripe.py` outputs is a plain number (`3462`), while `probe_asn` in OONI data carries an `AS` prefix (`AS3462`). A VLOOKUP across them matches nothing, so normalise before matching by adding or stripping the `AS` on one side.

With both numbers in hand:

```text title="Coverage formula"
coverage = distinct ASNs appearing in observation data ÷ total ASNs registered to the region
```

In the community's December 2023 analysis (see [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/)), Taiwan had roughly 437 ASNs at the time, and the observation data covered 7.32% of them as distinct ASNs. You can rerun the same formula over a recent range to see whether coverage has improved.

## miniooni and OONI Run v2 lists {#miniooni}

[miniooni](https://github.com/ooni/probe-cli), the command-line build of OONI Probe, can run an OONI Run v2 list on a server, in a research script or on a schedule. Its `-i` flag needs the API's descriptor URL; the `run.ooni.org` web URL fails:

```bash
# Fails: the CLI gets HTML and JSON parsing breaks
miniooni oonirun -i https://run.ooni.org/v2/10328

# Works: point at the API's descriptor JSON
miniooni oonirun -i https://api.ooni.org/api/v2/oonirun/links/10328
```

miniooni GETs whatever URL `-i` is given and expects descriptor JSON back, but `run.ooni.org/v2/<ID>` is a page for browsers and returns HTML. The descriptor lives at `https://api.ooni.org/api/v2/oonirun/links/<LINK_ID>`, where `<LINK_ID>` is the last segment of the web URL; the community's list is `10328`. Desktop and mobile apps are unaffected, since the operating system hands the web URL to OONI Probe. Upstream has a [TODO note](https://github.com/ooni/probe-cli/blob/master/internal/oonirun/link.go) in the code, so the conversion may become automatic later.

## Related reading

- [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/): the fields in a single measurement and how to read them
- [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/): what `blocking` and the other verdict fields mean
- [OONI Nettest Quick Reference](/projects/asn-coverage/ooni-nettests-map/): what each nettest measures
- [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/): the coverage analysis behind this page, citing the report used in the worked example
- [Maintaining the OONI Test List](/join/ooni-test-list/): how the test list that OONI Probe measures against is maintained
- [Development Environment Setup](/join/dev-setup/): the tools needed before contributing to anoni.net's repositories
