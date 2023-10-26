""" 
1 SEC MAIL ENDPOINTS
"""
NEW_EMAILS = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count="
CHECK_INBOXES = "https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}"
CHECK_EXACT_MESSAGES = "https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}"
ATTACHMENT_DOWNLOAD = "https://www.1secmail.com/api/v1/?action=download&login={}&domain={}&id={}&file={}"