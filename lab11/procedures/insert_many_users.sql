
CREATE OR REPLACE PROCEDURE insert_many_users(users TEXT[][], OUT invalid_users TEXT[][])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
    user_name TEXT;
    user_phone TEXT;
BEGIN
    invalid_users := ARRAY[]::TEXT[][];
    WHILE i <= array_length(users, 1) LOOP
        user_name := users[i][1];
        user_phone := users[i][2];
        IF user_phone ~ '^\d{3}-\d{2}-\d{2}$' OR user_phone ~ '^\d+$' THEN
            CALL insert_or_update_user(user_name, user_phone);
        ELSE
            invalid_users := array_append(invalid_users, ARRAY[user_name, user_phone]);
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;
