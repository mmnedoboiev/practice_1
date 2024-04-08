-- Dumping structure for таблиця public.tbl_notes
CREATE TABLE IF NOT EXISTS "tbl_notes" (
	"id" INTEGER NOT NULL DEFAULT 'nextval(''tbl_notes_id_seq''::regclass)',
	"user_id" INTEGER NULL DEFAULT NULL,
	"title" VARCHAR NULL DEFAULT NULL,
	"description" VARCHAR NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);



-- Dumping structure for таблиця public.tbl_privilege
CREATE TABLE IF NOT EXISTS "tbl_privilege" (
	"id" INTEGER NOT NULL DEFAULT 'nextval(''tbl_privilege_id_seq''::regclass)',
	"type" VARCHAR(20) NULL DEFAULT NULL,
	"description" VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);



-- Dumping structure for таблиця public.tbl_users
CREATE TABLE IF NOT EXISTS "tbl_users" (
	"id" INTEGER NOT NULL DEFAULT 'nextval(''tbl_users_id_seq''::regclass)',
	"username" VARCHAR(20) NULL DEFAULT NULL,
	"email" VARCHAR(50) NULL DEFAULT NULL,
	"join_date" DATE NULL DEFAULT NULL,
	"password" VARCHAR(20) NULL DEFAULT NULL,
	"address" VARCHAR(100) NULL DEFAULT NULL,
	"education" VARCHAR(100) NULL DEFAULT NULL,
	"country" VARCHAR(100) NULL DEFAULT NULL,
	"state" VARCHAR(100) NULL DEFAULT NULL,
	"phone" VARCHAR(24) NULL DEFAULT NULL,
	"lastname" VARCHAR(40) NULL DEFAULT NULL,
	"firstname" VARCHAR(40) NULL DEFAULT NULL,
	"is_deleted" INTEGER NULL DEFAULT NULL,
	"id_privilege" INTEGER NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);
