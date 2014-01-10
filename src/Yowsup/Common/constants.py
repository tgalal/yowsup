'''
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
'''

class Constants:
	'''dictionary = [ None, None, None, None, None,  "1", "1.0", "ack", "action", "active", "add", "all", "allow", "apple", "audio", "auth", "author",
			"available", "bad-request", "base64", "Bell.caf", "bind", "body", "Boing.caf", "cancel", "category", "challenge", "chat", "clean",
			"code", "composing", "config", "conflict", "contacts", "create", "creation", "default", "delay", "delete", "delivered", "deny",
			"DIGEST-MD5", "DIGEST-MD5-1", "dirty", "en", "enable", "encoding", "error", "expiration", "expired", "failure", "false", "favorites",
			"feature", "field", "free", "from", "g.us", "get", "Glass.caf", "google", "group", "groups", "g_sound", "Harp.caf",
			"http://etherx.jabber.org/streams", "http://jabber.org/protocol/chatstates", "id", "image", "img", "inactive", "internal-server-error",
			"iq", "item", "item-not-found", "jabber:client", "jabber:iq:last", "jabber:iq:privacy", "jabber:x:delay", "jabber:x:event", "jid",
			"jid-malformed", "kind", "leave", "leave-all", "list", "location", "max_groups", "max_participants", "max_subject", "mechanism", "mechanisms",
			"media", "message", "message_acks", "missing", "modify", "name", "not-acceptable", "not-allowed", "not-authorized", "notify", "Offline Storage",
			"order", "owner", "owning", "paid", "participant", "participants", "participating", "fail", "paused", "picture", "ping", "PLAIN", "platform",
			"presence", "preview", "probe", "prop", "props", "p_o", "p_t", "query", "raw", "receipt", "receipt_acks", "received", "relay", "remove",
			"Replaced by new connection", "request", "resource", "resource-constraint", "response", "result", "retry", "rim", "s.whatsapp.net", "seconds",
			"server", "session", "set", "show", "sid", "sound", "stamp", "starttls", "status", "stream:error", "stream:features", "subject", "subscribe",
			"success", "system-shutdown", "s_o", "s_t", "t", "TimePassing.caf", "timestamp", "to", "Tri-tone.caf", "type", "unavailable", "uri", "url",
			"urn:ietf:params:xml:ns:xmpp-bind", "urn:ietf:params:xml:ns:xmpp-sasl", "urn:ietf:params:xml:ns:xmpp-session", "urn:ietf:params:xml:ns:xmpp-stanzas",
			"urn:ietf:params:xml:ns:xmpp-streams", "urn:xmpp:delay", "urn:xmpp:ping", "urn:xmpp:receipts", "urn:xmpp:whatsapp", "urn:xmpp:whatsapp:dirty",
			"urn:xmpp:whatsapp:mms", "urn:xmpp:whatsapp:push", "value", "vcard", "version", "video", "w", "w:g", "w:p:r", "wait", "x", "xml-not-well-formed",
			"xml:lang", "xmlns", "xmlns:stream", "Xylophone.caf", "account", "digest", "g_notify", "method", "password", "registration", "stat", "text", "user",
			"username", "event", "latitude", "longitude", "true", "after", "before", "broadcast", "count", "features", "first", "index", "invalid-mechanism",
			"last", "max", "offline", "proceed", "required", "sync", "elapsed", "ip", "microsoft", "mute", "nokia", "off", "pin", "pop_mean_time", "pop_plus_minus",
			"port", "reason", "server-error", "silent", "timeout", "lc", "lg", "bad-protocol", "none", "remote-server-timeout", "service-unavailable", "w:p", "w:profileicture",
			"notification" ]
	'''

	dictionary = [None, None, None, None, None, "account", "ack", "action", "active", "add", "after", "ib", "all", "allow", "apple", "audio", "auth", "author", "available", "bad-protocol", "bad-request", "before", "Bell.caf", "body", "Boing.caf", "cancel", "category", "challenge", "chat", "clean", "code", "composing", "config", "conflict", "contacts", "count", "create", "creation", "default", "delay", "delete", "delivered", "deny", "digest", "DIGEST-MD5-1", "DIGEST-MD5-2", "dirty", "elapsed", "broadcast", "enable", "encoding", "duplicate", "error", "event", "expiration", "expired", "fail", "failure", "false", "favorites", "feature", "features", "field", "first", "free", "from", "g.us", "get", "Glass.caf", "google", "group", "groups", "g_notify", "g_sound", "Harp.caf", "http://etherx.jabber.org/streams", "http://jabber.org/protocol/chatstates", "id", "image", "img", "inactive", "index", "internal-server-error", "invalid-mechanism", "ip", "iq", "item", "item-not-found", "user-not-found", "jabber:iq:last", "jabber:iq:privacy", "jabber:x:delay", "jabber:x:event", "jid", "jid-malformed", "kind", "last", "latitude", "lc", "leave", "leave-all", "lg", "list", "location", "longitude", "max", "max_groups", "max_participants", "max_subject", "mechanism", "media", "message", "message_acks", "method", "microsoft", "missing", "modify", "mute", "name", "nokia", "none", "not-acceptable", "not-allowed", "not-authorized", "notification", "notify", "off", "offline", "order", "owner", "owning", "paid", "participant", "participants", "participating", "password", "paused", "picture", "pin", "ping", "platform", "pop_mean_time", "pop_plus_minus", "port", "presence", "preview", "probe", "proceed", "prop", "props", "p_o", "p_t", "query", "raw", "reason", "receipt", "receipt_acks", "received", "registration", "relay", "remote-server-timeout", "remove", "Replaced by new connection", "request", "required", "resource", "resource-constraint", "response", "result", "retry", "rim", "s.whatsapp.net", "s.us", "seconds", "server", "server-error", "service-unavailable", "set", "show", "sid", "silent", "sound", "stamp", "unsubscribe", "stat", "status", "stream:error", "stream:features", "subject", "subscribe", "success", "sync", "system-shutdown", "s_o", "s_t", "t", "text", "timeout", "TimePassing.caf", "timestamp", "to", "Tri-tone.caf", "true", "type", "unavailable", "uri", "url", "urn:ietf:params:xml:ns:xmpp-sasl", "urn:ietf:params:xml:ns:xmpp-stanzas", "urn:ietf:params:xml:ns:xmpp-streams", "urn:xmpp:delay", "urn:xmpp:ping", "urn:xmpp:receipts", "urn:xmpp:whatsapp", "urn:xmpp:whatsapp:account", "urn:xmpp:whatsapp:dirty", "urn:xmpp:whatsapp:mms", "urn:xmpp:whatsapp:push", "user", "username", "value", "vcard", "version", "video", "w", "w:g", "w:p", "w:p:r", "w:profile:picture", "wait", "x", "xml-not-well-formed", "xmlns", "xmlns:stream", "Xylophone.caf", "1", "WAUTH-1"]

	host = "c2.whatsapp.net"
	port = 443
	domain = "s.whatsapp.net"

	v="0.81"

	tokenData = {
		"v": "2.12.10",
		"r": "S40-2.12.10",
		"u": "WhatsApp/2.12.10 S40Version/14.26 Device/Nokia302",
		"t": "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1386883946914{phone}",
		"d": "Nokia302"
	}

	tokenStorage = "~/.yowsup/t_%s"%(v.replace(".", "_"))
	tokenSource = ("openwhatsapp.org", "/t")

	#t


