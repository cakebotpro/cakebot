from PIL import Image
import io
import warnings
import discord


class Filter:
    def __init__(self, allowed=("png", "gif", "jpg", "jpeg", "webp", "webm", "ogg", "mp3", "amv", "mp4", "avi", "txt",
                                "json"), prefix="media"):
        self.allowed = []
        for item in allowed:
            self.allowed.append(item.lower())
        self.prefix = prefix

    async def clean(self, file, read):
        im = None
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        try:
            im = Image.open(io.BytesIO(read))
        except (OSError, IOError, Image.DecompressionBombWarning):
            pass
        if not im:
            return False
        image_format = im.format.lower()
        if image_format not in self.allowed:
            return False
        return {"read": read,
                "filename": f"gc{self.prefix}.{image_format}",
                "spoiler": file.is_spoiler()}
