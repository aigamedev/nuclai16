# nuclai16 Hands-On Workshops

This repository contains the source code and data to participate in the workshops at the nucl.ai Conference 2016.  Programs should work on Windows, Linux and Mac OSX with Python 3.5.

You'll find multiple folders here:
1. **name —** desc
2. **name —** desc
  
See each sub-folder for further details and instructions.

## Installation & Dependencies

### Windows

#### PACKAGE MANAGER

We recommend you use [Chocolatey](https://chocolatey.org/) to manage the installation of packages.

1. **Install —** Run [this script](https://chocolatey.org/) to install Chocolatey locally on your machine.
2. **Update —** Type `choco upgrade chocolatey` to be sure you have the latest version.
3. **Tools —** Use `choco install -y msysgit cmdermini` to setup a modern console with Git.

You can find the Cmder executable in `C:\Tools`, and to out more about how to use Cmder on the official page. If the Cmder install fails the first time and refuses to try again, consider `--force` as an extra argument to Chocolatey.

#### GLOBAL DEPENDENCIES
Some libraries will be installed globally with Chocolatey for simplicity, as this avoids having to compile them during later setup.

1. **Python 3.5+ —** Type `choco install -y miniconda3` to get the latest version of 3.x.
2. **Close/Reopen —** Restart your terminal so the new PATH is reloaded automatically.
3. **Numpy & Scipy —** Type `conda install -y numpy scipy` to install computing libraries.

You can use `choco uninstall` to remove these packages once you’re done.

#### LOCAL ENVIRONMENT
You’ll be using a Python 3.x instance in a virtual environment. This means it’s both self-contained and can easily be deleted later.

1. **Download the repository —** In your home folder, `git clone https://github.com/aigamedev/nuclai16.git; cd nuclai16`
2. **virtualenv —** Type `python -m venv --system-site-packages pyvenv` to setup local Python.
3. **Activate —** In a shell, use `pyvenv\Scripts\activate.bat` to use the local version of Python 3.x.

### MAC OSX

We recommend you use [Homebrew](http://brew.sh/) to manage the installation of packages.

1. **Install —** Run [this script](http://brew.sh/) to install it on your machine.
2. **Update —** Type `brew update` to get the latest package listings.

You can find the Cmder executable in `C:\Tools`, and to out more about how to use Cmder on the official page. If the Cmder install fails the first time and refuses to try again, consider `--force` as an extra argument to Chocolatey.

#### GLOBAL DEPENDENCIES
Some libraries will be installed globally with Homebrew for simplicity, as this avoids having to compile them during later setup.

1. **Python 3.5+ —** Type `brew install python3` to get the latest version of 3.x.
2. **Numpy & Scipy —** Type `brew install numpy scipy` to install computing libraries.

You can use `brew uninstall` to remove these packages once you’re done.

#### LOCAL ENVIRONMENT
You’ll be using a Python 3.x instance in a virtual environment. This means it’s both self-contained and can easily be deleted later.

1. **Download the repository —** In your home folder, `git clone https://github.com/aigamedev/nuclai16.git; cd nuclai16`
2. **virtualenv —** To setup local Python type `/usr/local/bin/python3 -m venv --system-site-packages pyvenv` into your console.
3. **Activate —** For bash, use source pyvenv/bin/activate to use the local version of Python 3.x.
4. **Setup pip —** Run `python -m pip install pip --ignore-installed` to work around [this bug](http://bugs.python.org/issue24875).

### Linux 

#### SUPPORTED DISTRIBUTIONS
- **Ubuntu 14.04 —** Requires a Debian-based system with compatible libraries and runtimes.
- **64-bit Platform —** Only 64-bit operating systems are officially supported.

#### GLOBAL DEPENDENCIES
To install these, you will probably need to `sudo` to run the command as the system administrator.

1. **Python 3.5+ —** Type `apt-get install python3.5 python3.5-venv` to setup Python 3.x.
2. **Numpy & Scipy —** Run `apt-get install python3-numpy python3-scipy python3-pil` to install libraries.

You can use `apt-get uninstall` to remove these packages once you’re done.

#### LOCAL ENVIRONMENT
You’ll be using a Python 3.x instance in a virtual environment. This means it’s both self-contained and can easily be deleted later.

1. **Download the repository —** In your home folder, `git clone https://github.com/aigamedev/nuclai16.git; cd nuclai16`
2. **virtualenv —** To setup local Python type `python3 -m venv --system-site-packages pyvenv` into your console.
3. **Activate —** For bash, use `source pyvenv/bin/activate` to use the local version of Python 3.x.
4. **Setup pip —** Run python -m pip install pip --ignore-installed to work around [this bug](http://bugs.python.org/issue24875).