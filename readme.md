# Fidem Mobile Icons

Designed by [@loizo](http://lloizo.com).

They are free to use and licensed under [MIT](http://opensource.org/licenses/MIT).


## Getting Started

 1. Download and extract the font pack
 2. Copy the `fidemicons.css` to your project
 3. Copy the `fonts` folder to your project
 4. Ensure the font urls within `fidemicons.css` properly reference the `fonts` path within your project.
 5. Include a reference to the `fidemicons.css` file from every webpage you need to use it.

Or install with [component](https://github.com/component/component):

    $ component install fidemapps/fidemicons
    
Or perhaps you're known to use [bower](http://bower.io/)?
   
    $ bower install fidemicons


## HTML Example

Once you've copied the desired icon's CSS classname, simply add the `icon` and icon's classname, such as `fidem-home` to an HTML element.

    <i class="icon fidem-home"></i>


## Build Instructions

This repo already comes with all the files built and ready to go, but can also build the fonts from the source. Requires Python, FontForge and Sass:

1) Install FontForge, which is the program that creates the font files from the SVG files:

    $ brew install fontforge ttfautohint

2) Install [Sass](http://sass-lang.com/)

    $ gem install sass

3) Add or subtract files from the `src/` folder you'd like to be apart of the font files.

4) Modify any settings in the `builder/manifest.json` file. You can change the name of the font-family and CSS classname prefix.

5) Run the build command:

    python ./builder/generate.py


## License

Fidem Mobile Icons is licensed under the [MIT license](http://opensource.org/licenses/MIT).
