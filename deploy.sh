#!/bin/bash

# Automatizovaný skript pro nasazení aplikace s logováním a zálohováním

LOGFILE="deploy.log"
BACKUP_DIR="backups"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

# Vytvoření adresáře pro zálohy, pokud neexistuje
mkdir -p $BACKUP_DIR

# Zálohování databáze
if [ -f "akcie_project/db.sqlite3" ]; then
    cp akcie_project/db.sqlite3 $BACKUP_DIR/db_backup_$DATE.sqlite3
    echo "[$DATE] Záloha databáze byla vytvořena." >> $LOGFILE
else
    echo "[$DATE] Databáze nebyla nalezena, záloha nebyla vytvořena." >> $LOGFILE
fi

# Aktivace virtuálního prostředí
source venv/bin/activate

# Migrace databáze
python3 manage.py migrate >> $LOGFILE 2>&1
if [ $? -eq 0 ]; then
    echo "[$DATE] Migrace databáze proběhla úspěšně." >> $LOGFILE
else
    echo "[$DATE] Chyba při migraci databáze." >> $LOGFILE
    exit 1
fi

# Sběr statických souborů
python3 manage.py collectstatic --noinput >> $LOGFILE 2>&1
if [ $? -eq 0 ]; then
    echo "[$DATE] Statické soubory byly úspěšně nasbírány." >> $LOGFILE
else
    echo "[$DATE] Chyba při sběru statických souborů." >> $LOGFILE
    exit 1
fi

# Spuštění serveru
python3 manage.py runserver 0.0.0.0:8000 >> $LOGFILE 2>&1 &
if [ $? -eq 0 ]; then
    echo "[$DATE] Server byl úspěšně spuštěn." >> $LOGFILE
else
    echo "[$DATE] Chyba při spuštění serveru." >> $LOGFILE
    exit 1
fi
