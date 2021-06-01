#allows you to access libraries js like quasar and HighCharts
import justpy as jp
import pandas
from datetime import datetime
from pytz import utc

#creates dataframe
data = pandas.read_csv("reviews.csv",parse_dates=["Timestamp"])
#adds a column for the week the review was made through using the timestamp column
data["Week"] = data["Timestamp"].dt.strftime("%Y-%U")
#creates a new dataframe where each week is an index and a column of the mean ratings
week_average = data.groupby(["Week"]).mean()
#js code from https://www.highcharts.com/docs/chart-and-series-types/spline-chart copied the json portion from HighCharts
#js code for spline chart
#triple quote string allows the string to be multi lined and not get confused with double/single quotes within it
chart_def = """
{
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Average Rating by Week'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '({point.x}, {point.y})'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Average Rating',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}

"""
def app():
    #create web page
    wp = jp.QuasarPage()
    #order of elements determines where it will be in web page
    #the classes variable allows to change styling. See https://quasar.dev/style for how to
    #heading
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center q-pa-md")
    #paragraph
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    #JP.HighCharts converts chart_def to dictionary so python can understand and puts it
    #the dictionary is makes is different then a normal one. Can access keys inside using dot notation
    hc = jp.HighCharts(a=wp, options=chart_def)

    #options becomes an attribute of hc as the dictionary.
    #then, accessing title key then text and changing the element to average rating by Day
    hc.options.title.text = "Average Rating by Week"
    #Changing Data
    #series is a list which has a dictionary in it with name and data
    #giving x axis data
    #dates are not considered numbers in high charts but rather as categories
    hc.options.xAxis.categories = list(week_average.index)
    #data takes a list of lists.
    #x coordinates are the dates, y coordinates are the mean ratings
    hc.options.series[0].data = list(week_average["Rating"])
    return wp
jp.justpy(app)
