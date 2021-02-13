from app import app

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from apps import home
from apps.temporal import temporal
from apps.prediction import attackprediction

side_nav = home.get_nav_bar_static()
# print(side_nav)
app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            <div class="app-header navbar sticky-top" style="z-index: 3; background: #252525;">
                <a href="/home">
                    <h1 class="project_banner">
                        AnTeVioLinc
                    </h1>
                </a>
                <a href="/home" style="padding-left: -20%">
                    <div class="project_title">
                        <h1>
                            <u>An</u>alysis of <u>Te</u>rrorist and <u>Viol</u>ent <u>Inc</u>idents
                        </h1>
                    </div>
                </a>
                <h1>.</h1>
            </div>
            
    ''' + side_nav + '''
            
            {%app_entry%}

            <footer>
                <div class="footerStatic">
                    <img src="assets/images/gtd_logo.gif" style="width: 265px; padding-left: 13px;"/>
                    <h1 class="animated_banner">
                        CoDTeEM
                    </h1>
                </div>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>

        </body>
    </html>
    '''
print(app.index_string)

# ''' + side_nav + '''
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content', className='page_content')
], className='main_layout')


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # components = [home.get_nav_bar()]
    components = []

    if pathname == '/temporal':
        components.append(temporal.get_layout())
        return components

    if pathname == '/temporal_islamic':
        components.append(temporal.get_layout(islamic=True))
        return components

    if pathname == '/correlation':
        components.append(home.get_layout(correlations=True))
        return components

    if pathname == '/predict_attacker':
        components.append(attackprediction.get_layout())
        return components

    # defaults to home page;
    components.append(home.get_layout())
    return components


if __name__ == '__main__':
    app.run_server(
        debug=True,
        # dev_tools_hot_reload=False
    )
