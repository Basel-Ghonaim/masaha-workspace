ALTER TABLE "visits" ADD CONSTRAINT "visits_write_off_check"
  CHECK (
    ("written_off_at" IS NULL) = ("written_off_by_id" IS NULL)
    AND ("written_off_at" IS NULL) = ("write_off_reason" IS NULL)
    AND ("write_off_reason" IS NULL OR btrim("write_off_reason") <> '')
    AND ("written_off_at" IS NULL OR ("checked_out_at" IS NOT NULL AND "charge_agorot" IS NOT NULL))
  );
