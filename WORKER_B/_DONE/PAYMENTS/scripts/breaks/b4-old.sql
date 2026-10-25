CREATE OR REPLACE FUNCTION "payments_guard_change"() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    RAISE EXCEPTION 'payments_append_only: a payment is never deleted; void it instead'
      USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_append_only';
  END IF;
  IF OLD."voided_at" IS NOT NULL THEN
    RAISE EXCEPTION 'payments_void_once: a voided payment never changes again'
      USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_void_once';
  END IF;
  IF NEW."voided_at" IS NULL
     OR (NEW."id", NEW."space_id", NEW."request_id", NEW."visit_id", NEW."subscription_id",
         NEW."amount_agorot", NEW."method", NEW."note", NEW."recorded_by_id", NEW."received_at",
         NEW."created_at")
        IS DISTINCT FROM
        (OLD."id", OLD."space_id", OLD."request_id", OLD."visit_id", OLD."subscription_id",
         OLD."amount_agorot", OLD."method", OLD."note", OLD."recorded_by_id", OLD."received_at",
         OLD."created_at") THEN
    RAISE EXCEPTION 'payments_append_only: a payment is never updated; only voided'
      USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_append_only';
  END IF;
  RETURN NEW;
END;
$$;
