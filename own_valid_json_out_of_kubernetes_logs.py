import sublime
import sublime_plugin
import json

class OwnFormatOpenLensLogToValidJson(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the entire content of the view
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)

        # Split the content into lines
        lines = content.strip().split('\n')

        # Initialize a dictionary to hold the numbered JSON objects
        formatted_json = {}

        # Process each line
        for i, line in enumerate(lines, 1):
            try:
                # Parse the JSON object from the line
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