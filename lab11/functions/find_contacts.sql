
CREATE OR REPLACE FUNCTION find_contacts(pattern TEXT)
RETURNS TABLE(contact_id INT, contact_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    WHERE contact_name ILIKE '%' || pattern || '%' 
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
