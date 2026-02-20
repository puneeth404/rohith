-- FILE: migrations/001_add_compliance_tables.sql

-- Add new columns to existing reports table (if it existed prior to V2)
-- SQLite doesn't support adding multiple columns in one ALTER TABLE, so we do them one by one.
-- NOTE: In production SQLite, migration tools like Alembic are preferred.
-- Assuming table 'reports' exists. If initializing fresh, the report_history.py handles creation.

ALTER TABLE reports ADD COLUMN pdf_path TEXT;
ALTER TABLE reports ADD COLUMN approved_by TEXT;
ALTER TABLE reports ADD COLUMN approved_date TIMESTAMP;
ALTER TABLE reports ADD COLUMN report_version INTEGER DEFAULT 1;

-- Create compliance tracking table
CREATE TABLE IF NOT EXISTS compliance_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER,
    action TEXT,
    performed_by TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(report_id) REFERENCES reports(id)
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_client_id ON reports(client_id);
CREATE INDEX IF NOT EXISTS idx_compliance_report_id ON compliance_log(report_id);
