## Gmailer - GMAIL templated bulk mailer

Use your GMAIL account to send templated bulk emails to recipients.  Note that GMAIL has a stated limitation of 500 email sends from an account per day.

This project uses the jinja2 templating engine which supports the "double mustache" syntax for variable substitution, as well as conditionals and looping.  Refer to the doc at https://jinja.palletsprojects.com/en/2.11.x/templates/ and as well the example provided within the templates folder of this repo.

You can store your mailing list and associated segmentation and/or informational fields in either a CSV file or a Google Sheet.  If you are using a CSV file, the CSV file needs to be in the same folder as your main module.
If you plan to use Google Sheets, you must first create a Google OAuth credentials file; that process is documented here: https://datasheets.readthedocs.io/en/latest/getting_oauth_credentials.html

The outcome of the OAuth process is the creation of two JSON files with filenames *client_secrets.json* and *service_key.json* which you save on your computer.  Additionally, pay particular attention to the SHARING of the sheets, as you really need to share each newly created sheet WITH YOURSELF to begin using it (this initially resulted in some serious head scratching on my part).

The email process embodied within supports recipients that can receive only plain text as well as those that can receive HTML emails.  You are required to create both a plain text and a html version of your email content template to support this.

File attachments can be added. Attachments should be placed within the attachments folder of this directory structure, and the appropriate method (as illustrated in the example myProject.py) must be called. 

#### IMPORTANT: GMAIL SETUP

Never expose email addresses and in particularly passwords within your code (duh)!

This process stores the sender's GMAIL account in a INI file named **emailcredentials.ini** which lives within the same folder as your main module, and is obviously not included within this repo!  

**You'll need to create this file!**  The file structure is illustrated here:

```
[email]
user = sender@gmail.com
pwd = sendersSecretGmailPwd
```
Additionally, you must configure your GMAIL account to support SMTP sending.  This involves turning on "less secure app access".  Please note that Google will turn this off automagically if you are not using this email process for awhile (not exactly sure how long, maybe 30 days?) meaning you might have to reset this setting every once and awhile.

Here's the process:

1) From your GMAIL account, click on the "hamburger grid" near your profile picture and choose Account.
2) Select Security from the left side menu.
3) Scroll down on the Security page until you see the section for Less Secure App Access.  Turn this feature ON.

If you have this Less Secure App Access "off" (i.e. the default), you'll receive an error like this:

SMTP Authentication Error:  (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials

... when running this process.


##### Version History
This repo was originally created Sept, 2020 as an illustration for [GirlsCodeIt](https://www.girlscodeit.org).

##### ACTIVE To-Dos    
None at this time.

##### COMPLETED To-Dos    
None at this time.