CREATE SEQUENCE "public"."seq_t_e_address"
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 200000000000
CACHE 1;
SELECT setval('"public"."seq_t_e_address"', 200000000000, false);
ALTER SEQUENCE "public"."seq_t_e_address" OWNER TO "aischool";

CREATE TABLE t_e_address (
  id  varchar(32) NOT NULL,
  address varchar(255) NOT NULL,
  PRIMARY KEY ("id")
);