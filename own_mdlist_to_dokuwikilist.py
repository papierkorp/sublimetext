import sublime
import sublime_plugin
import re


class OwnMarkdownToDokuwikiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        entire_region = sublime.Region(0, self.view.size())
        content = self.view.substr(entire_region)

        lines = content.split('\n')
        in_code_block = False
        processed_lines = []

        content_patterns = [
            (r'^- ', '  * '),
            (r'^  - ', '    * '),
            (r'^    - ', '      * '),
            (r'^      - ', '        * '),
            (r'^        - ', '          * '),
            (r'^          - ', '            * '),
            (r'^            - ', '              * '),
            (r'^\d+\. ', '  - '),  # numbered lists
            (r'^```(\w+)', r'<sxh \1>'),  # capture whatever language is behind the 3 backticks
            (r'```', '</sxh>'),
            (r'^##### (.+)$', r'== \1 =='),
            (r'^#### (.+)$', r'=== \1 ==='),
            (r'^### (.+)$', r'==== \1 ===='),
            (r'^## (.+)$', r'===== \1 ====='),
            (r'^# (.+)$', r'====== \1 ======'),
            (r'`', "''"),
            (r'https://\S+', r'[[\g<0>]]')  # capture links
        ]

        for line in lines:
            if line.strip().startswith('```'):
                if not in_code_block:
                    match = re.match(r'^```(\w+)', line.strip())
                    if match:
                        processed_lines.append(f'<sxh {match.group(1)}>')
                    else:
                        processed_lines.append('<sxh>')
                    in_code_block = True
                else:
                    processed_lines.append('</sxh>')
                    in_code_block = False
            else:
                if in_code_block:
                    processed_lines.append(line)
                else:
                    modified_line = line
                    for pattern, replacement in content_patterns:
                        modified_line = re.sub(pattern, replacement, modified_line)
                    processed_lines.append(modified_line)

        modified_content = '\n'.join(processed_lines)

        if modified_content != content:
            self.view.replace(edit, entire_region, modified_content)
            sublime.status_message("Converted Markdown to DokuWiki")
        else:
            sublime.status_message("No patterns found to convert")
