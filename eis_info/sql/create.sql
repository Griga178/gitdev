-- 1. Последовательность для consumers
CREATE SEQUENCE IF NOT EXISTS consumer_id_seq START 1;
CREATE SEQUENCE IF NOT EXISTS order_cards_id_seq START 1;

-- 2. Таблица заказчиков
CREATE TABLE IF NOT EXISTS consumers (
    id BIGINT DEFAULT nextval('consumer_id_seq') PRIMARY KEY,
    name TEXT NOT NULL UNIQUE ,
    eis_id TEXT
);

-- 3. Таблица поставщиков
CREATE SEQUENCE IF NOT EXISTS markets_id_seq START 1;
CREATE TABLE IF NOT EXISTS markets (
    id BIGINT DEFAULT nextval('markets_id_seq') PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    inn TEXT,
    address TEXT
);

-- 4. Таблица заказов
CREATE TABLE IF NOT EXISTS order_cards (
    id BIGINT PRIMARY KEY DEFAULT nextval('order_cards_id_seq'),
    contract_number TEXT UNIQUE,
    contract_type TEXT,
    placement_date DATE NOT NULL,
    end_date DATE,
    update_date DATE,
    name TEXT,
    consumer_id BIGINT NOT NULL,
    market_id BIGINT,
    products_count INTEGER,
    total_price DECIMAL(18,2),
    status TEXT,
    FOREIGN KEY (consumer_id) REFERENCES consumers(id),
    FOREIGN KEY (market_id) REFERENCES markets(id)
);

-- 5. Таблица товаров
CREATE SEQUENCE IF NOT EXISTS products_id_seq START 1;
CREATE TABLE IF NOT EXISTS products (
    id BIGINT DEFAULT nextval('products_id_seq') PRIMARY KEY,
    card_id BIGINT NOT NULL,
    name TEXT NOT NULL,
    okpd_number TEXT,
    ktru_number TEXT,
    price DECIMAL(18,2) NOT NULL,
    measure TEXT,
    amount DECIMAL(18,3),
    chars JSON,
    FOREIGN KEY (card_id) REFERENCES order_cards(id)
);

-- 6. Таблица дат для парсера
CREATE TABLE IF NOT EXISTS parser_data (
  date DATE NOT NULL,
  card_amount INTEGER,
  card_parsed INTEGER,
  is_parsed BOOLEAN NOT NULL DEFAULT FALSE,
  queries_params JSON -- список, содержащий простые словари [{},{},...]
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_order_cards_consumer ON order_cards(consumer_id);
CREATE INDEX IF NOT EXISTS idx_order_cards_market ON order_cards(market_id);
CREATE INDEX IF NOT EXISTS idx_products_card ON products(card_id);
