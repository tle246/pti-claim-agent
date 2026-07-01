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

---

### Token Mapping for `Giay-Yeu-Cau-Tra-Tien-Bao-Hiem.docx`
If you are modifying the form yourself, here is where the agent maps the tokens:
- `{{POLICY_NUMBER}}` -> Hợp đồng bảo hiểm số (Policy No)
- `{{INSURED_NAME}}` -> Tên người được bảo hiểm (Name of Insured)
- `{{INSURED_CCCD}}` -> CCCD/Hộ Chiếu (ID/Passport of Insured)
- `{{INSURED_DOB}}` -> Ngày sinh (D.O.B of Insured)
- `{{AMOUNT_VND}}` -> Số tiền yêu cầu chi trả (Total amount claimed)
- `{{BANK_ACCOUNT}}` -> Account No/ (Số tài khoản)
- `{{BANK_NAME}}` -> Bank name/ (Tên Ngân hàng)
- `{{BANK_BENEFICIARY}}` -> Beneficiary/ (Người thụ hưởng)
- `{{VISIT_DATE}}` -> Ngày nhập viện (Date of admission)
- `{{HOSPITAL}}` -> Tên cơ sở y tế (Name of Hospital or clinic)
- `{{DIAGNOSIS}}` -> Chẩn đoán bệnh / Nguyên nhân tai nạn
- `{{SIGNATURE}}` -> (Chữ ký và họ tên của Người được bảo hiểm)
