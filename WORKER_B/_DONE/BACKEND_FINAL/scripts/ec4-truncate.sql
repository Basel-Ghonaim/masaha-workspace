-- Empties every table of masaha_b_test but the migrations' (as the test lane's reset does).
DO $$ DECLARE t text; BEGIN
  SELECT string_agg(format('%I', tablename), ', ') INTO t FROM pg_tables
    WHERE schemaname = 'public' AND tablename <> '_prisma_migrations';
  EXECUTE 'TRUNCATE ' || t || ' RESTART IDENTITY CASCADE';
END $$;
