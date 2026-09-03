import os
from pk_pbpk_extractor.ingestion.xml_parser import parse_xml_tables

def test_parse_xml_tables():
    # Create a dummy XML file
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <article>
        <table-wrap id="T1">
            <caption>Table 1 PK Parameters</caption>
            <table>
                <tr>
                    <td>CL<sub>ren</sub></td>
                    <td>10</td>
                </tr>
            </table>
            <table-wrap-foot>Footer note</table-wrap-foot>
        </table-wrap>
    </article>
    '''
    
    with open("dummy.xml", "w") as f:
        f.write(xml_content)
        
    tables = parse_xml_tables("dummy.xml")
    assert len(tables) == 1
    assert tables[0]["caption"] == "Table 1 PK Parameters"
    assert tables[0]["rows"][0][0] == "CL_ren"
    assert tables[0]["rows"][0][1] == "10"
    
    os.remove("dummy.xml")
