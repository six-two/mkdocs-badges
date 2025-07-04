import traceback
# pip dependency
import mkdocs
from mkdocs.config.config_options import Type, ExtraScriptValue
from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.exceptions import PluginError
# local files
from . import warning, disable_warnings
from .install_badge import InstallBadgeManager
from .assets import BADGE_CSS, BADGE_JS, INSTALL_BADGE_DATA, copy_asset_if_target_file_does_not_exist
from .badge_replacer import replace_badges
from .tag_badge import TagBadgeManager

DEFAULT_BADGE_CSS_PATH = "assets/stylesheets/badge.css"
DEFAULT_BADGE_JS_PATH = "assets/javascripts/badge.js"


class BadgesPluginConfig(Config):
    enabled = Type(bool, default=True)
    # Options to allow overwriting CSS and/or JS files
    badge_css = Type(str, default="")
    badge_js = Type(str, default="")
    # Load script as async? You can deactivate it if it causes trouble
    async_ = Type(bool, default=True)
    # Allow overwriting the install badge data
    install_badge_data = Type(str, default="")
    # Base link for the tag links
    tag_page_link = Type(str, default="/index.html")
    # Disable warnings, do this at your own risk
    disable_warnings = Type(bool, default=False)
    # This is the badge separator, change it at your own risk
    separator = Type(str, default="|")
    table_separator = Type(str, default="^")
    inline_badge_start = Type(str, default="[")
    inline_badge_end = Type(str, default="]")


class BadgesPlugin(BasePlugin[BadgesPluginConfig]):
    def on_config(self, config: MkDocsConfig, **kwargs) -> MkDocsConfig:
        """
        Called once when the config is loaded.
        It will make modify the config and initialize this plugin.
        """
        if self.config.disable_warnings:
            disable_warnings()

        # Make sure that the CSS and JS badge files are included on every page
        badge_css_path = self.config.badge_css or DEFAULT_BADGE_CSS_PATH
        extra_css = config.extra_css
        if badge_css_path not in extra_css:
            extra_css.append(badge_css_path)

        badge_js_path = ExtraScriptValue(self.config.badge_js or DEFAULT_BADGE_JS_PATH)
        if self.config.async_:
            badge_js_path.async_ = True
        
        extra_js = config.extra_javascript
        if badge_js_path not in extra_js:
            extra_js.append(badge_js_path)
        
        if len(self.config.separator) != 1:
            raise PluginError(f"The 'separator' field needs to contain a single character, but has {len(self.config.separator)}: '{self.config.separator}'")

        if len(self.config.table_separator) != 1:
            raise PluginError(f"The 'table_separator' field needs to contain a single character, but has {len(self.config.table_separator)}: '{self.config.table_separator}'")

        if self.config.table_separator == "|":
            raise PluginError("The 'table_separator' field is not allowed to be '|', since that character conflicts with Markdown's table syntax")

        self.install_badge_manager = InstallBadgeManager()
        # load the defaults
        self.install_badge_manager.load_badge_templates_from_file(INSTALL_BADGE_DATA)
        if self.config.install_badge_data:
            # Add new badge data or overwrite default definitions
            self.install_badge_manager.load_badge_templates_from_file(self.config.install_badge_data)

        self.tag_badge_manager = TagBadgeManager(self.config.tag_page_link)

        return config

    # @event_priority(50)
    # Earlier than most other plugins to update the tags properly. Did not work
    # SEE https://www.mkdocs.org/dev-guide/plugins/#event-priorities
    def on_page_markdown(self, markdown: str, page: Page, config: MkDocsConfig, files: Files) -> str:
        """
        The page_markdown event is called after the page's markdown is loaded from file and can be used to alter the Markdown source text. The meta- data has been stripped off and is available as page.meta at this point.
        See: https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
        """
        try:
            if self.config.enabled:
                file_name = page.file.src_path
                markdown = replace_badges(file_name, markdown, self.config.separator, self.config.table_separator, self.config.inline_badge_start, self.config.inline_badge_end, self.install_badge_manager, self.tag_badge_manager)
                self.tag_badge_manager.apply_tags_to_page(page)
            else:
                warning("Plugin is disabled")

            return markdown
        except Exception as error:
            raise mkdocs.exceptions.PluginError("Uncaught exception in badges_plugin::on_page_markdown.\n" + traceback.format_exc())

    def on_post_build(self, config: MkDocsConfig) -> None:
        """
        Copy the default files if the user hasn't supplied his/her own version
        """
        output_dir = config.site_dir
        badge_css_path = self.config.badge_css or DEFAULT_BADGE_CSS_PATH
        copy_asset_if_target_file_does_not_exist(output_dir, badge_css_path, BADGE_CSS)

        badge_js_path = self.config.badge_js or DEFAULT_BADGE_JS_PATH
        copy_asset_if_target_file_does_not_exist(output_dir, badge_js_path, BADGE_JS)
