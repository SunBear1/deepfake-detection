## 1SecMail
1SecMail został wybrany ze względu na działające API.

https://www.1secmail.com/api/

### Założenia:
- Wszystko robimy całym zbiorem maili

### Lista Funkcjonalności
- INICJALIZACJA: `MAILCENTRAL = mailGenerator.OneSecMail()`
- ZMIENNA: `NUMBEROFEMAILS`

- `create_new_emails(NUMBEROFEMAILS)` - tworzy daną liczbę emaili
- `list_emails()` - zwraca listę maili
- `list_domains()` - zwraca listę domen
- `list_usernames()` - zwraca listę nazw użytkownika
- `update_messages()` - robi update wszystkich wiadomości dla danych maili
- `list_messages()` - zwraca listę maili w formacie json
- `update_attachments()` - pobiera załącznik, jeżeli istnieje w postaci `byte b'XYZ'`, jeżeli nie istnieje zostaiwa puste `""` 
```json
[{'id': 283082465, 'from': 'kuba.sachajko@gmail.com', 'subject': 'te', 'date': '2023-07-31 01:40:04'}]
```
- `list_last_messages_attachment_name()` - listuje nazwy załączników
- `list_last_messages_attachment_bytes_file()` - listuje załączniki w postaci `byte b'XYZ'`
- `list_last_messages_body()` - listuje zawartość ostatniej wiadomości dla każdego maila
- `update_last_messages()` - robi update ostatniej wiadomości w formacie json. Jeśli nie ma żadnej wiadomości wtedy zwraca `"NO DATA"` w formacie string. Dodatkowo zapisuje informacje takie jak `lastMessageBody` oraz `lastMessageAttachmentName`
```json
{'id': 283082465, 'from': 'kuba.sachajko@gmail.com', 'subject': 'te', 'date': '2023-07-31 01:40:04', 'attachments': [], 'body': '<div dir="ltr">adsasdasd</div>\n', 'textBody': 'adsasdasd\n', 'htmlBody': '<div dir="ltr">adsasdasd</div>\n'}
```
