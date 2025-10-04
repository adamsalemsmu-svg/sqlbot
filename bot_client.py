"""
Command‑line interface for SQLBot.

This script provides a simple way to interact with the bot from your
terminal.  You can send a single message via flags or drop into an
interactive REPL.  All interactions are logged to the configured
database.  The bot uses a language model backend configured in
``llm_client`` and falls back to echo mode if no API key is set.

Examples::

    # one‑off message
    python bot_client.py --user alice --message "Hello!"

    # interactive mode
    python bot_client.py
"""

import argparse
import sys
from typing import Optional

from models import SessionLocal, Message
from llm_client import call_llm
from db_setup import create_tables


def chat(user: str, message: str) -> str:
    """Send a message on behalf of ``user`` and persist the conversation.

    Args:
        user: Name of the sender.
        message: The message text to send.

    Returns:
        The assistant’s reply.
    """

    session = SessionLocal()
    try:
        response = call_llm(message)
        msg = Message(user=user, message=message, response=response)
        session.add(msg)
        session.commit()
        return response
    finally:
        session.close()


def interactive(user: str) -> None:
    """Start an interactive REPL for the given user."""

    print(f"Starting interactive chat for {user}. Press Ctrl+C to exit.")
    try:
        while True:
            try:
                message = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting chat.")
                break
            if not message:
                continue
            response = chat(user, message)
            print(f"Bot: {response}\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")


def main(args: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="SQLBot CLI")
    parser.add_argument("--user", type=str, default="anonymous", help="User name")
    parser.add_argument("--message", type=str, help="Message to send")
    ns = parser.parse_args(args)

    # Ensure tables exist before chatting
    create_tables()

    if ns.message:
        response = chat(ns.user, ns.message)
        print(response)
    else:
        interactive(ns.user)


if __name__ == "__main__":
    main()