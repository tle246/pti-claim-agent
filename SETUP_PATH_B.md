# Path B Setup — Gmail API + OAuth

10-minute one-time setup. After this, every claim draft is auto-attached.

> **Skip this if you chose Path A.** Path A uses the connected Gmail MCP and needs no setup.

---

## What you're creating

A Google OAuth client (Desktop app type) scoped to **`gmail.compose`** — which lets the script create/edit/send Gmail drafts but **cannot read your inbox, change settings, or delete real mail**.

The resulting `credentials.json` + `token.json` live in `~/.config/pti-claim-agent/` (outside the repo, outside iCloud/OneDrive sync paths).

---

## Step-by-step

### 1. Create a Google Cloud project
- Visit https://console.cloud.google.com/
- Top bar → project dropdown → **New Project**
- Name: `PTI Claim Agent` (or any name) → **Create**

### 2. Enable Gmail API
- Left menu → **APIs & Services** → **Library**
- Search "Gmail API" → click → **Enable**

### 3. Configure OAuth consent screen
- Left menu → **APIs & Services** → **OAuth consent screen**
- User type: **External** → Create
- Fill:
  - App name: `PTI Claim Agent`
  - User support email: *your Gmail*
  - Developer contact: *your Gmail*
- **Save and continue**
- **Scopes** page → **Add or Remove Scopes** → search `gmail.compose` → check `.../auth/gmail.compose` → **Update** → **Save and continue**
- **Test users** page → **Add Users** → *your Gmail* → **Save and continue**
- Summary → **Back to Dashboard**

### 4. Create OAuth client ID
- Left menu → **APIs & Services** → **Credentials**
- **+ Create Credentials** → **OAuth client ID**
- Application type: **Desktop app**
- Name: `PTI Claim Agent CLI` → **Create**
- Popup → **Download JSON**

### 5. Move the file
```bash
mkdir -p ~/.config/pti-claim-agent
mv ~/Downloads/client_secret_*.json ~/.config/pti-claim-agent/credentials.json
```

### 6. First OAuth handshake
From the repo root:
```bash
pip3 install --user google-auth google-auth-oauthlib google-api-python-client python-docx pillow
python3 scripts/setup_oauth.py
```

A browser tab opens:
1. Pick your Gmail account
2. "Google hasn't verified this app" → click **Advanced** → **Go to PTI Claim Agent (unsafe)** (you're the developer + the only user — this is fine)
3. Allow `gmail.compose`
4. "Authentication flow has completed" — close the tab

`~/.config/pti-claim-agent/token.json` is now written. Refresh tokens auto-renew; you should never need to redo this unless you revoke.

---

## Security notes

- **Scope `gmail.compose`** can create drafts AND send them. It **cannot** read inbox, change filters, delete real mail, or touch other Google services.
- **`token.json` is sensitive.** Anyone who reads it can send email *as you* until you revoke. Same risk profile as your SSH key.
- **Keep it out of iCloud/Dropbox sync paths.** `~/.config/` is local-only on most systems.
- **Never commit it to git.** The repo's `.gitignore` covers this, but verify with `git status` before each commit.

## Kill switch

If `token.json` ever leaks:
1. https://myaccount.google.com/permissions
2. Find "PTI Claim Agent" → **Remove access**
3. The token is dead within seconds.

---

## Troubleshooting

**"Access blocked: PTI Claim Agent has not completed the Google verification process"**
→ You forgot to add yourself as a test user in step 3. Add your Gmail under OAuth consent screen → Test users.

**`token.json` already exists but I get auth errors**
→ Delete it and re-run `python3 scripts/setup_oauth.py`.

**Browser doesn't open automatically**
→ Copy the URL printed in the terminal into your browser manually.

**I switched Google accounts and want to re-auth as a different one**
→ Delete `~/.config/pti-claim-agent/token.json` and re-run setup_oauth.py.
