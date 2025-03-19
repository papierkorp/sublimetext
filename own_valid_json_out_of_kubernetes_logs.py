import sublime
import sublime_plugin
import json
import re

class OwnFormatOpenLensLogToValidJson(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the entire content of the view
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)

        # Split the content into lines
        lines = content.strip().split('\n')

        # Initialize a dictionary to hold the numbered JSON objects
        formatted_json = {}

        # Regular expression to match ISO date format at the beginning of a line
        date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+\+\d{2}:\d{2})\s+(.*)')

        # Process each line
        for i, line in enumerate(lines, 1):
            try:
                # Check if line starts with a date
                date_match = date_pattern.match(line)

                if date_match:
                    # Extract the date and JSON content
                    date_str = date_match.group(1)
                    json_content = date_match.group(2)
                    # Parse the JSON object from the line
                    json_obj = json.loads(json_content.strip())
                    # Use the date as the key
                    formatted_json[date_str] = json_obj
                else:
                    # Regular line without date prefix
                    json_obj = json.loads(line.strip())
                    # Add it to our formatted JSON with a numbered key
                    formatted_json[str(i)] = json_obj
            except json.JSONDecodeError as e:
                # If a line isn't valid JSON, show an error message
                sublime.error_message(f"Error parsing line {i}: {e}")
                return

        # Convert the formatted JSON back to a string with pretty printing
        formatted_content = json.dumps(formatted_json, indent=4)

        # Replace the content of the view with the formatted JSON
        self.view.replace(edit, region, formatted_content)

        # Set syntax to JSON
        self.view.set_syntax_file("Packages/JavaScript/JSON.sublime-syntax")

        # Run the pretty_json command for additional formatting
        self.view.run_command("pretty_json")

        # Show a success message
        sublime.status_message("JSON formatted successfully")