
cat dumpfile.sql | sqlite3 secureserver.db
sqlite3 secureserver.db ".dump 'user__sessions'" | grep '^INSERT'