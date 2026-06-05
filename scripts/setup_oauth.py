"""One-time OAuth handshake. Run after placing credentials.json in ~/.config/pti-claim-agent/.

After this writes token.json, claim drafts can be created with attachments automatically.
"""
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

CRED_DIR = Path.home() / ".config" / "pti-claim-agent"
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def main() -> None:
    creds_path = CRED_DIR / "credentials.json"
    token_path = CRED_DIR / "token.json"

    if not creds_path.exists():
        raise SystemExit(
            f"Missing {creds_path}. See SETUP_PATH_B.md for how to get credentials.json "
            "from Google Cloud Console."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", open_browser=True)
    token_path.write_text(creds.to_json())
    print(f"✅ Wrote {token_path}. Scopes: {creds.scopes}")


if __name__ == "__main__":
    main()
