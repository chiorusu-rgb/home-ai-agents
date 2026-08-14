import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.adapters.email_imap import _decode_mime_header, _extract_body_text


class EmailImapAdapterTests(unittest.TestCase):
    def test_decode_mime_header_plain(self) -> None:
        self.assertEqual(_decode_mime_header("Hello"), "Hello")

    def test_extract_body_text_plain(self) -> None:
        message = MIMEText("This is a test email body.", "plain", "utf-8")
        self.assertEqual(_extract_body_text(message), "This is a test email body.")

    def test_extract_body_text_multipart(self) -> None:
        message = MIMEMultipart()
        message.attach(MIMEText("Plain part", "plain", "utf-8"))
        message.attach(MIMEText("<b>HTML part</b>", "html", "utf-8"))
        self.assertEqual(_extract_body_text(message), "Plain part")


if __name__ == "__main__":
    unittest.main()
