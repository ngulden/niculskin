# Theme for weewx weather station

Niculskin is a skin for the [weewx project](http://weewx.com/). It is based on two other skins:

1. [Sofaskin for Weewx](http://neoground.com/projects/weewx/)
1. [Bootstrap skin for Weewx](https://github.com/brewster76/fuzzy-archer/)

## Installation

The skins have been testet with weewx 3.5.0 and sqlite database.

In order to install this skin into your weewx installation follow these steps:

1. Clone this repository to your machine, where weewx is installed.
1. Stop the weewx service.
1. Copy the files in `bin/user` to `$WEEWX_ROOT/bin/user`.
1. Copy the directory `skins/languages` to `$WEEWX_ROOT/skins`.
1. Copy the directory `skins/niculskin` to `$WEEWX_ROOT/skins`.
1. Edit your `$WEEWX_ROOT/weewx.conf` and set `skin` in the section `StdReport` and subsection `StandardReport` niculskin.
1. Edit `$WEEWX_ROOT/skins/niculskin/skin.conf` and set `Language.language` to your language.

## License

See [LICENSE](LICENSE) file.

## Credits

Thanks to Sven Reifschneider, the creator of Sofaskin. I liked his skin most as I was looking for something different in the look and feel of weewx.

And thanks to Nick Dajda. He had the history for the weather data. I'm glad I found his code.
