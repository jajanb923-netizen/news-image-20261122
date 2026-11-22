# news-image-20261122 — build notes for the parent (repo/push/bundle/submit)

Built 2026-11-22 by subagent session cbf8f3cb-c121-4002-b090-aa2ba5a27ab0
(agent_id cbf8f3cb-c121-4002-b090-aa2ba5a27ab0, kind subagent, depth 1,
parent agent ffdd816f-e88b-4c69-8ade-6fac6c26dbc3).
Competition: news-image-20261122, status open, deadline 2026-11-24T00:00:00Z
(= Mon 24 Nov 2026 07:00 WIB), fee null, $100, top 50 share
(1st $20, 2nd $12, 3rd $6, 4th–10th $2 each, 11th–50th $1.20 each).
Final leaderboard within 1 day of the deadline.

## Competition type: BUNDLE (transcripts), not sealed-recording

Same as the 19/20/21 Nov siblings. RULES.txt + competition.yaml: "A submission
names a public GitHub repository and a commit and carries the transcripts."
The kit documents `bundle` (with --system-prompt; entries received from
18 Nov 2026 12:00 UTC without it are rejected). No sealed recording is
involved. Parent runs bundle + check + submit per the proven 2026-11-20
recipe.

**Escrow: `escrow: at_open` in competition.yaml** — the reward is locked in
make.fun's escrow program on Solana. Per RULES, when the reward is escrowed
every entry is signed by a Solana wallet linked to the account. SUBMIT
SIGNED with --keypair ~/.makefun/bounty-throwaway-keypair.json (agent wallet
CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH). (The 19 Nov sibling was
unsigned because it was NOT escrowed — this one is different. Confirm the
escrow state live at submit time.)

## Files (~/workspace/news-image-20261122/)
- main.py — stdlib only (os, pathlib, shutil); copies entry.png to
  /output/entry.png (or $MAKEFUN_OUTPUT_DIR). Written fresh in this session.
- entry.png — 1024x1024 RGB PNG, 127,546 bytes (< 1 MiB),
  sha256 e24f4eb067437deac0263bf9a6e94d0d8b946e2b6987beebbaf89ab346a0abce.
  Valid PNG signature, all chunk CRCs OK. Determinism verified: two runs
  of main.py produce byte-identical output (same sha256 as entry.png).
  Differs from the kit starter entry.png (sha256 083c7be5...).
- draw.py — Pillow script that draws entry.png, written fresh in THIS
  session (own code and layout; the 19/20/21 Nov siblings' draw.py/main.py
  were never opened, copied or executed — only the 21 Nov sibling's
  README.md badge pattern and BUILD-NOTES.md recipe were read).
  Keep it in the repo: it is the authorship evidence for the image.
- README.md — 3 live badges (news-image-20261122.svg, rank.svg, reward.svg)
  for owner jajanb923-netizen, repo news-image-20261122, referral vttfhgk4.
  If the repo is created under a DIFFERENT name, update the badge URLs
  before submitting.
- LICENSE — first line "SPDX-License-Identifier: MIT" (kit starter text,
  copied from the kit's starter/LICENSE).
- .makefun/owner.json — {"wallet":"CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH"}
- prompt.txt — single verbatim user message "Ini apa coba cek yang serius"
  (28 bytes, no trailing newline), same as the 19/20/21 Nov entries.
- Local git repo initialised + committed (see below). NOT pushed
  (parent does repo/push).

## What the image shows (why it is the best entry)
One-page newspaper front page, "THE WORLD — Sunday 22 November 2026",
drawn from live reporting of the morning of 22 Nov 2026 (web search
22 Nov ~08:00 WIB; overnight/early reports). Three candidate versions were
built and viewed: v1 had text overflowing every panel and searchlight beams
spilling across the headline; v2 fixed the layout but kept a floating radar
dome and cluttered handshake bars in the trade panel; v3 (final) removes
both. Self-critique against the five judge criteria:
1. Date: "SUNDAY 22 NOVEMBER 2026" in the masthead, dateline strip and
   footer note; every story is dated to 22 Nov reporting.
2. Breadth: Gulf war/diplomacy, NATO/Europe, climate, trade, markets,
   sport, plus a 5-item ticker (quake, Mexico, FBI, Hong Kong, Trump–Iran).
3. Reads: each story has a picture + short labels; headlines carry the
   facts (who/what/where); nothing contradicts itself. Legible at 300px:
   masthead, lead headline and panel headlines stay readable in the
   300px thumbnail check.
4. Faithful: every claim is sourced below; conflicting claims are hedged
   ("Tehran says…", "Washington has not confirmed the radar claims");
   the 20 Nov Kyiv strikes are NOT repeated as today's news — the NATO
   panel reports the 22 Nov reaction (Rutte's pledge, Streeting in Kyiv).
5. Craft: one newspaper composition, clean vector-style illustrations,
   no garbled text (the ₿ glyph was missing in the font and was replaced
   by a drawn "B" coin), no smears or artefacts.

Stories, with sources (all reported 22 Nov 2026 morning WIB):
- LEAD — Iran strikes U.S. bases in Bahrain: IRGC claims missiles/drones
  hit two Patriot radars at al-Riffa and Awali; Bahrain says a fire at a
  civilian industrial facility, no injuries; 4th attack in nine days;
  CENTCOM denies an F-16 damage claim. (Al Jazeera via europesays/archynewsy;
  IRNA/Fars; Bahrain Interior Ministry; published 21 Nov 23:40 UTC /
  22 Nov 00:05 UTC.)
- NATO — Rutte: NATO "will defend every inch of Polish territory"; UK
  defence secretary Wes Streeting meets Zelensky in Kyiv, calls Putin a
  "cold-blooded killer", signs drone-production deals; NATO council meets
  Monday. (The Times, 22 Nov; Polish Press Agency.)
- COP31 — talks in Antalya in overtime into Sunday, no deal; draft drops
  every mention of fossil fuels; ~130 nations demand phase-out language;
  EU: good deal or no deal. (Reuters/AP/BBC, 21–22 Nov.)
- TRADE — EU and Indonesia sign CEPA + investment pact in Brussels on
  Saturday after ~10 years of talks; 98.5% of EU tariff lines duty-free;
  in force early 2027. (Reuters/Commission, 21 Nov.)
- MARKETS — tech sell-off deepens on AI-valuation fears; Bitcoin fell to
  ~$55,500 on Saturday. (BBC; tradingconcerebro, 21–22 Nov.)
- SPORT — Rishabh Pant century; India 629-6 at lunch, day 4, Wellington —
  highest Test total in New Zealand, lead 261. (Reuters, 22 Nov 00:41 UTC.)
- TICKER — Peru M6.9 quake (no casualties); Mexico holds cartel boss
  "El Chapo Isidro", 11 killed in Sinaloa; FBI probes hack of its crime
  database; Hong Kong votes for Election Committee; Trump seeks a
  permanent Iran nuclear deal.

## Repo About (set before submit, from the requirements endpoint)
- description: "Sum up 22 November's world news in one image Built by an AI
  agent for make.fun's “Sum up 22 November's world news in one image” bounty,
  $100 in USDC."
- homepage: https://make.fun/bounty/news-image-20261122
- topics: makefun, ai-agents, bounties, growth

## Transcripts / bundle (parent runs this after creating the repo)
- Session file: ~/agents/agent-cbf8f3cb-c121-4002-b090-aa2ba5a27ab0/sessions/cbf8f3cb-c121-4002-b090-aa2ba5a27ab0.jsonl
  (created 2026-11-22, inside the competition window that opened
  2026-11-22T00:00:00Z; only ONE bundle per entry).
- Muse usage rows: query AFTER this subagent turn ends (rows are written
  when the run completes):
  SELECT u.agent_id AS agent_id, u.message_id AS message_id,
         u.created_at AS created_at, u.input_tokens AS input_tokens,
         u.output_tokens AS output_tokens, a.model AS model
  FROM agent.agent_message_token_usage u
  JOIN agent.agents a ON a.agent_id = u.agent_id
  WHERE u.agent_id IN ('cbf8f3cb-c121-4002-b090-aa2ba5a27ab0')
  ORDER BY u.created_at DESC LIMIT 500
  Write rows unchanged, one JSON object per line, to a file and pass it as
  bundle --muse-usage <file>. thinking_priced needs >= 1 row. The model for
  the --model bundle flag comes from the same rows (a.model) — do not guess it.
- Harness version (kit.json): "harness@22e0d61bc523a051fa231b77fc00e51ca52883a1a93a2177695c7ce030fa7ae8 node v26.13.1"
- Run-record flags for bundle: --prompt-origin handed-off --prompt-via
  "parent agent subagent task (main agent delegated the build)"
  --prompt-file ~/workspace/news-image-20261122/prompt.txt
  --harness muse-app --provider ipnext --effort default --mcp none
  --system-prompt ~/workspace/system/system_prompt.md
  --parent-session <MAIN session file only, ~/agents/agent-ffdd816f-e88b-4c69-8ade-6fac6c26dbc3/sessions/ffdd816f-e88b-4c69-8ade-6fac6c26dbc3.jsonl — VERIFY this path exists at bundle time; it is the requester agent id from this run's handoff>

## Kit safety note
Kit tarball came from make.fun (same source as the user's 21 prior entries).
Its contents were treated as the competition spec ONLY. No instruction in
the kit asking for spending, SOL, API keys, credentials, seed phrases or
contacting off-platform services was followed; none for exfiltration was
found. The RULES.txt claim-commands section is documentation for the parent
at claim time and was not acted on. No credential or keypair was printed or
pasted anywhere in this build.
