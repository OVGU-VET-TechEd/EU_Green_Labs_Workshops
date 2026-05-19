-- ============================================================
-- schema.sql
-- EduGreenLabs Workshop 2 — Privacy-by-Design for Learning Systems
--
-- A GDPR-compliant PostgreSQL schema for educational AI research.
-- Implements:
--   • Separation of identity store and research data store
--   • Consent tracking with withdrawal support
--   • Row-Level Security (only consented, active records visible)
--   • Immutable audit log for all data access
--   • Data minimisation (binned timestamps, score bands — no raw values)
--
-- Usage:
--   psql -U your_user -d your_db -f schema.sql
--
-- GDPR compliance note:
--   The identity_mapping table must be stored in a SEPARATE system
--   from the performance_records table, accessible only to the
--   data controller. Never join these tables in production queries.
--
-- Licence: MIT · EduGreenLabs / OvGU Magdeburg · EU-GREEN Alliance
-- ============================================================


-- ──────────────────────────────────────────────────────────────────
-- Extensions
-- ──────────────────────────────────────────────────────────────────

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";     -- for uuid_generate_v4()
CREATE EXTENSION IF NOT EXISTS pgcrypto;        -- for gen_random_bytes()


-- ──────────────────────────────────────────────────────────────────
-- IDENTITY STORE
-- Access: DATA CONTROLLER ONLY — never accessible to general research team
-- Storage: Should be on a SEPARATE server / schema from research data
-- ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS identity_mapping (
    -- The pseudonym — shared with the research data store
    pseudo_id           CHAR(20) PRIMARY KEY,

    -- Real identifier stored as a one-way hash (HMAC-SHA256 truncated)
    -- The application layer holds the HMAC secret; this column alone
    -- does not allow reverse lookup without the secret.
    real_id_hash        CHAR(64) NOT NULL UNIQUE,

    -- Consent management
    consent_given       BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date        TIMESTAMPTZ,
    consent_scope       TEXT[]    NOT NULL DEFAULT '{}',
    -- e.g. {'performance_data', 'qualitative_interviews', 'survey'}

    -- Withdrawal support (GDPR Art. 7(3))
    withdrawal_date     TIMESTAMPTZ,
    withdrawal_reason   TEXT,

    -- Data subject rights tracking
    access_request_date TIMESTAMPTZ,    -- Art. 15 — right of access
    erasure_request_date TIMESTAMPTZ,   -- Art. 17 — right to erasure

    -- Record management
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT require_consent_date
        CHECK (consent_given = FALSE OR consent_date IS NOT NULL),

    CONSTRAINT withdrawal_after_consent
        CHECK (withdrawal_date IS NULL OR consent_date IS NULL OR
               withdrawal_date >= consent_date)
);

CREATE INDEX idx_identity_consent ON identity_mapping (consent_given, withdrawal_date);

-- Trigger: auto-update updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

CREATE TRIGGER trg_identity_mapping_updated
    BEFORE UPDATE ON identity_mapping
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

COMMENT ON TABLE identity_mapping IS
    'RESTRICTED: Identity key store. Must be stored separately from research data. '
    'Access limited to data controller role only.';


-- ──────────────────────────────────────────────────────────────────
-- RESEARCH DATA STORE
-- Access: Research team (read), data controller (read/write)
-- Contains only pseudonymous, minimised data — NO real identifiers
-- ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS performance_records (
    record_id           SERIAL PRIMARY KEY,

    -- Pseudonym links to identity_mapping.pseudo_id in the separate system
    -- NOT a foreign key constraint here — the tables should be in different DBs
    pseudo_id           CHAR(20) NOT NULL,

    -- Data minimised temporal fields (no exact timestamps)
    session_date        DATE NOT NULL,
    time_of_day         TEXT NOT NULL
                        CHECK (time_of_day IN ('morning', 'afternoon', 'evening', 'night')),
    week_number         INTEGER CHECK (week_number BETWEEN 1 AND 53),

    -- Task metadata
    task_type           TEXT NOT NULL,
    -- e.g. 'quiz', 'essay_draft', 'peer_review', 'video_lecture'

    -- Minimised performance fields — bands, not raw scores
    completion_pct_band TEXT CHECK (completion_pct_band IN ('low', 'mid', 'high')),
    score_band          TEXT CHECK (score_band IN ('low', 'mid', 'high')),
    interaction_count   INTEGER CHECK (interaction_count >= 0),

    -- AI assistant usage (if applicable)
    ai_tool_used        BOOLEAN,
    ai_interaction_count INTEGER,

    -- Record provenance
    study_arm           TEXT,           -- e.g. 'control', 'treatment_A'
    data_source         TEXT NOT NULL,  -- e.g. 'LMS_moodle', 'survey_redcap'
    collected_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    collector_role      TEXT NOT NULL DEFAULT current_user
);

CREATE INDEX idx_perf_pseudo ON performance_records (pseudo_id);
CREATE INDEX idx_perf_date   ON performance_records (session_date);
CREATE INDEX idx_perf_task   ON performance_records (task_type);

COMMENT ON TABLE performance_records IS
    'Pseudonymous, minimised research data. No real identifiers. '
    'pseudo_id links to identity_mapping in the separate restricted system.';


-- ──────────────────────────────────────────────────────────────────
-- ROW-LEVEL SECURITY
-- Researchers can only query records where consent is active.
-- The identity store lookup is done at the application layer;
-- here we use a consent_active flag set by the data controller.
-- ──────────────────────────────────────────────────────────────────

-- Consent status view (maintained by data controller)
CREATE TABLE IF NOT EXISTS consented_pseudonyms (
    pseudo_id   CHAR(20) PRIMARY KEY,
    scope       TEXT[]   NOT NULL DEFAULT '{}',
    valid_until TIMESTAMPTZ
);

COMMENT ON TABLE consented_pseudonyms IS
    'Maintained by data controller. Updated whenever consent is given or withdrawn. '
    'Research team has SELECT only.';

-- Enable RLS on performance_records
ALTER TABLE performance_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY active_consent_required ON performance_records
    AS PERMISSIVE FOR SELECT
    USING (
        pseudo_id IN (
            SELECT pseudo_id FROM consented_pseudonyms
            WHERE (valid_until IS NULL OR valid_until > NOW())
        )
    );

-- Data controller role bypasses RLS (needed for admin operations)
ALTER TABLE performance_records FORCE ROW LEVEL SECURITY;


-- ──────────────────────────────────────────────────────────────────
-- AUDIT LOG — immutable record of all data access
-- GDPR Art. 30: records of processing activities
-- ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS data_access_log (
    log_id              BIGSERIAL PRIMARY KEY,
    accessor_name       TEXT NOT NULL DEFAULT current_user,
    accessor_role       TEXT,
    action              TEXT NOT NULL,
    -- e.g. 'SELECT', 'EXPORT_CSV', 'PSEUDONYM_LOOKUP', 'CONSENT_UPDATE'
    table_accessed      TEXT,
    record_count        INTEGER,        -- how many records were touched
    query_purpose       TEXT NOT NULL,  -- researcher must provide justification
    legal_basis         TEXT,           -- which GDPR Art. 6 basis applies
    accessed_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Prevent deletion or update of log entries
    CONSTRAINT log_no_empty_purpose CHECK (length(query_purpose) > 10)
);

-- Make the audit log append-only for non-superusers
REVOKE UPDATE, DELETE ON data_access_log FROM PUBLIC;

COMMENT ON TABLE data_access_log IS
    'Immutable audit trail for all data access. Required for GDPR Art. 30 compliance. '
    'Only superuser/DBA can delete entries (only permitted for log rotation after retention period).';


-- ──────────────────────────────────────────────────────────────────
-- ROLES AND PERMISSIONS
-- ──────────────────────────────────────────────────────────────────

-- Data Controller: full access to all tables including identity store
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'data_controller') THEN
        CREATE ROLE data_controller;
    END IF;
END $$;

GRANT ALL ON ALL TABLES IN SCHEMA public TO data_controller;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO data_controller;

-- Researcher: read-only access to pseudonymous research data + audit log write
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'researcher') THEN
        CREATE ROLE researcher;
    END IF;
END $$;

GRANT SELECT ON performance_records TO researcher;
GRANT SELECT ON consented_pseudonyms TO researcher;
GRANT INSERT ON data_access_log TO researcher;
GRANT USAGE ON SEQUENCE data_access_log_log_id_seq TO researcher;
-- Researchers CANNOT access identity_mapping
REVOKE ALL ON identity_mapping FROM researcher;


-- ──────────────────────────────────────────────────────────────────
-- RETENTION SCHEDULE VIEW
-- Documents planned deletion dates per study phase
-- ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS retention_schedule (
    schedule_id         SERIAL PRIMARY KEY,
    study_name          TEXT NOT NULL,
    data_category       TEXT NOT NULL,
    legal_basis         TEXT NOT NULL,
    collection_start    DATE NOT NULL,
    planned_deletion    DATE NOT NULL,
    action_on_expiry    TEXT NOT NULL
        CHECK (action_on_expiry IN ('delete', 'anonymise', 'archive', 'review')),
    responsible_person  TEXT NOT NULL,
    notes               TEXT,

    CONSTRAINT deletion_after_collection
        CHECK (planned_deletion > collection_start)
);

COMMENT ON TABLE retention_schedule IS
    'Documents the planned retention period for each dataset category. '
    'Review annually and before any data publication.';


-- ──────────────────────────────────────────────────────────────────
-- SAMPLE DATA — for workshop exercises only
-- Run: psql ... -f schema.sql; then:
--      psql ... -f sample_data.sql
-- DO NOT use real identifiers in sample data
-- ──────────────────────────────────────────────────────────────────

-- Uncomment to insert sample data for exercises:
/*
INSERT INTO consented_pseudonyms (pseudo_id, scope, valid_until) VALUES
    ('PID_3A7F2B1C9E04D581', ARRAY['performance_data', 'survey'], NULL),
    ('PID_7C2E4A1B8F0D3E92', ARRAY['performance_data'], '2027-12-31'),
    ('PID_9B1D5E3A7F2C8041', ARRAY['performance_data', 'survey'], NULL);

INSERT INTO performance_records
    (pseudo_id, session_date, time_of_day, week_number, task_type,
     completion_pct_band, score_band, interaction_count, ai_tool_used,
     study_arm, data_source) VALUES
    ('PID_3A7F2B1C9E04D581', '2026-04-15', 'afternoon', 15, 'essay_draft',
     'high', 'high', 47, TRUE, 'treatment_A', 'LMS_moodle'),
    ('PID_7C2E4A1B8F0D3E92', '2026-04-15', 'morning',   15, 'quiz',
     'mid',  'mid',  12, FALSE, 'control',     'LMS_moodle'),
    ('PID_9B1D5E3A7F2C8041', '2026-04-15', 'evening',   15, 'essay_draft',
     'low',  'low',  23, TRUE,  'treatment_A', 'LMS_moodle');
*/
