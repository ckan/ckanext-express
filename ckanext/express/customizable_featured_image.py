import pylons.config as config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def featured_caption():
    return config.get(
        "ckanext.express.featured_caption", "This is a featured section")


def featured_image():
    return config.get(
        "ckanext.express.featured_image", "http://placehold.it/420x220")


def featured_alt_text():
    return config.get(
        "ckanext.express.featured_alt_text", "Placeholder")


class CustomizableFeaturedImagePlugin(plugins.SingletonPlugin):
    """A plugin that allows the front page "featured image" to be customized.

    """
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")

    def get_helpers(self):
        return {
            "express_featured_caption": featured_caption,
            "express_featured_image": featured_image,
            "express_featured_alt_text": featured_alt_text,
        }
