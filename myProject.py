"""
    myProject.py - an example of a "main" module that illustrates how to use the Gmailer class.

    Within we utilize the CSV example file included within this repo, but do note that the Gmailer class
    supports use of a Google Sheet as a substitute for use of a CSV file.

    Please carefully review the README.md file within this repo for further details, in addition to examining
    the gmailer.py module source.
"""
import sys, time
from gmailer import Gmailer

"""
    Filter functions can be created on the file to segment your mailing list.
    Two illustrative filter functions follow below, one without parameters and one with.
    Create these in an ad-hoc nature specific to the mailing you are sending.
"""

def Tag1Values(d, lstTagValues):
    """
        Return TRUE if you have a match within the list of tags (strings)
    """
    bool = False

    if d['TAG1'] in lstTagValues:
        bool = True

    return bool

def Python(d):
    """
        Return TRUE if the CLASS field is set to Python
    """
    bool = False

    if d['CLASS'].lower() == 'python':
        bool = True

    return bool


if __name__ == '__main__':
    print("Hello from module %s. Python version: %s" % (sys.argv[0], sys.version))
    sys.stdout.write("--------------------------------------------------------------\n")
    sys.stdout.write("Start of %s Gmailer Job: %s\n\n" % (sys.argv[0], time.strftime("%H:%M:%S", time.localtime())))

    mailing = Gmailer()

    mailing.LoadCSV('CSVasDatabase.csv')  # load a CSV file with an example set of fields
    mailing.filterList(filter(Python, mailing.lstMailingList))  # ... for this mailing, filter this list based on the Python function above
    # mailing.filterList(filter(lambda d: TagValues(d, ['NEW','OLD']), mailing.lstMailingList))  # more complex filter example

    mailing.setEmailSubject('Illustrative Email Subject Line')
    mailing.setContentTemplate('ContentTemplateExample')
    # mailing.setAttachments(lstAttachmentFileNames)   # you can provide a list file names of attachments found in the attachments folder

    # mailing.testTemplate()  # useful method for testing your template logic.  use in place of SendEmails as a check before mailing
    mailing.SendEmails()

    sys.stdout.write("\n\nEnd of %s Gmailer Job: %s. %5d emails sent\n" % ( \
    sys.argv[0], time.strftime("%H:%M:%S", time.localtime()), mailing.sendCount))
    sys.stdout.write("-------------------------------------------------------------\n")

    del mailing
