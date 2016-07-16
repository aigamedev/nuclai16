Image Synthesis with Neural Networks
====================================

0. Installation
---------------

We suggest installing `Docker <https://docker.com>`_ to run the code. On Windows there are no alternatives, but on Linux and MacOS it's recommended. Then you can setup an alias command from bash:

.. code:: bash

    alias doodle="docker run -v $(pwd)/style:/nd/style -v $(pwd)/content:/nd/content \
                             -v $(pwd)/output:/nd/output -v $(pwd)/frames:/nd/frames \
                        -it alexjc/neural-doodle:fast"

The various folders named ``style``, ``content``, ``output`` or ``frames`` are taken from the current folder, presumably ``nuclai16/images`` and will be used to pass files back and forth to the container.


1. Image Reconstruction
-----------------------

.. code:: bash

    doodle --content content/Village.noise64.jpg --style content/Village.jpg \
           --passes 1 --layers 4 --iterations 1 --frames


2. Texture Synthesis
--------------------

.. code:: bash

    doodle --style style/sketch4.jpg --output-size=512x512\
           --passes 2 --layers 5 4 3 --iterations 4 3 2

    doodle --style style/paint4.jpg --output-size=512x512 \
           --passes 2 --layers 5 4 3 --iterations 4 3 2


3. Style Transfer
-----------------

.. code:: bash

    doodle --content content/Freddie.jpg --style style/charcoal1.jpg \
           -passes 2 --layers 5 4 --iterations 3 3 \
           --variety 20 10 0 --content-weight 0.3 0.1 0.0


4. Neural Doodle
----------------

.. code:: bash

    doodle --content content/Freddie.jpg --style style/charcoal2.jpg --semantic-weight=1.0 \
           --passes 2 --layers 5 4 --iterations 3 2 \
           --variety 100 0 --content-weight 0.1 0.0 --noise-weight 0.1 0.0
