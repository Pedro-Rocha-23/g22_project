"""
Created on Sun Apr 26 13:36:31 2026

@author: pipa
"""

from classes.director import Director
from classes.lab import Lab
from classes.uni_grant import Uni_grant
from classes.university import University
from classes.grant import Grant

# ler dados
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "g22_db.db"

Director.read(str(DB_PATH))
Lab.read(str(DB_PATH))
Uni_grant.read(str(DB_PATH))
University.read(str(DB_PATH))
Grant.read(str(DB_PATH))


#teste Grant

if Uni_grant.lst:
    ug = Uni_grant.obj[Uni_grant.lst[0]]

    uni_name = University.obj[ug.university_id].name
    grant_title = Grant.obj[ug.grant_id].title

    print("TESTE Uni_grant")
    print(f"ID Uni_grant:   {ug.id}")
    print(f"Universidade:   {uni_name}")
    print(f"Grant:          {grant_title}")
    print(f"Montante:       {ug.amount}")
    print(f"Data Início:    {ug.start_date}")
    print("\nSUCESSO: Uni_grant corretamente associado.\n")
else:
    print("AVISO: Sem dados em Uni_grant.\n")


#teste lab
if Lab.lst:
    lab = Lab.obj[Lab.lst[0]]

    uni_name = University.obj[lab.university_id].name

    print("TESTE Lab")
    print(f"ID Lab:         {lab.id}")
    print(f"Info Extra:     {lab.extra_info}")
    print(f"Universidade:   {uni_name}")
    print("\nSUCESSO: Lab corretamente associado.\n")
else:
    print("AVISO: Sem dados em Lab.\n")


#teste director
if Director.lst:
    d = Director.obj[Director.lst[0]]

    print("TESTE Director ")
    print(f"ID Director:    {d.id}")
    print(f"Nome:           {d.director_name}")
    print(f"Data Nasc:      {d.dob}")
    print(f"Idade:          {d.age}")
    print("\nSUCESSO: Director carregado corretamente.\n")
else:
    print("AVISO: Sem dados em Director.\n")


#resultado
print(" TODOS OS TESTES EXECUTADOS.")