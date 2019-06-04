---
name: New issue
about: Use this for creating issues. Please fill all required information relevant
  to your issue. Issues missing necessary information requested in this template will
  be closed without consideration.
title: ''
labels: ''
assignees: tgalal

---

**Describe the bug**

What happened? Please make sure to first search existing issues and read the [FAQ](https://github.com/tgalal/yowsup/wiki/FAQ) in case this is already addressed.

**Debug output**

Switch on debug logging and include output along with the error or problem you see. If you are using yowsup-cli, this can be enabled by passing ```---debug```.

Please include any output as code blocks for proper formatting. For example:
```
debug output here
```

**Config file**

It's sometimes useful to post contents of your configuration file. If you do some, make sure to mask out your phone number, login, id, client_static_keypair, fdid, expid, otherwise you risk your account getting taken over.

Also please always post contents of your profile's config.json, and not just a different path you pass to yowsup-cli
(see [What is inside a profile's config.json?](https://github.com/tgalal/yowsup/wiki/FAQ#what-is-inside-a-profiles-configjson))

**Versions**

Please include python version, yowsup version, yowsup-cli version, as well as versions for consonance, dissononce, python-axolotl, and cryptography packages. Some of this information can be obtained if you run yowsup-cli with ```--debug``` flag, or through ```yowsup-cli version```.

If you are not using a released version but code directly from the repository, please indicate the commit hash.

**To Reproduce**

Include information about how to reproduce, even if the problem is sporadic any hints about the environment would help.

**Expected behavior**
A clear and concise description of what you expected to happen.

**OS (please complete the following information):**
Which OS did you encounter the bug on?

**Additional context**
Add any other context about the problem here.
