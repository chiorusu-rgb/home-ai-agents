from src.adapters.ollama_client import OllamaClient
from src.schemas import EmailMessage, EmailSummary


class EmailAgent:
    def __init__(self, llm: OllamaClient) -> None:
        self.llm = llm

    def summarize(self, message: EmailMessage) -> EmailSummary:
        prompt = f"""
Classify and summarize this email.

Sender: {message.sender}
Subject: {message.subject}
Received: {message.received_at.isoformat()}

Body:
{message.body}

Return exactly:
CATEGORY: one of personal, work, finance, alert, homelab, newsletter, other
PRIORITY: one of low, normal, high, urgent
SUMMARY: one concise paragraph
ACTIONS: one action per line, or NONE
""".strip()

        result = self.llm.chat(
            system=(
                "You are a read-only email analysis agent. "
                "Never send, delete, archive, or modify email."
            ),
            user=prompt,
        )

        category = "other"
        priority = "normal"
        summary = result
        actions: list[str] = []

        for line in result.splitlines():
            key, separator, value = line.partition(":")
            if not separator:
                continue
            value = value.strip()
            if key.upper() == "CATEGORY":
                category = value.lower()
            elif key.upper() == "PRIORITY":
                priority = value.lower()
            elif key.upper() == "SUMMARY":
                summary = value
            elif key.upper() == "ACTIONS" and value.upper() != "NONE":
                actions.append(value)

        return EmailSummary(
            message_id=message.message_id,
            category=category,
            priority=priority,
            summary=summary,
            action_items=actions,
        )
