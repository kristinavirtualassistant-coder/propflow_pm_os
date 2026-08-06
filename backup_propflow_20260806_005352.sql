BEGIN TRANSACTION;
CREATE TABLE financial_records (
	id VARCHAR NOT NULL, 
	owner_name VARCHAR NOT NULL, 
	property_address VARCHAR NOT NULL, 
	gross_rent FLOAT NOT NULL, 
	management_fee_pct FLOAT, 
	reserve_fund_pct FLOAT, 
	maintenance_deductions FLOAT, 
	month_year VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "financial_records" VALUES('fin_01','Apex Lone Star Holdings LLC','4500 Congress Ave',14500.0,0.08,0.05,350.0,'August 2026');
INSERT INTO "financial_records" VALUES('fin_02','Apex Lone Star Holdings LLC','1204 East 6th St',8200.0,0.08,0.05,120.0,'August 2026');
INSERT INTO "financial_records" VALUES('fin_03','Apex Lone Star Holdings LLC','8804 South Lamar Blvd',5800.0,0.08,0.05,0.0,'August 2026');
CREATE TABLE leads (
	id VARCHAR NOT NULL, 
	address VARCHAR NOT NULL, 
	city VARCHAR NOT NULL, 
	owner VARCHAR NOT NULL, 
	type VARCHAR NOT NULL, 
	equity VARCHAR NOT NULL, 
	tags JSON, 
	phones JSON, 
	PRIMARY KEY (id)
);
INSERT INTO "leads" VALUES('lead_a81f3c','4500 Congress Ave','Austin, TX','Apex Lone Star Holdings LLC','LLC',',000','["ABSENTEE_OWNER", "HIGH_EQUITY"]','["+1 (512) 555-0199"]');
INSERT INTO "leads" VALUES('lead_b92e4d','8804 South Lamar Blvd','Austin, TX','Robert Miller','INDIVIDUAL',',000','["VACANT", "TAX_DELINQUENT"]','["+1 (737) 555-0142"]');
CREATE TABLE work_orders (
	id VARCHAR NOT NULL, 
	property_address VARCHAR NOT NULL, 
	unit VARCHAR, 
	title VARCHAR NOT NULL, 
	description TEXT NOT NULL, 
	priority VARCHAR, 
	status VARCHAR, 
	created_at VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO "work_orders" VALUES('wo_101','1204 East 6th St','Apt 2B','HVAC Unit Making Loud Buzzing Sound','AC unit isn''t cooling effectively.','HIGH','IN_PROGRESS','2026-08-06 00:18');
INSERT INTO "work_orders" VALUES('wo_102','4500 Congress Ave','Suite 100','Main Entrance Door Lock Sticking','Keycard latch fails to engage.','MEDIUM','OPEN','2026-08-06 00:18');
INSERT INTO "work_orders" VALUES('wo_fc50','4500 Congress Ave','Suite 100','HVAC System Failure','Main cooling unit stopped functioning.','HIGH','OPEN','2026-08-06 00:42');
CREATE INDEX ix_leads_id ON leads (id);
CREATE INDEX ix_work_orders_id ON work_orders (id);
CREATE INDEX ix_financial_records_id ON financial_records (id);
COMMIT;
