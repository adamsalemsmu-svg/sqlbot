"""
Conversation analysis utility.

This script reads from the conversation database and prints simple
statistics.  It shows how many messages each user has sent and
displays the most recent interactions with timestamps.

Run it after your bot has been used to get an overview of activity.
"""

from collections import Counter
from datetime import timezone
from typing import List

from models import SessionLocal, Message


def summarise(n_recent: int = 10) -> None:
    """Print a summary of the conversation logs.

    Args:
        n_recent: Number of most recent messages to display.
    """

    session = SessionLocal()
    try:
        # Count messages per user
        users: List[str] = [m.user for m in session.query(Message.user).all()]
        counts = Counter(users)
        if counts:
            print("Messages per user:")
            for user, count in counts.most_common():
                print(f"  {user}: {count}")
        else:
            print("No conversations recorded.")

        # Show recent messages
        recent_msgs = (
            session.query(Message)
            .order_by(Message.timestamp.desc())
            .limit(n_recent)
            .all()
        )
        if recent_msgs:
            print(f"\nMost recent {len(recent_msgs)} messages:")
            for msg in reversed(recent_msgs):
                ts = msg.timestamp.replace(tzinfo=timezone.utc).isoformat()
                user_line = f"[{ts}] {msg.user} -> "
                print(f"{user_line}{msg.message}")
                print(f"{' ' * len(user_line)}bot -> {msg.response}\n")
    finally:
        session.close()


if __name__ == "__main__":
    summarise()