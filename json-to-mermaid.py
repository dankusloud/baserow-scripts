import json
import re

INPUT_FILE = "schema.json"
OUTPUT_FILE = "schema.mmd"


def to_camel_case(name: str) -> str:
    """Convert snake_case or spaced names to camelCase."""
    parts = re.split(r"[_\s]+", name)
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])


def to_pascal_case(name: str) -> str:
    """Convert snake_case or spaced names to PascalCase."""
    parts = re.split(r"[_\s]+", name)
    return ''.join(word.capitalize() for word in parts)


def to_mermaid_type(field_type):
    """Basic Baserow → Mermaid type mapping."""
    mapping = {
        "text": "string",
        "long_text": "string",
        "number": "int",
        "boolean": "bool",
        "date": "date",
        "datetime": "datetime",
        "link_row": "int",   # shown as int but connection still visualized
    }
    return mapping.get(field_type, "string")


def generate_mermaid(schema):
    lines = ["erDiagram\n"]

    table_lookup = {}  # map original -> pascal
    for t in schema["tables"]:
        table_lookup[t["name"]] = to_pascal_case(t["name"])

    # ---- Tables ----
    for table in schema["tables"]:
        table_name_raw = table["name"]
        table_name = table_lookup[table_name_raw]

        lines.append(f"    {table_name} {{")

        for field in table["fields"]:
            field_type = to_mermaid_type(field["type"])
            field_name = to_camel_case(field["name"])
            lines.append(f"        {field_type} {field_name}")

        lines.append("    }\n")

    # ---- Relationships ----
    for rel in schema.get("relationships", []):
        from_table = table_lookup.get(rel["from_table"], rel["from_table"])
        to_table = table_lookup.get(rel["to_table"], rel["to_table"])
        field_label = to_camel_case(rel["from_field"])

        # Escape the first brace, keep Mermaid syntax
        lines.append(f"    {from_table} }}o--|| {to_table} : {field_label}")

    return "\n".join(lines)


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        schema = json.load(f)

    mermaid_output = generate_mermaid(schema)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(mermaid_output)

    print(f"Mermaid ERD saved to: {OUTPUT_FILE}")