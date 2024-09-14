import email
from email import policy
from email.parser import BytesParser
from markdownify import markdownify as md

def convert_eml_to_md(input_file, output_file):
    with open(input_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    # Extract the email body
    body = msg.get_body(preferencelist=('plain', 'html')).get_content()
    
    # Convert HTML to Markdown if necessary
    if msg.get_body(preferencelist=('html')):
        body = md(body)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(body)

# Example usage
input_file = 'C:\\Users\\Nitin\\Downloads\\JustThinkingAboutYou.eml'
output_file = 'C:\\Users\\Nitin\\Downloads\\output.md'
convert_eml_to_md(input_file, output_file)
