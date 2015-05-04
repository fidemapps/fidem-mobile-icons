from subprocess import call
import os
import json


BUILDER_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(BUILDER_PATH, '..')
FONTS_FOLDER_PATH = os.path.join(ROOT_PATH, 'fonts')
CSS_FOLDER_PATH = os.path.join(ROOT_PATH, 'css')
SCSS_FOLDER_PATH = os.path.join(ROOT_PATH, 'scss')
LESS_FOLDER_PATH = os.path.join(ROOT_PATH, 'less')


def main():
  generate_font_files()

  data = get_build_data()

  rename_svg_glyph_names(data)
  generate_scss(data)
  generate_less(data)
  generate_cheatsheet(data)
  generate_component_json(data)
  generate_composer_json(data)
  generate_bower_json(data)


def generate_font_files():
  print "Generate Fonts"
  cmd = "fontforge -script %s/scripts/generate_font.py" % (BUILDER_PATH)
  call(cmd, shell=True)


def rename_svg_glyph_names(data):
  # hacky and slow (but safe) way to rename glyph-name attributes
  svg_path = os.path.join(FONTS_FOLDER_PATH, 'fidemicons.svg')
  svg_file = open(svg_path, 'r+')
  svg_text = svg_file.read()
  svg_file.seek(0)

  for ionicon in data['icons']:
    # uniF2CA
    org_name = 'uni%s' % (ionicon['code'].replace('0x', '').upper())
    ion_name = 'fidemicons-%s' % (ionicon['name'])
    svg_text = svg_text.replace(org_name, ion_name)

  svg_file.write(svg_text)
  svg_file.close()


def generate_less(data):
  print "Generate LESS"
  font_name = data['name']
  font_version = data['version']
  css_prefix = data['prefix']
  variables_file_path = os.path.join(LESS_FOLDER_PATH, '_ionicons-variables.less')
  icons_file_path = os.path.join(LESS_FOLDER_PATH, '_ionicons-icons.less')

  d = []
  d.append('/*!');
  d.append('Fidemicons, v%s' % (font_version) );
  d.append('Created by Sebastien Guimont for the Fidem 360 Inc., http://fidem360.com/');
  d.append('MIT License: https://github.com/fidemapps/fidem-mobile-icons');
  d.append('*/');
  d.append('// Fidemicons Variables')
  d.append('// --------------------------\n')
  d.append('@fidemicons-font-path: "../fonts";')
  d.append('@fidemicons-font-file-name: "fidemicons";')
  d.append('@fidemicons-font-family: "%s";' % (font_name) )
  d.append('@fidemicons-version: "%s";' % (font_version) )
  d.append('@fidemicons-prefix: %s;' % (css_prefix) )
  d.append('')
  for ionicon in data['icons']:
    chr_code = ionicon['code'].replace('0x', '\\')
    d.append('@fidemicons-var-%s: "%s";' % (ionicon['name'], chr_code) )
  f = open(variables_file_path, 'w')
  f.write( '\n'.join(d) )
  f.close()

  d = []
  d.append('// Fidemicons Icons')
  d.append('// --------------------------\n')

  group = [ '.%s' % (data['name'].lower()) ]
  for ionicon in data['icons']:
    group.append('.@{fidemicons-prefix}%s:before' % (ionicon['name']) )

  d.append( ',\n'.join(group) )

  d.append('{')
  d.append('  &:extend(.ion);')
  d.append('}')

  for ionicon in data['icons']:
    chr_code = ionicon['code'].replace('0x', '\\')
    d.append('.@{fidemicons-prefix}%s:before { content: @fidemicons-var-%s; }' % (ionicon['name'], ionicon['name']) )

  f = open(icons_file_path, 'w')
  f.write( '\n'.join(d) )
  f.close()


def generate_scss(data):
  print "Generate SCSS"
  font_name = data['name']
  font_version = data['version']
  css_prefix = data['prefix']
  variables_file_path = os.path.join(SCSS_FOLDER_PATH, '_ionicons-variables.scss')
  icons_file_path = os.path.join(SCSS_FOLDER_PATH, '_ionicons-icons.scss')

  d = []
  d.append('// Fidemicons Variables')
  d.append('// --------------------------\n')
  d.append('$fidemicons-font-path: "../fonts" !default;')
  d.append('$fidemicons-font-file-name: "fidemicons" !default;')
  d.append('$fidemicons-font-family: "%s" !default;' % (font_name) )
  d.append('$fidemicons-version: "%s" !default;' % (font_version) )
  d.append('$fidemicons-prefix: %s !default;' % (css_prefix) )
  d.append('')
  for ionicon in data['icons']:
    chr_code = ionicon['code'].replace('0x', '\\')
    d.append('$fidemicons-var-%s: "%s";' % (ionicon['name'], chr_code) )
  f = open(variables_file_path, 'w')
  f.write( '\n'.join(d) )
  f.close()

  d = []
  d.append('// Fidemicons Icons')
  d.append('// --------------------------\n')

  group = [ '.%s' % (data['name'].lower()) ]
  for ionicon in data['icons']:
    group.append('.#{$fidemicons-prefix}%s:before' % (ionicon['name']) )

  d.append( ',\n'.join(group) )

  d.append('{')
  d.append('  @extend .ion;')
  d.append('}')

  for ionicon in data['icons']:
    chr_code = ionicon['code'].replace('0x', '\\')
    d.append('.#{$fidemicons-prefix}%s:before { content: $fidemicons-var-%s; }' % (ionicon['name'], ionicon['name']) )

  f = open(icons_file_path, 'w')
  f.write( '\n'.join(d) )
  f.close()

  generate_css_from_scss(data)


def generate_css_from_scss(data):
  print "Generate CSS From SCSS"

  scss_file_path = os.path.join(SCSS_FOLDER_PATH, 'fidemicons.scss')
  css_file_path = os.path.join(CSS_FOLDER_PATH, 'fidemicons.css')
  css_min_file_path = os.path.join(CSS_FOLDER_PATH, 'fidemicons.min.css')

  cmd = "sass %s %s --style compact" % (scss_file_path, css_file_path)
  call(cmd, shell=True)

  print "Generate Minified CSS From SCSS"
  cmd = "sass %s %s --style compressed" % (scss_file_path, css_min_file_path)
  call(cmd, shell=True)


def generate_cheatsheet(data):
  print "Generate Cheatsheet"

  cheatsheet_file_path = os.path.join(ROOT_PATH, 'cheatsheet.html')
  template_path = os.path.join(BUILDER_PATH, 'cheatsheet', 'template.html')
  icon_row_path = os.path.join(BUILDER_PATH, 'cheatsheet', 'icon-row.html')

  f = open(template_path, 'r')
  template_html = f.read()
  f.close()

  f = open(icon_row_path, 'r')
  icon_row_template = f.read()
  f.close()

  content = []

  for ionicon in data['icons']:
    css_code = ionicon['code'].replace('0x', '\\')
    escaped_html_code = ionicon['code'].replace('0x', '&amp;#x') + ';'
    html_code = ionicon['code'].replace('0x', '&#x') + ';'
    item_row = icon_row_template

    item_row = item_row.replace('{{name}}', ionicon['name'])
    item_row = item_row.replace('{{prefix}}', data['prefix'])
    item_row = item_row.replace('{{css_code}}', css_code)
    item_row = item_row.replace('{{escaped_html_code}}', escaped_html_code)
    item_row = item_row.replace('{{html_code}}', html_code)

    content.append(item_row)

  template_html = template_html.replace("{{font_file_name}}", "fidemicons")
  template_html = template_html.replace("{{font_name}}", data["name"])
  template_html = template_html.replace("{{font_version}}", data["version"])
  template_html = template_html.replace("{{icon_count}}", str(len(data["icons"])) )
  template_html = template_html.replace("{{content}}", '\n'.join(content) )

  f = open(cheatsheet_file_path, 'w')
  f.write(template_html)
  f.close()


def generate_component_json(data):
  print "Generate component.json"
  d = {
    "name": data['name'],
    "repo": "fidemapps/fidem-mobile-icons",
    "description": "The premium icon font for Fidem Mobile 360.",
    "version": data['version'],
    "keywords": [],
    "dependencies": {},
    "development": {},
    "license": "MIT",
    "styles": [
      "css/%s.css" % (data['name'].lower())
    ],
    "fonts": [
      "fonts/%s.eot" % (data['name'].lower()),
      "fonts/%s.svg" % (data['name'].lower()),
      "fonts/%s.ttf" % (data['name'].lower()),
      "fonts/%s.woff" % (data['name'].lower())
    ]
  }
  txt = json.dumps(d, indent=4, separators=(',', ': '))

  component_file_path = os.path.join(ROOT_PATH, 'component.json')
  f = open(component_file_path, 'w')
  f.write(txt)
  f.close()


def generate_composer_json(data):
  print "Generate composer.json"
  d = {
    "name": "fidemapps/fidem-mobile-icons",
    "description": "The premium icon font for Fidem Mobile.",
    "keywords": [ "fonts", "icon font", "icons", "fidem", "web font"],
    "homepage": "http://fidem360.com/",
    "authors": [
      {
        "name": "Sebastien Guimont",
        "email": "sguimont@fidem360.com",
        "role": "Developer"
      },
    ],
    "extra": {},
    "license": [ "MIT" ]
  }
  txt = json.dumps(d, indent=4, separators=(',', ': '))

  composer_file_path = os.path.join(ROOT_PATH, 'composer.json')
  f = open(composer_file_path, 'w')
  f.write(txt)
  f.close()


def generate_bower_json(data):
  print "Generate bower.json"
  d = {
    "name": data['name'],
    "version": data['version'],
    "homepage": "https://github.com/fidemapps/fidem-mobile-icons",
    "authors": [
      "Sebastien Guimont <sguimont@fidem360.com>"
    ],
    "description": "Fidemicons - free and beautiful icons from the creators of Fidem 360",
    "main": [
      "css/%s.css" % (data['name'].lower()),
      "fonts/*"
    ],
    "keywords": [ "fonts", "icon font", "icons", "fidem", "web font"],
    "license": "MIT",
    "ignore": [
      "**/.*",
      "builder",
      "node_modules",
      "bower_components",
      "test",
      "tests"
    ]
  }
  txt = json.dumps(d, indent=4, separators=(',', ': '))

  bower_file_path = os.path.join(ROOT_PATH, 'bower.json')
  f = open(bower_file_path, 'w')
  f.write(txt)
  f.close()


def get_build_data():
  build_data_path = os.path.join(BUILDER_PATH, 'build_data.json')
  f = open(build_data_path, 'r')
  data = json.loads(f.read())
  f.close()
  return data


if __name__ == "__main__":
  main()
