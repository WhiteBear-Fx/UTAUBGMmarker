import json


class ThemeLoader:
    def __init__(self, theme_filepath: str):
        self.theme = None
        self.load_theme(theme_filepath)

    def load_theme(self, theme_filepath: str):
        with open(theme_filepath, encoding="utf-8") as file:
            self.theme = json.load(file)

    def get_style(self, widget: str) -> dict:
        if widget in self.theme:
            return self.theme[widget]
