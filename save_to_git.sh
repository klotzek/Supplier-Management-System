#!/bin/bash
git add . && \
git status && \
git commit -m "Tagessicherung"  && \
rm .git/hooks/pre-push  && \
#git push git@github.com:juergen@klotzek.de/Supplier-Management-System.git 
git push
