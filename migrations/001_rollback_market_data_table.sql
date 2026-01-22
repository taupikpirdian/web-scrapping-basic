-- Migration Rollback: Drop market_data table
-- Description: Rollback migration untuk menghapus market_data table
-- Created: 2025-01-22

-- Drop trigger
DROP TRIGGER IF EXISTS update_market_data_updated_at ON market_data;

-- Drop function
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Drop view
DROP VIEW IF EXISTS v_latest_market_data;

-- Drop indexes
DROP INDEX IF EXISTS idx_market_data_emiten;
DROP INDEX IF EXISTS idx_market_data_date_time_scraping;
DROP INDEX IF EXISTS idx_market_data_emiten_date;
DROP INDEX IF EXISTS idx_market_data_last_update;

-- Drop table
DROP TABLE IF EXISTS market_data;
