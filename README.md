# ghost_key

An educational Python tool that demonstrates how password cracking works, from targeted profile attacks to dictionary attacks to brute force.

---

## Background

I started ghost_key as a personal project for my Boot.dev course. With a growing interest in security I saw it as both a course deliverable and a genuine opportunity to learn about password cracking in real world scenarios. Armed with Computerphile's extensive library and a curiosity I couldn't ignore, I set out to understand the fundamentals before building anything. With the concepts down, ghost_key was born.

---

## Why it exists

Most people don't realize how vulnerable their passwords are until they see an attack in real time. ghost_key was built to make that visible.

During development, watching `password123` crack in under a second from a 14 million entry wordlist was eye opening. Watching `*7¡Vamos!`, the last entry in rockyou.txt, fall at attempt 14,344,391 in 7 seconds made it visceral. These aren't hypothetical attacks. rockyou.txt is 14 million real passwords from a real breach. The patterns are depressingly predictable.

Understanding how attackers approach credential cracking is foundational security knowledge. You can't defend against attacks you don't understand mechanically.

---

## The math that puts it in perspective

```
lowercase only, 6 chars  →  ~309 million combinations
lowercase only, 8 chars  →  ~208 billion combinations  →  gave up after 20 seconds in Python
```

Each extra character multiplies the search space by 26. Length is the single most important factor in password strength, not complexity, not symbols, just pure length.

Pure Python manages roughly 1-5 million attempts per second. Real tools like hashcat operate at billions of attempts per second on consumer GPU hardware, the same GPU sitting in a gaming PC. That gap is why algorithm choice matters as much as password strength.

---

## The OSINT angle

> _(Target profile mode is currently in development — this section will be updated on completion)_

You don't need to brute force blindly. A motivated attacker who knows your name and rough age doesn't search quadrillions of combinations, they build a targeted wordlist. Name variations, birth years, pet names, favorite teams, all freely available on public social media. A targeted wordlist of 50,000 candidates collapses what would take years down to seconds.

ghost_key's target profile mode demonstrates exactly this. Enter a name, birth year, and a few keywords; the tool generates likely password candidates and runs them first before falling back to rockyou.txt.

---

## Features

- **Target profile mode** — generates a targeted wordlist from known information about a target _(in development)_
- **Dictionary attack** — runs rockyou.txt against a target hash
- **Brute force** — exhaustive search with configurable character sets and length
- **Auto hash detection** — detects MD5 vs SHA256 from hash length automatically
- **Attempt counter and elapsed time** — on all attack modes

---

## How it works

Everything comes down to one loop:

```
take a guess  →  hash it  →  does it match the target hash?  →  yes: cracked / no: next guess
```

Three escalating attack modes, fastest and most targeted first:

```
target profile  →  dictionary (rockyou.txt)  →  brute force
```

---

## Ethical note

ghost_key was built for educational purposes only. Building it taught me how hashing works, why weak passwords are dangerous, and how attackers think. Use it only against hashes you generated yourself. Don't be a bad actor.

If this tool makes you update your passwords and turn on a password manager, good. Randomly generated passwords have no OSINT profile. There's nothing to research. You're back to billions of years in Python.
