


class DavinciResolveRenderFullMovie:
    """Render full movie in Davinci Resolve"""

    def __init__(self, project, render_settings):
        self.project = project
        self.render_settings = render_settings

    def render(self):
        """Render full movie in Davinci Resolve"""
        print("Render full movie in Davinci Resolve")

class DavinciResolveRenderShortMovie:
    """Render short movie in Davinci Resolve"""

    def __init__(self, project, render_settings):
        self.project = project
        self.render_settings = render_settings

    def render(self):
        """Render short movie in Davinci Resolve"""
        print("Render short movie in Davinci Resolve")


class Renderer:
    """Factory class for initializing renders"""



# current_project.SetRenderSettings({"VideoQuality":3373})