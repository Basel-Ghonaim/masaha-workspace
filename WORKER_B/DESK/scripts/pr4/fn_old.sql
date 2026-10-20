CREATE OR REPLACE FUNCTION "payments_guard_insert"() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
  due integer;
  paid bigint;
BEGIN
  IF NEW."voided_at" IS NOT NULL THEN
    RAISE EXCEPTION 'payments_void_once: a payment is recorded first, then voided'
      USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_void_once';
  END IF;

  IF NEW."visit_id" IS NOT NULL THEN
    SELECT "charge_agorot" INTO due FROM "visits" WHERE "id" = NEW."visit_id" FOR UPDATE;
    -- An unknown item is left to its foreign key.
    IF NOT FOUND THEN RETURN NEW; END IF;
    IF due IS NULL THEN
      RAISE EXCEPTION 'payments_visit_uncharged: a visit is paid once its charge is set'
        USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_visit_uncharged';
    END IF;
  ELSE
    SELECT CASE WHEN "billing" = 'FIXED' THEN "price_agorot" END INTO due
      FROM "subscriptions" WHERE "id" = NEW."subscription_id" FOR UPDATE;
    IF NOT FOUND OR due IS NULL THEN RETURN NEW; END IF;
  END IF;

  -- A retried request is left to its unique key, so the service can return the first payment.
  IF EXISTS (SELECT 1 FROM "payments"
             WHERE "space_id" = NEW."space_id" AND "request_id" = NEW."request_id") THEN
    RETURN NEW;
  END IF;

  SELECT COALESCE(sum("amount_agorot"), 0) INTO paid FROM "payments"
    WHERE "voided_at" IS NULL
      AND ("visit_id" = NEW."visit_id" OR "subscription_id" = NEW."subscription_id");
  IF paid + NEW."amount_agorot" > due THEN
    RAISE EXCEPTION 'payments_within_due: % agorot would exceed the % due (% paid)',
        NEW."amount_agorot", due, paid
      USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_within_due';
  END IF;
  RETURN NEW;
END;
$$;
