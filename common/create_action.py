from rules.models import Action

action_names = ["slack", "gmail"]

for action_name in action_names:
    Action.create_action(action_name)
