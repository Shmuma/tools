#!/usr/bin/env python

import imaplib
import sys
import netrc

host = 'imap.mail.ru'

nrc = netrc.netrc ()
auths = nrc.authenticators (host)

if auths == None:
    print 'No auth for host "%s"' % host
    sys.exit (-1)

imap = imaplib.IMAP4_SSL (host)

imap.login (auths[0], auths[2])
imap.select ('INBOX', False)

# check for unseen
ans, msgs = imap.fetch ('1:*', '(FLAGS)')
if any (map (lambda m: m.find ('Unseen') != -1, msgs)):
    sys.exit (0)
else:
    sys.exit (1)
