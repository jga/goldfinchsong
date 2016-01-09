=============
Configuration
=============

The **goldfinch** project uses an **ini** file for configuration. The ``goldfinch`` command
expects the file to be in the directory from which the command is called. The default
name is ``goldfinch.ini``. However, these defaults can be changed by passing arguments
when calling the command. Review the :doc:`command line module guide <cli>` for details.

Python ``ini`` file options
---------------------------

**[goldfinch]** (section required)

This section is must have ``consumer_secret``, ``consumer_key``, ``access_token``, ``access_token_secret`` entries.

**[goldfinch.log]** (optional)

You can optionally provide an entry keyed to ``log_level`` with a
Python log level as a the value (e.g. ``INFO``)

**[goldfinch.conversions]** (optional)

The key/value entries in this file section are a convenient dictionary of text conversions,
typically abbreviations. For example::

    [goldfinch.conversions]
    FYI=for your information
    etc=etcetera
    abbr=abbreviation

These entries are optional, but can be quite helpful depending on the knowledge domain
covered by your image library.

**[goldfinch.images]** (optional)

``image_directory`` is an optional entry that sets the path to the image directory from
which images will be sourced for tweet posts.

Example ``ini`` file
--------------------

The example below covers all of the sections; however, only the first ``[goldfinch]`` section
is required.
::

    [goldfinch]
    consumer_key=goldfinch-consumer-key
    consumer_secret=goldfinch-consumer-secret
    access_token=goldfinch-access-token
    access_token_secret=goldfinch-access-token-secret
    [goldfinch.images]
    image_directory=my-alternative-directory/images
    [goldfinch.log]
    log_level=INFO
    [goldfinch.conversions]
    BVD=Better View Desired
    etc=etcetera
    FYI=for your information

