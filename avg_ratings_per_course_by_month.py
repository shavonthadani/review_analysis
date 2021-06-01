import justpy as jp
import pandas
from datetime import datetime
from pytz import utc

#creates dataframe
data = pandas.read_csv("reviews.csv",parse_dates=["Timestamp"])
#adds a column for the week the review was made through using the timestamp column
data["Month"] = data["Timestamp"].dt.strftime("%Y-%m")
#Collects the data into groups by course and month and has a column for rating mean
month_average = data.groupby(["Month", "Course Name"])["Rating"].mean().unstack()
#js code from https://www.highcharts.com/docs/chart-and-series-types/spline-chart copied the json portion from HighCharts
#js code for spline chart
#triple quote string allows the string to be multi lined and not get confused with double/single quotes within it
chart_def = """
{
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Average fruit consumption during one week'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: false,
        borderWidth: 1,
        backgroundColor:
            '#FFFFFF'
    },
    xAxis: {
        categories: [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ],
        plotBands: [{ // visualize the weekend
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Fruit units'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ' units'
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: 'John',
        data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
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
    hc.options.xAxis.categories = list(month_average.index)
    #Adding the data
    hc_data = [{"name":v1, "data":[v2 for v2 in month_average[v1]]} for v1 in month_average.columns]
    hc.options.series = hc_data
    return wp
jp.justpy(app)
