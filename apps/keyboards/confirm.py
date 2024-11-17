from telethon import Button


def confirm_keyboard():
    buttons = [
        [
            Button.inline(
                text="Yes",
                data="confirm_yes"
            ),
            Button.inline(
                text="No",
                data="confirm_no"
            )
        ]
    ]
    return buttons
