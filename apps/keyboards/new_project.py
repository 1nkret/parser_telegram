from telethon import Button


def new_project_keyboard(
        target_channel,
        msg_id
):
    buttons = [
        [
            Button.inline(
                text="Call by name",
                data=f"{target_channel}/{msg_id}_give_name_actuality"
            ),
            Button.inline(
                text="Delete",
                data=f"{target_channel}/{msg_id}_delete_actuality"
            ),
        ],
        [
            Button.inline(
                text="Save as unnamed",
                data=f"{target_channel}/{msg_id}_save_as_unnamed"
            )
        ],
    ]
    return buttons
