import json
# local files
from . import warning_for_entry
from .badge_html import generate_badge_html
from .parser import ParserResultEntry


class InstallBadgeData:
    def __init__(self, title: str, link_template: str, command_template: str) -> None:
        self.title = title
        self.link_template = link_template
        self.command_template = command_template

    def get_link(self, value: str) -> str:
        return self.link_template.replace("{{value}}", value)

    def get_command(self, value: str) -> str:
        return self.command_template.replace("{{value}}", value)


class InstallBadgeManager:
    def __init__(self) -> None:
        self.badges: dict[str,InstallBadgeData] = {}

    def load_badge_templates_from_file(self, file_path: str):
        with open(file_path, "r") as f:
            file_data = json.load(f)

        for badge_type, badge_data in file_data.items():
            title = badge_data["title"]
            link_template = badge_data["link_template"]
            command_template = badge_data["command_template"]

            self.badges[badge_type.replace("-", "_")] = InstallBadgeData(title, link_template, command_template)

    def format_badge(self, badge_entry: ParserResultEntry) -> str:
        badge_type = badge_entry.parsed_badge.title.replace("-", "_")
        badge_value = badge_entry.parsed_badge.value

        badge_data = self.badges.get(badge_type)
        if badge_data:
            title = badge_data.title
            install_command = badge_data.get_command(badge_value)
            package_url = badge_data.get_link(badge_value)

            return generate_badge_html(title, badge_value, copy_text=install_command, link=package_url, extra_classes=["badge-install"])
        else:
            warning_for_entry(badge_entry, f"Unknown install badge type: '{badge_type}'. Known values are {', '.join(self.badges.keys())}")
            # fallback: use a normal badge
            return generate_badge_html(badge_type, badge_value)
