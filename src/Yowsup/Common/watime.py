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

import time,datetime,re
try:
	from dateutil import tz
except ImportError:
	from .dateutil import tz

class WATime():
	def parseIso(self,iso):
		d=datetime.datetime(*map(int, re.split('[^\d]', iso)[:-1]))
		return d
		
	def utcToLocal(self,dt):
		utc = tz.gettz('UTC');
		local = tz.tzlocal()
		dtUtc =  dt.replace(tzinfo=utc);
		
		return dtUtc.astimezone(local)

	def utcTimestamp(self):
		#utc = tz.gettz('UTC')
		utcNow = datetime.datetime.utcnow()
		return self.datetimeToTimestamp(utcNow)
	
	def datetimeToTimestamp(self,dt):
		return time.mktime(dt.timetuple());
	
