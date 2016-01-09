===============
Getting Started
===============

Design intent
-------------

You use twitter. You've got an image library (with, say, a bunch of jpg and png files) from
which you create tweets.  Instead of hand-crafting them on a twitter client or social media
application, you just want to automate posting tweets of images from your library.  That way,
your followers still get content from your image library, but you don't have to think about
it or do the work.

Making this happen is what **goldfinch** is for. It leverages Tweepy_ to make it easy to
automate sharing of your images. By default, **goldfinch** intelligently crafts the
status text for a tweet from the file name of the image, making it even easier to
manage your tweet output just from an image directory.

There's a straight-forward ``goldfinch`` command you can run from a terminal or
cron job. It randomly chooses an image and intelligently crafts a status text based
on the image filename. Or you can build your own application/CLI tools through re-use the
functions in the :doc:`utilities </utils>` module.

Install
-------

Use ``pip`` to install.

    pip install goldfinchsong

Putting **goldfinch** on your machine is not enough to make API calls to twitter.
You'll also need a Python ``ini`` file to provide twitter credentials.

Obtaining twitter credentials
-----------------------------

The information below helps you get going with **goldfinch** quickly, but it's
strongly recommended that your read Tweepy's `authentication tutorial`_ to better
grasp what is happening 'under the hood'.

Here are step-by-step instructions on how to obtain the credentials needed to
run **goldfinch** and post image tweets.

1. Create a twitter account.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2. Register the application with twitter.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Twitter's OAuth authentication model provides an "application-user" option; this is the approach that the
Tweepy_ package **goldfinch** relies on targets. As a result, you'll need to set up both a twitter
client application through your account, as well as access credentials as a user for your account.

Go to your account's `application management center`_. Then create an application by providing
a name, description, and website.

Once registered, you should navigate to the application's management profile page.

There should be a link that takes you to the *Keys and Access Tokens* tab. There,
you can get the application's *Consumer Key* and *Consumer Secret*. These will go in your **ini**
configuration file.

3. Generate an Access Token
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the same *Keys and Access Tokens* profile page, request generation yor *Access Token*, which will
also provide you the *Access Token Secret*. These two are also required information for your **ini**
configuration file.

Your first configuration
------------------------

At a minimum **goldfinch** requires your twitter authentication credentials to post. The command line script
included in the package expects these credentials to be placed in the configuration *ini* file. Read
the :doc:`configuration section </configuration>` for details.

Organizing your production files
--------------------------------

Select the directory where the your images directory and **ini** configuration file will reside.

You may choose to create a new, specialized directory (e.g. "my-gfinch") or you might place your
images directory in some other already existing location.  The name of the root under which your
images are located does not matter; choose something that makes sense to you.

Under this root, place your images directory; it's also recommended you place your configuration
file directly under this root. So, this is what your files would look like if you went with a new
"my-gfinch" root::

    my-gfinch/
        images/
            img1.png
            img2.jpg
            img3.png
        goldfinch.ini

You'll run the ``goldfinch`` command from the "my-finch" directory.

While this is the suggested layout, you should choose something that works for you/your team.

While ``images`` is the default location, you can change the location of the image directory
in the the configuration file or pass it as the value for the ``--images`` argument when you
run the ``goldfinch`` command.  Similarly, you can alter the expected location/name of configuration
file by passing it as the value for the ``--conf`` argument when you run the ``goldfinch`` command.

A simple cron job
-----------------

Using ``cron`` is a relatively simple, well-documented approach to automating execution of scheduled tasks
on a Linux machine. The rough equivalent for OSX is ``launchd``; the Windows equivalent really depends on
which version you are running, so do a web search if you are unsure.

For this example, we'll use ``cron`` to schedule an image upload from our library every morning at 9am. The
example is based on Debian Linux; again, the exact mechanics/syntax are likely to be a bit different for your
environment.

Once you've configured your file layout, you'll need to create a ``cron`` job that depends on the
``goldfinch`` command.  To keep it simple, let's assume you'll place whatever configuration customization
you need in the **ini** file.

It's quite typical in Python to use a virtual environment; we'll write a shell script that can be easily
executed by ``cron`` that also activates and deactivates the virtual environment you want to use for
running the ``goldfinch`` command. Let's create ``tweet-image.sh`` shell script. Open up a text
editor and create the following file::

    #!/bin/bash
    source ~/.env/goldfinch-env/bin/activate
    cd ~/my-gfinch
    goldfinch
    deactivate

Let's go line-by-line to understand what is happening in the script.

The first line is a convention that tells Linux what interpreter to run. Then, a Python virtual
environment is activated (the ``goldfinch-env`` name is illustrative, you may choose a
different name). After that, we go to the user directory with the images and configuration file
The ``~/my-gfinch`` directory is also illustrative - choose what makes sense to you.
Then the ``goldfinch`` command is run. Finally, the virtual environment is deactivated.

Now that we've covered what is in the file, finish setting up the script by using ``chmod`` to
make it executable::

    chmod +x tweet-image.sh


Next, we switch gears and focus on getting the script scheduled for execution. To do this,
you have to edit your ``cron`` jobs. Use::

    crontab -e

Within the file that opens up, you'll need to add a line. This line indicates you want the the shell script
run every day at 9am.
::

    00 9 * * * ~/scripts/tweet-image.sh


And that's it. You've used **goldfinch** to schedule automatic tweets with your images.


.. _application management center: https://apps.twitter.com
.. _authentication tutorial: http://docs.tweepy.org/en/latest/auth_tutorial.html
.. _configuration guide: configuration.hmtl
.. _Tweepy: http://www.tweepy.org
