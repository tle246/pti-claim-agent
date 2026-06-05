# PTI Claim Agent — Project Memory

This file is auto-loaded by Claude Code in this folder. It tells the agent how to help with PTI insurance claims.

> **First-run setup**: if any `[BRACKETED_PLACEHOLDER]` below is unfilled, the agent should walk the user through the [setup checklist](#first-run-setup-checklist) before doing anything else.

---

## First-run setup checklist

When the user first invokes Claude Code in this folder, **and any of the placeholders below are unfilled**, do this:

1. Ask: *"Which Gmail integration path do you want — A (manual attach, zero setup) or B (auto attach, 10 min OAuth setup)?"*
2. Read the README's "Two integration paths" table to them if they're unsure.
3. Save their choice as `# Chosen path: A` or `# Chosen path: B` at the top of this CLAUDE.md (replace this checklist with it).
4. Walk through filling in [profile](#profile), [insureds](#insured-persons), [bank](#bank), [email routing](#email-routing) — one section at a time.
5. Confirm assets are in place: `assets/blank_form.docx` and `assets/signature.png`. If not, ask the user to add them (README §3).
6. If Path B: walk through `SETUP_PATH_B.md` (Google Cloud Console + OAuth handshake).
7. Once everything is in place, delete this checklist section and reply *"Setup complete. Drop evidence files in chat and say 'file a claim for [name]' whenever you're ready."*

---

## Profile

- Policyholder (employee): `[YOUR_FULL_NAME]`
- Policyholder (corporate, if group policy): `[CORPORATE_POLICY_HOLDER_NAME]`
- Policy number: `[POLICY_NUMBER]`
- Policy label (e.g. "VSDC (NAB Vietnam)"): `[POLICY_LABEL]`
- Employee ID at your company: `[EMPLOYEE_ID]`
- Gmail: `[YOUR_GMAIL]`
- Phone: `[YOUR_PHONE]`

## Insured persons

Fill in every person covered under the policy. The agent uses this to map a partial name like "my dad" or "Châu" to a specific row.

| Name | DOB | ID number | Relationship | Plan |
|------|-----|-----------|--------------|------|
| `[FULL_NAME_1]` | `[DD/MM/YYYY]` | `[CCCD]` | Self / Spouse / Father / etc. | `[Plan X]` |
| `[FULL_NAME_2]` | `[DD/MM/YYYY]` | `[CCCD]` | | |

## Bank (for reimbursement)
- Account: `[ACCOUNT_NUMBER]`
- Bank: `[BANK_NAME]`
- Beneficiary: `[BENEFICIARY_NAME]` (must match the account holder name exactly)

## Email routing
- TO: `[INSURER_CLAIMS_EMAIL]` (e.g. `nhanhsbt.mn@pti.com.vn`)
- CC: `[BROKER_EMAIL]`, `[YOUR_HR_OR_WORK_EMAIL]`
- Subject pattern: `HS YCBT - [Insured Name] - [POLICY_NUMBER] - [POLICY_LABEL]`

---

## Per-claim workflow

When the user says **"file a claim for [name]"** and drops evidence files in chat:

1. **Extract** from evidence (PDFs + images): insured name (match against the [insured table](#insured-persons)), visit date, hospital, diagnosis, total out-of-pocket VND.
   - If the policy includes Vietnamese social insurance: report the net "after BHYT" amount.
2. **Confirm** with the user — present a summary table and ask y/n before filling.
3. **Fill the form**: use `assets/blank_form.docx`. Replace `{{KEY}}` placeholder tokens if present (recommended); otherwise append labeled rows.
4. **Embed signature** (`assets/signature.png`) — see [Signature embedding](#signature-embedding-technique) below.
5. **Save** the filled form to `output/[NameCamelCase]_[YYYY-MM-DD]/GYC_[Name]_[VisitDate].docx`.
6. **Bundle** copies of all evidence files into the same `output/[Name]_[Date]/` folder (compress big phone photos to <1 MB each).
7. **Create the Gmail draft** — see the [Gmail draft](#gmail-draft) section for your path.

## Gmail draft

### If Chosen path = A (manual attach)
- Use the Gmail MCP `create_draft` tool (body only).
- Report back to the user: subject, body, and the **absolute path to the bundle folder** so they can drag everything in at once.

### If Chosen path = B (auto attach)
- Use `scripts/send_claim_oauth.py` (it reads `~/.config/pti-claim-agent/token.json`).
- Report back: subject, attachment list, draft URL.
- If the token is missing or expired, run `python3 scripts/setup_oauth.py` once.

## Email body template

Adapt language/tone to the insurer. The default below is what's worked for PTI (English, polite, summary-only):

```
Hi PTI,

Please find the claim form and supplementary documents for insured [Full Vietnamese Name] from [POLICY_LABEL] as attached.

Claim summary:
- Insured: [Full Vietnamese Name]
- Hospital: [Hospital]
- Date of visit: DD/MM/YYYY
- Total claimed: [N,NNN,NNN] VND (out-of-pocket[, after BHYT if applicable])

Please let us know if any additional documents are required.

--
Best regards,

[YOUR_NAME_WESTERN_ORDER]
Cellphone: [YOUR_PHONE]
```

---

## Signature embedding technique

`python-docx` can't reliably insert inline images into a specific paragraph. The agent uses ZIP manipulation:

1. `shutil.copy` the blank form to its output path; save the form via python-docx after field fills.
2. Open the docx as a ZIP.
3. Add `signature.png` bytes to `word/media/`.
4. Add a `<Relationship Id="rIdN" Type=".../image" Target="media/signature.png"/>` to `word/_rels/document.xml.rels`.
5. Ensure `[Content_Types].xml` has `<Default Extension="png" ContentType="image/png"/>`.
6. Insert a `<w:p><w:r><w:drawing><wp:inline>…<a:blip r:embed="rIdN"/>…</wp:inline></w:drawing></w:r></w:p>` block right after the paragraph containing one of these markers (in order of preference): `{{SIGNATURE}}`, `Chữ ký người yêu cầu`, `Signature of the Insured`. Fallback: append before `</w:body>`.
7. Compute image extent in EMUs (914400 per inch, assume 96 DPI). Cap signature width at ~2 inches.
8. Rewrite the ZIP and replace the original.

## File conversions

- **HEIC** (iPhone photos): convert with `sips -s format jpeg input.HEIC --out output.jpg`.
- **Large JPEGs**: resize so the longest side is ≤2000px and re-encode at quality 82 (Pillow). Typical 5 MB phone photo → ~500 KB.
- **PDFs**: pass through unchanged — readable directly by Claude.

---

## Where assets live

| File | Location | In git? |
|------|----------|---------|
| `blank_form.docx` | `assets/` | No (`.gitignore`) |
| `signature.png` | `assets/` | No (`.gitignore`) |
| Filled forms + bundles | `output/[Name]_[Date]/` | No (`.gitignore`) |
| `credentials.json` (Path B) | `~/.config/pti-claim-agent/` | Outside repo |
| `token.json` (Path B) | `~/.config/pti-claim-agent/` | Outside repo |

**Why outside repo for Path B**: if you sync this folder to iCloud / OneDrive / a public GitHub repo, your tokens would leak. `~/.config/` is local-only.

## Useful commands

```bash
# Open today's bundle folder in Finder
open "output/$(ls -t output | head -1)"

# Re-trigger OAuth if token.json is missing/expired (Path B)
python3 scripts/setup_oauth.py

# Revoke OAuth token (Path B, if leaked)
# → visit https://myaccount.google.com/permissions
```
