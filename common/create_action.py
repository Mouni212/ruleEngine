from rules.models import Action

action_names = ["slack", "gmail"]


def action_table():
    for action_name in action_names:
        Action.create_action(action_name)
