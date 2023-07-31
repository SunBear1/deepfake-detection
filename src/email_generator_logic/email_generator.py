import requests
import email_endpoints

class OneSecMail():
    def __init__(self):
        self.session = requests.session()
        self.mails = []
        self.domains = []
        self.usernames = []
        self.messages = []
        self.lastMessages = []
        self.lastMessagesBody = []
        self.lastMessagesAttachment = []
        self.lastMessagesAttachmentName = []

    def create_new_emails(self, numberOfEmails):
        self.mails = self.session.get(email_endpoints.NEW_EMAILS + str(numberOfEmails)).json()        
        for email in self.mails:
            self.messages.append([])
            self.lastMessagesAttachment.append("")
            self.lastMessagesAttachmentName.append("")
            self.lastMessages.append("")
            self.lastMessagesBody.append("")
            self.usernames.append(email.split("@")[0])
            self.domains.append(email.split("@")[1])

    def update_messages(self):
        for idx in range(len(self.mails)):
            self.messages[idx] = self.session.get(email_endpoints.CHECK_INBOXES.format(self.usernames[idx], self.domains[idx])).json()

    def update_last_messages(self):
        for idx in range(len(self.mails)):
            try:
                self.lastMessages[idx] = self.session.get(email_endpoints.CHECK_EXACT_MESSAGES.format(self.usernames[idx], self.domains[idx], self.messages[idx][-1]['id'])).json()
                self.lastMessagesBody[idx]= self.lastMessages[idx]['textBody']
                try:
                    self.lastMessagesAttachmentName[idx]= self.lastMessages[idx]['attachments']['filename']
                except:
                    pass
            except:
                self.lastMessages[idx] = "NO DATA"

    def update_attachments(self):
        for idx in range(len(self.mails)):
            try:
                self.lastMessagesAttachment[idx] = self.session.get(email_endpoints.ATTACHMENT_DOWNLOAD.format(self.usernames[idx], self.domains[idx], self.messages[idx][-1]['id'], self.lastMessagesAttachmentName))
            except:
                pass

    def list_last_messages_attachment_bytes_file(self):
        return self.lastMessagesAttachment

    def list_last_messages_attachment_name(self):
        return self.lastMessagesAttachmentName

    def list_last_messages_body(self):
        return self.lastMessages

    def list_last_messages(self):
        return self.lastMessages

    def list_messages(self):
        return self.messages

    def list_emails(self):
        return self.mails
    
    def list_domains(self):
        return self.domains
    
    def list_usernames(self):
        return self.usernames