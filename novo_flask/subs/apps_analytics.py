"""
apps_analytics.py  —  Gráficos Plotly com pandas + SQLAlchemy.

Segue o padrão do professor (Lesson 11):
  - pd.read_sql() com sqlalchemy engine
  - plotly.express para criar os gráficos
  - fig.to_html(full_html=False) para gerar o HTML+JS
  - variáveis plot_div passadas ao template com {{ plot_div | safe }}
"""
from flask import render_template, session
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Importamos as classes para resolver nomes a partir dos ids
from classes.university import University
from classes.director   import Director
from classes.grant      import Grant

DB_PATH = 'data/g22_db.db'

def apps_analytics():

    # ── Ligação à base de dados via SQLAlchemy (padrão do professor) ───────────
    engine = create_engine('sqlite:///' + DB_PATH)

    # ══════════════════════════════════════════════════════════════════════════
    # Gráfico 1 — Labs por universidade (bar chart)
    # Lê as tabelas University e Lab e faz o join para contar labs por uni
    # ══════════════════════════════════════════════════════════════════════════
    df_lab = pd.read_sql('Lab', con=engine)
    df_uni = pd.read_sql('University', con=engine)

    # groupby: conta quantos labs tem cada university_id
    result1 = df_lab.groupby('university_id')['lab_id'].count()

    # Resolve os ids para nomes usando a classe University
    uni_names = []
    for uid in result1.index:
        obj = University.obj.get(uid)
        uni_names.append(obj.name if obj else str(uid))

    fig1 = px.bar(
        x=uni_names,
        y=result1.values,
        labels={'x': 'Universidade', 'y': 'Nº de Labs'},
        title='Número de Labs por Universidade',
        color=result1.values,
        color_continuous_scale='teal'
    )
    fig1.update_layout(showlegend=False, coloraxis_showscale=False)
    plot_labs = fig1.to_html(full_html=False, div_id='plot-labs')

    # ══════════════════════════════════════════════════════════════════════════
    # Gráfico 2 — Financiamento total por universidade (horizontal bar)
    # ══════════════════════════════════════════════════════════════════════════
    df_ugrant = pd.read_sql('Uni_grant', con=engine)

    result2 = df_ugrant.groupby('university_id')['amount'].sum()

    uni_names2 = []
    for uid in result2.index:
        obj = University.obj.get(uid)
        uni_names2.append(obj.name if obj else str(uid))

    fig2 = px.bar(
        x=result2.values,
        y=uni_names2,
        orientation='h',
        labels={'x': 'Total (€)', 'y': 'Universidade'},
        title='Financiamento Total por Universidade',
        color=result2.values,
        color_continuous_scale='purples'
    )
    fig2.update_layout(coloraxis_showscale=False)
    plot_funding = fig2.to_html(full_html=False, div_id='plot-funding')

    # ══════════════════════════════════════════════════════════════════════════
    # Gráfico 3 — Grants por categoria (pie / donut)
    # ══════════════════════════════════════════════════════════════════════════
    df_grant = pd.read_sql('Grant', con=engine)

    result3 = df_grant.groupby('category')['grant_id'].count()

    fig3 = px.pie(
        names=result3.index,
        values=result3.values,
        title='Distribuição de Grants por Categoria',
        hole=0.35
    )
    plot_categories = fig3.to_html(full_html=False, div_id='plot-categories')

    # ══════════════════════════════════════════════════════════════════════════
    # Gráfico 4 — Evolução do financiamento por ano (line chart)
    # Usa pandas para extrair o ano da coluna start_date
    # ══════════════════════════════════════════════════════════════════════════
    df_ugrant['start_date'] = pd.to_datetime(df_ugrant['start_date'])
    df_ugrant['year']       = df_ugrant['start_date'].dt.year

    result4 = df_ugrant.groupby('year')['amount'].sum().reset_index()

    fig4 = px.line(
        result4,
        x='year',
        y='amount',
        markers=True,
        labels={'year': 'Ano', 'amount': 'Total (€)'},
        title='Evolução do Financiamento por Ano'
    )
    fig4.update_traces(line_color='#D85A30', marker_size=8)
    plot_timeline = fig4.to_html(full_html=False, div_id='plot-timeline')

    # ══════════════════════════════════════════════════════════════════════════
    # Gráfico 5 — Distribuição de idades dos diretores (histogram)
    # Usa directamente os objetos da classe Director (já estão em memória)
    # ══════════════════════════════════════════════════════════════════════════
    ages = [d.age for d in Director.obj.values()]

    fig5 = px.histogram(
        x=ages,
        nbins=10,
        labels={'x': 'Idade', 'y': 'Nº de Diretores'},
        title='Distribuição de Idades dos Diretores',
        color_discrete_sequence=['#185FA5']
    )
    plot_ages = fig5.to_html(full_html=False, div_id='plot-ages')

    # ── Passa todas as variáveis plot_div ao template ──────────────────────────
    return render_template(
        'analytics.html',
        plot_labs       = plot_labs,
        plot_funding    = plot_funding,
        plot_categories = plot_categories,
        plot_timeline   = plot_timeline,
        plot_ages       = plot_ages,
        ulogin          = session.get('user')
    )
