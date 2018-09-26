#!/bin/bash
git add . && \
git status && \
git commit -m "Tagessicherung"  && \
rm .git/hooks/pre-push  && \
cp db.sqlite3 db.sqlite_sicher  && \
#git push git@github.com:juergen@klotzek.de/Supplier-Management-System.git 
git push
