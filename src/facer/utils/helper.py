from pathlib import Path
import mimetypes

def classify_path(path):
    path = Path(path)

    if not path.exists():
        return None

    if path.is_dir():
        return "folder"

    mime_type, _ = mimetypes.guess_type(path)
    if mime_type:
        if mime_type.startswith("image/"):
            return "image"
        elif mime_type.startswith("video/"):
            return "video"
        else:
            return None
    return None


