import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = data

# Group the data by country and year, and calculate the total budget for each group
budget_by_country = df.groupby(['Country', 'Year']).agg({'Budget': 'sum'})

# Line chart using matplotlib
budget_by_country = budget_by_country.reset_index().pivot(index='Year', columns='Country', values='Budget')
plt.plot(budget_by_country)
plt.xlabel('Year')
plt.ylabel('Total budget')
plt.legend(budget_by_country.columns)
plt.show()

# Bar chart using plotlyimport pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = data

# Group the data by country and year, and calculate the total budget for each group
budget_by_country = df.groupby(['Country', 'Year']).agg({'Total IDA and IBRD Commitment $US': 'Total Project Cost $US'})

# Line chart using matplotlib
budget_by_country = budget_by_country.reset_index().pivot(index='Year', columns='Country', values='Total Project Cost $US')
plt.plot(budget_by_country)
plt.xlabel('Year')
plt.ylabel('Total budget')
plt.legend(budget_by_country.columns)
plt.show()

# Bar chart using plotly
fig = px.bar(df, x='Year', y='Total Project Cost $US', color='Country', barmode='group')
fig.show()

# Pie chart using plotly
budget_by_country_year = df.groupby(['Country', 'Year']).agg({'Total Project Cost $US': 'sum'}).reset_index()
fig = px.pie(budget_by_country_year, values='Budget', names='Country', hole=0.5)
fig.show()

# Donut chart using plotly
fig = px.pie(budget_by_country_year, values='Total Project Cost $US', names='Country', hole=0.7)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

fig = px.bar(df, x='Year', y='Budget', color='Country', barmode='group')
fig.show()

# Pie chart using plotly
budget_by_country_year = df.groupby(['Country', 'Year']).agg({'Budget': 'sum'}).reset_index()
fig = px.pie(budget_by_country_year, values='Budget', names='Country', hole=0.5)
fig.show()

# Donut chart using plotly
fig = px.pie(budget_by_country_year, values='Budget', names='Country', hole=0.7)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
