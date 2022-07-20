import json
import os
import plotly.offline as opy
import plotly.graph_objects as go
from jinja2 import Environment, PackageLoader, select_autoescape
MEDIA_ROOT = './'

env = Environment(loader=PackageLoader('analysis'))
template = env.get_template('report.html')


jdata = json.load(open(MEDIA_ROOT+'/json/sppBuild.json'))
buildsummary = jdata['buildSummary']
stagesummary = jdata['stageSummary']
resourcesummary = [{'status':each.split('-',1)[0],'resource':each.split('-',1)[1].split(' - <')[0],'reason': each.split('-')[-1]} for each in jdata['resourceSummary']]
rulesummary = jdata['rulesSummary']
compsummary = jdata['complianceScanSummary']
colors = ['green', 'red']
fig = go.Figure(data=[go.Pie(labels=['Resources Passed','Resources failed'],values=[compsummary['rulesRun'],compsummary['resourceFailed']])])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.update_layout(title_text='Compliance Scan Summary')
div = opy.plot(fig, auto_open=False, output_type='div')
#return render(request, 'report.html', context)

with open('rep_html/report.html', 'w') as fh:
    fh.write(template.render(
        buildsummary = buildsummary,
        stagesummary = stagesummary,
        resourcesummary = resourcesummary,
        rulesummary = rulesummary,
        fig = div
    ))