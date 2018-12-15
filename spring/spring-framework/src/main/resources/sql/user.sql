CREATE SEQUENCE "public"."seq_t_e_user"
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 200000000000
CACHE 1;
SELECT setval('"public"."seq_t_e_user"', 200000000000, false);
ALTER SEQUENCE "public"."seq_t_e_user" OWNER TO "aischool";

CREATE TABLE t_e_user (
  id INTEGER NOT NULL,
  username varchar(255) NOT NULL,
  address varchar(255) DEFAULT NULL,
  PRIMARY KEY ("id")
);