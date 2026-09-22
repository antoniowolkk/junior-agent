---
name: migrate
description: Change a live schema or backfill data in steps that are safe to deploy and safe to stop halfway. Use for /migrate (Codex CLI: $migrate), "add a column", "rename this column", "drop this table", "backfill", "zero-downtime migration", or any change where old code and the new schema run at the same time.
---

# Migrate

Plan a schema or data change as a sequence of deploys, each of which works with the code already running. Writing the migration file is the small part; the sequence, the down path, and the rehearsal are the work.

This skill never runs a migration against anything but a local throwaway database. Everything else stops and asks.

## 0. Precedence and the stop line

`AGENTS.md` section 7 outranks this file. Two of its clauses land directly here:

- "Write to, migrate, seed, or drop any database that is not a local throwaway."
- "Delete or rename any file, directory, branch, or database table."

Both need an explicit yes from the human first, every time. A local throwaway is one you can drop and recreate from scratch with a command in this repo. Anything shared, remote, or holding data someone would miss is not a throwaway.

Writing and reviewing the migration needs no permission. Running it anywhere else does.

## 1. Name the change and its deploy count

| Change | Deploys | Why |
| --- | --- | --- |
| New table, or new nullable column | 1 | Nothing reads it yet. |
| New column with a default or `NOT NULL` | 1, after checking section 3 | May rewrite or scan the whole table. |
| Rename or retype a column | 3 | Expand, migrate, contract. Section 2. |
| Drop a column or table | 2 or more | Stop referencing it, ship that, then drop. |
| Backfill existing rows | Its own deploy | Never in the same step as the DDL. Section 5. |
| New index | Its own migration | Usually cannot share a transaction. Section 3. |

**The rule the whole skill hangs on:** between any two deploys, the schema must work with both the code currently running and the code about to run. Processes started before your deploy are still serving traffic, and a rollback puts the old code back in front of the new schema.

An ORM makes this stricter than it looks. Rails caches a table's columns at boot, so dropping a column breaks running processes that never referenced it. GitLab's answer is to tell the model to ignore the column in one release and drop it in the next. Check what your ORM caches before assuming an unreferenced column is unused.

## 2. Expand, migrate, contract

The three phases of parallel change, applied to a schema.

| Phase | Schema | Code | Move on when |
| --- | --- | --- | --- |
| **Expand** | Add the new column, table, or index. Old one untouched. | Writes go to both. Reads still use the old. | The new structure exists everywhere and dual writes are deployed. |
| **Migrate** | No DDL. | Backfill old rows. Then flip reads to the new, falling back to the old when the new is null. | Backfill is complete and reads have been on the new path long enough to roll back from. |
| **Contract** | Drop the old column or table. | Stop writing the old. | Nothing reads or writes the old thing, proven by a search across the repo plus a deployed release with no fallback hits. |

Contract is the phase that gets skipped and the one that is irreversible. It is a separate PR, at least one release later, with its own yes from the human.

## 3. Ask the engine, not your memory

Before writing DDL, look up this exact operation in your engine's own documentation for your version, and quote the line in the PR. Lock level, table rewrite, and whether the statement can live in a transaction vary by operation, by engine, and by version.

What the primary docs say, as of PostgreSQL 18 and MySQL 8.4:

| Fact | Engine |
| --- | --- |
| `ALTER TABLE` takes `ACCESS EXCLUSIVE` unless a subform says otherwise; with several subcommands, the strictest lock any of them needs is the one taken. | PostgreSQL |
| `ADD COLUMN` with a non-volatile default stores the default as metadata and does not rewrite the table. A volatile default, a stored generated column, an identity column, or a constrained domain type rewrites the table and its indexes. | PostgreSQL |
| `ADD CONSTRAINT ... NOT VALID` commits without scanning the table; the later `VALIDATE CONSTRAINT` takes only `SHARE UPDATE EXCLUSIVE` and does not lock out writers. | PostgreSQL |
| `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block. If it fails it leaves an index marked `INVALID` that is ignored by queries but still costs every write; recovery is to drop it and retry. | PostgreSQL |
| Atomic DDL is not transactional DDL: a DDL statement implicitly commits the open transaction and cannot run inside one. | MySQL |
| Online DDL support is per operation. Changing a column's data type rebuilds the table and blocks concurrent DML; adding a secondary index does not. | MySQL |
| Stating `LOCK=NONE` makes the server raise an error when it cannot do the operation without blocking, instead of blocking. Ask for the concurrency you need rather than hoping for it. | MySQL |
| On an engine without DDL transactions, a migration that fails partway leaves the database half-changed and you unpick it by hand. | MySQL, Oracle |

Two consequences worth planning for:

- **The lock queue is the real risk, not the lock.** A DDL statement waiting for its lock sits in the queue ahead of every query that arrives after it, so a fast `ALTER` behind one slow `SELECT` can stall the table. Set a short lock timeout and retry, rather than letting the statement wait.
- **Frameworks wrap migrations in a transaction where the engine supports it, and give you an escape hatch.** `atomic = False` in Django, `disable_ddl_transaction!` in Rails and GitLab. Concurrent index builds need the hatch. A migration that runs outside a transaction must be written so that re-running it after a mid-way failure is safe.

## 4. Write the down path, then prove it does what you claim

Every migration declares one of three, in the file itself:

| Kind | Means |
| --- | --- |
| **Reversible** | Down restores both the schema and any data the up path could have destroyed. |
| **Forward-only** | Reversal is a new migration written later. Say so in the file; do not ship an empty `down`. |
| **Irreversible** | Down cannot exist. Dropping a column drops its data. Django raises `IrreversibleError` rather than pretending. |

Prove a reversible claim with a schema round trip against a throwaway copy: dump the schema, run up, run down, dump again, diff. A non-empty diff means the down path is wrong.

```bash
sqlite3 throwaway.db .schema | sort > before.sql
# run the up migration, then the down migration
sqlite3 throwaway.db .schema | sort > after.sql
diff before.sql after.sql && echo "schema round-trip clean"
```

Adapt the dump command to your engine (`pg_dump --schema-only`, `mysqldump --no-data`).

**A clean round trip proves the schema and nothing else.** Measured on SQLite 3.51: add a column, write a value into it, drop the column, and the schema diff is empty and the original rows are byte-identical. The value written during the expanded window is gone, and re-adding the column brings it back as null. So for any step that can destroy data, the real down path is a restore from backup. Confirm the backup exists and check its timestamp before running the up, not after.

## 5. Backfill as its own job

- Separate from the DDL. A backfill inside the migration that adds the column holds a lock for the length of the backfill.
- Batch by primary key with a bounded batch size and a pause between batches. One `UPDATE` across the whole table is one long transaction and one long lock.
- Idempotent: re-running a batch changes nothing the second time. Non-transactional migrations fail partway, and something has to be safe to rerun.
- Resumable: record progress somewhere durable, so a restart continues instead of starting over.
- During the window, reads take the new value and fall back to the old when it is null. Remove the fallback only after the backfill is complete, and treat a fallback hit after that point as a bug worth alerting on.

## 6. Rehearse before you ask

| Check | How |
| --- | --- |
| It applies | Restore a copy of a production-shaped dump into a throwaway, run the migration against it. |
| How long it takes | Time that run and report the number. An untimed migration is a guess about downtime. |
| What it actually does | Print the SQL your framework will run (`sqlmigrate`, `rails db:migrate --dry-run` or the equivalent) and read it. The generated SQL is what runs, not what you wrote. |
| It stops safely | Kill it partway on the copy, then run it again. This is the state a timeout leaves you in. |
| The down path | Section 4's round trip. |
| The old code survives it | Run the currently deployed version of the app's tests against the migrated throwaway. |

Report every claim as measured, inferred, or guess, as `rigor` section 4 requires. "It should be fast" is a guess. "9.4s against a 2M-row copy" is measured.

## 7. What the human gets before the yes

1. The exact statements that will run, in generated-SQL form.
2. The lock each one takes, quoted from the engine's docs.
3. The measured duration against a production-shaped copy, and the row count it ran against.
4. Which of the three down kinds this is, and for irreversible steps, the timestamp of the backup you are relying on.
5. The deploy sequence, including which phase this PR is and what the next one will be.

Then stop and wait. Applying it is their call.

## Failure modes

| Smell | What it means |
| --- | --- |
| Migration and the code that needs it in one deploy | Old processes are still running against the new schema. Split it. |
| `down` that only drops what `up` added | Fine for schema, silently lossy for data. Say which kind it is. |
| Backfill inside the DDL migration | The lock is held for the length of the backfill. |
| "It ran fine locally" | Local has a thousand rows. Rehearse against a production-shaped copy or say inconclusive. |
| Expand and contract in the same PR | You have written a downtime migration with extra steps. |
| Index added without checking transaction support | Concurrent builds cannot run in a transaction and leave an invalid index when they fail. |
| A dropped column that nothing references | The ORM may still cache it. Ignore it in one release, drop it in the next. |

## Sources

- [PostgreSQL 18: `ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html) — lock levels, table rewrites, `NOT VALID` and `VALIDATE CONSTRAINT`.
- [PostgreSQL 18: `CREATE INDEX`, Building Indexes Concurrently](https://www.postgresql.org/docs/current/sql-createindex.html) — no transaction block, invalid index on failure.
- [MySQL 8.4: Online DDL Operations](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html) — per-operation support tables.
- [MySQL 8.4: `ALTER TABLE`](https://dev.mysql.com/doc/refman/8.4/en/alter-table.html) — `ALGORITHM` and `LOCK` clause semantics.
- [MySQL 8.4: Atomic DDL](https://dev.mysql.com/doc/refman/8.4/en/atomic-ddl.html) — atomic is not transactional.
- [Django: Migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/) — DDL transaction support by backend, `IrreversibleError`, non-atomic migrations.
- [GitLab: Avoiding downtime in migrations](https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/) — ignore-then-drop for columns, staged renames, batched backfills.
- [GitLab: Migration Style Guide](https://docs.gitlab.com/development/migration_style_guide/) — lock queue behavior, lock-retry and statement timeouts.
- [Danilo Sato, Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) — the expand, migrate, contract pattern.
