ENUM is a good practice. It acts as labels/tags you can use, like in Notion.

users instead of user because user is a keyword in Postgres SQL.

userID is uuid v7() (a very recent thing). It creates random IDs based on current time- they still look random, take less time than v4. Also, UUID is only 16 byte, while a text string can take 36 byte space.

JSONB is for JSON blocks. You can even filter by the contents of this block with the `->>` operator.

