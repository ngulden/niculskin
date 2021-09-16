#
# Copyright (c) 2013-2016  Nick Dajda <nick.dajda@gmail.com>
#
# Distributed under the terms of the GNU GENERAL PUBLIC LICENSE
#
"""Extends the Cheetah generator search list to add html historic data tables in a nice colour scheme.

Tested on Weewx release 3.0.1.
Works with all databases.
Observes the units of measure and display formats specified in skin.conf.

WILL NOT WORK with Weewx prior to release 3.0.
  -- Use this version for 2.4 - 2.7:  https://github.com/brewster76/fuzzy-archer/releases/tag/v2.0

To use it, add this generator to search_list_extensions in skin.conf:

[CheetahGenerator]
    search_list_extensions = user.historygenerator.MyXSearch

1) The $alltime tag:

Allows tags such as $alltime.outTemp.max for the all-time max
temperature, or $seven_day.rain.sum for the total rainfall in the last
seven days.

2) Nice colourful tables summarising history data by month and year:

Adding the section below to your skins.conf file will create these new tags:
   $min_temp_table
   $max_temp_table
   $avg_temp_table
   $rain_table

############################################################################################
#
# HTML month/year colour coded summary table generator
#
[HistoryReport]
    # minvalues, maxvalues and colours should contain the same number of elements.
    #
    # For example,  the [min_temp] example below, if the minimum temperature measured in
    # a month is between -50 and -10 (degC) then the cell will be shaded in html colour code #0029E5.
    #

    # Default is temperature scale
    minvalues = -50, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35
    maxvalues =  -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 60
    colours =   "#0029E5", "#0186E7", "#02E3EA", "#04EC97", "#05EF3D2, "#2BF207", "#8AF408", "#E9F70A", "#F9A90B", "#FC4D0D", "#FF0F2D"
    monthnames = Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec

    # The Raspberry Pi typically takes 15+ seconds to calculate all the summaries with a few years of weather date.
    # refresh_interval is how often in minutes the tables are calculated.
    refresh_interval = 60

    [[min_temp]]                           # Create a new Cheetah tag which will have a _table suffix: $min_temp_table
        obs_type = outTemp                 # obs_type can be any weewx observation, e.g. outTemp, barometer, wind, ...
        aggregate_type = min               # Any of these: 'sum', 'count', 'avg', 'max', 'min'

    [[max_temp]]
        obs_type = outTemp
        aggregate_type = max

    [[avg_temp]]
        obs_type = outTemp
        aggregate_type = avg

    [[rain]]
        obs_type = rain
        aggregate_type = sum

        # Override default temperature colour scheme with rain specific scale
        minvalues = 0, 25, 50, 75, 100, 150
        maxvalues = 25, 50, 75, 100, 150, 1000
        colours = "#E0F8E0", "#A9F5A9", "#58FA58", "#2EFE2E", "#01DF01", "#01DF01"
"""

from datetime import datetime
import time
import syslog
import os.path

from weewx.cheetahgenerator import SearchList
from weewx.tags import TimespanBinder
import weeutil.weeutil

class MyXSearch(SearchList):
    def __init__(self, generator):
        SearchList.__init__(self, generator)

        self.table_dict = generator.skin_dict['HistoryReport']

        # Calculate the tables once every refresh_interval mins
        self.refresh_interval = int(self.table_dict.get('refresh_interval', 5))
        self.cache_time = 0

        self.search_list_extension = {}

        # Make bootstrap specific labels in config file available to
        if 'niculskinLabels' in generator.skin_dict:
            self.search_list_extension['niculskinLabels'] = generator.skin_dict['niculskinLabels']
        else:
            syslog.syslog(syslog.LOG_DEBUG, "%s: No bootstrap specific labels found" % os.path.basename(__file__))

        # Make observation labels available to templates
        if 'Labels' in generator.skin_dict:
            self.search_list_extension['Labels'] = generator.skin_dict['Labels']
        else:
            syslog.syslog(syslog.LOG_DEBUG, "%s: No observation labels found" % os.path.basename(__file__))

    def get_extension_list(self, valid_timespan, db_lookup):
        """For weewx V3.x extensions. Should return a list
        of objects whose attributes or keys define the extension.

        valid_timespan:  An instance of weeutil.weeutil.TimeSpan. This will hold the
        start and stop times of the domain of valid times.

        db_lookup: A function with call signature db_lookup(data_binding), which
        returns a database manager and where data_binding is an optional binding
        name. If not given, then a default binding will be used.
        """

        # Time to recalculate?
        if (time.time() - (self.refresh_interval * 60)) > self.cache_time:
            self.cache_time = time.time()

            #
            # The all time statistics
            #

            # If this generator has been called in the [SummaryByMonth] or [SummaryByYear]
            # section in skin.conf then valid_timespan won't contain enough history data for
            # the colourful summary tables.
            alltime_timespan = weeutil.weeutil.TimeSpan(db_lookup().first_timestamp, db_lookup().last_timestamp)


            # First, get a TimeSpanStats object for all time. This one is easy
            # because the object valid_timespan already holds all valid times to be
            # used in the report.
            all_stats = TimespanBinder(alltime_timespan, db_lookup, formatter=self.generator.formatter,
                                      converter=self.generator.converter)

            # Now create a small dictionary with keys 'alltime' and 'seven_day':
            self.search_list_extension['alltime'] = all_stats

            #
            #  The html history tables
            #
            t1 = time.time()
            ngen = 0

            for table in self.table_dict.sections:
                noaa = True if table == 'NOAA' else False

                table_options = weeutil.weeutil.accumulateLeaves(self.table_dict[table])
                dbind = None
                if 'data_binding' in table_options:
                    dbind = table_options['data_binding']
                all_stats = TimespanBinder(alltime_timespan, db_lookup, data_binding=dbind, formatter=self.generator.formatter,
                                      converter=self.generator.converter)

                # Show all time unless starting date specified
                startdate = table_options.get('startdate', None)
                if startdate is not None:
                    table_timespan = weeutil.weeutil.TimeSpan(int(startdate), db_lookup(dbind).last_timestamp)
                    table_stats = TimespanBinder(table_timespan, db_lookup, data_binding=dbind, formatter=self.generator.formatter,
                                      converter=self.generator.converter)
                else:
                    table_stats = all_stats

                table_name = table + '_table'
                self.search_list_extension[table_name] = self._statsHTMLTable(table_options, table_stats, table_name,
                                                                              NOAA=noaa)
                ngen += 1

            t2 = time.time()

            syslog.syslog(syslog.LOG_INFO, "%s: Generated %d tables in %.2f seconds" %
                          (os.path.basename(__file__), ngen, t2 - t1))

        return [self.search_list_extension]

    def _statsHTMLTable(self, table_options, table_stats, table_name, NOAA=False):
        """
        table_options: Dictionary containing skin.conf options for particluar table
        all_stats: Link to all_stats TimespanBinder
        """

        bgColours = zip(table_options['minvalues'], table_options['maxvalues'], table_options['colours'])

        reading = None
        if NOAA is True:
            unit_formatted = ""
        else:
            obs_type = table_options['obs_type']
            aggregate_type = table_options['aggregate_type']
            converter = table_stats.converter

            # obs_type
            readingBinder = getattr(table_stats, obs_type)

            # Some aggregate come with an argument
            if aggregate_type in ['max_ge', 'max_le', 'min_le', 'sum_ge']:

                try:
                    threshold_value = float(table_options['aggregate_threshold'][0])
                except KeyError:
                    syslog.syslog(syslog.LOG_INFO, "%s: Problem with aggregate_threshold. Should be in the format: [value], [units]" %
                                  (os.path.basename(__file__)))
                    threshold_value = 0

                threshold_units = table_options['aggregate_threshold'][1]

                try:
                    reading = getattr(readingBinder, aggregate_type)((threshold_value, threshold_units))
                except IndexError:
                    syslog.syslog(syslog.LOG_INFO, "%s: Problem with aggregate_threshold units: %s" % (os.path.basename(__file__),
                                                                                                       str(threshold_units)))
                    return "Could not generate table %s" % table_name
            else:
                try:
                    reading = getattr(readingBinder, aggregate_type)
                except KeyError:
                    syslog.syslog(syslog.LOG_INFO, "%s: aggregate_type %s not found" % (os.path.basename(__file__),
                                                                                        aggregate_type))
                    return "Could not generate table %s" % table_name

            unit_type = reading.converter.group_unit_dict[reading.value_t[2]]

            unit_formatted = ''

            # 'units' option in skin.conf?
            if 'units' in table_options:
                unit_formatted = table_options['units']
            else:
                if (unit_type == 'count'):
                    unit_formatted = "Days"
                else:
                    if unit_type in reading.formatter.unit_label_dict:
                        unit_formatted = reading.formatter.unit_label_dict[unit_type]

            # For aggregrate types which return number of occurrences (e.g. max_ge), set format to integer

            # Don't catch error here - we absolutely need the string format
            if unit_type == 'count':
                format_string = '%d'
            else:
                format_string = reading.formatter.unit_format_dict[unit_type]

        htmlText = '<table class="table">'
        htmlText += "    <thead>"
        htmlText += "        <tr>"
        htmlText += "        <th>%s</th>" % unit_formatted

        for mon in table_options.get('monthnames', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
            htmlText += "        <th>%s</th>" % mon

        htmlText += "    </tr>"
        htmlText += "    </thead>"
        htmlText += "    <tbody>"

        for year in table_stats.years():
            year_number = datetime.fromtimestamp(year.timespan[0]).year

            htmlLine = (' ' * 8) + "<tr>\n"

            if NOAA is True:
                htmlLine += (' ' * 12) + "%s\n" % \
                                         self._NoaaYear(datetime.fromtimestamp(year.timespan[0]), table_options)
            else:
                htmlLine += (' ' * 12) + "<td>%d</td>\n" % year_number

            for month in year.months():
                if NOAA is True:
                    #for property, value in vars(month.dateTime.value_t[0]).iteritems():
                    #    print property, ": ", value

                    if (month.timespan[1] < table_stats.timespan.start) or (month.timespan[0] > table_stats.timespan.stop):
                        # print "No data for... %d, %d" % (year_number, datetime.fromtimestamp(month.timespan[0]).month)
                        htmlLine += "<td>-</td>\n"
                    else:
                        htmlLine += self._NoaaCell(datetime.fromtimestamp(month.timespan[0]), table_options)
                else:
                    if unit_type == 'count':
                        try:
                            # The binding of threshold_value and threshold_units
                            # are bounded in this code is a bit weird. Sadly,
                            # reading the value out and then initializing it if
                            # it fails was the only way I could figure out How
                            # to support group_count without breaking anything.
                            # (Initializing the variable in an outer scope,
                            # actually breaks this code.)
                            #
                            # We check if we need to intialzie threshold_value
                            # and threshold_units depending on if we reading
                            # the value out fails.
                            x = threshold_value
                        except UnboundLocalError:
                            threshold_value = 0
                            threshold_units = 'count'

                        # I don't get why the group needs to be passed only sometimes.
                        # Specifically, pass group_count only if it is a group_count,
                        # but do not pass a unit group if it is a different unit group.
                        try:
                            value = getattr(getattr(month, obs_type), aggregate_type)((threshold_value, threshold_units)).value_t
                        except:
                            try:
                                value = getattr(getattr(month, obs_type), aggregate_type)((threshold_value, threshold_units, 'group_count')).value_t
                            except Exception as e:
                                value = [0, 'count']
                    else:
                        value = converter.convert(getattr(getattr(month, obs_type), aggregate_type).value_t)

                    htmlLine += (' ' * 12) + self._colorCell(value[0], format_string, bgColours)

            htmlLine += (' ' * 8) + "</tr>\n"

            htmlText += htmlLine

        htmlText += (' ' * 8) + "</tr>\n"
        htmlText += (' ' * 4) + "</tbody>\n"
        htmlText += "</table>\n"

        return htmlText

    def _colorCell(self, value, format_string, bgColours):
        """Returns a '<td> bgcolor = xxx y.yy </td>' html table entry string.

        value: Numeric value for the observation
        format_string: How the numberic value should be represented in the table cell.
        bgColours: An array containing 3 lists. [minvalues], [maxvalues], [html colour code]
        """

        if value is not None:
            cellText = "<td"

            for c in bgColours:
                if (value >= int(c[0])) and (value <= int(c[1])):
                    cellText += " bgcolor = \"%s\"" % c[2]

            formatted_value = format_string % value
            cellText += "> %s </td>" % formatted_value

        else:
            cellText = "<td>-</td>\n"

        return cellText

    def _NoaaCell(self, dt, table_options):
        cellText = '<td> <a href="%s" class="btn btn-default btn-xs active" role="button"> %s </a> </td>' % \
                   (dt.strftime(table_options['month_filename']), dt.strftime("%m-%y"))

        return cellText

    def _NoaaYear(self, dt, table_options):
        cellText = '<td> <a href="%s" class="btn btn-primary btn-xs active" role="button"> %s </a> </td>' % \
                   (dt.strftime(table_options['year_filename']), dt.strftime("%Y"))

        return cellText
