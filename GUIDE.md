# PrepLab Guide

**The target environment for Data & Applications Security, Sessions 1 to 12.**

Everything in PrepLab runs on your own machine inside Docker. You own it, which
means testing it is authorised. Never point these techniques at any other system
without written permission: an unauthorised scan is unauthorised access under the
Criminal Justice (Offences Relating to Information Systems) Act 2017.

---

## Starting and stopping

From this `lab/` folder:

```bash
docker compose up -d      # start
docker compose ps         # check all three containers are running
docker compose down       # stop
docker compose down -v    # stop and remove data
```

| Service | URL | What it is |
|---|---|---|
| `web` | http://localhost:8080 | Application tier (deliberately weak) |
| `files` | http://localhost:8081 | Unauthenticated static file share |
| `db` | localhost:5432 | PostgreSQL, published to the host |

Check it is working: `curl http://localhost:8080/health` should return
`{"status":"ok"}`.

---

## What is deliberately wrong

Do not read this section before Session 3. Work it out yourself first: finding
them is the skill being assessed. Use it afterwards to check your coverage.

<details>
<summary>Click to reveal the planted weaknesses</summary>

| # | Weakness | Session it lands in |
|---|---|---|
| 1 | Secrets in environment and source, never rotated | 5 |
| 2 | Passwords stored as fast unsalted SHA-256 | 5 |
| 3 | Every account is admin: no least privilege | 6 |
| 4 | Session cookie without HttpOnly, Secure or SameSite | 6 |
| 5 | Insecure direct object reference on `/record/<id>` | 8 |
| 6 | Unauthenticated `/debug` endpoint leaking config | 8 |
| 7 | Debug mode on, bound to all interfaces | 3 |
| 8 | Database port published to the host | 3, 4 |
| 9 | File share with no authentication | 4, 9 |
| 10 | Backups unencrypted, restore never tested | 9 |
| 11 | Flat network reachability between tiers | 9 |

</details>

---

## Session by session

| Session | What you do with PrepLab |
|---|---|
| 1 | Bring it up; map the attack surface |
| 3 | Assess what the controls can and cannot see |
| 4 | Test whether the separation actually holds |
| 5 | Find the keys and secrets; check what encryption defends against |
| 6 | Review accounts, privileges and cookie flags |
| 7 | Map shared responsibility; find what is publicly reachable |
| 8 | Assess against OWASP ASVS and a CIS benchmark |
| 9 | Classify the data; map where copies exist; redesign |
| 11 | Run your chosen testing and verify every finding |
| 12 | Report on everything you found |

---

## Troubleshooting

**Port already in use.** Something else is on 8080, 8081 or 5432. Either stop it,
or change the left-hand number in `docker-compose.yml` (for example `8090:5000`).

**`docker compose` not found.** You have an older Docker. Try `docker-compose`
with a hyphen, or update Docker Desktop.

**Containers keep restarting.** Run `docker compose logs web` to see why. The most
common cause is a typo introduced while editing `app.py`.

**Nothing on localhost.** On Docker Desktop, confirm the engine is actually
running (the whale icon should be steady, not animating).

---

## A note on safety

PrepLab contains no malware and no real personal data. The "staff list" and
"backup notes" are invented. The weaknesses are ordinary configuration and coding
mistakes of the kind found in real assessments, chosen because they are
instructive rather than dangerous.
