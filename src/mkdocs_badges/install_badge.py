import re
import html
from typing import NamedTuple
# local files
from . import replace_regex_matches, LOGGER
from .normal_badge import replace_function as normal_badge_replace_function

# |@name:value|
REGEX = re.compile("\|@([a-zA-Z0-9]+):([^\|]+)\|")


class SpecialBadge(NamedTuple):
    title: str
    link_template: str
    command_template: str


# TODO: add an option to load those from a file
BADGE_DATA_MAP = {
    "aur": SpecialBadge(
        title="Arch Linux (AUR)",
        link_template="https://aur.archlinux.org/packages/{package}",
        command_template="sudo pacaur -S {package}",
    ),
    "gem": SpecialBadge(
        title="Ruby Gem",
        link_template="https://rubygems.org/gems/{package}",
        command_template="gem install {package}",
    ),
    "github": SpecialBadge(
        title="Github",
        link_template="https://github.com/{package}",
        command_template="git clone https://github.com/{package}",
    ),
    "gitlab": SpecialBadge(
        title="Gitlab",
        link_template="https://gitlab.com/{package}",
        command_template="git clone https://gitlab.com/{package}",
    ),
    "kali": SpecialBadge(
        title="Kali Linux",
        link_template="https://pkg.kali.org/pkg/{package}",
        command_template="sudo apt install {package}",
    ),
    "pacman": SpecialBadge(
        title="Arch Linux",
        link_template="https://archlinux.org/packages/?name={package}",
        command_template="sudo pacman -S {package}",
    ),
    "pypi": SpecialBadge(
        title="PyPI",
        link_template="https://pypi.org/project/{package}",
        command_template="pip install {package}",
    ),
}


def replace_function(match: re.Match) -> str:
    badge_type = match.group(1)
    badge_value = match.group(2)

    badge_data = BADGE_DATA_MAP.get(badge_type)

    if badge_data:
        install_command = badge_data.command_template.format(package=badge_value)
        install_command = html.escape(install_command)
        package_url = badge_data.link_template.format(package=badge_value)
        package_url = html.escape(package_url)

        return ("<span class='badge special'>"+
            f"<span class=title onclick=\"on_click_badge_name('{install_command}')\">{badge_data.title}</span>"+
            f"<a href=\"{package_url}\">"+
                f"<span class=value>{badge_value}</span>"+
            "</a>"+
        "</span>")
    else:
        LOGGER.warn(f"Unknown special badge type: '{badge_type}' in '{match.group(0)}'")
        # fallback: use 
        return normal_badge_replace_function(match)


def replace_install_badges(text: str) -> str:
    return replace_regex_matches(REGEX, text, replace_function)

