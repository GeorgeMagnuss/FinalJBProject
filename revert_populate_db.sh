#!/bin/bash

# Script to revert populate_db.py changes if needed

echo "Reverting populate_db.py to original version..."

# Check if backup exists
if [ -f "vacation_website/vacations/management/commands/populate_db.py.backup" ]; then
    cp vacation_website/vacations/management/commands/populate_db.py.backup vacation_website/vacations/management/commands/populate_db.py
    echo "Successfully reverted populate_db.py to original version"
else
    echo "Error: Backup file not found at vacation_website/vacations/management/commands/populate_db.py.backup"
    exit 1
fi