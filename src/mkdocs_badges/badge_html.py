import html
from typing import Optional

# Invisible separator. Used to make spell checking work correctly and have the copied text be more natural
def as_separator_html(value: str) -> str:
    return f"<span class=sep>{value}</span>"

START = as_separator_html(" [")
SEPARATOR = as_separator_html(" | ")
END = as_separator_html("] ")


def generate_badge_html(badge_type: str, badge_value: str, copy_text: Optional[str] = None, link: Optional[str] = None, extra_classes: list[str] = []) -> str:
    value_link = None
    outer_link = None
    title_copy = None
    outer_copy = None
    if link and copy_text:
        value_link = link
        title_copy = copy_text
    elif link and not copy_text:
        outer_link = link
    elif not link and copy_text:
        outer_copy = copy_text
    else:
        # no special actions
        pass

    title_html = element(badge_type, ["title"], copy_text=title_copy)
    value_html = element(badge_value, ["value"], link=value_link)

    inner_html = START + title_html + SEPARATOR + value_html + END
    outer_classes = ["badge", *extra_classes]
    return element(inner_html, outer_classes, link=outer_link, copy_text=outer_copy)


def element(value: str, class_list: list[str], link: Optional[str] = None, copy_text: Optional[str] = None) -> str:
    if link and copy_text:
        raise Exception("You can not specify both link and copy_text")
    if link:
        return f'<a href="{html.escape(link)}"{class_attribute(class_list)}>{value}</a>'
    elif copy_text:
        class_list = ["badge-copy", *class_list]
        return f'<span{class_attribute(class_list)} onclick="on_click_badge_name(\'{html.escape(copy_text)}\')">{value}</span>'
    else:
        return f'<span{class_attribute(class_list)}>{value}</span>'


def class_attribute(class_list: list[str]) -> str:
    if not class_list:
        return ""
    else:
        for class_name in class_list:
            if len(class_name.split()) > 1:
                raise Exception(f"Class contains white space: '{class_name}'")
        if len(class_list) == 1:
            return f" class={class_list[0]}"
        else:
            classes = " ".join(class_list)
            return f' class="{classes}"'
