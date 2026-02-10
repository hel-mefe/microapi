def split_path(path: str) -> list[str]:
    return [segment for segment in path.split("/") if segment]


def is_param(segment: str) -> bool:
    return segment.startswith("{") and segment.endswith("}")


def param_name(segment: str) -> str | None:
    if not is_param(segment):
        return None
    return segment[1:-1]


def allowed_methods(self, path: str) -> set[str] | None:
    node = self.root
    segments = split_path(path)

    for segment in segments:
        if segment in node.static_children:
            node = node.static_children[segment]
            continue

        if node.param_child is not None:
            node = node.param_child
            continue

        return None

    return set(node.handlers.keys())
