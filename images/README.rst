Installation
============

For the setup to work, you need `Docker <https://docker.com>`_ installed. Then you can setup an alias command.

.. code:: bash
   alias doodle="docker run -v $(pwd)/style:/nd/style -v $(pwd)/content:/nd/content \
			    -v $(pwd)/output:/nd/output -v $(pwd)/frames:/nd/frames \
                        -it alexjc/neural-doodle:fast"

The various folders named ``style``, ``content``, ``output`` or ``frames`` are taken from the current folder, presumably ``nuclai16/images`` and will be used to pass files back and forth to the container.

