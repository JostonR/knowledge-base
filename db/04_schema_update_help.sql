CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sources_updated_at
BEFORE UPDATE ON source
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

SELECT COUNT(*) AS null_updated_at
FROM source
WHERE updated_at IS NULL;