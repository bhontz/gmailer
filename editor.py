"""
    editor.py - provides an HTML wysiwyg editor that will support creation of HTML and TXT templates
    within this project's template folder.

    Run this module first (i.e. python editor.py) to create content that you can then mail with your myProject.py

    NOTE: you must have a local webserver (i.e. "localhost") in order to use this module!  The wysiwyg editor will
    appear in your browser after you visit the URL http://127.0.0.1/8080 (or locahost:8080)

    Once you have created your content, you can just "Ctrl+C" to close the webserver created by this module
"""
import os, sys, html2text
from flask import Flask, request, render_template

app = Flask(__name__)

def ProcessContent(d):
    """
        Save HTML and TXT versions of the HTML wysiwyg content into the templates folder of this project
    """
    header = \
"""<!DOCTYPE html>
<html lang = "en">
<head>
  <meta charset="utf-8">                        
  <title>Email Content from GMAILER</title>
</head>
<body style="font-family: {}">
""".format(d["bodyfont"])

    footer = """
</body>
</html>
"""
    # TODO: do something if you're about to overwrite an existing file ...
    #
    if "filename" in d.keys():
        try:
            fpHTML = open("templates/{}.html".format(d["filename"]), "wt")
        except IOError as detail:
            print("unable to open file %s for WRITE - details:%s" % ("{}.html".format(d["filename"]), detail))
            sys.exit(1)

        try:
            fpTXT = open("templates/{}.txt".format(d["filename"]), "wt")
        except IOError as detail:
            print("unable to open file %s for WRITE - details:%s" % ("{}.txt".format(d["filename"]), detail))
            sys.exit(1)

        strContent = header + d["editor"] + footer
        fpHTML.write(strContent)
        fpHTML.close()
        fpTXT.write(html2text.html2text(strContent))
        fpTXT.close()

        del strContent
        del fpHTML
        del fpTXT

    return

@app.route('/', methods=["GET", "POST"])
def editor():
    if request.method == "POST":
        ProcessContent(request.form)

    return render_template("wysiwygEditor.html")   # or use index.html


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='127.0.0.1')
