import justpy as jp
import pandas
from datetime import datetime
from pytz import utc

#creates dataframe
data = pandas.read_csv("reviews.csv",parse_dates=["Timestamp"])
#Create groups by course and make column number of ratings
share = data.groupby(["Course Name"])["Rating"].count()
chart_def = """
{
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: '% of number of reviews'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Brands',
        colorByPoint: true,
        data: [{
            name: 'Chrome',
            y: 61.41,
            sliced: true,
            selected: true
        }, {
            name: 'Internet Explorer',
            y: 11.84
        }, {
            name: 'Firefox',
            y: 10.85
        }, {
            name: 'Edge',
            y: 4.67
        }, {
            name: 'Safari',
            y: 4.18
        }, {
            name: 'Sogou Explorer',
            y: 1.64
        }, {
            name: 'Opera',
            y: 1.6
        }, {
            name: 'QQ',
            y: 1.2
        }, {
            name: 'Other',
            y: 2.61
        }]
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

    hc_data = [{"name":v1, "y":v2} for v1, v2 in zip(share.index, share)]
    hc.options.series[0].data = hc_data
    return wp
jp.justpy(app)
