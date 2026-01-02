**VS Code Übertragen: Backup‑ und Transfer‑Anleitung**

Übersicht
- Nutze `scripts/backup_vscode.sh`, um VS Code Einstellungen, die Liste der Erweiterungen, `.vscode`‑Ordner und optional SSH‑Schlüssel bzw. Projektarchive zu sammeln.
- Nutze `scripts/transfer_to_notebook.sh`, um das aktuellste Backup per `rsync` auf dein Notebook zu übertragen.

Schnellstart
1) Mache die Skripte ausführbar:
```bash
chmod +x scripts/*.sh
```
2) Erstelle ein Backup (mit SSH‑Schlüsseln, falls gewünscht):
```bash
./scripts/backup_vscode.sh --include-ssh --projects "$HOME/Portfolio"
```
3) Übertrage das Backup auf das Notebook (ersetze `user@notebook`):
```bash
./scripts/transfer_to_notebook.sh user@notebook /home/user/vscode-backup
```

Wiederherstellung auf dem Notebook
- Packe die Archive im Backup‑Ordner aus und kopiere die Einstellungen nach `~/.config/Code/User/`:
```bash
tar -xzf ~/vscode-backup-2025-12-29/vscode-user.tgz -C ~/
cp -a ~/vscode-backup-2025-12-29/user-settings/* ~/.config/Code/User/
cat ~/vscode-backup-2025-12-29/extensions.txt | xargs -L 1 code --install-extension
```

Hinweise & Sicherheit
- Die Skripte entfernen nichts auf deinen Rechnern.
- Wenn du SSH‑Schlüssel einschließt, stelle sicher, dass das Notebook sicher ist, bevor du sie verwendest.
- Wenn du die Settings Sync von VS Code nutzt, ist eine manuelle Übertragung nicht zwingend nötig; ein lokales Backup ist aber trotzdem empfehlenswert.

Wenn du möchtest, kann ich jetzt:
- A) `./scripts/backup_vscode.sh` hier ausführen (erstellt ein Backup auf diesem Rechner).  
- B) Einen `rsync`/`scp`‑Befehl für dein Notebook vorbereiten (nenn mir `user@host`).  
- C) Eine GitHub Actions Workflowdatei erstellen, die Backups geplant in ein privates Repo schiebt.
