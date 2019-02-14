# ezmail

Easily customise emails for each recipient. Made for non-programmers.

## Requirements

- Python 3

## Running the program

```
python send.py config.yaml
```

## Customisation

You only have to modify three simple parts:

1. HTML file for the email body template.
2. CSV file for the contact list and their customised values.
3. YAML file for your smtp server details and other metadata.

### HTML Template

An example of a simple HTML template is:

```
Hello ${name},
<br><br>
Congratulations! You won a ${medal} medal!
```

where `name` and `medal` will be substituted by the values in the csv file.

### CSV File

The CSV file should at least contain the emails of the recipients. You can add other columns for names, age etc.

```
name,email,medal
alice,alice@example.com,Gold
bob,bob@example.com,Silver
```

The `name` and `medal` column will be substituted into the HTML placeholder.

### YAML File

```
server:
  host: smtp.gmail.com
  port: 587
  username: your_email@example.com
  password: randompassword
data:
  contacts: contacts.csv
  template: template.html
email-data:
  from: your_email@example.com
  cc: your_email@example.com
  subject: Hello, World!
  attachments:
    - file1.txt
    - file2.txt
    - file3.txt
```
