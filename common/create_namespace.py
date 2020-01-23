from rules.models import Namespace

namespaces = ["Recommendation", "Bookmarking"]

for namespace in namespaces:
    Namespace.create_namespace(namespace)