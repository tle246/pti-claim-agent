"""Create a Gmail draft with attachments (Path B).

Usage (called by the agent, not by hand):

    python3 scripts/send_claim_oauth.py \\
        --to nhanhsbt.mn@pti.com.vn \\
        --cc broker@example.com,you@nab.com.au \\
        --subject "HS YCBT - Ngoc - 0000.../MAR01 - VSDC" \\
        --body-file /tmp/body.txt \\
        --attach output/Foo_2026-05-25/

Attaches every file in the given directory (or the listed files). Prints the draft id on success.
"""
from __future__ import annotations

import argparse
import base64
import mimetypes
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CRED_DIR = Path.home() / ".config" / "pti-claim-agent"
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def _gmail():
    token = CRED_DIR / "token.json"
    if not token.exists():
        sys.exit(
            f"Missing {token}. Run `python3 scripts/setup_oauth.py` first (see SETUP_PATH_B.md)."
        )
    creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    return build("gmail", "v1", credentials=creds)


def _collect_attachments(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(f for f in path.iterdir() if f.is_file() and not f.name.startswith(".")))
        elif path.is_file():
            files.append(path)
        else:
            sys.exit(f"Not found: {path}")
    return files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="Comma-separated TO addresses")
    ap.add_argument("--cc", default="", help="Comma-separated CC addresses")
    ap.add_argument("--from", dest="from_addr", required=True, help="Sender address")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True, help="Path to plain-text body file")
    ap.add_argument("--attach", nargs="+", required=True, help="Files and/or directories to attach")
    args = ap.parse_args()

    msg = MIMEMultipart()
    msg["to"] = args.to
    if args.cc:
        msg["cc"] = args.cc
    msg["from"] = args.from_addr
    msg["subject"] = args.subject
    body = Path(args.body_file).read_text(encoding="utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))

    files = _collect_attachments(args.attach)
    if not files:
        sys.exit("No attachments collected.")

    for f in files:
        mime, _ = mimetypes.guess_type(str(f))
        if mime is None:
            mime = "application/octet-stream"
        maintype, subtype = mime.split("/", 1)
        part = MIMEBase(maintype, subtype)
        part.set_payload(f.read_bytes())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{f.name}"')
        msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    svc = _gmail()
    draft = svc.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    print(f"draft_id={draft['id']}")
    print(f"attachments={len(files)}")
    for f in files:
        print(f"  + {f.name}")


if __name__ == "__main__":
    main()
