"""
Usage: cli2web.py [options] [script]
cli2web creates a web interface for a given Python script that uses argparse
for the CLI.

Examples:
cli2web.py my_script.py #creates web interface for my_script.py

Options:
I haven't decided on these yet
"""

import os
import pprint
import argparse
import imp
from bottle import template, get, post, run, request


#ArgumentParser description. The object is kept global so that it remains
#accessible for import and therefore cli2web can work from a self-generated
#web interaface.
desc = ("Creates a web interface for a given Python script that uses "
        "argparse for CLI.")
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('script', type=file)

#Template for the web interface
html = """
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Cli2Web</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="Generated by Cli2Web">
            <meta name="author" content="alixedi">
          </head>
          <body>
            <h1>{{ prog }}</h1>
            % if description:
                <p>{{ description }}</p>
            % end
            <hr>
            <form method="POST" action=".">
                % for group in _action_groups:
                    <legend>{{ group.title }}</legend>
                    % for action in group._group_actions:
                        % import argparse
                        % if not type(action) is argparse._HelpAction:
                            {{ action.dest }}: \ 
                            <input type="text" \ 
                                   {{ 'required' if action.required else '' }} \
                                   id = '{{ action.dest }}' name='{{ action.dest }}'
                                   value={{ action.default if hasattr(action.default, '__dict__') else '' }}>
                            <br>
                            {{ action.help }}<br>
                        % end
                    % end
                % end
                <input type=submit value="Go" />
            </form>
            % if epilog:
                <p>{{ epilog }}</p>
            % end
          </body>
        </html>
    """

context = {}

@get('/')
def index():
    return template(html, **context)

@post('/')
def form():
    print request.forms.get('integers') 
    return 'coming soon!'
    # Now we can access the post data, we just need to plug it into the cli
    # script, run the thing and return results!

def main():
    args = parser.parse_args()
    root, ext = os.path.splitext(args.script.name)
    if not ext == '.py':
        parser.error('Not a Python script!')
    module = imp.load_source('', args.script.name)
    for sym in dir(module):
        obj = getattr(module, sym)
        if isinstance(obj, argparse.ArgumentParser):
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(obj.__dict__)
            #print template(html, **obj.__dict__)
            global context
            context = obj.__dict__
            print template(html, **context)
    run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()
