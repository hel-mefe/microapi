def split_path(path: str) -> List[str]:
    return [segment for segment in path.split('/') if segment]

def is_param(segment: str) -> bool:
    return segment.startswith('{') and segment.endswith('{')

def param_name(segment: str) -> str | None:
    if not is_param(segment):
        return None
    return segment[1:-1]
