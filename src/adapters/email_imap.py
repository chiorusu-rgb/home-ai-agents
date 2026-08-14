import email
import imaplib
import os
from dataclasses import dataclass, field
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime
from typing import Any


@dataclass
class EmailFetchResult:
    uid: str
    sender: str
    subject: str
    received_at: datetime | None
    body_text: str
    headers: dict[str, Any] = field(default_factory=dict)


def _decode_mime_header(value: str | None) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    decoded: list[str] = []
    for part, encoding in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return "".join(decoded)


def _extract_body_text(message: email.message.Message) -> str:
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in disposition.lower():
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = part.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace").strip()
        return ""
    payload = message.get_payload(decode=True)
    if payload is None:
        return ""
    charset = message.get_content_charset() or "utf-8"
    return payload.decode(charset, errors="replace").strip()


class IMAPEmailClient:
    def __init__(
        self,
        server: str | None = None,
        username: str | None = None,
        password: str | None = None,
        mailbox: str = "INBOX",
    ) -> None:
        self.server = server or os.getenv("IMAP_SERVER", "")
        self.username = username or os.getenv("EMAIL_ACCOUNT", "")
        self.password = password or os.getenv("EMAIL_PASSWORD", "")
        self.mailbox = mailbox

    def _connect(self) -> imaplib.IMAP4_SSL:
        if not all([self.server, self.username, self.password]):
            raise RuntimeError("IMAP credentials are not fully configured.")
        client = imaplib.IMAP4_SSL(self.server)
        client.login(self.username, self.password)
        client.select(self.mailbox)
        return client

    def fetch_unread_emails(self, limit: int = 5) -> list[EmailFetchResult]:
        client = self._connect()
        try:
            status, data = client.search(None, "UNSEEN")
            if status != "OK":
                raise RuntimeError("Failed to search mailbox.")

            message_ids = data[0].split()[-limit:]
            results: list[EmailFetchResult] = []

            for message_id in message_ids:
                status, msg_data = client.fetch(message_id, "(RFC822 UID)")
                if status != "OK":
                    continue

                raw_message = None
                uid_value = message_id.decode()

                for item in msg_data:
                    if not isinstance(item, tuple):
                        continue
                    raw_message = item[1]
                    if isinstance(item[0], bytes) and b"UID " in item[0]:
                        prefix = item[0].decode(errors="replace")
                        if "UID " in prefix:
                            uid_value = prefix.split("UID ", 1)[1].split()[0]

                if raw_message is None:
                    continue

                message = email.message_from_bytes(raw_message)
                subject = _decode_mime_header(message.get("Subject"))
                sender = _decode_mime_header(message.get("From"))
                received_raw = message.get("Date")
                received_at = None
                if received_raw:
                    try:
                        received_at = parsedate_to_datetime(received_raw)
                    except Exception:
                        received_at = None

                results.append(
                    EmailFetchResult(
                        uid=uid_value,
                        sender=sender,
                        subject=subject,
                        received_at=received_at,
                        body_text=_extract_body_text(message),
                        headers={
                            "message_id": message.get("Message-ID", ""),
                            "date": received_raw or "",
                        },
                    )
                )

            return results
        finally:
            try:
                client.close()
            except Exception:
                pass
            client.logout()
