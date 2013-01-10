import re

def parseSyncOutput2XML (theInput):
	allTheContent = re.split(r'c: \[', theInput)[1] # removing leading c: [
	allTheContent = re.split(r']', allTheContent)[0] # removing trailing ]
	allTheContent = re.split(r'\}, \{|\{|\}', allTheContent) # removing leading { from first user data tuple
	n = 1 # element zero is empty string, first usable elment of list is 1
	theOutput = ""
	while n < (len(allTheContent)-1): # visit all the elements of the list, except the last (-1), because is always a null, useless string
		# SHOWTIMEEEE - Here comes the REGEX MAGICCCCCCCC
		tempContactDataTuple = re.sub(r'u\'(.+?)\'', r'\g<1>', allTheContent[n] ) # u'blablabla' becomes blablabla
		tempContactDataTuple = re.sub(r'u"(.+?)"', r'\g<1>', tempContactDataTuple ) # special scaped cases (status that have a single quote become sorrounded by double quotes)
		tempContactDataTuple = re.sub(r'p: (.+?), ', r'<p>\g<1></p>\n', tempContactDataTuple ) # parse phone #
		tempContactDataTuple = re.sub(r's: (.+?), ', r'<s>\g<1></s>\n', tempContactDataTuple ) # parse status quote
		tempContactDataTuple = re.sub(r't: (.+?), ', r'<t>\g<1></t>\n', tempContactDataTuple ) # parse time account signed in (I think)
		tempContactDataTuple = re.sub(r'w: (.+?), ', r'<w>\g<1></w>\n', tempContactDataTuple ) # parse whatsapp account existence 0/1
		tempContactDataTuple = re.sub(r'n: (.+)', r'<n>\g<1></n>\n', tempContactDataTuple ) # parse number in full format (w/countrycode)
		theOutput = theOutput + '<contact>\n' + tempContactDataTuple + '</contact>'
		n += 1
		if n < len(allTheContent)-1:
			theOutput = theOutput + '\n'
		
	return theOutput
	
	
