p = 'C:/dev/masaha/app-lane-t/docker-compose.yml'
s = open(p, encoding='utf8').read()
old = """      - masaha-pgdata:/var/lib/postgresql
      # Runs once, when the volume is first created: adds masaha_test next to masaha_dev.
      - ./docker/postgres/create-test-database.sql:/docker-entrypoint-initdb.d/create-test-database.sql:ro
"""
new = """      - masaha-pgdata:/var/lib/postgresql
    # Runs once, when the volume is first created: adds masaha_test next to masaha_dev. Inline, so
    # the container depends on no folder, and every folder's configuration is the same (finding 48).
    configs:
      - source: create-test-database
        target: /docker-entrypoint-initdb.d/create-test-database.sql
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
old = """volumes:
  masaha-pgdata:
"""
new = """volumes:
  masaha-pgdata:

configs:
  create-test-database:
    content: |
      -- The API test lane's database; test:api migrates and truncates it, never masaha_dev.
      CREATE DATABASE masaha_test;
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf8', newline='').write(s)
