from bs4 import BeautifulSoup

def parse_xml_tables(xml_filepath: str):
    with open(xml_filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    
    tables_data = []
    
    # Isolate table-wrap elements which usually contain the table, caption, and footer
    table_wraps = soup.find_all('table-wrap')
    
    for tw in table_wraps:
        table_id = tw.get('id', 'Unknown Table ID')
        
        # Caption
        caption_tag = tw.find('caption')
        caption = caption_tag.get_text(separator=' ', strip=True) if caption_tag else ""
        
        # Footer
        footer_tag = tw.find('table-wrap-foot')
        footer = footer_tag.get_text(separator=' ', strip=True) if footer_tag else ""
        
        # Handle the actual table HTML-like element
        table_html = tw.find('table')
        if not table_html:
            continue
            
        # Extract headers and body, preserving sup/sub
        def extract_text_preserve_tags(tag):
            if not tag: return ""
            result = ""
            for child in tag.children:
                if child.name == 'sup':
                    result += f"^{child.text.strip()}"
                elif child.name == 'sub':
                    result += f"_{child.text.strip()}"
                elif child.name is None:
                    result += child.text
                else:
                    result += extract_text_preserve_tags(child)
            return result.strip()
            
        table_rows = []
        for tr in table_html.find_all('tr'):
            row_data = []
            for cell in tr.find_all(['td', 'th']):
                row_data.append(extract_text_preserve_tags(cell))
            table_rows.append(row_data)
            
        tables_data.append({
            "table_id": table_id,
            "caption": caption,
            "footer": footer,
            "rows": table_rows
        })
        
    return tables_data
