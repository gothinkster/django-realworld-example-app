from __future__ import unicode_literals

import markdown


def parse(text):

    # First run through the Markdown parser
    text = markdown.markdown(text, extensions=["extra"], safe_mode=False)

    # Sanitize using html5lib
    # bits = []
    # parser = html5parser.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    # for token in parser.parseFragment(text).childNodes:
    #     bits.append(token.toxml())
    # return "".join(bits)
    return text
