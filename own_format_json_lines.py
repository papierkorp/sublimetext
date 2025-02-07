import sublime
import sublime_plugin
import json

class OwnFormatJsonLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get all lines in the file
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        lines = content.split('\n')
        formatted_lines = []

        # Process each line
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                try:
                    # Parse and format JSON for each line
                    json_obj = json.loads(line)
                    formatted_json = json.dumps(json_obj, indent=2)
                    formatted_lines.append(formatted_json)
                except json.JSONDecodeError as e:
                    # Keep original line if it's not valid JSON
                    print(f"Error processing line: {e}")
                    formatted_lines.append(line)

        # Join the formatted lines with double newlines for readability
        final_content = '\n\n'.join(formatted_lines)
        
        # Replace the entire content
        self.view.replace(edit, region, final_content)