"""
ui/menus.py

ONE reusable menu, used by all three levels of the app:
  main menu (object types) / object list / metadata options.

It prints a numbered list, adds a final option (Exit or Back),
asks for a number and returns the choice.
"""

from ui import prompts


def show_menu(title, items, last_label):
    """
    Show a numbered menu.

    - title      : heading printed above the list
    - items      : list of strings to number 1..N
    - last_label : text of the extra last option ("Exit", "Back", ...)

    Returns the 0-based index of the chosen item,
    or None if the user picked the last option.
    """
    print()
    print(title)
    for number, item in enumerate(items, start=1): # Produces pairs (1, "Tables"), (2, "Views"), ...
        print(f"{number}. {item}")

    last_number = len(items) + 1 # Last option (Exit or Back) is numbered len(items) + 1
    print(f"{last_number}. {last_label}") 

    choice = prompts.ask_number(1, last_number) # Asks for a valid number in range
    if choice == last_number:
        return None
    return choice - 1