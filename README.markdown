ckanext-express
===============

CKAN plugins for CKAN Express.


customizable_featured_image
---------------------------

Allows the featured image, alt text and caption (in the middle of the front
page in the default CKAN theme) to be customized with config settings:


    ckan.plugins = customizable_featured_image
    ckanext.express.featured_image = /birmingham_featured_image.jpeg
    ckanext.express.featured_alt_text = Birmingham!
    ckanext.express.featured_caption = This is Birmingham

To get no caption set it empty:

    ckanext.express.featured_caption =
