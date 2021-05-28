import justpy as jp

def app():
    #create web page
    wp = jp.QuasarPage()
    #the classes variable allows to change styling. See https://quasar.dev/style for how to
    #heading
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center q-pa-md")
    #paragraph
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    return wp

jp.justpy(app)
