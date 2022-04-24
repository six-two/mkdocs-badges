import re
import html
import json
from typing import NamedTuple, Optional
# local files
from . import replace_regex_matches, LOGGER
from .normal_badge import normal_badge
from .custom_badge import custom_badge

# |@name:value|
REGEX = re.compile("\|@([a-zA-Z0-9]+):([^\|]+)\|")


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
    def __init__(self, file_path: str) -> None:
        self.badges = {}
        
        with open(file_path, "r") as f:
            file_data = json.load(f)

        for badge_type, badge_data in file_data.items():
            title = badge_data["title"]
            link_template = badge_data["link_template"]
            command_template = badge_data["command_template"]

            self.badges[badge_type] = InstallBadgeData(title, link_template, command_template)

    def replace_install_badges(self, text: str) -> str:
        return replace_regex_matches(REGEX, text, self._replace_function)

    def _replace_function(self, match: re.Match) -> str:
        badge_type = match.group(1)
        badge_value = match.group(2)

        badge_data = self.badges.get(badge_type)
        if badge_data:
            install_command = badge_data.get_command(badge_value)
            package_url = badge_data.get_link(badge_value)

            return custom_badge(badge_type, badge_value, install_command, package_url)
        else:
            LOGGER.warn(f"Unknown special badge type: '{badge_type}' in '{match.group(0)}'")
            # fallback: use a normal badge
            return normal_badge(badge_type, badge_value)
