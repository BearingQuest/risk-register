# Bearing Register: Product Requirements (PRD)

Version 1.0, 15 Nov 2026, approved by Dusten Harrison. Specified and directed by Dusten Harrison; drafted by Claude from Dusten's recorded decisions. History: v0.1 draft 6 Nov 2026; v0.2 6 Nov (FAIR moved into v0.1); v0.3 13 Nov (open questions decided); v0.4 15 Nov (an independent AI review by ChatGPT, whose findings are cited as CG#n, and the decisions it led to); v1.0 15 Nov (approved and committed).

- **Source of truth.** This file and `docs/decisions.md` are the source of truth for what Bearing Register does. Changes go through pull requests that update both. Pull requests cite requirement IDs (R1–R106) in the template's Requirements line.
- **Markers.** Every requirement carries its target version and the date of the decision behind it. **[P]** marks a detail Claude proposed that Dusten approved with this PRD on 15 Nov 2026 rather than by a separate decision; changing one is an ordinary PRD change. "Item N" refers to the maintainer's planning record, which isn't in this repo.
- **Repo.** github.com/BearingQuest/risk-register, moved from github.com/dustenatx/bearing-register in Nov 2026 (repo name only: the product stays Bearing Register, the package `bearing-register`, the CLI `brg`; decided 4 Nov 2026).

## 1. What it is

Bearing Register is an open-source, GRC-as-code risk register. Each risk, issue, finding, control and acceptance is a YAML file in a Git repository. The `brg` command-line tool and CI enforce the governance rules that spreadsheet registers can't: computed scores, required approvals, expiring acceptances and an audit trail from Git history. A read-only website shows the register, each risk and a heat map.

It targets the failures collected in the pain-point batches: version sprawl, edits no one checks, owners never told, scores typed by hand, findings logged as risks, acceptances that never expire, and no history.

Licence: Apache-2.0 (23 Oct; reconfirmed 25 Oct 2026).

## 2. Principles

1. **A first risk takes about 5 answers and under 5 minutes** (28 Oct). Fields beyond the minimum become required only at later lifecycle statuses. Every new field or rule is checked against this.
2. **Rules are enforced, not documented.** A rule is a schema rule or a lint check that blocks a merge, or it is a warning that says so.
3. **Dollars drive the colours.** Tiers come from expected annual loss against the adopter's own appetite bands. Ordinal levels are never multiplied.
4. **One record, many views.** The register, a POA&M, reports and the website are views of the same records, never copies (27 Oct).
5. **Layered checks, never guarantees.** Every control states what it can't stop (for example a repo admin who bypasses the ruleset).
6. **$0 to Dusten.** Bearing never hosts adopters' registers. Only free tiers and free services, each with how its free tier could end (section 10).
7. **Plain words for non-developers.** Anything a non-developer reads (website, brg's comments on a change) says "proposed change", never "pull request"; terminal output for developers keeps Git terms (29 Oct).

## 3. Users and roles

| Who | What they do | How they reach Bearing in v0.1 |
|---|---|---|
| Register maintainer (GRC engineer, security engineer) | Sets up the register, adds and edits records, runs lint | `brg` CLI, Git, pull requests |
| Risk owner (a functional role: Security, Finance, HR…) | Owns risks, reviews them, approves within their authority | Pull request reviews on the Git host; the website to read |
| Approvers by tier (owning role, Security, CISO, executive, Risk Committee) | Approve acceptances and tier changes | Pull request reviews; `brg verify-approvals` checks them |
| Auditor | Reads the register and its history | Website; Git history |
| Non-technical owner (HR, Finance, Facilities) | No way to enter items in v0.1 | Accepted limitation (6 Nov 2026): a non-CLI route comes much later, with no GitHub web editor and no GitHub credentials |

Functional roles only; Bearing never manages users (15 Oct). People map to roles by GitHub username in `roles.yaml`; teams are used only to request reviews through the generated CODEOWNERS (15 Nov, CG#6).

## 4. Scope by version

Version scoping beyond what is listed as decided is **[P]**. v0.1 ships as one release with every feature decided for it so far (23 Oct), built as many small pull requests in four milestones, each with its tests green before the next starts (15 Nov, CG#21):

1. **M1 Records:** schemas, IDs, strict loading, `brg init`, `brg new`, `brg edit`, lint (schema, lifecycle, content safety, confidentiality, duplicates, delete guard), `brg explain`, `brg renumber`, `brg evidence hash`.
2. **M2 Scoring:** appetite config, the qualitative lookup table, the FAIR engine and `brg estimate`, computed-field recomputation, input checks.
3. **M3 Approvals and governance:** `brg verify-approvals`, tier authority, self-approval block, locked records, acceptance limits and expiry, bulk guard, config-change approval, new-risk review, approval fixtures.
4. **M4 Outputs:** `brg due`, `brg summary`, `brg site build`, the Lantern Bay sample register, the generated workflow's publishing step, docs.

| Version | Theme | Contents |
|---|---|---|
| v0.1 | Foundations | Schemas and IDs; `brg init` with its short questionnaire; `brg new` triage for risk, issue, finding and Not sure, with root-cause prompts; qualitative scoring through the generated lookup table; lint (schema, lifecycle gates, content safety, confidentiality, duplicates, computed fields, delete and bulk-change guards); approvals with the self-approval block, tier authority and locked records; acceptance limits and expiry; `brg due` issues with escalation, Slack through GitHub's Slack app (docs and labels only); plain-language change summaries; evidence as link plus hash; CSF anchors; POA&M-ready fields; AI-category fields; approval fixtures for demo and test; Lantern Bay sample register; read-only website with register, risk page and 5×5 heat map; FAIR engine with `brg estimate`, tiers from P50 expected annual loss, and input range and unit checks (6 Nov) |
| v0.2 | Scoring consistency **[P]** | Independent assessments and the divergence flag; reference risks |
| v0.3 | Report and audit | Report packs (executive summary, risk committee pack); `brg history`, `brg snapshot`, `brg audit-export`; loss-exceedance chart; KRIs with thresholds; per-record `classification`; export allow-lists and record counts; mirror-and-restore docs and `brg verify`; report-time content safety |
| v0.4 | Coverage | Framework mappings (SP 800-53 via OSCAL, ISO 27001 IDs via OLIR, HIPAA via CPRT), suggested controls, `brg coverage`, the coverage pack; CMMC decision after a terms check |
| v0.5 | Reach | OSCAL POA&M export |
| After v0.3 (version set later) | | Opportunity records; owner and audit evidence packs; one-person-role warning and role deputies; Presidio as an optional detector; more Git hosts |
| Much later | | A non-CLI way for non-technical owners to propose changes. Direction (6 Nov): a small adopter-hosted web app, sign-in through the company's identity provider, forms reusing `brg new` triage, pull requests opened by one service account (no GitHub accounts for these users), approvals signed with a per-user Bearing passkey (WebAuthn) and checked offline by `brg` against a public-key roster kept in the register |

## 5. Data model

### 5.1 Record types and IDs

| Type | Prefix | Folder | Purpose |
|---|---|---|---|
| Risk | R- | `risks/` | Something that could go wrong. Only risks are scored |
| Issue | I- | `issues/` | Something that has already gone wrong |
| Finding | F- | `findings/` | A problem an audit, test, scan or review found |
| Control | C- | `controls/` | A safeguard that reduces a risk |
| Acceptance | A- | `acceptances/` | A dated, approved decision to tolerate a risk |
| Assessment | **[P]** AS- | `assessments/` | One assessor's score for a risk (independent assessments, v0.2) |

IDs are the prefix plus a zero-padded number (R-0042), stored as strings, never changed once merged. File names are the ID plus a short slug (`risks/R-0042-phished-credentials.yaml`); the slug may change, the ID never does (23 Oct). Vulnerabilities stay in scanners and are referenced from findings, not stored as a record type (27 Oct).

### 5.2 Minimum to create a risk (status `identified`)

Five answers (29 Oct): title; what could happen, as one sentence following "Because [cause], [event], so [consequence]"; owning role; likelihood level; impact level. `brg` fills the ID, dates, status `identified`, type `threat` and horizon 12 months. The tier shows as "unquantified" until a dollar estimate exists.

### 5.3 Fields by tier of requirement (Core / Conditional / Enhanced, 27 Oct)

| Field group | When required | Version |
|---|---|---|
| Title, what could happen, owning role, likelihood, impact | Always (creation) | v0.1 |
| `horizon` (default 12 months) | Always | v0.1 |
| `type` (default `threat`; `opportunity` later) | Always | v0.1 |
| Category (14-category taxonomy anchored to NIST CSF 2.0 and SP 800-30, with "AI and automated decision systems") | At `assessing` **[P]** | v0.1 |
| Current residual assessment, with its control baseline | At `active` | v0.1 |
| Target residual | When a treatment is planned | v0.1 |
| Inherent assessment | Optional | v0.1 |
| Response (accept / avoid / mitigate / transfer / share) with rationale | At `active` | v0.1 |
| Contingency with trigger; secondary-risk links; transfer details | Only when the response calls for them | v0.1 |
| Treatment actions with action owner and dated milestones | When the response is mitigate | v0.1 |
| `objective`, `scope`, `assumptions`, `confidence` | Optional | v0.1 |
| `parent`, `related`, event-driven `triggers` | Optional | v0.1 |
| `evidence` list (URL, collected date, description, SHA-256) | Optional | v0.1 |
| `precedents` list | Optional | v0.1 |
| `dpia`, `soa` references (links out) | Optional | v0.1 |
| AI-category fields: `ai_system`, `aiia` (with status), `lifecycle_stage`, AI trigger presets | Optional, shown only on AI-category risks | v0.1 |
| Non-financial impact (individuals, groups, society, environment) with free text | Optional | v0.1 (13 Nov) |
| POA&M-ready fields: affected assets, vendor dependency flag; on findings: original detection date and source; on acceptances: deviation type | As each record type needs | v0.1 |
| Framework references (CSF anchors) | Optional, never asked on a first risk | v0.1 |
| KRIs with thresholds; `classification` | Optional | v0.3 |

Field names are fixed in the first schema PR. Every field above is optional at creation except the five answers.

### 5.4 Status lifecycle

`identified` → `assessing` → `active` → `accepted` or `monitored` → `closed` or `superseded` (27 Oct). Each gate's required fields are enforced by the sequence lint (for example, assessment before acceptance). Records are never deleted: they close or are superseded (6 Nov).

### 5.5 Computed fields

Score, tier and loss figures are computed by `brg`, marked read-only in the schema, and any hand edit fails lint (23 Oct). Lint also recomputes every stored result from its recorded inputs, engine version and seed, so a well-formed but altered figure fails too (R100).

## 6. Scoring

- **Appetite bands:** dollar edges where Medium, High and Critical start (three edges for four tiers), plus objective, tolerance or limit, indicator, escalation and response (27 Oct). `appetite.yaml` holds one `default` band set and optional per-category entries; a risk's tier uses its category's bands if present, otherwise the default (15 Nov, CG#9). `brg init` writes only the default set, which counts as the adopter's own (6 Nov); per-category entry in init comes later. Bearing ships labelled samples only; `brg` computes no tiers until the adopter sets their own (23 Oct).
- **Qualitative fallback** (27 Oct; table rules 13 Nov, OQ2): five likelihood and five impact levels, each anchored to numbers. The tier comes from a lookup table `brg` generates, so qualitative and dollar-scored risks share the same tier lines. Results are labelled "unquantified".
  - *Likelihood* (fixed; describes how often, not appetite), as loss events per year: Very low under 0.05; Low 0.05–0.2; Moderate 0.2–0.5; High 0.5–0.9; Very high 0.9–3 **[P: the cap of 3 a year]**.
  - *Impact* (per event), derived from the adopter's tier edges E1 < E2 < E3 (where Medium, High and Critical start, in expected annual loss): Very low under E1/10; Low E1/10–E1; Moderate E1–E2; High E2–E3; Very high E3–10×E3 **[P: the E1/10 lower edge and the 10×E3 cap]**. Using annual-loss edges as per-event impact edges is deliberate: at a frequency near once a year the two coincide, and the likelihood axis scales the rest.
  - *Cells:* each cell's expected annual loss ranges from (lowest frequency × lowest impact) to (highest frequency × highest impact). A cell takes the tier of its upper bound, so a cell that crosses a tier line rounds up.
  - *Check on the sample edges* ($100K, $1M, $5M; Claude, 15 Nov): 10 Low, 6 Medium, 4 High, 5 Critical cells out of 25. Rounding up doesn't push most cells to High or Critical. Rows from Very high likelihood down: L M H C C / L L M H C / L L M H C / L L M M C / L L L M H.
  - *Overrides:* adopters may override cells in config; an override is a config change needing governance approval (R98).
- **Tier override for non-financial impact** (6 Nov; guardrails confirmed 13 Nov, OQ5): a governance role may raise a tier for harm to individuals, groups, society or the environment, with a required reason. Raise only, never lower; the dollar-based tier stays visible beside the raised one, labelled as raised; the raise needs the higher tier's approval authority; reports count raised tiers (R33).
- **FAIR** (v0.1, decided 6 Nov): Bearing's own small numpy engine summing losses per event, a seeded RNG recorded with each result, tested against pyfair and riskquant (23 Oct). Tiers from P50 expected annual loss. FAIR vocabulary without Open FAIR text or marks. Simulation contract (15 Nov, CG#8; distribution choices **[P]**):
  - Inputs: loss event frequency (events per year) and loss magnitude per event (dollars), each as minimum, most likely and maximum.
  - Per simulated year: draw the frequency from a PERT distribution over its range; draw the event count from a Poisson distribution with that mean; draw each event's loss independently from a PERT distribution over the magnitude range; sum the year's losses. A year with no events counts as $0.
  - 10,000 simulated years per estimate **[P]**, numpy's PCG64 generator seeded from the recorded seed.
  - Outputs: P10, P50 and P90 of annual loss, plus the mean. The same inputs, seed and engine version always give the same outputs (R97).
  - Not modelled in v0.1: correlation between risks, secondary loss as a separate term, and control effectiveness as an input; adopters fold these into their ranges.
  - Reference fixtures with expected outputs and tolerances live in the tests, cross-checked against pyfair and riskquant.

## 7. Requirements (v0.1 unless marked)

EARS wording: "brg shall …" (always), "When …, brg shall …" (event), "If …, then brg shall …" (unwanted condition), "Where …, brg shall …" (optional feature).

### 7.1 Install and first run

- **R1.** The install docs shall show `uv tool install bearing-register` as the only install path (6 Nov).
- **R2.** When a user runs `brg init` in an empty folder, brg shall ask whether to start an empty register or copy the Lantern Bay sample register.
- **R3.** When the user chooses an empty register, brg shall ask for owning roles (picked from a list, with "add your own") and for one set of tier band edges applying to all categories, then write `bearing.yaml` (with `mode: live`), `roles.yaml`, `appetite.yaml`, the record folders, `.github/workflows/bearing.yml` (rules in R103), `.github/CODEOWNERS` generated from `roles.yaml`, and `.github/pull_request_template.md`.
- **R4.** When `brg init` finishes, brg shall list what remains before the first risk: approvers per tier in `roles.yaml`, and making `brg lint` a required check on the Git host.
- **R5.** When the user chooses the sample register, brg shall copy it with `mode: demo` and the fictional-company notice in its README.
- **R6.** If `brg init` runs in a folder that already holds a register, then brg shall stop without changing any file.

### 7.2 Records, IDs and files

- **R7.** brg shall load YAML strictly against the schema, rejecting values whose type would change silently (for example `NO` read as false, or an ID losing leading zeros) (23 Oct).
- **R8.** When lint finds a file whose name's ID differs from the ID inside it, brg shall report an error.
- **R9.** When lint finds the same ID in two records, brg shall report an error; when a branch adds an ID that another open pull request also adds, lint shall fail on the later pull request. Collisions between pull requests are caught by R101 (15 Nov, CG#13).
- **R10.** `brg renumber <ID>` shall give a record on the current branch the next free ID and update every reference to it.
- **R11.** If a change removes a record file that exists on the default branch, then lint shall report an error whose Fix line says to set the status to `closed` or `superseded` instead. Records created and removed on the same branch, and slug renames, shall pass (6 Nov).
- **R12.** When a new record's title closely matches an existing record's title, lint shall warn (23 Oct).
- **R13.** If a record holds a hand-entered value in a computed field, then lint shall report an error (23 Oct).
- **R14.** If the register repo contains a binary file outside the adopter's allow-listed paths, then lint shall report an error (23 Oct).

### 7.3 Adding records: `brg new`

- **R15.** When a user runs `brg new`, brg shall first ask "What are you adding?" with four choices and a one-line definition each: Risk (something that could go wrong), Issue (something that has already gone wrong), Finding (a problem an audit, test or review found), Not sure (28 Oct).
- **R16.** When the user picks Risk, brg shall ask the five answers of section 5.2, numbered 1/5 to 5/5, with likelihood and impact choices showing their numeric anchors and dollar bands inline (29 Oct).
- **R17.** When a risk title reads like a gap (for example starting "Lack of", "No" or "Missing"), brg shall offer "This sounds like a finding. Keep as risk, or switch?" with the hint line "A risk says what could go wrong, for example 'Attacker signs in with a stolen password'." Either choice shall take one keypress (28–29 Oct).
- **R18.** When the user picks Issue, brg shall ask title, what happened, when it happened or was found, and owning role, then offer an optional fix-by date and an optional incident or ticket link, each skippable with Enter (6 Nov).
- **R19.** When the user picks Finding, brg shall ask title, what was found, who or what found it (external audit, internal audit, penetration test, scanner, access review, other), when it was found, and owning role; for a scanner finding it shall ask for the scanner's finding ID and store no scan details.
- **R20.** When the user picks Not sure, brg shall ask, in order and stopping at the first yes: "Did an audit, test, scan or review find this?" (Finding), "Has it already happened?" (Issue), "Could it happen in the next year?" (Risk). If all three are no, brg shall say no entry is needed and write nothing (6 Nov).
- **R21.** After the fields of an Issue or Finding, brg shall run the root-cause steps: first "What caused this?", then "You said: <their last answer>. What led to that?", showing "Step N of up to 5" (23 Oct).
- **R22.** After each root-cause answer, brg shall ask "Can someone act on this directly? (y/n)"; a yes, or step 5, shall end the chain and save it (6 Nov).
- **R23.** When the user types `?` at a root-cause step, brg shall save the record and its chain so far and flag it for follow-up in `brg due` (23 Oct).
- **R24.** Prompts shall never say "why" as a command or "5-Whys"; the docs explain the method (23 Oct).
- **R25.** After the root-cause steps, brg shall ask which risk the issue or finding belongs to, offering the closest matches with their tiers, and shall require either a link to a risk or a recorded reason that none applies (23 Oct).
- **R26.** When an issue is linked to an existing risk, that risk shall stay active and linked (27 Oct).
- **R27.** When brg creates a record, it shall print the file path, the status, the next step, and any warning that applies (for example a High unquantified risk).
- **R28.** `brg edit <ID>` shall open a record for adding optional and conditional fields, prompting for what the record's next status gate requires **[P: interaction detail]**.
- **R29.** brg shall never write to the default branch; created and edited records reach it only through a pull request.

### 7.4 Scoring and tiers

- **R30.** If `appetite.yaml` holds no adopter-set bands, then brg shall compute no tiers and lint shall report error BRG-E101 (23 Oct).
- **R31.** brg shall compute a qualitative risk's tier from the generated lookup table, never by multiplying levels, and label it "unquantified" (27 Oct).
- **R32.** When a High or Critical risk is unquantified, lint shall warn (BRG-W110) without blocking (27 Oct).
- **R33.** When a tier override for non-financial impact is present (13 Nov, OQ5):
  - (a) if the override is not higher than the dollar-based tier, lint shall report an error (raise only);
  - (b) brg shall show both tiers wherever the tier appears, labelling the higher one "raised for non-financial impact";
  - (c) lint shall require a reason, and `brg verify-approvals` shall require the raised tier's approval authority;
  - (d) report counts and the register's sort shall use the raised tier and state how many tiers are raised.
- **R34.** `brg estimate <ID>` shall add a FAIR estimate (ranges for loss event frequency and loss magnitude) to a risk, compute its expected annual loss at P10, P50 and P90, set its tier from P50 against the appetite bands, and record the engine version and seed with the result (6 Nov).

### 7.5 Lint messages

- **R35.** Every lint message shall show severity, rule code, file and line (or "this branch"), one plain sentence of what is wrong and why, and a line starting "Fix:" (6 Nov).
- **R36.** Errors shall fail the check and block the merge; warnings shall never fail it (6 Nov).
- **R37.** `brg explain <rule code>` shall show the rule, why it exists and an example of passing and failing records.
- **R38.** Rule codes shall follow `BRG-E` or `BRG-W` plus three digits **[P]** grouped by area: 0xx–1xx setup, schema and records; 2xx lifecycle and acceptances; 3xx change control; 4xx content safety and confidentiality.
- **R39.** Lint shall end with the counts of errors and warnings and the number of records checked.

### 7.6 Lifecycle and change control

- **R40.** Lint shall enforce each status gate's required fields (section 5.3) and the required sequence, for example an assessment before an acceptance (23 Oct).
- **R41.** When a pull request changes a record, lint shall require a reason for the change in the pull request template's reason field (23 Oct).
- **R42.** When a pull request changes the owning role of a risk, brg shall require a review request to the new owner's role (23 Oct).
- **R43.** When a pull request edits an accepted risk, brg shall require a fresh approval of the authority for that risk's tier (23 Oct).
- **R44.** When a change edits more than a threshold of records' meaning fields (likelihood, impact, FAIR inputs, tier, owner, status, response, acceptance; sample threshold 10, adopter-set), lint shall require a "Bulk change: why" reason in the pull request, and brg's summary shall list every record changed. If any of those records is High or Critical before or after the change, brg shall also require one approval from a governance role set in config (sample: the CISO) (6 Nov; 13 Nov, OQ4). How records are counted is R102.
- **R45.** Typo fixes and slug renames shall not count toward the bulk threshold (6 Nov).

### 7.7 Approvals

- **R46.** `brg verify-approvals` shall run as a required status check on pull requests where the host supports required checks, and shall pass only when every acceptance, tier change, new risk (R99) and config change (R98) in the pull request has the approvals it requires (18 and 23 Oct; 15 Nov). It shall count only approving reviews on the pull request's current head commit from users listed for the required role, as read under R104.
- **R47.** If the pull request's author is the approving authority, then `brg verify-approvals` shall not count their approval, at every tier (23 Oct).
- **R48.** A tier change shall need the approval authority of the higher of the two tiers (29 Oct).
- **R49.** `roles.yaml` shall list each role's members by GitHub username, optionally name a team used only to request reviews, name an `executive` per role, and name the approving roles per tier (15 Nov, CG#6; amends OQ10). The Lantern Bay sample: Low, another member of the owning role; Medium, the owning role plus Security; High, the CISO plus the executive over the owning role; Critical, the Risk Committee (23 Oct).
- **R50.** If no approvers are set for a tier, then lint shall warn (BRG-W021) that acceptances at that tier can't be approved yet.
- **R51.** Where `mode: demo` is set on the default branch, `brg verify-approvals` shall read approval fixtures instead of the host API (23 Oct). Tests supply fixtures by passing a fixture provider to the code under test; brg shall never detect a test run from the environment (15 Nov, CG#2).
- **R52.** If an approval fixture file exists, or fixtures are requested, while `mode` is not `demo`, then lint shall report an error and `brg verify-approvals` shall fail (fail closed) (23 Oct; 15 Nov, CG#2).
- **R53.** When approvals come from fixtures, every summary, page and report shall mark them "SIMULATED" (23 Oct).

### 7.8 Acceptances, reviews and `brg due`

- **R54.** Every acceptance shall have an expiry date within its tier's limit; sample defaults Low 12 months, Medium 12, High 6, Critical 3 (6 Nov).
- **R55.** If an acceptance's expiry is past its tier's limit, then lint shall report an error.
- **R56.** Renewal shall be a new acceptance with a new rationale and a fresh approval at the same tier authority, never an edited date (6 Nov).
- **R57.** When an acceptance is 30 days from expiry, `brg due` shall open a host issue for the owning role (6 Nov).
- **R58.** If an acceptance has expired, then brg shall treat the risk as unaccepted and lint shall report error BRG-E214 on the next change, until the risk is renewed or treated. brg shall never change a record's status by itself (6 Nov).
- **R59.** `brg due` shall open or update one host issue per overdue item (review dates, treatment milestones, flagged root-cause chains, expiring acceptances), labelled for filtering (for example `bearing:overdue`), and shall escalate when an item stays overdue (23 Oct): at 14 days overdue, or on the first day for a Critical item, the issue shall mention the executive over the owning role, once per item, and add the label `bearing:escalated` (13 Nov, OQ6).
- **R60.** Review cadence defaults (sample, adopter-set): Critical, continuous monitoring with prompt escalation; High treatment actions, weekly or biweekly; risk-owner review, monthly; risk committee, quarterly plus exceptions; methodology, taxonomy and appetite, annually and after material change (27 Oct).
- **R61.** `brg due` issues shall carry only an ID, tier, due date and a link, never risk details, so a Slack channel subscribed to them through GitHub's Slack app holds no register content (21–23 Oct).
- **R62.** If a `brg due` notification step fails, then it shall not fail a required check.

### 7.9 Change summaries

- **R63.** When a pull request changes register records, brg shall post or update one comment summarising it in plain sentences: what changed and why, the approvals needed and who has given them, and check results, with the field-by-field table collapsed under "Details" (29 Oct).
- **R64.** The summary shall say "proposed change", not "pull request" (29 Oct).

### 7.10 Content safety and confidentiality

- **R65.** Lint shall require links to use https and reject `javascript:`, `data:` and `file:` links, bare IP addresses, link shorteners and links with embedded credentials; it shall warn on mixed-script (lookalike) domains (23 Oct). Links shall be parsed with one standard URL parser; lint shall reject any user-info part, reject percent-encoded or otherwise non-canonical hosts, convert internationalized hosts to their ASCII (IDNA) form before the other checks, and warn when that form is punycode (15 Nov, CG#15). The docs shall say a passing link is not a verified or safe destination.
- **R66.** Lint shall reject invisible and bidirectional-override Unicode characters and warn on instruction-like phrases in free text (23 Oct).
- **R67.** brg shall never fetch a link or call an external scanner (23 Oct).
- **R68.** Where the adopter sets an evidence-link domain allow-list (off by default), lint shall warn or fail, as configured, on links outside it (23 Oct).
- **R69.** `brg evidence hash <file>` shall print the file's SHA-256 without storing the file (23 Oct). The docs shall say the hash proves only that a file matches the one hashed, and that the evidence entry should record who collected it and where the hashed copy is kept (15 Nov, CG#17).
- **R70.** The generated register workflow shall run gitleaks secret scanning as a required check (23 Oct).
- **R71.** Lint shall warn on personal-data patterns (email addresses, phone numbers, ID-number patterns) in free-text fields (23 Oct). The docs shall explain how to remove personal data from Git history and the limits of doing so: clones and forks keep their copies (15 Nov, CG#18).
- **R72.** The website shall HTML-escape all register text and run no inline scripts **[P: applies the 23 Oct report-time rule to the v0.1 website, since it renders register text]**.

### 7.11 Website (read-only)

- **R73.** `brg site build` (13 Nov, OQ7) shall generate a static, read-only website from the register, with no server and no forms.
- **R74.** The register page shall show ID, title, category, owning role, status, tier with expected annual loss (P50) where quantified, and next review, sorted by tier then dollars (29 Oct). By default it shall show open records, with a visible count of closed and superseded records and a one-click filter to show them; every record, in any status, keeps its own page (15 Nov, CG#11).
- **R75.** Each risk page shall show what could happen, the assessment (with engine version and seed when quantified), treatment, controls with their CSF "related to" IDs, evidence as link plus hash, acceptance, linked issues and findings, and a logbook history (29 Oct).
- **R76.** The heat map shall be a 5×5 grid coloured by the generated tier lookup, with unquantified risks outlined (29 Oct).
- **R77.** A tier colour shall always appear with its tier label and, where quantified, its dollar figure (18 Oct; 3 Nov).
- **R78.** The site shall use the Bearing Quest design system: the approved tier scale (Low #D6E4F0, Medium #8DB0D9, High #5E5BA8, Critical #3B1E6B in light; #2E4A72, #6F93C4, #A9A4EC, #E2D2FB in dark), the Register mark, and the Bearing Quest mark beside the Bearing Register name in the header; orange stays out of data views (29 Oct; 3 Nov).
- **R79.** The site shall meet WCAG 2.2 AA in light and dark themes, checked by a token contrast test (29 Oct).
- **R80.** Where `mode: demo` is set, every page shall show the fictional-company notice under the header and in the footer (29 Oct).
- **R81.** The site shall self-host its fonts (Inter, IBM Plex Mono, Cinzel for the wordmark only) and make no third-party requests **[P: no third-party requests]**.

### 7.12 Framework content

- **R82.** brg shall ship NIST CSF 2.0 anchors for the taxonomy, and framework fields shall always be optional and never asked for on a first risk (28 Oct).
- **R83.** Coverage and references shall always be labelled "related to", never "satisfies" (18 and 28 Oct).
- **R84.** The repo shall have one NOTICE file covering shipped third-party content (18 Oct).
- **R85.** brg shall ship no SOC 2 criteria IDs or text, no PCI DSS or CIS content, and no ISO text or titles; ISO/IEC 42001 Annex A references stay adopter-plugin only (6 Nov); the docs shall include a "Using Bearing for SOC 2" page explaining the NIST route (28 Oct).
- **R86.** (v0.4) brg shall ship SP 800-53 Rev 5 controls from NIST's CC0 OSCAL content, ISO/IEC 27001:2022 clause and Annex A IDs only through NIST's OLIR crosswalk (with item 21's pinning and parsing rules), HIPAA Security Rule mappings through NIST's CPRT, suggested controls, `brg coverage` and the coverage pack (28 Oct).
- **R87.** Optional tags shall accept MITRE ATT&CK technique IDs (with MITRE's notice) and OWASP Top 10 category IDs and names (28 Oct).

### 7.13 Sample register (Lantern Bay Software)

- **R88.** The sample shall describe Lantern Bay Software, a fictional ~250-person B2B customer-support SaaS with an AI assistant, with eight owning roles (Security, IT Operations, Platform Engineering, Product/AI, Finance, Legal & Compliance, HR, Facilities) and a Risk Committee (23 Oct).
- **R89.** The sample's risks shall be written in Bearing's own words and include a deliberate spread of treatments (some accepted, transferred and avoided, not only mitigated), tiers (including High and Critical after controls), issues, findings and an expired or expiring acceptance, so the demo exercises every flow (3 Nov). The Perplexity sample sheet is input only, not copied (its SOC 2 IDs, L × I scores and seven wrong CMMC IDs are excluded).
- **R90.** The sample shall pass `brg lint` in demo mode, and its simulated approvals shall show "SIMULATED".

### 7.14 Bearing's own repo and CI

These apply to Bearing's source repo, following the maintainer's engineering baseline (items 29–33).

- **R91.** Required checks shall include `lint` (ruff check and format) and the test job, reported by GitHub Actions only (integration 15368); third-party actions shall be pinned to commit SHAs.
- **R92.** The first code PR shall add `uv.lock`, move the settings guard test onto locked dependencies, add a root Python `.gitignore`, and add Dependabot for uv and github-actions (monthly, minor and patch grouped, 7-day cooldown, majors separate) (items 20e, 31, 33).
- **R93.** A scheduled daily pip-audit shall run on main, and each release shall carry a CycloneDX SBOM (item 32).
- **R94.** Every lint rule shall have a test with at least one passing and one failing record.
- **R95.** The repo shall carry the base PR template and an agent rule to fill in its sections (items 29–30).

### 7.15 Added 6 Nov 2026: FAIR inputs and config changes

- **R96.** If a FAIR estimate's ranges are out of order (min above likely, likely above max), negative, missing their unit, or outside plausible bounds the adopter can set in config **[P: default bounds]**, then lint shall report an error naming the field and the expected form (23 Oct candidate n; moved to v0.1 6 Nov).
- **R97.** The FAIR engine shall be tested against pyfair and riskquant on shared fixtures, and the same seed shall always give the same result (23 Oct).
- **R98.** When a pull request changes `roles.yaml`, `appetite.yaml`, the likelihood and impact scales, lookup-table overrides, or the `mode` setting in `bearing.yaml`, `brg verify-approvals` shall require an approval from the governance role as defined on the default branch (sample: the Risk Committee), and the author's own approval shall not count (6 Nov; `mode` and authority source 15 Nov, CG#1–2).

### 7.16 Added 15 Nov 2026: ChatGPT review

- **R99.** When a pull request adds a risk, brg shall require a review from a member of its owning role (not the author); when the new risk is High or Critical, `brg due` or the summary step shall mention the executive over the owning role. Adding a risk shall never need tier-authority approval (15 Nov, CG#4).
- **R100.** Lint shall recompute every stored FAIR result from its inputs, engine version and seed, and report an error if P10, P50, P90 or the tier differ. If the recorded engine version differs from the installed one, lint shall warn and suggest `brg estimate <ID> --recompute` instead (15 Nov, CG#7).
- **R101.** The setup docs and `brg init`'s closing list (R4) shall require the ruleset option that branches be up to date before merging, so a second pull request is re-checked after the first merges; the generated workflow shall also run lint on pushes to the default branch and fail on duplicate IDs (15 Nov, CG#13).
- **R102.** The bulk count (R44) shall be the number of distinct records whose meaning fields differ between the default branch and the pull request head. Added and removed records count; a rename counts only if a meaning field changed. Tests shall cover counts one below, at and one above the threshold (15 Nov, CG#14).
- **R103.** The generated `bearing.yml` shall: trigger on `pull_request` and on pushes to the default branch, never `pull_request_target`; set `permissions:` per job, with `contents: read` by default and `pull-requests: write` or `issues: write` only on the jobs that comment or open issues; use no secrets in v0.1; pin every action to a commit SHA; and give fork pull requests read-only checks. A test shall assert these properties of the generated file (15 Nov, CG#3).
- **R104.** `brg verify-approvals` shall read `roles.yaml`, `appetite.yaml` and `bearing.yaml` from the default branch, never from the pull request, when deciding who may approve and what a change needs. A user not listed on the default branch shall not count. If the host API can't return the reviews, the check shall fail (15 Nov, CG#1, CG#6).
- **R105.** Where `mode: demo` is set, the generated workflow shall build the site and publish it to GitHub Pages. In live mode, `brg site build` shall write the site to a local folder with a "Confidential" banner on every page, and the generated workflow shall not publish it (15 Nov, CG#5).
- **R106.** The docs shall include a cost matrix: Dusten (maintainer) $0; a public register $0; a private register needs GitHub Team, or another host with required checks, for the checks to block merges, otherwise they only detect (15 Nov, CG#22).

## 8. Commands in v0.1

| Command | Purpose |
|---|---|
| `brg init` | Start a register (empty with questionnaire, or sample) |
| `brg new` | Add a risk, issue or finding through triage |
| `brg edit <ID>` | Add fields a record's next status needs |
| `brg lint` | Check schema, rules, content safety |
| `brg explain <code>` | Show a lint rule with examples |
| `brg verify-approvals` | Required check for approvals and authority |
| `brg due` | Open and update issues for overdue and expiring items |
| `brg renumber <ID>` | Fix an ID collision before merge |
| `brg evidence hash <file>` | Print a file's SHA-256 |
| `brg summary` | Post the plain-language change summary in CI |
| `brg site build` | Build the read-only website (publishes only in demo mode, R105) |
| `brg estimate <ID>` | Add a FAIR estimate and compute the tier from dollars |

## 9. Non-goals

- Scanner, SIEM and incident integrations; Bearing never reads from Slack or any other service (15 and 23 Oct).
- User and identity administration; policy and vendor management; a database-backed server.
- Hosting adopters' registers (18 Oct).
- Telemetry of any kind (25 Oct).
- GitHub's web editor or GitHub credentials as the route for non-technical owners (6 Nov).
- Storing evidence files or scan details in the register (23 and 27 Oct).
- Shipping SOC 2, PCI DSS, CIS or ISO text (28 Oct).
- Import from spreadsheets or other tools (18 Oct; design recorded for later).
- Multiplying ordinal levels to make scores (27 Oct).

## 10. Cost

| Item | Cost | How the free tier could end |
|---|---|---|
| Source repo on GitHub, public, with Actions, rulesets and CodeQL | $0 | GitHub changes free terms for public repos |
| Demo website hosting on GitHub Pages (13 Nov, OQ3) | $0 | Pages limits or acceptable-use terms |
| PyPI publishing | $0 | PyPI policy change |
| Cross-checks (Perplexity, Gemini app, ChatGPT, CodeRabbit) | $0 | Free tiers' limits change |
| Paid API tokens | None used | |
| Adopters' costs (not Dusten's) | Enforcing approvals on private registers needs GitHub Team or another host with required checks | |

## 11. Privacy and confidentiality

- Adopters keep their register in their own private repo; Bearing never sees it.
- brg makes no network calls except to the Git host's API for approvals, issues and summaries in CI, and never fetches links (R67).
- Live registers' sites are built locally and never published by the generated workflow (R105).
- No telemetry. Adoption visibility comes from ADOPTERS.md and an anonymous Discussions thread (25 Oct).
- Secret scanning and personal-data warnings run on every register change (R70–R71).
- `brg due` issues carry no risk details (R61); Slack history on free plans is 90 days, so no register content should reach it.
- During development only public material and the fictional sample go to free-tier AI tools, never a real company's register (18 Oct).
- Adopters should not publish real registers on GitHub Pages; private Pages needs GitHub Enterprise Cloud (18 Oct research).

## 12. Threat model

Assets: register records and their history; approval decisions; the integrity of computed tiers; evidence references; adopters' confidential content; Bearing's own release artifacts.

Trust boundaries: contributor's machine → Git host; pull request → required checks; Git host API → `brg verify-approvals`; register text → website and (later) AI report packs; Bearing's release → adopters' CI.

| Abuse case | Control | What it can't stop |
|---|---|---|
| Someone edits `roles.yaml` or `appetite.yaml` to change who approves or where tiers start, including adding themselves to the governance role | R98 governance approval, with authority read from the default branch (R104); no self-approval | A repo admin bypassing the ruleset; a governance role that approves carelessly |
| Untrusted pull-request code abuses the workflow token | R103 least-privilege permissions, `pull_request` only, no secrets | A compromised pinned action |
| A new risk enters already under- or over-rated | R99 owning-role review; executive notice for High and Critical | A reviewer who doesn't read it |
| A stored loss figure or tier is altered but well-formed | R13 and R100 recomputation from inputs and seed | Altered inputs, which the change review and summary show |
| A confidential register is published | R105 publishing only in demo mode | An adopter who publishes the local build by hand |
| An author approves their own acceptance or tier change | R47 self-approval block; R46 required check | A repo admin bypassing the ruleset |
| A risk is under-rated to avoid approvals | R48 higher-tier authority for tier changes; R13 computed tiers | Dishonest inputs that stay within a tier |
| Many records changed quietly in one change | R44–R45 bulk guard and full listing | Many small changes over time |
| A record is deleted or closed to hide it | R11 delete block; closed records stay findable on the site (R74); Git history; ruleset blocks force pushes | Admin bypass; hosts without required checks (detective only) |
| Two pull requests take the same new ID | R101 up-to-date branches and lint on the default branch | A ruleset without the up-to-date option |
| Approval fixtures used to fake approvals in a live register | R51–R53 fixtures only when the default branch is in demo mode, no environment detection, fail closed in live mode, SIMULATED marking; a change to `mode` needs governance approval (R98) | A repo admin bypassing the ruleset |
| Another app reports a check named `lint` to satisfy it | Required checks pinned to GitHub Actions as the source (R91) | Compromise of GitHub Actions itself |
| Hand-typed or coerced values (YAML type conversion) | R7 strict loading; R13 computed fields | |
| Malicious links or prompt injection in register text | R65–R67 link, URL-parsing and Unicode rules, never fetching; R72 escaping. AI report packs arrive in v0.3 with their own controls (23 Oct: delimited untrusted data, non-agentic use, human review) | Text that is harmful but passes the patterns |
| Cross-site scripting through the website | R72 escaping and no inline scripts; static site with no forms | |
| Secrets or personal data committed | R70–R71 gitleaks and pattern warnings | Patterns the scanners miss; history keeps what was committed |
| Evidence swapped after collection | R69 SHA-256 recorded with each link | Evidence that was wrong when hashed; the hash proves a match only to the copy that was hashed |
| Zombie acceptances | R54–R58 expiry limits, warnings, lint failure | |
| Supply-chain compromise of Bearing | SHA-pinned actions, locked dependencies, daily pip-audit, Dependabot, SBOM (R91–R93) | A malicious release of a pinned dependency before advisories exist |
| Private register on a free plan with no required checks | Docs state checks are detective there, not preventive | Merges that skip checks |

## 13. Open questions (all decided by 13 Nov 2026; kept as the record)

- **OQ1. Decided 6 Nov 2026:** the FAIR engine, `brg estimate`, and the input range and unit checks all move into v0.1 (R34, R96). Supersedes the 23 Oct timing of input checks "in v0.2 with the FAIR engine".
- **OQ2. Decided 13 Nov 2026:** as recommended. To write out in the next revision: how five impact bands come from three tier edges, and how annual-loss edges translate to per-event impact; check that round-up doesn't push most cells to High or Critical. Was: **Qualitative lookup table.** Where do the five impact-level dollar bands and likelihood anchors come from (init asks only tier edges), and how is each cell's tier computed? Recommendation: ship numeric anchors for likelihood as fixed defaults (they describe probability, not appetite), derive impact-level bands from the tier edges, compute each cell from the band ranges' expected annual loss rounding up when a cell straddles a tier line, and let adopters override cells in config with approval.
- **OQ3. Decided 13 Nov 2026:** GitHub Pages for the v0.1 demo site. Was: **Demo hosting.** GitHub Pages (no AWS) or a CloudFront Free flat-rate plan (deferred items 2, 4 and 7). Recommendation: GitHub Pages for v0.1; it needs no AWS account work.
- **OQ4. Decided 13 Nov 2026:** confirmed as written. Was: **Bulk guard details.** Confirm "High or Critical before or after the change" and the CISO as the sample governance role.
- **OQ5. Decided 13 Nov 2026:** confirmed, in v0.1. Was: **Non-financial override guardrails.** Confirm raise-only, both tiers shown, higher-tier authority, and v0.1 timing.
- **OQ6. Decided 13 Nov 2026:** as recommended (14 days; Critical day 1). Was: **Escalation in `brg due`.** Recommendation: when an item is 14 days overdue **[P]**, the issue mentions the executive over the owning role; Critical items escalate on day 1.
- **OQ7. Decided 13 Nov 2026:** kept. Was: **Command names.** `brg summary` and `brg site build`.
- **OQ8. Decided 13 Nov 2026:** adopted as recommended, Scorecard after v0.1. Was: **Open-source setup in v0.1 (item 5).** Recommendation: SECURITY.md with private vulnerability reporting, CONTRIBUTING.md with DCO sign-off, semantic versioning, PyPI Trusted Publishing for the first release (which also secures the name, item 9), and OpenSSF Scorecard later.
- **OQ9. Decided 13 Nov 2026:** one sentence, as recommended. Was: **"What could happen" structure.** Kept as one sentence (29 Oct). Recommendation: no separate cause, event and consequence fields in v0.1; revisit if reports need them.
- **OQ10. Decided 13 Nov 2026, amended 15 Nov 2026:** approvers are GitHub usernames per role in `roles.yaml`, read from the default branch; teams only request reviews (CG#6: Actions' `GITHUB_TOKEN` can't read team membership). Was: **Approver mapping.** Recommendation: `roles.yaml` maps roles to GitHub teams, falling back to usernames, and the generated CODEOWNERS follows it.

## 14. Definition of done for v0.1

- At least one Lantern Bay risk per tier is quantified with `brg estimate`, and the website shows its dollars.
- Every v0.1 requirement in section 7 has a test or a documented manual check, and every lint rule has passing and failing fixtures (R94).
- The Lantern Bay sample passes `brg lint` and `brg verify-approvals` in demo mode, and the website builds from it with every page in both themes passing the contrast test.
- First-risk test (15 Nov, CG#19): start in a register just created by `brg init`, with the questionnaire answered; end when `brg new` writes the risk file. Record the number of prompts answered (target 5 plus triage) and the time (target under 5 minutes) on the first attempt. Run by Dusten and, where possible, by one person who hasn't used brg.
- The four milestones (section 4) are complete in order, each with its tests green.
- Required checks on Bearing's repo: `lint`, tests, gitleaks, CodeQL; daily pip-audit and Dependabot running (R91–R93).
- Docs: README quick start, setup including required checks, the "proposed change" explainer, "Using Bearing for SOC 2", the review cadence and acceptance defaults, and the limits of each control.
- NOTICE file, SECURITY.md and the open-source items chosen under OQ8.
- `docs/decisions.md` carries a row for each decision taken while building.
- The design pack (`docs/design.md`, `docs/design/`) is in the repo and the website follows it (item 27).
