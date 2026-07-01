# Chosen path: A

# PTI Claim Agent — Project Memory

This file is auto-loaded by Antigravity in this folder. It tells the agent how to help with PTI insurance claims.

---

## Profile

- Policyholder (employee): `Lê Văn Tính`
- Policyholder (corporate, if group policy): `NAB Vietnam`
- Policy number: `0000185/HD/CN.4.5/000-2/2024/MAR01`
- Policy label (e.g. "VSDC (NAB Vietnam)"): `VSDC NAB Vietnam`
- Employee ID at your company: `[EMPLOYEE_ID]`
- Gmail: `figurineofficial@gmail.com`
- Phone: `[YOUR_PHONE]`

## Insured persons

Fill in every person covered under the policy. The agent uses this to map a partial name like "my dad" or "Châu" to a specific row.

| Name | DOB | ID number | Relationship | Plan |
|------|-----|-----------|--------------|------|
| `Lê Văn Tính` | `10/02/1963` | `[CCCD]` | Self | `[Plan X]` |

## Bank (for reimbursement)
- Account: `0041 3814 102`
- Bank: `TPBank`
- Beneficiary: `Lê Văn Tài`

## Email routing
- TO: `figurineofficial@gmail.com`
- CC: `[BROKER_EMAIL]`, `[YOUR_HR_OR_WORK_EMAIL]`
- Subject pattern: `HS YCBT - [Insured Name] - [POLICY_NUMBER] - [POLICY_LABEL]`

---

## Per-claim workflow

When the user says **"file a claim for [name]"**:

1. **Interactive Prompting (Default Values)**: Do NOT ask for Visit date, Hospital, Diagnosis, or Amount. Ask the user if they want to use the default bank values specified in the profile (Account: 0041 3814 102, Bank: TPBank, Beneficiary: Lê Văn Tài). If they agree, proceed to the next step. If they do not, ask them for the new bank details ONE BY ONE.
2. **Confirm** with the user — summarize the bank information provided and ask them to double check before proceeding.
3. **Fill the form**: Run `python3 scripts/fill_claim.py` passing the collected bank details as command-line arguments: `--bank_account`, `--bank_name`, `--bank_beneficiary`. (Make sure to pass any other required arguments if the script needs them).
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
- **PDFs**: pass through unchanged — readable directly by Antigravity.

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
