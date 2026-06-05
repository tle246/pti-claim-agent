# `assets/`

Drop two files here (both are `.gitignore`d):

1. **`blank_form.docx`** — the official PTI claim form.
   - Source: your HR or insurance broker, or PTI's website.
   - Optional but recommended: open it once in Word, add `{{INSURED_NAME}}`, `{{INSURED_DOB}}`, `{{INSURED_CCCD}}`, `{{POLICY_NUMBER}}`, `{{VISIT_DATE}}`, `{{HOSPITAL}}`, `{{DIAGNOSIS}}`, `{{AMOUNT_VND}}`, `{{BANK_ACCOUNT}}`, `{{BANK_NAME}}`, `{{BANK_BENEFICIARY}}`, `{{SIGNATURE}}` tokens where you want fills. If you skip this, the agent falls back to label matching.

2. **`signature.png`** — your handwritten signature, ideally:
   - Transparent background (PNG)
   - 300–800 px wide
   - Black ink on white (the agent auto-makes white pixels transparent if needed)
   - On a Mac you can sketch it in Notes → export → drop here.

Neither file is included in the repo for privacy. They're loaded at run-time when the agent fills a claim.
