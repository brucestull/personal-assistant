#!/usr/bin/env python3

import markdown
import sys

name = sys.argv[1]

with open(f"{name}.md", "r") as file:
    markdown_content = file.read()

html_content = markdown.markdown(markdown_content)

with open(f"{name}.html", "w") as html_file:
    html_file.write(html_content)
