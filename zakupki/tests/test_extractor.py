
from extractor import parse_common_data

COMMON_INFO_SAMPLE_HTML_FULL = """
<html>
  <body>
    <div class="cardMainInfo__section">
      <span class="cardMainInfo__title">Единица измерения — кг</span>
      <span class="cardMainInfo__content">Масса</span>
    </div>
    <div class="cardMainInfo__section">
      <span class="cardMainInfo__title">Обновлено</span>
      <span class="cardMainInfo__content">2025-08-01</span>
    </div>
    <section class="blockInfo__section">
      <span class="section__title">Указание дополнительных характеристик запрещено</span>
      <span class="section__info">Да</span>
    </section>
  </body>
</html>
"""

COMMON_INFO_SAMPLE_HTML_MISSING = """
<html>
  <body>
    <div class="cardMainInfo__section">
      <span class="cardMainInfo__title">Единица измерения</span>
      <!-- missing content -->
    </div>
  </body>
</html>
"""

def test_get_common_data_full():
    data = parse_common_data(COMMON_INFO_SAMPLE_HTML_FULL)
    assert data['name'] == "Масса"
    assert data['unit'] == "кг"
    assert data['dateUpdate'] == "2025-08-01"
    assert data['ownCharsIsForbidden'] is True

def test_get_common_data_missing_elements():
    data = parse_common_data(COMMON_INFO_SAMPLE_HTML_MISSING)
    assert data['name'] is None
    assert data['ownCharsIsForbidden'] is None
