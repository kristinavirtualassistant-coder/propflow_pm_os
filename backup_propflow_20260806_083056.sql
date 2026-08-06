BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('1197a33b3189');
CREATE TABLE audit_logs (
	id VARCHAR NOT NULL, 
	event_type VARCHAR, 
	description TEXT, 
	timestamp VARCHAR, 
	payload JSON, 
	PRIMARY KEY (id)
);
INSERT INTO "audit_logs" VALUES('audit_35fac5','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:09:21','null');
INSERT INTO "audit_logs" VALUES('audit_47d72c','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:09:21','null');
INSERT INTO "audit_logs" VALUES('audit_626ca4','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:11:26','null');
INSERT INTO "audit_logs" VALUES('audit_f2031e','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:11:26','null');
INSERT INTO "audit_logs" VALUES('audit_f448ba','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:20:54','null');
INSERT INTO "audit_logs" VALUES('audit_79cd34','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:20:54','null');
INSERT INTO "audit_logs" VALUES('audit_a2df40','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:26:00','null');
INSERT INTO "audit_logs" VALUES('audit_0e2b79','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:26:00','null');
INSERT INTO "audit_logs" VALUES('audit_5c6b05','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:30:54','null');
INSERT INTO "audit_logs" VALUES('audit_958789','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:30:54','null');
INSERT INTO "audit_logs" VALUES('audit_d664dd','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:34:34','null');
INSERT INTO "audit_logs" VALUES('audit_a92202','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:34:34','null');
INSERT INTO "audit_logs" VALUES('audit_bacc76','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:37:18','null');
INSERT INTO "audit_logs" VALUES('audit_96e09f','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:37:18','null');
INSERT INTO "audit_logs" VALUES('audit_20a93f','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 10:38:03','null');
INSERT INTO "audit_logs" VALUES('audit_2823b5','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 10:38:03','null');
INSERT INTO "audit_logs" VALUES('audit_1786012684027','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T10:38:04.027249+00:00','"{\"raw\": \"{\\\"score\\\":85}\"}"');
INSERT INTO "audit_logs" VALUES('audit_79e83c','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 11:42:09','null');
INSERT INTO "audit_logs" VALUES('audit_3c01b9','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 11:42:09','null');
INSERT INTO "audit_logs" VALUES('audit_1786016529669','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:42:09.668927+00:00','"{\"raw\": \"{\\\"score\\\":85}\"}"');
INSERT INTO "audit_logs" VALUES('audit_8545ed','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 11:43:58','null');
INSERT INTO "audit_logs" VALUES('audit_2aa4c8','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 11:43:58','null');
INSERT INTO "audit_logs" VALUES('audit_1786016638214','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:43:58.214550+00:00','"{\"raw\": \"{\\\"score\\\":85}\"}"');
INSERT INTO "audit_logs" VALUES('audit_be6e04','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 11:44:42','null');
INSERT INTO "audit_logs" VALUES('audit_a52f9d','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 11:44:42','null');
INSERT INTO "audit_logs" VALUES('audit_1786016682873','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:44:42.873398+00:00','"{\"raw\": \"{\\\"score\\\":85}\"}"');
INSERT INTO "audit_logs" VALUES('audit_a61ac0','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 11:55:15','null');
INSERT INTO "audit_logs" VALUES('audit_ba040b','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 11:55:15','null');
INSERT INTO "audit_logs" VALUES('audit_1786017315810','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:55:15.810868+00:00','"{\"raw\": \"{\\\"score\\\":85}\"}"');
INSERT INTO "audit_logs" VALUES('audit_c73d0d','STATEMENT_PDF_GENERATED','Generated Owner Statement PDF for John Doe','2026-08-06 11:56:09','null');
INSERT INTO "audit_logs" VALUES('audit_4c5926','LEASE_PDF_GENERATED','Generated official PDF lease agreement for Sarah Connor','2026-08-06 11:56:09','null');
INSERT INTO "audit_logs" VALUES('audit_1786017369115','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:56:09.115302+00:00','"{\"raw\": \"{\\\"score\\\":85}\"}"');
INSERT INTO "audit_logs" VALUES('audit_1786017493317','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:58:13.317512+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('audit_1786017539652','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T11:58:59.651984+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('audit_1786017609918','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T12:00:09.918043+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('audit_1786017669450','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T12:01:09.450174+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786017669467','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T12:01:09.467413+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786019991582','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T12:39:51.582089+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786019991601','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T12:39:51.601836+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786020062391','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T12:41:02.391860+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786020062412','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T12:41:02.412645+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786028782440','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:06:22.440128+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786028782475','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:06:22.475184+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786028947632','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:09:07.632714+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786028947664','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:09:07.664761+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786029161051','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:12:41.051842+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786029161085','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:12:41.085331+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786029487131','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:18:07.131596+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786029487150','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:18:07.150535+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786029505697','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:18:25.697584+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786029505739','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:18:25.739699+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786029525253','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:18:45.253761+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786029525272','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:18:45.272591+00:00',NULL);
INSERT INTO "audit_logs" VALUES('audit_1786029712771','LEAD_QUALIFIED','Lead scored HOT','2026-08-06T15:21:52.771429+00:00','"{\"score\": 85}"');
INSERT INTO "audit_logs" VALUES('sms_1786029712796','INBOUND_SMS_RECEIVED','SMS from +15550199: Is there any available rent unit?','2026-08-06T15:21:52.796432+00:00',NULL);
CREATE TABLE "financial_records" (
	id VARCHAR NOT NULL, 
	owner_name VARCHAR NOT NULL, 
	property_address VARCHAR NOT NULL, 
	gross_rent FLOAT NOT NULL, 
	management_fee_pct FLOAT NOT NULL, 
	reserve_fund_pct FLOAT NOT NULL, 
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
CREATE TABLE vendors (
	id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	trade VARCHAR NOT NULL, 
	phone VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	active BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO "vendors" VALUES('vnd_4b03b0','Apex Plumbing Services','PLUMBING','+15125550101','dispatch@apexplumbing.com',1);
INSERT INTO "vendors" VALUES('vnd_cfc566','Lone Star HVAC & Cooling','HVAC','+15125550102','service@lonestarhvac.com',1);
INSERT INTO "vendors" VALUES('vnd_b6b371','VoltCraft Electrical','ELECTRICAL','+15125550103','jobs@voltcraftelectrical.com',1);
INSERT INTO "vendors" VALUES('vnd_4b6e18','Austin General Contractors','GENERAL','+15125550104','contact@austincm.com',1);
CREATE TABLE "work_orders" (
	id VARCHAR NOT NULL, 
	property_address VARCHAR NOT NULL, 
	unit VARCHAR, 
	title VARCHAR NOT NULL, 
	description TEXT, 
	priority VARCHAR, 
	status VARCHAR, 
	created_at VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO "work_orders" VALUES('wo_101','1204 East 6th St','Apt 2B','HVAC Unit Making Loud Buzzing Sound','AC unit isn''t cooling effectively.','HIGH','IN_PROGRESS','2026-08-06 00:18');
INSERT INTO "work_orders" VALUES('wo_102','4500 Congress Ave','Suite 100','Main Entrance Door Lock Sticking','Keycard latch fails to engage.','MEDIUM','OPEN','2026-08-06 00:18');
INSERT INTO "work_orders" VALUES('wo_fc50','4500 Congress Ave','Suite 100','HVAC System Failure','Main cooling unit stopped functioning.','HIGH','OPEN','2026-08-06 00:42');
INSERT INTO "work_orders" VALUES('wo_4e23','1204 East 6th St','Apt 4','Severe Water Leak From Bathroom Ceiling','Water leaking through ceiling fixtures.','HIGH','OPEN',NULL);
INSERT INTO "work_orders" VALUES('wo_e637','1204 East 6th St','Apt 4','Severe Water Leak From Bathroom Ceiling','Water leaking through ceiling fixtures.','HIGH','OPEN','2026-08-06 08:12:17');
CREATE INDEX ix_audit_logs_id ON audit_logs (id);
CREATE INDEX ix_audit_logs_event_type ON audit_logs (event_type);
COMMIT;
