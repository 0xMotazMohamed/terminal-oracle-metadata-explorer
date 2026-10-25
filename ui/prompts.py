"""
ui/prompts.py

Small helpers that ASK the user for something and make sure the answer is valid.
"""

import getpass


def ask_text(label, default=None):
    """Ask for a non-empty text. If a default exists, pressing Enter uses it."""
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default:
            return default
        print("This field cannot be empty.")


def ask_password(label="Enter password"):
    """Ask for a password WITHOUT showing what is typed (uses getpass)."""
    return getpass.getpass(f"{label}: ")


def ask_number(low, high, prompt="Enter option number: "):
    """
    Keep asking until the user types a whole number between low and high.
    This prevents crashes from letters, empty input or out-of-range numbers.
    """
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and low <= int(raw) <= high:
            return int(raw)
        print(f"Please enter a number between {low} and {high}.")