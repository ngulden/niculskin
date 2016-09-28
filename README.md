# Theme for weewx weather station

Niculskin is a skin for the [weewx project](http://weewx.com/). It is based on two other skins:

1. [Sofaskin for Weewx](http://neoground.com/projects/weewx/)
1. [Bootstrap skin for Weewx](https://github.com/brewster76/fuzzy-archer/)

## Installation

The skins have been testet with weewx 3.5.0 and sqlite database.

### With extension package

1. Clone this repository to your machine, where weewx is installed.
1. Create an extension archive:
```bash
$ git archive master --prefix=niculskin/ | gzip > ../niculskin.tar.gz
```

3. Install it using the Weewx extension installer.
 1. If you have installed weewx yourself:
```bash
$ cd /home/weewx # or where your base install is
/home/weewx $ bin/wee_extension --install=[wherever you've put the .tar.gz archive]
```

 2. If you used the Debian installer:
```bash
$ sudo wee_extension --install=[wherever you've put the .tar.gz archive]
```

### Manual installation

In order to install this skin into your weewx installation follow these steps:

1. Clone this repository to your machine, where weewx is installed.
1. Stop the weewx service.
1. Copy the files in `bin/user` to `$WEEWX_ROOT/bin/user`.
1. Copy the directories `skins/languages` and `skins/niculskin` to `$WEEWX_ROOT/skins`.

## Configuration

No matter how you installed the skin, you should configure it afterwards to you needs. Here's how:

1. Edit your `$WEEWX_ROOT/weewx.conf` and set `skin` in the section `StdReport` so it will look something like this:
```conf
[StdReport]

    # Where the skins reside, relative to WEEWX_ROOT
    SKIN_ROOT = skins

    # Where the generated reports should go, relative to WEEWX_ROOT
    HTML_ROOT = public_html

    # The database binding indicates which data should be used in reports.
    data_binding = wx_binding

    # Each of the following subsections defines a report that will be run.

    [[StandardReport]]
        # See the customizing guide to change the units, plot types and line
        # colors, modify the fonts, display additional sensor data, and other
        # customizations. Many of those changes can be made here by overriding
        # parameters, or by modifying templates within the skin itself.

        # The StandardReport uses the 'Standard' skin, which contains the
        # images, templates and plots for the report.
        #        skin = Standard
        skin = niculskin
```
2. Edit `$WEEWX_ROOT/skins/niculskin/skin.conf` and set `Language` to your language. It should look like this:
```conf
[Language]

    #
    # Set a language below and labels will be overridden with any that are specified in
    # skins/languages/[language].conf
    #
    # Choices are: dutch, espanol, finnish, francais, italian, german

    language = german
```
3. Set the page title and page footer through the `[niculskinLabels]` section in `skins/niculskin/skin.conf`.
```conf
[niculskinLabels]
    title = "The weather, [where you are]"
    location_href = ["#" for nothing, or a hyperlink to some more information on your location]
    footer = "&copy; [who you are]"
```

## Customization

1. You may customize the labels in your language for your needs. The language labels can be found in the appropriate language file in the language skin, e.g. `$WEEWX_ROOT/skins/language/german.conf` for the German language.
1. If your language is not available, simply copy one of the present language configuration files, change to labels appropriately and refer to it in the Niculskin skin.conf at `WEEWX_ROOT/skins/niculskin/skin.conf`. If you would like to contribute your language file, please open a merge request according to the [Contribution Guideline](CONTRIBUTING.md). Your contribution is welcome.

## License

See [LICENSE](LICENSE) file.

## Credits

Thanks to Sven Reifschneider, the creator of Sofaskin. I liked his skin most as I was looking for something different in the look and feel of weewx.

And thanks to Nick Dajda. He had the history for the weather data. I'm glad I found his code.
