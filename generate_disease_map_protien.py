import csv
import json


disease_protein_map = {}


with open("disgenet-gene-attribute-edgelist.tsv", "r") as file:
   reader = csv.reader(file, delimiter='\t')
   next(reader)  # Skip header if present


   for gene, disease in reader:
       if disease not in disease_protein_map:
           disease_protein_map[disease] = set()
       disease_protein_map[disease].add(gene)


# Convert sets to lists
disease_protein_map = {k: list(v) for k, v in disease_protein_map.items()}


# Save to JSON
with open("disease_protein_map.json", "w") as out:
   json.dump(disease_protein_map, out, indent=2)




