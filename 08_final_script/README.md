# Recommendation script 

for the Semantic Web project by

- Adelia Khasanova
- Shane Kaszefski-Yaschuk
- Dimitra Niaouri
- Luis Antonio Vasquez Reina


# Setup

Load the file `Basic_Games_Ontology_Final.owl` to Blazegraph, under a new namespace called `swproj`, and leave Blazegraph running.

In case your blazegraph endpoint is not the default one, you will have to modify line 9 of `recommendation_script.py` to your endpoint:

```
endpoint_url = "http://10.11.120.183:9999/blazegraph/namespace/swproj/sparql"
```

# Usage

To start the recommendation script, it is only necessary to run

```
python3 recommendation_script.py
```

See the **video demo** for a step by step walkthrough.