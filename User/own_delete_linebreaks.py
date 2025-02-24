import sublime
import sublime_plugin

class OwnDeleteLinebreaksCommand(sublime_plugin.TextCommand):
    def run(self, edit, format_json=False):
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        content = content.replace('\n', '')
        self.view.replace(edit, region, content)

        if format_json:
            self.view.run_command("pretty_json")
