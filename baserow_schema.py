from dotenv import load_dotenv
import os
import json
import requests

# Load .env file
load_dotenv()

BASEROW_API_TOKEN = os.getenv("BASEROW_API_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
BASE_URL = os.getenv("BASE_URL", "https://api.baserow.io/api")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "schema.json")

def get_tables(database_id: int):
    """
    Fetch all tables for a given Baserow database.
    Uses the backend/REST API "list tables for a database" endpoint.
    """
    url = f"{BASE_URL}/api/database/tables/all-tables/"
    headers = {
        "Authorization": f"Token {BASEROW_API_TOKEN}",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_fields(table_id: int):
    """Fetch all fields for a given table."""
    url = f"{BASE_URL}/api/database/fields/table/{table_id}/"
    headers = {
        "Authorization": f"Token {BASEROW_API_TOKEN}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_dbdiagram():
    tables = get_tables()
    schema_output = []
    relationships = []

    for table in tables:
        table_name = table["name"]
        table_id = table["id"]

        schema_output.append(f"Table {table_name} {{")
        fields = get_fields(table_id)

        for field in fields:
            field_name = field["name"]
            field_type = field["type"]
            sql_type = map_baserow_type_to_sql(field_type)

            # Mark ID field as primary key
            if field_name.lower() == "id":
                schema_output.append(f"  {field_name} {sql_type} [pk]")
            else:
                schema_output.append(f"  {field_name} {sql_type}")

            # Detect relationships via link_row
            if field_type == "link_row":
                link_table = field["link_row_table"]["name"]
                relationships.append(f"Ref: {table_name}.{field_name} > {link_table}.id")

        schema_output.append("}\n")

    schema_output.extend(relationships)

    return "\n".join(schema_output)

if __name__ == "__main__":
    print(f"\n Fetching tables and fields for database {DATABASE_ID}...\n")

    schema = {
        "database_id": DATABASE_ID,
        "tables": []
    }

    try:
        tables = get_tables(DATABASE_ID)

        for table in tables:
            table_id = table["id"]
            table_name = table["name"]

            print(f"=== Table: {table_name} (ID: {table_id}) ===")

            fields = get_fields(table_id)

            field_list = []
            for field in fields:
                field_list.append({
                    "id": field["id"],
                    "name": field["name"],
                    "type": field["type"]
                })

                print(f"  - Field: {field['name']} | Type: {field['type']} | ID: {field['id']}")

            schema["tables"].append({
                "id": table_id,
                "name": table_name,
                "fields": field_list
            })

            print()  # spacing

        # ------------------------------
        #  Save to JSON file
        # ------------------------------
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2)

        print(f"\n Schema saved to: {OUTPUT_FILE}\n")

    except Exception as e:
        print(" Unexpected error:", type(e).__name__, "-", e)