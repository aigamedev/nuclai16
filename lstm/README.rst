Recurrent Neural Networks
=========================

0. Installation
---------------

We suggest installing `Docker <https://docker.com>`_ to run the code. Then you can enter a bash prompt within the image as follows:

.. code:: bash
    
    docker run -it alexjc/nuclai16:lstm

There is no output from this docker container, just text printed on the console.


1. Long Short-Term Memory
-------------------------

Using pre-trained data:

.. code:: bash

    python tweet.py --load lstm512

    python tweet.py --load lstm256x3

Training it yourself:

.. code:: bash

    python tweet.py --train --save lstm64


2. Simple Sequence To Sequence
------------------------------

.. code:: bash

    python s2s.py


3. Complex Sequence To Sequence
-------------------------------

.. code:: bash

    python reply.py

