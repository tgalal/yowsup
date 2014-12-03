class Group(object):
    def __init__(self, groupId, ownerJid, subject, subjectOwnerJid, subjectTime, creationTime):
        self._groupId           = groupId
        self._ownerJid          = ownerJid
        self._subject           = subject
        self._subjectOwnerJid   = subjectOwnerJid
        self._subjectTime       = int(subjectTime)
        self._creationTime      = int(creationTime)

    def getId(self):
        return self._groupId

    def getOwner(self):
        return self._ownerJid

    def getSubject(self):
        return self._subject

    def getSubjectOwner(self):
        return self._subjectOwnerJid

    def getSubjectTime(self):
        return self._subjectTime

    def getCreationTime(self):
        return self._creationTime

    def __str__(self):
        return "ID: %s, Subject: %s, Creation: %s, Owner: %s, Subject Owner: %s, Subject Time: %s" %\
                (self.getId(), self.getSubject(), self.getCreationTime(), self.getOwner(),  self.getSubjectOwner(), self.getSubjectTime())

