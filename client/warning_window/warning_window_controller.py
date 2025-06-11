from .warning_window_view import WarningWindowView

class WarningWindowController:
    def __init__(self):
        self._view = WarningWindowView()

    def append_warning(self, warning: str):
        self._view.append_warning(warning)

    def get_view(self) -> WarningWindowView:
        return self._view


warning_window_controller = WarningWindowController()