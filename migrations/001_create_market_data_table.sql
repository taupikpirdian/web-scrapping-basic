-- Migration: Create market_data table
-- Description: Table untuk menyimpan data hasil scraping harga saham dari Katadata
-- Created: 2025-01-22

-- Create market_data table
CREATE TABLE IF NOT EXISTS market_data (
    -- Primary key
    id BIGSERIAL PRIMARY KEY,

    -- Informasi emiten
    emiten VARCHAR(10) NOT NULL,
    url TEXT NOT NULL,

    -- Timestamp
    date_time_scraping TIMESTAMP WITH TIME ZONE NOT NULL,
    last_update_text TIMESTAMP WITH TIME ZONE,

    -- Data harga
    price NUMERIC(18, 2),
    high_price NUMERIC(18, 2),
    low_price NUMERIC(18, 2),
    last_price NUMERIC(18, 2),
    open_price NUMERIC(18, 2),

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT market_data_emiten_check CHECK (emiten ~* '^[A-Z]{4,6}$')
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_market_data_emiten ON market_data(emiten);
CREATE INDEX IF NOT EXISTS idx_market_data_date_time_scraping ON market_data(date_time_scraping DESC);
CREATE INDEX IF NOT EXISTS idx_market_data_emiten_date ON market_data(emiten, date_time_scraping DESC);
CREATE INDEX IF NOT EXISTS idx_market_data_last_update ON market_data(last_update_text DESC);

-- Add comments for documentation
COMMENT ON TABLE market_data IS 'Tabel untuk menyimpan data hasil scraping harga saham';
COMMENT ON COLUMN market_data.id IS 'Primary key auto-increment';
COMMENT ON COLUMN market_data.emiten IS 'Kode saham emiten (contoh: BBCA, INDF)';
COMMENT ON COLUMN market_data.url IS 'URL sumber data scraping';
COMMENT ON COLUMN market_data.date_time_scraping IS 'Waktu ketika scraping dilakukan';
COMMENT ON COLUMN market_data.last_update_text IS 'Waktu update terakhir dari sumber data';
COMMENT ON COLUMN market_data.price IS 'Harga saham saat ini';
COMMENT ON COLUMN market_data.high_price IS 'Harga tertinggi';
COMMENT ON COLUMN market_data.low_price IS 'Harga terendah';
COMMENT ON COLUMN market_data.last_price IS 'Harga terakhir';
COMMENT ON COLUMN market_data.open_price IS 'Harga pembukaan';
COMMENT ON COLUMN market_data.created_at IS 'Waktu record dibuat di database';
COMMENT ON COLUMN market_data.updated_at IS 'Waktu record terakhir diupdate';

-- Create trigger for automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_market_data_updated_at
    BEFORE UPDATE ON market_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create view untuk get latest data per emiten
CREATE OR REPLACE VIEW v_latest_market_data AS
SELECT DISTINCT ON (emiten)
    id,
    emiten,
    url,
    date_time_scraping,
    last_update_text,
    price,
    high_price,
    low_price,
    last_price,
    open_price,
    created_at,
    updated_at
FROM market_data
ORDER BY emiten, date_time_scraping DESC;

COMMENT ON VIEW v_latest_market_data IS 'View untuk mendapatkan data terbaru per emiten';
