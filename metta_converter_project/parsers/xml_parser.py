"""XML parser using xml.etree.ElementTree. Produces nodes and attributes as MeTTa expressions."""
import xml.etree.ElementTree as ET
from .utils import make_id, sanitize_token, format_value

def _element_to_metta(elem, parent_id=None, id_prefix=None):
    lines = []
    tag = sanitize_token(elem.tag)
    node_id = None
    # If element has an 'id' attribute, prefer it
    if 'id' in elem.attrib:
        node_id = sanitize_token(elem.attrib['id'])
    else:
        node_id = sanitize_token(id_prefix or f"{tag}") + "_" + make_id()
    lines.append(f"({tag} {node_id})")
    # attributes
    for k, v in elem.attrib.items():
        if k == 'id':
            lines.append(f"(id {node_id} {format_value(v)})")
        else:
            lines.append(f"({sanitize_token(k)} {node_id} {format_value(v)})")
    # text
    text = (elem.text or '').strip()
    if text:
        lines.append(f"(text {node_id} {format_value(text)})")
    # parent relation
    if parent_id:
        lines.append(f"({tag} {parent_id} {node_id})")
    # children
    for child in list(elem):
        lines.extend(_element_to_metta(child, parent_id=node_id, id_prefix=child.tag))
    return lines

def parse_xml(file_path: str):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return _element_to_metta(root, parent_id=None, id_prefix=root.tag)
