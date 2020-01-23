from rules.models import Namespace

namespaces = ["Recommendation", "Bookmarking"]


def namespace_table():
    for name in namespaces:
        Namespace.create_namespace(name=name)
