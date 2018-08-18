# Script to create the bulk insert scripts from the old surveys

import pandas as pd
import numpy as np
import pickle

from website.location_uploads import hash_anonymize as ha


old_surveys = pd.read_csv('scripts/old_surveys/old_surveys.csv', dtype = {"Cédula del estudiante": str, "ID (del encuestado)": str})

new_col = ["Marca temporal","carnet","id_entrevistado","edad","sexo","twitter","estado_civil","hijos","vive","ocupacion","medio_ambiente","cultura_ciudadana","movilidad","calidad_vida","practicas_democraticas","tarot_calidad","tarot_ambiental","tarot_cultura","tarot_democraticas"]
old_surveys.columns = new_col

#Drops unanswered surveys
old_surveys.dropna(subset = ['carnet','id_entrevistado'], inplace = True)

old_surveys['carnet'] = np.array( old_surveys['carnet'] ).astype(str)
old_surveys['carnet'] = old_surveys['carnet'].map(lambda x: x.replace(' ',''))

old_surveys['id_entrevistado'] = np.array( old_surveys['id_entrevistado'] ).astype(str)
old_surveys['id_entrevistado'] = old_surveys['id_entrevistado'].map(lambda x: x.replace(' ',''))


old_surveys['edad'] = np.array( old_surveys['edad'] ).astype(int)
old_surveys['medio_ambiente'] = np.array( old_surveys['medio_ambiente'] ).astype(int)
old_surveys['cultura_ciudadana'] = np.array( old_surveys['cultura_ciudadana'] ).astype(int)
old_surveys['movilidad'] = np.array( old_surveys['movilidad'] ).astype(int)
old_surveys['calidad_vida'] = np.array( old_surveys['calidad_vida'] ).astype(int)
old_surveys['hijos'] = np.array( old_surveys['hijos'] ).astype(int)
old_surveys['practicas_democraticas'] = np.array( old_surveys['practicas_democraticas'] ).astype(int)

#Anonyze the interviewd id
old_surveys['id_entrevistado'] = old_surveys['id_entrevistado'].map(lambda x: ha.anonymize(str(x)))

#Standarizes all the columns so that they are consistent with the new survey
#edad
old_surveys[['edad']] = old_surveys[['edad']].fillna('-1')
old_surveys.loc[ (old_surveys.edad < 0) | (old_surveys.edad > 135 ), 'edad'] = -1

#Sexo
old_surveys[['sexo']] = old_surveys[['sexo']].fillna('No Dice')
dic = {'Prefiero no decirlo':'No Dice','bisexual':'No Dice' }
old_surveys.replace({"sexo": dic}, inplace = True)

#estado_civil
dic = {'En soltería':'En Solteria','En unión libre':'En Union Libre' ,'En pareja':'En Pareja', 'Divorciado o divorciada': 'Divorciado o Divorciada' }
old_surveys.replace({"estado_civil": dic}, inplace = True)
old_surveys['estado_civil'] = old_surveys['estado_civil'].map(str)
old_surveys.loc[old_surveys.estado_civil == 'nan','estado_civil'] = None

#hijos
old_surveys.loc[ (old_surveys.hijos < 0) | (old_surveys.hijos > 20 ), 'hijos'] = 0

#twitter
old_surveys['twitter'] = old_surveys['twitter'].map(str)
old_surveys.loc[old_surveys.twitter == 'nan','twitter'] = None

#Ocupacion
old_surveys['ocupacion'] = old_surveys['ocupacion'].map(str)
old_surveys.loc[old_surveys.ocupacion == 'nan','ocupacion'] = None

#vive
dic = {'Pareja y/o hijos':'Pareja-hijos','Solo o sola':'Solo','amigos':'Amigos', 'Con sus padres':'Con Sus Padres',
       'hermano':'Hermanos', 'hermana':'Hermanos', 'Hermana':'Hermanos',
       'hermanos':'Hermanos', 'Comunidad religiosa':'Comunidad Religiosa'}
old_surveys.replace({"vive": dic}, inplace = True)
old_surveys[['vive']] = old_surveys[['vive']].fillna('Otro')

def temp(x):
    if ('estudiantil' in str(x).lower() or 'universitaria' in str(x).lower()):
        return('Residencia Estudiantil')
    elif 'religiosa'in str(x).lower():
        return('Comunidad Religiosa')
    elif('mamá' in str(x).lower()
         or 'papá' in str(x).lower()):
        return('Con Sus Padres')
    elif('amig' in str(x).lower()
         or 'compañer' in str(x).lower()
        or 'mate' in str(x).lower()):
        return('Amigos')
    elif 'herman' in str(x).lower():
        return('Hermanos')
    elif('hijo' in str(x).lower() or 'hija' in str(x).lower()):
        return('Pareja-Hijos')
    elif ('abuel' in str(x).lower()
          or 'tio' in str(x).lower()
          or 'tia' in str(x).lower()
          or 'tío' in str(x).lower()
          or 'tía' in str(x).lower()
          or 'familia' in str(x).lower()
          or 'primo' in str(x).lower()
          or 'prima' in str(x).lower()):
        return('Familiares')
    elif(x not in ['Pareja-Hijos','Solo','Con Sus Padres','Comunidad Religiosa','Amigos','Hermanos']):
        return('Otro')
    else:
        return(x)

old_surveys['vive'] = old_surveys['vive'].map(temp)

#tarots
old_surveys['tarot_calidad'] = old_surveys['tarot_calidad'].map(str)
old_surveys.loc[old_surveys.tarot_calidad == 'nan','tarot_calidad'] = None
old_surveys['tarot_ambiental'] = old_surveys['tarot_ambiental'].map(str)
old_surveys.loc[old_surveys.tarot_ambiental == 'nan','tarot_ambiental'] = None
old_surveys['tarot_cultura'] = old_surveys['tarot_cultura'].map(str)
old_surveys.loc[old_surveys.tarot_cultura == 'nan','tarot_cultura'] = None
old_surveys['tarot_democraticas'] = old_surveys['tarot_democraticas'].map(str)
old_surveys.loc[old_surveys.tarot_democraticas == 'nan','tarot_democraticas'] = None









survey_table_scheme =  pd.read_csv('website/location_uploads/static/location_uploads/config/table_survey_scheme.csv', index_col = 'name')
survey_columns = np.intersect1d(old_surveys.columns.tolist(), survey_table_scheme.index.tolist())
summary_columns = ["carnet","id_entrevistado", "timestamp_encuesta","entrego_encuesta"]


sql_survey = 'INSERT INTO survey_prod ( '

for col in survey_columns:
    sql_survey = sql_survey + col + ','
sql_survey = sql_survey[:-1] + ') VALUES '


sql_summary = 'INSERT INTO summary_prod ('

for col in summary_columns:
    sql_summary = sql_summary + col + ','
sql_summary = sql_summary[:-1]  + ') VALUES '

json_map = {}

for i in range(old_surveys.shape[0]):
    row = old_surveys.iloc[i]
    json_map[str(row['id_entrevistado'])] = str(row['carnet'])

    #survey
    sql_survey = sql_survey + '('
    for col in survey_columns:
        if(col not in old_surveys.columns):
             insert_val = 'NULL'
        else:
            val = row[col]
            if(val is None):
                insert_val = 'NULL'
            elif('VARCHAR' in survey_table_scheme.loc[col,'type']):
                val = str(val).replace('"','')
                val = str(val).replace("'",'')
                insert_val = "'" + val + "'"
            elif('INT' in survey_table_scheme.loc[col,'type']):
                insert_val = val
            else:
                raise ValueError("Columna: " + col + " no es numerica ni cadena de caracteres.")

        sql_survey = sql_survey + str(insert_val) + ','

    sql_survey = sql_survey[:-1] + '),' +'\n'

    #summary
    sql_summary = sql_summary + '('
    summary_row = {'carnet': "'" + str(row['carnet']) + "'", "id_entrevistado": "'" + str(row["id_entrevistado"]) + "'", "timestamp_encuesta": str(ha.get_timestamp()),"entrego_encuesta": 'TRUE' }
    for col in summary_columns:
        sql_summary = sql_summary + str(summary_row[col]) + ','
    sql_summary = sql_summary[:-1]  + '),' +'\n'

sql_survey = sql_survey[:-2] + ';'
sql_summary = sql_summary[:-2]  + ';'


with open('scripts/json_map.pickle', 'wb') as file:
    pickle.dump(json_map, file, protocol=pickle.HIGHEST_PROTOCOL)


file = open('scripts/sql_scripts/insert_old_surveys.sql','w')
file.write(sql_survey)
file.close()

file = open('scripts/sql_scripts/insert_old_summaries.sql','w')
file.write(sql_summary)
file.close()
