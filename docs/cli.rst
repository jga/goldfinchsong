======================
Command line interface
======================

The ``goldfinchsong`` command
-----------------------------

Once you've installed **goldfinchsong** into your active Python environment, you have
the ``goldfinchsong`` command at your disposal.  This command chooses a random image
from your local image library, constructs a status text, and posts it with the
credentials in your configuration file.

There are three option flags available for the command.

``--action`` (default: *post*)

The action the script should take.  The *post* action uploads a tweet.

``--conf`` (default: *goldfinchsong.ini*)

The location of the configuration file.

``--images`` (default: ``None``)

The location of the image directory. You can also configure this in the **ini** file, but
the command line value overrides (i.e. takes precedence) the **ini** settings. If there's
no value passed to the command or found in the configuration file, then 'images' is used
as the default directory location.

Module functions
----------------

.. autofunction:: goldfinchsong.cli.get_image_directory

.. autofunction:: goldfinchsong.cli.parse_configuration

.. py:function:: goldfinchsong.cli.run(action='post', conf='goldfinchsong.ini', images=None)

    Uploads an image tweet.

    The :class:`~.goldfinchsong.classes.Manager` class does the actual
    work; this function contributes logic for extracting configuration
    settings and creating a ``TinyDB`` instance.

    :param str action: An action name.
    :param str conf: File path for a configuration file. By default, this
        function looks for ``goldfinchsong.ini`` under the directory from
        which the user executes the function.
    :param str images: File path to a directory with images that will be uploaded by tweets.
