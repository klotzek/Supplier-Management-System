#!/bin/bash
# cp db.sqlite3 db.sqlite_sicher  && \
git add . && \
git status && \
git commit -m "Tagessicherung"  && \
# rm .git/hooks/pre-push  && \
#git push git@github.com:juergen@klotzek.de/Supplier-Management-System.git 
git push origin master
# rm db.sqlite_sicher
