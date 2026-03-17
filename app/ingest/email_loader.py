import imaplib
import os
import re
from datetime import datetime, timedelta, timezone
from email import message_from_bytes
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from typing import Dict, List


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _decode_header_value(value: str) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def _strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _decode_payload(payload: bytes, charset: str | None) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    for enc in [charset, "utf-8", "latin-1"]:
        if not enc:
            continue
        try:
            return payload.decode(enc, errors="ignore")
        except Exception:
            continue
    return ""


def _extract_message_text(msg) -> str:
    plain_parts: List[str] = []
    html_parts: List[str] = []

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition", "").lower().startswith("attachment"):
                continue

            content_type = part.get_content_type()
            charset = part.get_content_charset()
            payload = part.get_payload(decode=True)
            text = _decode_payload(payload, charset).strip()
            if not text:
                continue

            if content_type == "text/plain":
                plain_parts.append(text)
            elif content_type == "text/html":
                html_parts.append(_strip_html(text))
    else:
        content_type = msg.get_content_type()
        charset = msg.get_content_charset()
        payload = msg.get_payload(decode=True)
        text = _decode_payload(payload, charset).strip()
        if content_type == "text/html":
            text = _strip_html(text)
        if text:
            plain_parts.append(text)

    return "\n\n".join(plain_parts if plain_parts else html_parts).strip()


def _parse_email_date(value: str) -> str:
    if not value:
        return ""
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return value


def fetch_recent_emails(
    host: str,
    username: str,
    password: str,
    mailbox: str = "INBOX",
    days: int = 90,
    port: int = 993,
    limit: int = 200,
) -> List[Dict[str, str]]:
    if not host or not username or not password:
        raise ValueError("IMAP host/username/password are required")
    if days <= 0:
        raise ValueError("days must be > 0")

    client = imaplib.IMAP4_SSL(host, port)
    docs: List[Dict[str, str]] = []

    try:
        client.login(username, password)

        status, _ = client.select(mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"Cannot open mailbox: {mailbox}")

        since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%d-%b-%Y")
        status, data = client.search(None, "SINCE", since_date)
        if status != "OK":
            raise RuntimeError("IMAP search failed")

        uids = data[0].split() if data and data[0] else []
        if limit > 0 and len(uids) > limit:
            uids = uids[-limit:]

        for uid in uids:
            status, msg_data = client.fetch(uid, "(RFC822)")
            if status != "OK" or not msg_data:
                continue

            raw_msg = None
            for row in msg_data:
                if isinstance(row, tuple) and len(row) > 1:
                    raw_msg = row[1]
                    break
            if not raw_msg:
                continue

            msg = message_from_bytes(raw_msg)
            subject = _decode_header_value(msg.get("Subject", ""))
            from_ = _decode_header_value(msg.get("From", ""))
            to_ = _decode_header_value(msg.get("To", ""))
            date_raw = msg.get("Date", "")
            date_iso = _parse_email_date(date_raw)
            body = _extract_message_text(msg)
            if not body:
                continue

            content = (
                f"Subject: {subject}\n"
                f"From: {from_}\n"
                f"To: {to_}\n"
                f"Date: {date_raw}\n\n"
                f"{body}"
            )

            docs.append(
                {
                    "source_path": f"imap://{username}/{mailbox}/{uid.decode(errors='ignore')}",
                    "file_type": ".email",
                    "title": subject or "(no subject)",
                    "content": content,
                    "loaded_at": _utc_now_iso(),
                    "email_uid": uid.decode(errors="ignore"),
                    "email_from": from_,
                    "email_to": to_,
                    "email_date": date_iso,
                }
            )

        return docs
    finally:
        try:
            client.logout()
        except Exception:
            pass


def load_recent_emails_from_env() -> List[Dict[str, str]]:
    host = os.getenv("IMAP_HOST", "").strip()
    username = os.getenv("IMAP_USER", "").strip()
    password = os.getenv("IMAP_PASSWORD", "").strip()
    mailbox = os.getenv("IMAP_MAILBOX", "INBOX").strip() or "INBOX"
    port = int(os.getenv("IMAP_PORT", "993"))
    days = int(os.getenv("EMAIL_LOOKBACK_DAYS", "90"))
    limit = int(os.getenv("EMAIL_FETCH_LIMIT", "200"))

    return fetch_recent_emails(
        host=host,
        username=username,
        password=password,
        mailbox=mailbox,
        days=days,
        port=port,
        limit=limit,
    )
