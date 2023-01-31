from dash import Dash, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
#--------------------------------------------------
# get data, and organise
#--------------------------------------------------
data_dir = '../results_test/'
archive = 'CallDallFall_archive.csv'
archive = pd.read_csv(data_dir+archive)

r = pd.read_csv('../data_test/race_test.csv')
r.set_index('race_id', inplace=True)
r = r['start_time']

horse_names = pd.read_csv('../data_test/horse_test.csv')  # contains names, stables, parents ect..
horse_names.set_index('horse_id', inplace=True)

#-------------------------------------------------
# build components
#--------------------------------------------------

app = Dash(__name__, external_stylesheets= [dbc.themes.VAPOR])

title = dcc.Markdown(children = 'ZedR: track your horses performance data')
maingraph = dcc.Graph(id = 'maingraph',figure={})

h_input = dcc.Input(id = 'h_input',
                    placeholder = 'enter horse id',
                    type = 'number',
                    debounce = True,
                    )
graph_dd = dcc.Dropdown(id = 'graph_dd',
                        placeholder = 'select property to display',
                        )

# main layout
app.layout = dbc.Container([title,h_input,maingraph,graph_dd])



#call back for graph
@app.callback(
    Output('maingraph',component_property= 'figure'),
    Output('graph_dd',component_property = 'options'),
    Input('h_input', component_property= 'value'),
    Input('graph_dd',component_property = 'value'))
def get_horse_archive(h_id,to_disp):

    h_results = archive[archive['horse_id'] == h_id]
    n_races = [i for i in range(len(h_results))]

    # get race start_times and merge into new column
    r_db = r.loc[h_results['race_id']]
    h_results.set_index('race_id', inplace = True)
    h = h_results.merge(r_db,on = 'race_id')

    # for display on graph
    h_id4graph = h['horse_id'][0]
    h_name = horse_names.loc[h_id]['name']
    address = horse_names.loc[h_id]['address']

    # build figure
    print(to_disp)
    if to_disp is None:
        fig = px.line(h,x = 'no_races', y = 'preELO',text = 'start_time',title = h_name+': '+str(h_id4graph)+' @ '+address)
    # fig = px.line(h,x = 'no_races', y = 'mean_speed_t',title = h_name+': '+str(h_id4graph)+' @ '+address)
        fig.update_traces(textposition="bottom right")
    else:
        fig = px.line(h,x = 'no_races', y = to_disp,text = 'start_time',title = h_name+': '+str(h_id4graph)+' @ '+address)
    # fig = px.line(h,x = 'no_races', y = 'mean_speed_t',title = h_name+': '+str(h_id4graph)+' @ '+address)
        fig.update_traces(textposition="bottom right")

    dropdown_options = h.columns.values[2:]
    # print(dropdown_options)


    return [fig, [{'label': i, 'value':i} for i in dropdown_options]]




if __name__ == '__main__':
    app.run_server(port = 8051, debug = True)