CREATE TABLE "tbl_users" (
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
	PRIMARY KEY ("id")
)
;
COMMENT ON COLUMN "tbl_users"."id" IS '';
COMMENT ON COLUMN "tbl_users"."username" IS '';
COMMENT ON COLUMN "tbl_users"."email" IS '';
COMMENT ON COLUMN "tbl_users"."join_date" IS '';
COMMENT ON COLUMN "tbl_users"."password" IS '';
COMMENT ON COLUMN "tbl_users"."address" IS '';
COMMENT ON COLUMN "tbl_users"."education" IS '';
COMMENT ON COLUMN "tbl_users"."country" IS '';
COMMENT ON COLUMN "tbl_users"."state" IS '';
COMMENT ON COLUMN "tbl_users"."phone" IS '';
COMMENT ON COLUMN "tbl_users"."lastname" IS '';
COMMENT ON COLUMN "tbl_users"."firstname" IS '';



INSERT INTO "tbl_users" ("id", "username", "email", "join_date", "password", "address", "education", "country", "state", "phone", "lastname", "firstname") VALUES
	(3, 'test3', NULL, NULL, 'test', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(4, 'test', NULL, '2024-02-26', 'test', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(5, 'test2', NULL, NULL, 'test2', 'шевченка', '', 'Україна', 'область', '0971111111', 'first', 'last'),
	(1, 'work', '@gmail.com', '2024-02-26', 'test', 'шевченка', '', 'Україна', 'область', '0971111111', 'first', 'last');
/*!40000 ALTER TABLE "tbl_users" ENABLE KEYS */;