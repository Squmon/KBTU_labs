
CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE (contact_name = p_name OR p_name IS NULL)
       AND (phone = p_phone OR p_phone IS NULL);
END;
$$;
