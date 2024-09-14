import email
from email import policy
from email.parser import BytesParser
from markdownify import markdownify as md

def convert_eml_to_md(input_file, output_file):
    with open(input_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    # Extract email headers
    from_ = msg['From']
    to = msg['To']
    cc = msg['Cc']
    subject = msg['Subject']
    date = msg['Date']
    message_id = msg['Message-ID']
    reply_to = msg['Reply-To']
    in_reply_to = msg['In-Reply-To']
    
    # Function to extract and convert email parts
    def extract_body(part):
        text_plain = ''
        text_html = ''
        if part.is_multipart():
            for subpart in part.get_payload():
                if subpart.get_content_type() == 'text/plain':
                    text_plain += subpart.get_payload(decode=True).decode(subpart.get_content_charset())
                elif subpart.get_content_type() == 'text/html':
                    text_html += md(subpart.get_payload(decode=True).decode(subpart.get_content_charset()))
        else:
            if part.get_content_type() == 'text/plain':
                text_plain = part.get_payload(decode=True).decode(part.get_content_charset())
            elif part.get_content_type() == 'text/html':
                text_html = md(part.get_payload(decode=True).decode(part.get_content_charset()))
        
        return text_plain if text_plain else text_html
    
    # Extract the email body
    body = extract_body(msg)
    
    # Write to Markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {subject}\n\n")
        f.write(f"**From:** {from_}\n\n")
        f.write(f"**To:** {to}\n\n")
        if cc:
            f.write(f"**CC:** {cc}\n\n")
        f.write(f"**Date:** {date}\n\n")
        f.write(f"**Message-ID:** {message_id}\n\n")
        if reply_to:
            f.write(f"**Reply-To:** {reply_to}\n\n")
        if in_reply_to:
            f.write(f"**In-Reply-To:** {in_reply_to}\n\n")
        f.write(f"---\n\n")
        f.write(body)


# Example usage
input_file = 'C:\\Users\\Nitin\\Downloads\\JustThinkingAboutYou.eml'
output_file = 'C:\\Users\\Nitin\\Downloads\\output.md'
convert_eml_to_md(input_file, output_file)
