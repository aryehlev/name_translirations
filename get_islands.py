
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import re

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


    
    
endpoint_url = "https://query.wikidata.org/sparql"

query = f"""select ?city ?hebrew_label ?english_label
            where
            {{
            ?city wdt:P31 wd:Q23442.
            
            ?city rdfs:label ?hebrew_label filter (lang(?hebrew_label) = "he").
            ?city rdfs:label ?english_label filter (lang(?english_label) = "en").
            }}
            LIMIT 15000
            """




results = get_results(endpoint_url, query)
#   def next_available_row(sheet, cols_to_sample=2):
#     # looks for empty row based on values appearing in 1st N columns
#     cols = sheet.range(1, 1, sheet.row_count, cols_to_sample)
#     return max([cell.row for cell in cols if cell.value]) + 1


with open('islands.csv', 'a',  encoding="utf-8") as f:
    
    for result in results["results"]["bindings"]:
        hebrew_name =  result['hebrew_label']['value'].lower()
        english_name = result['english_label']['value'].lower()
        if not bool(re.search('[a-z]', hebrew_name)):
            hebrew_name= hebrew_name.split(" ")
            # print(result)

            english_name = english_name.split(" ")
            
        #   if hebrew_name and english_name:
        #     worksheet.update_acell(f'A{index}',hebrew_name[0])
        #     worksheet.update_acell(f'B{index}',english_name[0])
            if len(hebrew_name) > 1:
                if not '(אי)' in hebrew_name[1]:
                    hebrew = hebrew_name[1]
                else:
                    hebrew = hebrew_name[0]
            else:
                hebrew = hebrew_name[0]

                
            f.write(f'{hebrew},{english_name[0]}\n')
        
    