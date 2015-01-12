# Yowsup 2

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Z9KKEUVYEY6BN" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>

## Updates (January 12, 2015)

Yowsup 2.2.15 is out.

Image upload and send is now implemented. [Read here](https://github.com/tgalal/yowsup/wiki/Yowsup2:-Upload-and-send-Media) how to integrate in your code, or try it out with yowsup-cli

[Read full release notes](https://github.com/tgalal/yowsup/releases/tag/v2.2.15)

### Updates (January 1, 2015) 

Happy new year!

P.S: Yowsup's [license changed](https://github.com/tgalal/yowsup#license) to GPLv3 (previously the MIT License was used).

### (December 31, 2014)

New features land in yowsup. You will need to re-install to pull new dependencies. Follow the [updated install instructions for your OS](#installation-updated-dec-31-2014).

A couple of highlights:

### End-to-End encryption

Yowsup now implements the new end-to-end encryption recently introduced in WhatsApp (AKA axolotl) (AKA textsecure). To activate in demos pass in '--moxie' switch.
Example:
 
 > yowsup-cli demos --config /path/to/config --yowsup --moxie

This will make messages communication with WhatsApp platforms which support this feature encrypted. At the moment it's only Android, which means yowsup got this feature even before official WhatsApp clients on other platforms.

For platforms which do not support encryption, they will get plaintext messages as usual.

More technical details about axolotl in yowsup [here](https://github.com/tgalal/yowsup/wiki/Yowsup-2:-End-to-End-encryption)

### New Send client demo

Use the send client demo in yowsup-cli to login, send a message and exit.

 > yowsup-cli demos --config /path/to/config --send NUMBER "Hello world"
   
==========================================================

## Yowsup opened WhatsApp service under platforms!

Yowsup is a python library that enables you build application which use WhatsApp service. Yowsup has been used to create an unofficial WhatsApp client Nokia N9 through the Wazapp project which was in use by 200K + users as well as another fully featured unofficial client for Blackberry 10

## What's new in Yowsup 2

Everything! The old library code was so messed up that I was disgusted just by looking at it. I rewrote the library from ground up with a much more robust, extensible architecture and a much simpler and easier to read code. 
 
__For devs, the update is breaking for any old code. While old code will stay in "legacy" branch for a while, it's advised that you upgrade your code. Unless your code is a full fledged WhatsApp application, migrating won't be a hard task.__

Here is what you need to know about Yowsup 2.0 to get started: (Or quickly [jump to installation](#installation)):

 * **[The new architecture](https://github.com/tgalal/yowsup/wiki/Yowsup-2.0-Architecture)**
 * **[Create a sample app](https://github.com/tgalal/yowsup/wiki/Yowsup-2.0-Sample-app)**
 * **[yowsup-cli 2.0](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0)**
 * **[The new Command line client](https://github.com/tgalal/yowsup/wiki/Yowsup-2.0-Command-line-client)**
 * **[Yowsup development, debugging, maintainance and sanity](https://github.com/tgalal/yowsup/wiki/Yowsup-development,-debugging,-maintainance-and-sanity)**


## Installation 
(Updated Jan 12, 2015)

 - Requires python2.6+, or python3.0 +
 - Required python packages: python-dateutil, 
 - Required python packages for end-to-end encryption: protobuf, pycrypto, python-axolotl-curve25519
 - Required python packages for yowsup-cli: argparse, readline (or pyreadline for windows), pillow (for sending images)

Install using setup.py to pull all python dependencies, or using pip:

```
pip install yowsup2
```

### Linux

You need to have installed python headers (from probably python-dev package) and ncurses-dev, then run
```
python setup.py install
```
Because of a bug with python-dateutil package you might get permission error for some dateutil file called requires.txt when you use yowsup (see [this bug report](https://bugs.launchpad.net/dateutil/+bug/1243202)) to fix you'll need to chmod 644 that file.

### Mac
```
python setup.py install
```
Administrators privileges might be required, if so then run with 'sudo' 

### Windows

 - Install [mingw](http://www.mingw.org/) compiler
 - Add mingw to your PATH
 - In PYTHONPATH\Lib\distutils create a file called distutils.cfg and add these lines:
 
```
[build]
compiler=mingw32
```
 - Install gcc: ```mingw-get.exe install gcc```
 - Install [zlib](http://www.zlib.net/)
 - ```python setup.py install```

If pycrypto fails to install with some "chmod error". You can install it separately using something like 
```easy_install http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe```

or for python3 from:

 > [https://github.com/axper/python3-pycrypto-windows-installer](https://github.com/axper/python3-pycrypto-windows-installer)

and then rerun the install command again

# Special thanks

Special thanks to:

- [CODeRUS](https://github.com/CODeRUS) 
- [mgp25](https://github.com/mgp25) 
- [SikiFn](https://github.com/SikiFn)
- [0xTryCatch](https://github.com/0xTryCatch)
- [shirioko](https://github.com/shirioko)

and everyone else on the [WhatsAPI](https://github.com/mgp25/WhatsAPI-Official) project for their contributions to yowsup and the amazing effort they put into WhatsAPI, the PHP WhatsApp library

Special thanks goes to all other people who use and contribute to the library as well.

Please **[read this](https://github.com/tgalal/yowsup/wiki/Yowsup-development,-debugging,-maintainance-and-sanity)** if you'd like to contribute to yowsup 2.0

Thanks!


# License:

As of January 1, 2015 yowsup is licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html. 

Earlier versions were licensed under the MIT License and the reason for the change is the new dependency on [python-axolotl](https://github.com/tgalal/python-axolotl) (GPLv3) which provides us with End-to-End encryption, without which yowsup would have been unusable in the near future.
