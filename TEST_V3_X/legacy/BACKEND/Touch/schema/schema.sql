
-- in case you want to run this again and again:
-- DROP TABLE IF EXISTS scheduled_messages;
-- DROP TYPE IF EXISTS enum_status;

CREATE TYPE enum_status AS ENUM ('pending', 'sent', 'failed');

CREATE TABLE scheduled_messages (
    id UUID PRIMARY KEY DEFAULT uuidv4(),
    email TEXT NOT NULL,
    prompt TEXT NOT NULL,
    execute_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    job_status enum_status NOT NULL DEFAULT 'pending'
);

-- we can later add usernames and relevant users table for logins and stuff. But later, not now.
-- even if the technical scope of this project does not meet what the product delivers it creates a strong CRUD playground and framework we can implement to any ideas.