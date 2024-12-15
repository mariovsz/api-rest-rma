from rich.console import Console
from rich.theme import Theme
from rich.text import Text


class StyledConsole:
    def __init__(self, theme, tag_width: int = 11, padding: int = 2):
        self.console = Console(theme=theme)
        self.tag_width = tag_width
        self.padding = padding

    def __call__(self, message: str, tag: str):
        tags = tag.split()
        combined_tag = " ".join(tags)
        style_name = f"tag.{tags[0].lower()}"
        try:
            style = self.console.get_style(style_name)
        except Exception:
            style_name = "default"
            style = self.console.get_style(style_name)
        spaces_before_tag = self.tag_width - len(combined_tag) - 2

        text = Text()
        text.append(" " * spaces_before_tag, style=None)
        text.append(f" {combined_tag} ", style=style)
        text.append(" " * self.padding)
        text.append(message)
        self.console.print(text)


theme = Theme(
    {
        "default": "white on #007166",
        "tag.mqtt": "white on #36b88c",
        "tag.error": "white on #cb515d",
        "tag.info": "black on #eac454",
    }
)
styled_console = StyledConsole(theme)
