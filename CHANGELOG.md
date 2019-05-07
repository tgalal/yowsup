# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project (kinda) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.3] 2019-05-07

### Changed

- Fixed incoming message output format in cli demo

## [3.2.2] 2019-05-07

### Changed

- Updated python-axolotl to 0.2.2, fixes possible variable referenced before assignment error

## [3.2.1] 2019-05-07

### Changed

- Updated python-axolotl to 0.2.1
- Fixed encoding errors when communicating in group
- Fixed messages not delivered to groups, showing a "Waiting for this message, this may take a while"
- Fixed bug where getKeys for multiple jids would invoke the callback multiple times
- Fixes in RequestUpload and media classes in preparation for media sending

### Added

- More log output in AxolotlSendLayer

## [3.2.0] 2019-05-04

### Changed

- Set min protobuf version to fix an error
- Use WhatsApp version set by env in noise layer
- Fixed error when mcc,mnc and fdid were missing from config
- Don't crash when received an unrecognized ib node
- Don't crash when received an unrecognized media type and send receipt
- Don't crash when received an unrecognized notification type and send receipt
- Asyncore is now used as default ConnectionDispatcher
- Received protobuf messages are now handled in upper layers rather than Axolotl

### Added

- MediaCipher for encrypting and decrypting media files
- "media" yowsup-cli action with encrypt and decrypt media commands
- Receive Audio, Video, Image, Document, Contact, Location, GIF, URL message support
- MediaSink demo, access by yowsup-cli demos --mediasink

### Removed

- unused -w flag from yowsup-cli config

## [3.1.0] 2019-04-25

### Changed

- Network layer prevents createConnection if already connected
- Fixed crash when config path does not exist
- yowsup-cli will interpret -c as phone if load_path fails
- Allow keypair in credentials to be bytes
- Noise layer now uses credential's client_static_keypair if set, instead of loading it from stored config
- Improved config type detection logic, refs #2664
- Fixed some python2-related problems (long-type phone numbers, missing list.clear() method), refs #2664
- Updated consonance to fix dissononce's machine.next and enforce cryptography>=0.25
- Fixed some demos not shutting down properly

### Added

- Complete asyncore dispatcher implementation.
- Support for decoding deflate compressed data, fixes #2671
- Specifying a connection dispatcher (asyncore/socket) using YowNetworkLayer.PROP_DISPATCHER
- --layer-network-dispatcher to cli demos

### Removed

- threading from socket dispatcher, connecting application should ensure the connection is not blocking, for
example by triggering connect in a bg thread.

## [3.0.0] 2019-04-23

### Changed

- Changed default env to android
- Updated whatsapp version in env to 2.19.51
- Updated logs formatting to be more compact
- Changed storage dir on linux to ~/.config/yowsup
- yowsup-cli -p is now used for preview requests rather than specifying phone number
- Decoupled Axolotl management from Axolotl layer
- Fixed Python3.7 support
- Updated device details in Env to be of Samsung S9+
- Changed generated signed prekeys ids to be sequential
- Fixed some notifications getting redundant acks
- Fixed outgoing ack in a group now requiring participant to be specified

### Added

- WhatsApp Protocol 2.1 support
- Noise layer
- Login using Consonance; a new dependency
- New Registration parameters
- Encryption of registration parameters
- Auto saving of Config at registration
- Log which endpoint we are connecting to
- Support superadmin and multiple admins in group create notification
- Better Config management and JSON config files support 
- AxolotlManager
- Any Config property overriding in yowsup-cli
- yowsup-cli config
- yowsup-cli --log-dissononce
- yowsup-cli --log-dissononce
- Preview only registration and other http requests

### Removed

- Optional axolotl/e2e enc enabling, it's now forced.
- S40 env
- Password from Config
- Outdated http parameters in registration
- TimeTools along with python-dateutil dependency.

## [2.5.7] - 2017-12-30

### Changed

- Changed Token
- Fixed Python2 support
- Fixed #1842: Bug in protocol_groups RemoveGroupsNotificationProtocolEntity

## [2.5.2] - 2017-03-23

### Changed

- Fixed xml-not-well-formed when data is sent from multiple threads simultaneously
- Updated S40 Token

## [2.5.0] - 2016-05-22

### Changed

- Fixed python 2.6 support
- Fixed block detection in exists request, initiated by code request
- Fixed crash when node data is string
- Updated s40 token to 2.16.7
- Fixed timestamp in authentication not being UTC
- Fixed handling variant decrypt/encr fail scenarios

### Added

- Allowing autotrust changed identities via an exposed layer property
- Auto-reconnect on stream:error
- WA1.6 support
- Fully working group encryption support

## [2.4.103] - 2016-04-24

### Changed

- Updated token

## [2.4.102] - 2016-04-01

### Added

- Simpler env select using YowsupEnv.setEnv("env_name"), get using YowsupEnv.getCurrent()
- yowsup-cli allows setting preferred env using -E/--env argument

## [2.4.98] - 2016-03-31

### Changed

- Minor README update

## [2.4.97] - 2016-03-31

### Changed

- pillow, axolotl and ffvideo as optional modules
- Improved mimetypes detection in media sending
- Fixed some group Iqs callbacks getting swallowed and never invoked
- Fixed python3 compat in iq_statuses_result
- Fixed asyncore initialization
- Updated tokens and fixed registration
- Skip encryption of group messages
- Improved video sending support
- Fixed URL to country codes in yowsup-cli help

### Added

- New optional modules interface
- New @EventCallback decoration to replace layer's onEvent method
- echo and send clients now enable encryption by default
- Can now send videos from cli demo
- Added *BSD installation instructions

## [2.4.48] - 2015-12-14

### Changed

- Fixed bug that avoid some acks from being sent
- Check fields in video message before parsing
- Fixed image scaling in Palette mode
- Fixed image preview
- Fixed erroneous method in LiteAxolotlStore
- Fixed YowParallelLayer returning layer instead of the layer's interface
- Fixed login
- Updated registration token
- Updated android env data
- Fixed Warning that demos are not using YowParallelLayer

### Added

- Send read receipts for received messages in cli demo
- Can now get status of users
- new profile privacy options

## [2.4.0] - 2015-09-07

### Changed

- Updated S40 env to 2.12.96
- Fixed message forwarding
- Don't panic on try send something when offline
- Fixed interface not forwarding to upper layers unhandled protocolenties
- Don't crash on UntrustedIdentityException, will silently ignore the message
- E2E enc is now enabled by default, remove -m/--moxie switch

### Added
- Support sending receipt for multiple messages
- Layers can now expose an InterfaceLayer for outside interaction
- YowNetworkLayer and Auth Layer now expose an InterfaceLayer
- Allow setting props on stackbuilder, it passed them to the instantiated stack
- Handle DuplicateMessageException
- Added stack.send/receive
- Opt-out E2E enc using -M/--unmoxie

### Removed

- yowsup-cli's -m/--moxie switch

## [2.3.185] - 2015-08-01

### Changed

- Recover from possible no session/no prekey in a received message

### Added

- Send/receive v2 enc messages

## [2.3.183] - 2015-07-27

### Changed

- Fixed audio send
- improved cli demo usage display

### Added

- random endpoints selection
- Handle account ib
- "/audio send" to cli demo
- support for image caption in cli demo

## [2.3.167] - 2015-07-21

### Changed

- Updated to e16 serv
- Fixed callbacks for group info iq
- Use s40 env by default
- Updated to s40 v2.12.189
- Fixed error in android env with python 2.6
- Deprecated --moxie
- Fixed error when axolotl is not installed

### Added

- Added contact sync notification
- Optional arguments support in yowsup demo

### Removed

- "av" from enc nodes

## [2.3.124] - 2015-07-06

### Changed

- Fixed forward in groups

## [2.3.123] - 2015-06-22

### Changed

- Some code clean ups
- Fixed set status and set picture not triggering callbacks
- Handle multiple items in receipt

### Added

- Create an ack or a forwarded message directly from receipt message
- Allow getting Id of set profile picture
- Get contact's last seen time
- Notifications for participants add,remove in a group
- Receipts from participants in a group
- Promote,demote participants and rest of groups version 2 support
- New contacts sync demo
- New groups commands: /group promote, /group demote
- New contacts commands: /contact lastseen

## [2.3.84] - 2015-05-26

### Changed

- Updated s40 tokens
- Updated android token
- Fixed receive presence
- Fixed ack errors
- Propagate StreamFeaturesProtocolEntity to upper layers
- Fixes to incoming receipt
- Don't stream error on web notifications
- Fixed keys_get in cli demo
- Fixed invite to group in cli demo

### Added

- Allowing to specify ping interval
- Connect behind http proxy support
- Audio and video receive support
- Get contact's profile picture
- Handle calls
- Group info v2
- Kick from group in cli demo

## [2.2.78] - 2015-02-17

### Changed

- Fixed problem reading identity which caused reg error
- Keep connection alive through periodic pinging
- Fixed compatibility with the whole python 2.6-3.4 spectrum
- Distinguish received delivered and read receipt
- Fixed leave groups
- Fixes to registration
- Updated S40 registration token
- Fixed groups jid handling in sendclient
- Fixed readline redundant dependency in linux

### Added

- StackBuilder to make stack construction easier
- Profile Layer
- participants to a group
- Save next challenge and use in next auth
- Get contact profile picture
- group_invite in cli demo to add participants to a group
- leave_group in cli demo

## [2.2.15] - 2015-01-12

### Changed

- As of January 2015, Yowsup is GPLv3 licensed (previouly was MIT)
- Fixed broadcast
- Fixed registration no_routes error
- Updated registration token

### Added

- Experimental Axolotl support (end-to-end encryption)
- Upload and send images
- Initial support for groups v2
- Easy switch/ add new enviornment (S40/Android ..etc)
- _sendIq in YowProtocolLayer and YowInterfaceLayer with callbacks for Iq result and error
- new send and exit demo
- E2E encryption in yowsup and echo client demos
- image_send to yowsup demo

## [2.0.53] - 2014-12-15

### Changed

- Upgraded to WA 1.5
- Fixed previews in images
- Write date to socket as they come
- Fixed readline/pyreadline dependency problem

### Added

- Add chatstate support (typing/ paused)
- support for send/recv location
- support for send/recv vcards
- potential fix for not receiving registration sms
- Pass pongs to upper layers
- Ack notifications
- Parallels layers now get events sent by siblings
- Broadcast event on login
- send typing/paused state to cli demo
- Echo demo now echoes images
- Echo demo now echoes vcards

## [2.0.1] - 2014-12-01

### Changed

- Minor bug fixes

## [2.0] - 2014-11-28

yowsup 2.0 initial release

