'''
    def check_unread_emails_with_senders(self):
        # Load token.json or however you're authenticating
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            return "You have no unread emails."

        senders = []
        for message in messages[:5]:  # Limit to 5 emails for sanity
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['From']).execute()
            headers = msg['payload']['headers']
            for header in headers:
                if header['name'] == 'From':
                    senders.append(header['value'])
                    break

        return f"You have {len(messages)} unread emails. The first five are from: " + ", ".join(senders) 
'''