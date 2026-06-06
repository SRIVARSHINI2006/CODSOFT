LIGHT_THEME = {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#f0f0f0",
    "button_fg": "#000000",
    "info_bg": "#ffffff",
    "info_fg": "#000080"
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "button_bg": "#333333",
    "button_fg": "#ffffff",
    "info_bg": "#1e1e1e",
    "info_fg": "#00ff99"
}


class ThemeManager:

    def __init__(self):
        self.current_theme = LIGHT_THEME

    def toggle_theme(self):

        if self.current_theme == LIGHT_THEME:
            self.current_theme = DARK_THEME
        else:
            self.current_theme = LIGHT_THEME

        return self.current_theme

    def get_theme(self):
        return self.current_theme