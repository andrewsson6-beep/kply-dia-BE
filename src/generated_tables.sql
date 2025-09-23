-- ============================================================================
-- KPLY DIALYSIS PROJECT - AUTO-GENERATED TABLE CREATION SCRIPT
-- Generated from SQLAlchemy models on 339111.5544397
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
-- ============================================================================

-- Table: kply_roles

CREATE TABLE IF NOT EXISTS kply_roles (
	rol_id SERIAL NOT NULL, 
	rol_name VARCHAR(100) NOT NULL, 
	rol_description VARCHAR(500), 
	rol_is_deleted BOOLEAN, 
	rol_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	rol_created_by INTEGER, 
	rol_updated_at TIMESTAMP WITH TIME ZONE, 
	rol_updated_by INTEGER, 
	PRIMARY KEY (rol_id), 
	UNIQUE (rol_name)
)

;

-- Table: kply_system_users

CREATE TABLE IF NOT EXISTS kply_system_users (
	usr_id SERIAL NOT NULL, 
	usr_username VARCHAR(100) NOT NULL, 
	usr_password_hash TEXT NOT NULL, 
	usr_email VARCHAR(255) NOT NULL, 
	usr_full_name VARCHAR(255), 
	usr_rol_id INTEGER NOT NULL, 
	usr_status VARCHAR(20), 
	usr_is_deleted BOOLEAN, 
	usr_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	usr_created_by INTEGER, 
	usr_updated_at TIMESTAMP WITH TIME ZONE, 
	usr_updated_by INTEGER, 
	PRIMARY KEY (usr_id), 
	UNIQUE (usr_username), 
	UNIQUE (usr_email), 
	FOREIGN KEY(usr_rol_id) REFERENCES kply_roles (rol_id)
)

;

-- Table: kply_foranes

CREATE TABLE IF NOT EXISTS kply_foranes (
	for_id SERIAL NOT NULL, 
	for_unique_no BIGINT NOT NULL, 
	for_code VARCHAR(50), 
	for_name VARCHAR(255) NOT NULL, 
	for_location VARCHAR(255), 
	for_vicar_name VARCHAR(255), 
	for_total_contribution_amount NUMERIC(12, 2), 
	for_contact_number VARCHAR(255), 
	for_is_deleted BOOLEAN, 
	for_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	for_created_by INTEGER, 
	for_updated_at TIMESTAMP WITH TIME ZONE, 
	for_updated_by INTEGER, 
	PRIMARY KEY (for_id), 
	UNIQUE (for_unique_no), 
	UNIQUE (for_code), 
	FOREIGN KEY(for_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(for_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_parishes

CREATE TABLE IF NOT EXISTS kply_parishes (
	par_id SERIAL NOT NULL, 
	par_for_id INTEGER NOT NULL, 
	par_unique_no BIGINT NOT NULL, 
	par_code VARCHAR(50), 
	par_name VARCHAR(255) NOT NULL, 
	par_location VARCHAR(255), 
	par_vicar_name VARCHAR(255), 
	par_contact_number VARCHAR(255), 
	par_total_contribution_amount NUMERIC(12, 2), 
	par_is_deleted BOOLEAN, 
	par_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	par_created_by INTEGER, 
	par_updated_at TIMESTAMP WITH TIME ZONE, 
	par_updated_by INTEGER, 
	PRIMARY KEY (par_id), 
	FOREIGN KEY(par_for_id) REFERENCES kply_foranes (for_id), 
	UNIQUE (par_unique_no), 
	UNIQUE (par_code), 
	FOREIGN KEY(par_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(par_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_communities

CREATE TABLE IF NOT EXISTS kply_communities (
	com_id SERIAL NOT NULL, 
	com_for_id INTEGER, 
	com_par_id INTEGER, 
	com_unique_no BIGINT NOT NULL, 
	com_code VARCHAR(50), 
	com_name VARCHAR(255) NOT NULL, 
	com_total_contribution_amount NUMERIC(12, 2), 
	com_is_deleted BOOLEAN, 
	com_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	com_created_by INTEGER, 
	com_updated_at TIMESTAMP WITH TIME ZONE, 
	com_updated_by INTEGER, 
	PRIMARY KEY (com_id), 
	FOREIGN KEY(com_for_id) REFERENCES kply_foranes (for_id), 
	FOREIGN KEY(com_par_id) REFERENCES kply_parishes (par_id), 
	UNIQUE (com_unique_no), 
	UNIQUE (com_code), 
	FOREIGN KEY(com_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(com_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_families

CREATE TABLE IF NOT EXISTS kply_families (
	fam_id SERIAL NOT NULL, 
	fam_com_id INTEGER NOT NULL, 
	fam_unique_no BIGINT NOT NULL, 
	fam_code VARCHAR(50), 
	fam_house_name VARCHAR(255) NOT NULL, 
	fam_head_name VARCHAR(255) NOT NULL, 
	fam_phone_number VARCHAR(20), 
	fam_total_contribution_amount NUMERIC(12, 2), 
	fam_is_deleted BOOLEAN, 
	fam_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	fam_created_by INTEGER, 
	fam_updated_at TIMESTAMP WITH TIME ZONE, 
	fam_updated_by INTEGER, 
	PRIMARY KEY (fam_id), 
	FOREIGN KEY(fam_com_id) REFERENCES kply_communities (com_id), 
	UNIQUE (fam_unique_no), 
	UNIQUE (fam_code), 
	FOREIGN KEY(fam_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(fam_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_individuals

CREATE TABLE IF NOT EXISTS kply_individuals (
	ind_id SERIAL NOT NULL, 
	ind_unique_no BIGINT NOT NULL, 
	ind_code VARCHAR(50), 
	ind_full_name VARCHAR(255) NOT NULL, 
	ind_phone_number VARCHAR(20), 
	ind_email VARCHAR(255), 
	ind_address TEXT, 
	ind_total_contribution_amount NUMERIC(12, 2), 
	ind_is_deleted BOOLEAN, 
	ind_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	ind_created_by INTEGER, 
	ind_updated_at TIMESTAMP WITH TIME ZONE, 
	ind_updated_by INTEGER, 
	PRIMARY KEY (ind_id), 
	UNIQUE (ind_unique_no), 
	UNIQUE (ind_code), 
	FOREIGN KEY(ind_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(ind_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_institutions

CREATE TABLE IF NOT EXISTS kply_institutions (
	ins_id SERIAL NOT NULL, 
	ins_unique_no BIGINT NOT NULL, 
	ins_code VARCHAR(50), 
	ins_name VARCHAR(255) NOT NULL, 
	ins_type VARCHAR(100), 
	ins_address TEXT, 
	ins_total_contribution_amount NUMERIC(12, 2), 
	ins_phone VARCHAR(20), 
	ins_email VARCHAR(255), 
	ins_website VARCHAR(255), 
	ins_head_name VARCHAR(255), 
	ins_is_deleted BOOLEAN, 
	ins_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	ins_created_by INTEGER, 
	ins_updated_at TIMESTAMP WITH TIME ZONE, 
	ins_updated_by INTEGER, 
	PRIMARY KEY (ins_id), 
	UNIQUE (ins_unique_no), 
	UNIQUE (ins_code), 
	FOREIGN KEY(ins_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(ins_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_family_contributions

CREATE TABLE IF NOT EXISTS kply_family_contributions (
	fcon_id SERIAL NOT NULL, 
	fcon_fam_id INTEGER NOT NULL, 
	fcon_amount NUMERIC(12, 2) NOT NULL, 
	fcon_date TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	fcon_purpose VARCHAR(255), 
	fcon_is_deleted BOOLEAN, 
	fcon_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	fcon_created_by INTEGER, 
	fcon_updated_at TIMESTAMP WITH TIME ZONE, 
	fcon_updated_by INTEGER, 
	PRIMARY KEY (fcon_id), 
	FOREIGN KEY(fcon_fam_id) REFERENCES kply_families (fam_id), 
	FOREIGN KEY(fcon_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(fcon_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_individual_contributions

CREATE TABLE IF NOT EXISTS kply_individual_contributions (
	icon_id SERIAL NOT NULL, 
	icon_ind_id INTEGER NOT NULL, 
	icon_amount NUMERIC(12, 2) NOT NULL, 
	icon_date TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	icon_purpose VARCHAR(255), 
	icon_is_deleted BOOLEAN, 
	icon_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	icon_created_by INTEGER, 
	icon_updated_at TIMESTAMP WITH TIME ZONE, 
	icon_updated_by INTEGER, 
	PRIMARY KEY (icon_id), 
	FOREIGN KEY(icon_ind_id) REFERENCES kply_individuals (ind_id), 
	FOREIGN KEY(icon_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(icon_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_institution_contributions

CREATE TABLE IF NOT EXISTS kply_institution_contributions (
	incon_id SERIAL NOT NULL, 
	incon_ins_id INTEGER NOT NULL, 
	incon_amount NUMERIC(12, 2) NOT NULL, 
	incon_date TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	incon_purpose VARCHAR(255), 
	incon_is_deleted BOOLEAN, 
	incon_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	incon_created_by INTEGER, 
	incon_updated_at TIMESTAMP WITH TIME ZONE, 
	incon_updated_by INTEGER, 
	PRIMARY KEY (incon_id), 
	FOREIGN KEY(incon_ins_id) REFERENCES kply_institutions (ins_id), 
	FOREIGN KEY(incon_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(incon_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Table: kply_photos

CREATE TABLE IF NOT EXISTS kply_photos (
	pho_id SERIAL NOT NULL, 
	pho_for_id INTEGER, 
	pho_par_id INTEGER, 
	pho_com_id INTEGER, 
	pho_fam_id INTEGER, 
	pho_ins_id INTEGER, 
	pho_url TEXT NOT NULL, 
	pho_caption VARCHAR(255), 
	pho_is_primary BOOLEAN, 
	pho_is_deleted BOOLEAN, 
	pho_created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	pho_created_by INTEGER, 
	pho_updated_at TIMESTAMP WITH TIME ZONE, 
	pho_updated_by INTEGER, 
	PRIMARY KEY (pho_id), 
	FOREIGN KEY(pho_for_id) REFERENCES kply_foranes (for_id), 
	FOREIGN KEY(pho_par_id) REFERENCES kply_parishes (par_id), 
	FOREIGN KEY(pho_com_id) REFERENCES kply_communities (com_id), 
	FOREIGN KEY(pho_fam_id) REFERENCES kply_families (fam_id), 
	FOREIGN KEY(pho_ins_id) REFERENCES kply_institutions (ins_id), 
	FOREIGN KEY(pho_created_by) REFERENCES kply_system_users (usr_id), 
	FOREIGN KEY(pho_updated_by) REFERENCES kply_system_users (usr_id)
)

;

-- Performance Indexes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_kply_system_users_email ON kply_system_users(usr_email);
CREATE INDEX IF NOT EXISTS idx_kply_system_users_username ON kply_system_users(usr_username);
CREATE INDEX IF NOT EXISTS idx_kply_system_users_role ON kply_system_users(usr_rol_id);
CREATE INDEX IF NOT EXISTS idx_kply_parishes_forane ON kply_parishes(par_for_id);
CREATE INDEX IF NOT EXISTS idx_kply_communities_parish ON kply_communities(com_par_id);
CREATE INDEX IF NOT EXISTS idx_kply_communities_forane ON kply_communities(com_for_id);
CREATE INDEX IF NOT EXISTS idx_kply_families_community ON kply_families(fam_com_id);
CREATE INDEX IF NOT EXISTS idx_kply_families_unique_no ON kply_families(fam_unique_no);
CREATE INDEX IF NOT EXISTS idx_kply_individuals_unique_no ON kply_individuals(ind_unique_no);
CREATE INDEX IF NOT EXISTS idx_kply_individuals_email ON kply_individuals(ind_email);
CREATE INDEX IF NOT EXISTS idx_kply_institutions_unique_no ON kply_institutions(ins_unique_no);
CREATE INDEX IF NOT EXISTS idx_kply_family_contributions_family ON kply_family_contributions(fcon_fam_id);
CREATE INDEX IF NOT EXISTS idx_kply_individual_contributions_individual ON kply_individual_contributions(icon_ind_id);
CREATE INDEX IF NOT EXISTS idx_kply_institution_contributions_institution ON kply_institution_contributions(incon_ins_id);
CREATE INDEX IF NOT EXISTS idx_kply_photos_forane ON kply_photos(pho_for_id);
CREATE INDEX IF NOT EXISTS idx_kply_photos_parish ON kply_photos(pho_par_id);
CREATE INDEX IF NOT EXISTS idx_kply_photos_community ON kply_photos(pho_com_id);
CREATE INDEX IF NOT EXISTS idx_kply_photos_family ON kply_photos(pho_fam_id);
CREATE INDEX IF NOT EXISTS idx_kply_photos_institution ON kply_photos(pho_ins_id);

-- ============================================================================
-- END OF AUTO-GENERATED SCRIPT
-- ============================================================================
