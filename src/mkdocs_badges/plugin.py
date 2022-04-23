import mkdocs
from . import replace_install_badges, replace_normal_badges

class BadgesPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('install_badges', mkdocs.config.config_options.Type(bool, default=True)),
        ('normal_badges', mkdocs.config.config_options.Type(bool, default=True)),
    )

    def on_page_markdown(self, markdown: str, page, config, files) -> str:
        """
        The page_markdown event is called after the page's markdown is loaded from file and can be used to alter the Markdown source text. The meta- data has been stripped off and is available as page.meta at this point.
        See: https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
        """
        try:
            if self.config["install_badges"]:
                markdown = replace_install_badges(markdown)
            
            if self.config["normal_badges"]:
                markdown = replace_normal_badges(markdown)
                pass

            return markdown
        except KeyError as error:
            raise PluginError(str(error))
