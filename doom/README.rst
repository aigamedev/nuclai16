nucl.ai '16 VizDoom Workshop
============================

1. Clone the repository: `git clone https://github.com/Marqt/ViZDoom`

2. `Download WAD files <https://github.com/freedoom/freedoom/releases/download/v0.10.1/freedoom-0.10.1.zip>`_ and extract into `scenarios`.

3. Build or download binaries, `detailed instructions <https://github.com/Marqt/ViZDoom/blob/master/README.md#building>.`_

4. Setup Python, version 2.7 is recommended if you downloaded the binaries:

.. code:: bash

    conda create -n py27 mingw libpython numpy scikit-image
    activate py27
    pip install Theano git+https://github.com/Lasagne/Lasagne
    set PYTHONPATH=../../bin/python/

5. Run a basic script from the examples folder:

.. code:: bash

    cd examples/python
    python basic.py

6. Follow the `workshop-specific exercises <https://github.com/wjaskowski/nucl.ai-vizdoom-workshop>`_ here.