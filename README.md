### Installing
```
pip install md2steam
```

### Example
```python
from md2steam import markdown_to_steam_bbcode

md_text = """
# Пример заголовка

Текст с **жирным**, *курсивом* и [ссылкой](https://example.com).
"""

bbcode_text = markdown_to_steam_bbcode(md_text)
print(bbcode_text)
```