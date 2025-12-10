#Baserow Schema Extractor

Script retrieves table and field metadata from a Baserow database using the REST API and exports it to JSON. A converter script can then generate a Mermaid ERD diagram from the exported schema.

Requirements
	•	Python 3.10+
	•	requests
	•	python-dotenv

Install dependencies:

pip install -r requirements.txt

#Configuration

Create your .env file with cp example.env .env

Update your environment variables.

#Usage

Step 1: Export Schema

python baserow_schema.py

This creates a schema.json file containing table names, fields, and relationships.

Step 2: Generate Mermaid ERD

python json_to_mermaid.py

This produces schema.mmd, which can be used with Obsidian, GitHub, or any Mermaid renderer.

#Output Files

File	Description
schema.json	Raw exported metadata from Baserow
schema.mmd	Mermaid ERD diagram generated from schema.json

#Notes
	•	.env, generated files, and virtual environments should be excluded using .gitignore.
	•	The tool currently treats relationships based on Baserow link_row field types.