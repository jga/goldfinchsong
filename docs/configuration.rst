=============
Configuration
=============

The **goldfinchsong** project uses an **ini** file for configuration. The ``goldfinchsong`` command
expects the file to be in the directory from which the command is called. The default
name is ``goldfinchsong.ini``. However, these defaults can be changed by passing arguments
when calling the command. Review the :doc:`command line module guide <cli>` for details.

Python ``ini`` file options
---------------------------

**[goldfinchsong]** (section required)

This section is must have ``consumer_secret``, ``consumer_key``, ``access_token``, ``access_token_secret`` entries.

**[goldfinchsong.log]** (optional)

You can optionally provide an entry keyed to ``log_level`` with a
Python log level as a the value (e.g. ``ERROR``)::

    [goldfinchsong.log]
    log_level=ERROR


``log_location`` is an optional entry that sets the path to the file-based log. By default,
the log is filled at ``goldfinchsong.log``. So, for
example, if you wanted to have the log go to ``mysong.txt``, you would could create an
entry like this::

    [goldfinchsong.log]
    log_location=mysong.txt


**[goldfinchsong.conversions]** (optional)

The key/value entries in this file section are a convenient dictionary of text conversions,
typically abbreviations. For example::

    [goldfinchsong.conversions]
    FYI=for your information
    etc=etcetera
    abbr=abbreviation

These entries are optional, but can be quite helpful depending on the knowledge domain
covered by your image library.

**[goldfinchsong.images]** (optional)

``image_directory`` is an optional entry that sets the path to the image directory from
which images will be sourced for tweet posts.



Example ``ini`` file
--------------------

The example below covers all of the sections; however, only the first ``[goldfinchsong]`` section
is required.
::

    [goldfinchsong]
    consumer_key=goldfinchsong-consumer-key
    consumer_secret=goldfinchsong-consumer-secret
    access_token=goldfinchsong-access-token
    access_token_secret=goldfinchsong-access-token-secret
    [goldfinchsong.images]
    image_directory=my-alternative-directory/images
    [goldfinchsong.log]
    log_level=INFO
    [goldfinchsong.conversions]
    BVD=Better View Desired
    etc=etcetera
    FYI=for your information

