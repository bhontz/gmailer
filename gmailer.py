"""
    gmailer - SMTP protocol templated based mass mailing script for GMAIL accounts.
    Please review the README.md associated with this github repo regarding the appropriate settings for
    your GMAIL account and the emailcredentials.ini file format, which contains the email address and
    password of your GMAIL account.

    gmailer can utilize either Google Sheets (using module datasheets) or a CSV file as its "database".
    Use of Google Sheets requires creation of a Google Oath file which is documented here:
    https://datasheets.readthedocs.io/en/latest/getting_oauth_credentials.html

    The filter module supports segmenting the database based upon the fields you've created.
    Templates are based upon the jinja2 template engine, see more here:
    https://jinja.palletsprojects.com/en/2.11.x/templates/
"""

import os, time, csv, smtplib, jinja2
from configparser import ConfigParser
import datasheets  # required for Google Sheets
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class Gmailer():
    def __init__(self):
        self.subject = None
        self.htmlTemplate = None
        self.txtTemplate = None
        self.sendCount = 0
        self.lstMailingList = list()  # your mailing list (of dictionaries) as imported from a CSV or Google Sheet
        self.lstAttachments = list()
        self.cfg = ConfigParser()
        self.cfg.read('emailcredentials.ini')  # INI file needs to be in same folder as this module

        return

    def __del__(self):
        del self.cfg
        self.cfg = None
        del self.lstMailingList
        self.lstMailingList = None
        del self.lstAttachments
        self.lstAttachments = None

        return

    def setEmailSubject(self, s):
        """
            Parameter s of this module is the subject line of this email
        """
        self.subject = s
        return

    def setAttachments(self, lstAttachments):
        """
            Parameter lstAttachments contains a list of filenames (names+extensions) of files
            that are found within the attachments folder.
        """
        self.lstAttachments = lstAttachments
        return

    def setContentTemplate(self, strTemplateName):
        """
            Gmailer supports a MIME email payload that contains a plain text as well as a HTML version of the
            templated content, thereby supporting recipients that can only receive plain text.
            These two templates live within the template folder and are assumed to have the same
            base file name (e.g. exampleTemplate.txt and exampleTemplate.html) with TXT and HTML extensions.
            The argument to this method is the base file name (e.g. exampleTemplate).
        """
        try:
            fp = open('templates/%s.html' % strTemplateName, 'rt')
        except IOError as detail:
            s = "TEMPLATE DID NOT LOAD ERROR"
        else:
            s = fp.read()
            fp.close()

        self.htmlTemplate = jinja2.Template(s)  # this is associated with the file reading test

        try:
            fp = open('templates/%s.txt' % strTemplateName, 'rt')
        except IOError as detail:
            s = "TEMPLATE DID NOT LOAD ERROR"
        else:
            s = fp.read()
            fp.close()

        self.txtTemplate = jinja2.Template(s)

        return

    def LoadGoogleSheets(self, strSheetName, strTabName):
        """
            Note that the folder ~/.datasheets contains the Google Oath files required
            Returns a list of dictionary items representing the rows of the
            specified google sheet (strSheetName)'s tab (strTabName)
        """
        self.lstMailingList = list()

        client = datasheets.Client(service=True)
        workbook = client.fetch_workbook(strSheetName)
        tab = workbook.fetch_tab(strTabName)
        df = tab.fetch_data()

        del tab
        del workbook
        del client

        self.lstMailingList = df.to_dict(orient='record')
        del df

    def LoadCSV(self, strPathFilename, lstFloatFields=[]):
        """
            Returns a list of dictionaries formed by parsing a CSV file (strPathFilename) with a row header.
            You can specify fields that need to be forced to floats by adding a list of the field names
            as the option parameter lstFloatFields.  This is useful if you are trying to replicate the behavior
            of a Google Sheet database, which will force numeric fields to be floats.
        """

        try:
            fp = open(strPathFilename, 'r')
        except IOError as detail:
            print("can't open input file %s. Details:%s\n" % (strPathFilename, detail))
        else:
            reader = csv.reader(fp)
            lstHeader = next(reader)  # python 3, python 2 was reader.next()
            rows = list(reader)
            del reader
            fp.close()

            for r in rows:
                d = dict()
                for l in lstHeader:
                    if l in lstFloatFields:  # simulate float values as per the Google Sheets
                        d[l] = float(str(r[lstHeader.index(l)]).lstrip().rstrip())
                    else:
                        d[l] = str(r[lstHeader.index(l)]).lstrip().rstrip()
                self.lstMailingList.append(d)

    def filterList(self, f):
        """
            This module's parameter is a filter function that will filter the lstMailingList based
            upon a query of the fields of lstMailingList.  See the README.md file for examples
        """
        self.lstMailingList = list(f)

        return

    def __simpleEmailMessage(self, recipientEmailAddress, html, text):
        """
            Here we're using some of python's standard methods to send a simple email.
            I didn't finish this as you need to add your gmail account pw to make this work.
            Left it in here for you to discover and fix up.
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.cfg.get('email', 'user')
        msg['To'] = recipientEmailAddress

        msg.attach(MIMEText(text, 'plain'))  # these are the templates rendered within method SendEmails
        msg.attach(MIMEText(html, 'html'))

        # provides a mean for attachment of files
        if self.lstAttachments != []:
            for f in self.lstAttachments:
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=os.path.basename(f))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                    msg.attach(part)
                    fil.close()
        try:
            smtpObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # NOTE: SPECIFIC TO GMAIL HERE !!!
            smtpObj.ehlo()
            smtpObj.login(self.cfg.get('email', 'user'),
                          self.cfg.get('email', 'pwd'))  # Credentials found in local file emailcredentials.ini
            smtpObj.sendmail(self.cfg.get('email', 'user'), recipientEmailAddress,
                             msg.as_string())  # this could be a list of addresses to loop over with a pause in between

            smtpObj.close()
            del smtpObj
            print('\t sent email to: %s' % recipientEmailAddress)
            time.sleep(5)  # let the server rest a bit ...
        except smtplib.SMTPAuthenticationError as ex:
            print("SMTP Authentication Error: ", ex)

        return

    def SendEmails(self):
        """
            Loop over the (potentially filtered) list of recipients, load the template, and send the email.
            Each recipient's database record is a dictionary (i.e. r is a dictionary)
        """
        for r in self.lstMailingList:  # r is a dictionary record of an individual recipient...
            html = self.htmlTemplate.render(r)
            text = self.txtTemplate.render(r)

            self.__simpleEmailMessage(r['EMAIL'], html, text)
            self.sendCount += 1

        return

    def testTemplate(self):
        """
            This method is not required but it is handy for checking your template logic.
            Comment out your call to SendEmails and use this method instead.
            AS WELL, always send yourself a TEST EMAIL through this process as an additional check!  I normally reserve one of the
            database tags to use with value TEST for test records, then create the filter to filter down to "TEST".
        """
        for r in self.lstMailingList:
            html = self.htmlTemplate.render(r)
            text = self.txtTemplate.render(r)

            print(html)
            print('------------------------')
            print(text)
            print('\n**********************\n')

            self.sendCount += 1

        return


