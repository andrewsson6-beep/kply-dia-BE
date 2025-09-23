-- ============================================================================
-- ALTER TABLE SCRIPT: Add 'kply_' prefix to existing tables
-- ============================================================================
-- This script renames existing tables in your Supabase database to match
-- the table names defined in your SQLAlchemy models.
--
-- IMPORTANT: Run this script in your Supabase SQL Editor
-- Make sure to backup your database before running this script!
-- ============================================================================

-- Enable case-sensitive mode for PostgreSQL (if needed)
-- SET standard_conforming_strings = on;

-- 1. System/Auth tables
-- ============================================================================
ALTER TABLE IF EXISTS system_users RENAME TO kply_system_users;
ALTER TABLE IF EXISTS roles RENAME TO kply_roles;

-- 2. Location/Organizational tables
-- ============================================================================
ALTER TABLE IF EXISTS foranes RENAME TO kply_foranes;
ALTER TABLE IF EXISTS parishes RENAME TO kply_parishes;
ALTER TABLE IF EXISTS communities RENAME TO kply_communities;

-- 3. People and Institution tables
-- ============================================================================
ALTER TABLE IF EXISTS families RENAME TO kply_families;
ALTER TABLE IF EXISTS individuals RENAME TO kply_individuals;
ALTER TABLE IF EXISTS institutions RENAME TO kply_institutions;

-- 4. Contribution tables
-- ============================================================================
ALTER TABLE IF EXISTS family_contributions RENAME TO kply_family_contributions;
ALTER TABLE IF EXISTS individual_contributions RENAME TO kply_individual_contributions;
ALTER TABLE IF EXISTS institution_contributions RENAME TO kply_institution_contributions;

-- 5. Media tables
-- ============================================================================
ALTER TABLE IF EXISTS photos RENAME TO kply_photos;

-- ============================================================================
-- Update Foreign Key Constraints (if they exist and reference old table names)
-- ============================================================================
-- Note: PostgreSQL automatically updates foreign key references when tables are renamed,
-- but if you have any custom constraints or views, you might need to update them manually.

-- ============================================================================
-- Verification Query
-- ============================================================================
-- Run this query after executing the above statements to verify all tables have the kply_ prefix:
-- 
-- SELECT table_name 
-- FROM information_schema.tables 
-- WHERE table_schema = 'public' 
--   AND table_type = 'BASE TABLE'
--   AND table_name LIKE 'kply_%'
-- ORDER BY table_name;

-- ============================================================================
-- ROLLBACK SCRIPT (if needed)
-- ============================================================================
-- If you need to rollback these changes, uncomment and run the following:
--
-- ALTER TABLE IF EXISTS kply_system_users RENAME TO system_users;
-- ALTER TABLE IF EXISTS kply_roles RENAME TO roles;
-- ALTER TABLE IF EXISTS kply_foranes RENAME TO foranes;
-- ALTER TABLE IF EXISTS kply_parishes RENAME TO parishes;
-- ALTER TABLE IF EXISTS kply_communities RENAME TO communities;
-- ALTER TABLE IF EXISTS kply_families RENAME TO families;
-- ALTER TABLE IF EXISTS kply_individuals RENAME TO individuals;
-- ALTER TABLE IF EXISTS kply_institutions RENAME TO institutions;
-- ALTER TABLE IF EXISTS kply_family_contributions RENAME TO family_contributions;
-- ALTER TABLE IF EXISTS kply_individual_contributions RENAME TO individual_contributions;
-- ALTER TABLE IF EXISTS kply_institution_contributions RENAME TO institution_contributions;
-- ALTER TABLE IF EXISTS kply_photos RENAME TO photos;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================