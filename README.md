
# yowsup2 - with goodies [ by scratchie171 ]
## Current Build: [![Build Status](https://travis-ci.org/tgalal/yowsup.svg?branch=master)](https://travis-ci.org/tgalal/yowsup)


## NOTICE :)
The Current project is a fork of [Yowsup library](https://github.com/tgalal/yowsup) by [Takek Galal](https://github.com/tgalal). The following is just a mere collection of info and tweaks / patches that was left incomplete in the main project. Feel free to contribute to the info here and give feedback for any misleads.


## !! WARNING !!

Starting since 2018 Whatsapp has improved their servers and this makes the library partially unusable. Be aware that by registering through the `yowsup-cli` you may get a ban. Similar cases might be issued if the lib is used alike normal client, this would trigger anti-bot measures in the servers resulting in a ban.

Follow the status of the patching progress: [here](https://github.com/tgalal/yowsup/issues/2829).

---


## Quick Contents
 * **[Intro](#intro)**
 * **[Installation](#installation)**
 * **[Yowsup-cli Quickstart](#yowsup-cli)**
 * **[Yowsup - Getting Started](https://github.com/scratchie171/yowsup/wiki/Architecture)**
 * **[Create a Sample Script](https://github.com/scratchie171/yowsup/wiki/Sample-Application)**
  * **[See Also](#see-also)**
  * **[License and Credits](#license-and-credits)**

## INTRO

`yowsup2` is a python library that enables building applications that can communicate with WhatsApp users.
The project started as the protocol engine behind [Wazapp for Meego](https://wiki.maemo.org/Wazapp) and
[OpenWA for BB10](https://www.lowyat.net/2013/5896/try-this-openwhatsapp-for-blackberry-10/). The Clients are now banned as of 2019 due to revoked support for the devices.

The library can still be used to power any custom WhatsApp client.

```
updated: 2019-05-07
yowsup version: 3.2.3
yowsup-cli version: 3.2.0
requires:
- python>=2.7,<=3.7
- consonance==0.1.3-1
- python-axolotl==0.2.2
- protobuf>=3.6.0
- six==1.10
uses:
 - argparse [yowsup-cli]
 - readline [yowsup-cli]
 - pillow [send images]
 - tqdm [mediasink demo]
 - requests [mediasink demo]
```



## Installation

Install using setup.py to pull all Python dependencies, or pip3:

### Using Pip3
```
pip3 install yowsup2
```

### Linux

First we need to make sure `python3` and the dev libs are installed.
```
sudo apt-get install python3 python3-pip python3-dev ncurses-dev
```
Next we'll fetch the `python3` modules required.
```
pip3 install -r requirements.txt
```
Then, we'll build and install `yowsup2` to the system
```
python setup.py install
```

*(Alternatively you can use a python3 virtual environment for package isolation)*

### FreeBSD (*BSD)
You need to have installed: py27-pip-7.1.2(+), py27-sqlite3-2.7.11_7(+), then run
```
pip install yowsup
```

### Mac OS
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


## Yowsup-cli

You can make sure that the `yowsup-cli` is executable if you don't want to type `python3 yowsup-cli` everytime or edit `env python` in the script to `env python3`.

```
chmod +x yowsup-cli
```
To check the `yowsup-cli` and `yowsup2` versions
```
python3 yowsup-cli version
```
Lets Register our mobile number with Country Code ( cc: `01` for US) and your 10 digit MSISDN (phone number: `9876543210`), and lets set ( one ) of voice / sms as a paramater for registration.

You can find a full list here at [Wikipedia](https://en.wikipedia.org/wiki/Mobile_country_code), [CellIdFinder](https://cellidfinder.com/mcc-mnc) and [MCC-MNC](https://www.mcc-mnc.com/).
```
python3 yowsup-cli registration -r [sms / voice] --config-cc 01 --config-phone 019876543210  
```
We now have the code from the SMS (```171-171``` i.e. 171171), use your code in place of it.
```
python3 yowsup-cli registration --config-cc 01 -R 171171 --config-phone 019876543210  
```


After a successfull verification you'd receive a JSON text like.
If the registration did'nt work, try reading yowsup-patches-n-hotfixes.
```
{
    "__version__": 1,
    "cc": "91",
    "client_static_keypair": "yIpIQ*****************************************************1L/n9Tw==",
    "expid": "ByUTw5E****************==",
    "fdid": "c1d3****-****-****-86a1-12b3c0d0f19c",
    "id": "K2H1eL*******+NzYP1yi******=",
    "login": "**80014*****",
    "mcc": "000",
    "mnc": "000",
    "phone": "**80014*****",
    "sim_mcc": "**",
    "sim_mnc": "000"
}
```

Save contents to config.json

(you can use any of `vim` or `emacs` or even `vscode`. to keep this beginner friendly, and not to start a *Emacs-VS-Vim* thread i'll keep this neutral)

```nano config.json ```

Now let's send a message with the cli
```
python3 yowsup-cli demo --config config.json -s 01[a-number-here-to-test] [message]
```
Now lets run the echo demo *(echo's the message text)*

**-d**  tag is for debug logs
```
python3 yowsup-cli demo --config config.json -e -d 
```

## See also

During maintenance of yowsup, several projects have been spawned out in order to support different features that get
introduced by WhatsApp. Some of those features are not necessarily exclusive to WhatsApp and therefore it only made
sense to maintain some parts as standalone projects:

- [python-axolotl](https://github.com/tgalal/python-axolotl): Python port of
[libsignal-protocol-java](https://github.com/signalapp/libsignal-protocol-java), providing E2E encryption
- [consonance](https://github.com/tgalal/consonance/): WhatsApp's handshake implementation using Noise Protocol
- [dissononce](https://github.com/tgalal/dissononce):  A python implementation for
[Noise Protocol Framework](https://noiseprotocol.org/)

# License and Credits:
## Main Author: TGalal @ [Github](https://github.com/tgalal)
All of the bigger credits goes to TGalal for his immense hard work in this project.
## Maintainer and Patcher: Scratchie171 @ [Github](https://github.com/scratchie171)
Just a guy putting together a documentation and patching the gaps left in the original `yowsup` and `yowsup2` libs. Along with anti-ban tweaks.
Feel free to contact me Scratchie171 @ [Telegram](https://t.me/scratchressurect171).

---

As of January 1, 2015 yowsup is licensed under the GPLv3+: http://www.gnu.org/licenses/gpl-3.0.html to TarekGalal[https://github.com/tgalal]
