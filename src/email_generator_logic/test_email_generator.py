import email_generator


NUMBEROFEMAILS = 10
MAILCENTRAL = email_generator.OneSecMail()


MAILCENTRAL.create_new_emails(NUMBEROFEMAILS)

for email in MAILCENTRAL.list_emails():
    print(email)

for username in MAILCENTRAL.list_usernames():
    print(username)

for domain in MAILCENTRAL.list_domains():
    print(domain)

MAILCENTRAL.update_messages()

for message in MAILCENTRAL.list_messages():
    print(message)

MAILCENTRAL.update_last_messages()

for lastMessage in MAILCENTRAL.list_last_messages():
    print(lastMessage)

