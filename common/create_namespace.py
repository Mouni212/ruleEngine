from rules.models import Namespace

namespaces = ["Recommendation", "Bookmarking"]


def namespace_table():
    for namespace in namespaces:
        Namespace.create_namespace(namespace)
 namespace_table()