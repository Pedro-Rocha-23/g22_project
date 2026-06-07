from flask import render_template, session
import pandas as pd
import sqlite3
import plotly.express as px
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "g22_db.db")

def grafico_circular():
    conn = sqlite3.connect(DB_PATH)
    df_uni = pd.read_sql('SELECT * FROM University', con=conn)
    df_reg = pd.read_sql('SELECT * FROM Region', con=conn)
    conn.close()
    df_uni.columns = df_uni.columns.str.lower().str.lstrip('_')
    df_reg.columns = df_reg.columns.str.lower().str.lstrip('_')
    df = pd.merge(df_uni, df_reg, left_on='region_id', right_on='id', suffixes=('_uni', '_reg'))
    result = df.groupby('name_reg').size().reset_index(name='Quantidade')
    fig = px.pie(result, values='Quantidade', names='name_reg', title='Distribuição por Região')
    return render_template("plot_view.html", plot_div=fig.to_html(full_html=False), ulogin=session.get("user"))

def grafico_idades_diretores():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM Director', con=conn)
    conn.close()
    
    df.columns = df.columns.str.lower().str.lstrip('_')
    coluna_data = [c for c in df.columns if 'dob' in c or 'birth' in c][0]
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors='coerce')
    ano_atual = datetime.datetime.now().year
    df['idade'] = ano_atual - df[coluna_data].dt.year
    df = df.dropna(subset=['idade'])
    
    # Criar o histograma
    fig = px.histogram(
        df, 
        x="idade", 
        nbins=10, 
        title='Distribuição de Idades',
        labels={'idade': 'Idade (Anos)', 'count': 'Nº de Diretores'}
    )
    
    # Adicionar o contorno (outline) preto nas barras para melhor distinção
    fig.update_traces(marker_line_color='black', marker_line_width=1.5)
    
    # Forçar o eixo X de 30 a 75
    fig.update_xaxes(range=[30, 75])
    
    return render_template("plot_view.html", plot_div=fig.to_html(full_html=False), ulogin=session.get("user"))

def grafico_linhas():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT start_date FROM Uni_grant', con=conn)
    conn.close()
    df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True, errors='coerce')
    df['ano'] = df['start_date'].dt.year
    result = df.groupby('ano').size().reset_index(name='contagem')
    fig = px.line(result, x='ano', y='contagem', title="Cronologia de Projetos", markers=True)
    return render_template("plot_view.html", plot_div=fig.to_html(full_html=False), ulogin=session.get("user"))