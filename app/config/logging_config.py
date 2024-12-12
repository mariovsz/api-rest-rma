from rich_toolkit import RichToolkit, RichToolkitTheme
from rich_toolkit.styles import TaggedStyle


def get_rich_toolkit() -> RichToolkit:
    theme = RichToolkitTheme(
        style=TaggedStyle(tag_width=11),
        theme={
            "tag": "white on #007166",
            "eror": "white on red",
        },
    )
    return RichToolkit(theme=theme)
