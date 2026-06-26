-- DuckDB
-- 1. Очистить eis_id: оставить только цифры (извлечь первую группу цифр)
UPDATE consumers
SET eis_id = regexp_extract(eis_id, '(\d+)', 1)
WHERE eis_id IS NOT NULL AND regexp_matches(eis_id, '[^0-9]');

-- 2. Проверить, что остались только корректные ID
SELECT COUNT(*) FROM consumers WHERE eis_id IS NOT NULL AND NOT regexp_matches(eis_id, '^[0-9]+$');
-- должно вернуть 0
