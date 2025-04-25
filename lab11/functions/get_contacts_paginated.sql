
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(contact_id INT, contact_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    ORDER BY contact_id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
