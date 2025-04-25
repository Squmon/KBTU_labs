
CREATE OR REPLACE PROCEDURE insert_or_update_user(username TEXT, userphone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE contact_name = username) THEN
        UPDATE contacts SET phone = userphone WHERE contact_name = username;
    ELSE
        INSERT INTO contacts(contact_name, phone) VALUES (username, userphone);
    END IF;
END;
$$;
