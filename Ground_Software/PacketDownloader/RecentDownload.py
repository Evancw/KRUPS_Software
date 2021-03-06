#!/usr/bin/env python3
__author__ = 'Collin'
import imaplib
import email
import email.message
import sys

'''
Needed Args:
username
password
number to download
directory
'''

TOTAL_ARGS = 5
YELLOW = ("\033[1;33m")
GREEN = ("\033[1;32m")
RED = ("\033[1;31m")
NC = ("\033[0m")


def printColor(msg, color):
    print(color + msg + NC)


def main():
    if len(sys.argv) != TOTAL_ARGS:
        printColor("Correct Command Args: <username> <password> <number to download> <download directory>", RED)
        exit(-1)

    # Logging in
    m = imaplib.IMAP4_SSL('imap.mail.yahoo.com', 993)
    username = sys.argv[1] # input('Input your username: ')
    password = sys.argv[2]  # input('Input your password: ')
    response = m.login(username, password)
    if response[0] == "OK":
        printColor("Logged in", GREEN)
    else:
        printColor("Failled to log in", RED)
        exit(-1)

    dir = str(sys.argv[4])
    if dir[len(dir) - 1] != '/':
        dir += '/'

    # choose inbox
    response = m.select()

    totalEmails = int(response[1][0])
    toDownload = int(sys.argv[3])

    for i in range(toDownload):
        # Downloads the packet from the current email
        response, data = m.fetch(str(totalEmails - i), "(UID BODY.PEEK[])")
        if response != 'OK':
            printColor("Failed to fetch message", RED)
            exit(-1)

        mail = email.message_from_bytes(data[0][1])
        id = str(data[0][0]).split()[2]
        for part in mail.walk():
            headerInfo = part.get('Content-Disposition')
            if str(headerInfo).split(';')[0] == 'attachment':
                attachment = part.get_payload(decode=True)
                filename = part.get_filename()
                printColor(filename, YELLOW)
                open(dir + filename, 'wb').write(attachment)
                m.uid('store', id, '+FLAGS', '(\\Seen)')

    # logging out procedure
    response = m.close()
    if response[0] == 'OK':
        printColor('Mailbox closed', GREEN)
    response = m.logout()
    if response[0] == 'BYE':
        printColor('Logged out', GREEN)


main()
