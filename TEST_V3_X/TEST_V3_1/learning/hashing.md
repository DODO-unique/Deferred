Hashing is basically irreversible scrambling of data. 
Once hashed it cannot be turned back.

You take a password -> hash it -> store the digest
again, when verifying -> hash it -> compare to stored. If match -> verified, if not -> not verified.

Now, say if a hacker gets a hold of the digest, they can't reverse it. But they can use it to verify.
They can compare it to a list of common passwords and see if they match. 
Or, they can use a rainbow table to find the password.

What is a rainbow table though?
Imagine bruteforcing on the hash just to find relevant password-
You take a plaintext -> hash it -> compare, next. Over and over again.

So instead of letting go of those hashes, we can store them for future.
for example say you have `pass123` -> hash it -> `a1b2c3` store this hash.
if in future you get hashes again, you can compare with these stored hashes to find relevant password. This is a dictionary attack.

the problem with dictionary attacks is: memory. Millions of hashes can be space intensive.
So how do you reduce the space?
You make the hash go through a reduction function. This makes digest plaintext again... almost plaintext, at least. comprehensible kind.
```
start: "hello"

→ hash → H1  
→ reduce → P1  
→ hash → H2  
→ reduce → P2  
→ hash → H3  

store only:
"hello" → H3
```

Now, you only store the one reduction function and H3 digest 

say you get H2 digest- you simply apply reduction function, make it P2, hash it, it becomes H3.

reduction function are different, so ... different 'colors'... so rainbow 🧍‍♂️.

How do I avoid it?
Add salt.

`password + random_salt → hash`

now hash does not correspond to the same password. Say two users have the same password, if they have different salt they would have different hash. So compairing plaintext with hash becomes pointless. You need salt too... and you do get salt, since it is a part of the digest now, but its a pain to keep salt rainbow tables.

Also, bcrypt is very slow- so sha256 can do billions of hashes in a second. bcrypt is 2^cost rounds, so think if your cost is 10, it takes ~50-100/sec. for 12 (default) it is ~5-20/sec. for 14 it is ~1-5/sec. 
Bruteforcing also becomes a pain. 