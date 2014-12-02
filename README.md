# Yowsup 2.0
### Yowsup opened WhatsApp service under platforms!

Yowsup is a python library that enables you build application which use WhatsApp service. Yowsup has been used to create an unofficial WhatsApp client Nokia N9 through the Wazapp project which was in use by 200K + users as well as another fully featured unofficial client for Blackberry 10

## What's new in Yowsup 2.0

Everything! The old library code was so messed up that I was disgusted just by looking at it. I rewrote the library from ground up with a much more robust, extensible architecture and a much simpler and easier to read code. 
 
__For devs, the update is breaking for any old code. While old code will stay in "legacy" branch for a while, it's advised that you upgrade your code. Unless your code is a full fledged WhatsApp application, migrating won't be a hard task.__

Here is what you need to know about Yowsup 2.0 to get started: (Or quickly [jump to installation](#installation)):

 * **[The new architecture](https://github.com/tgalal/yowsup/wiki/Yowsup-2.0-Architecture)**
 * **[Create a sample app](https://github.com/tgalal/yowsup/wiki/Yowsup-2.0-Sample-app)**
 * **[yowsup-cli 2.0](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0)**
 * **[The new Command line client](https://github.com/tgalal/yowsup/wiki/Yowsup-2.0-Command-line-client)**
 * **[Yowsup development, debugging, maintainance and sanity](https://github.com/tgalal/yowsup/wiki/Yowsup-development,-debugging,-maintainance-and-sanity)**


#### Installation
 - Requires python2.6+, or python3.0 +
 - Required python packages: python-dateutil
 - Required python packages for yowsup-cli: argparse, readline (or pyreadline for windows)

Install using setup.py to pull all python dependencies
```
sudo python setup.py install
```
Because of a bug with python-dateutil package you might get permission error for some dateutil file called requires.txt when you use yowsup (see [this bug report](https://bugs.launchpad.net/dateutil/+bug/1243202)) to fix you'll need to chmod 644 that file.


## Special thanks

Special thanks to [CODeRUS](https://github.com/CODeRUS), [mgp25](https://github.com/mgp25), [shirioko](https://github.com/shirioko), and everyone else on the [WhatsAPI](https://github.com/mgp25/WhatsAPI-Official) project for their contributions to yowsup and the amazing effort they put into WhatsAPI, the PHP WhatsApp library

Special thanks goes to all other people who use and contribute to the library as well.

Please **[read this](https://github.com/tgalal/yowsup/wiki/Yowsup-development,-debugging,-maintainance-and-sanity)** if you'd like to contribute to yowsup 2.0

Thanks!


## License:
MIT License:

    Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this
    software and associated documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to use, copy, modify,
    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
    A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
    OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
