
#  Python-Based C2 Server

This repository contains a lightweight, Dockerized Python Flask Command & Control (C2) server designed for testing and simulation in hybrid environments. It supports:

- Downloading files from the internet (`/fetch`)
- Serving files to internal or air-gapped machines (`/payload/<filename>`)
- Browsing available payloads via web interface (`/files`)

---

##  API Endpoints & PowerShell Usage

Each endpoint below is designed to support red team and testing workflows. Examples are provided using **PowerShell** for compatibility with Windows-based agents or admin environments.

---

###  `POST /fetch`

**Purpose**: Download a file from the internet to the C2 server’s `payloads/` directory.

**URL**: `https://****/fetch`

**PowerShell Usage**:

```powershell
Invoke-RestMethod -Uri "https://****/fetch" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"url":"https://example.com/tool.exe"}'
```

**Expected Response**:
```json
{
  "status": "fetched",
  "file": "tool.exe"
}
```

📎 **Note**: The file is saved in the server's internal `/app/payloads` folder and becomes immediately accessible via `/payload/tool.exe`.

---

###  `GET /payload/<filename>`

**Purpose**: Uploads the file to Air Gapped Machine.

**URL Format**:
```
https://****/payload/<filename>
```

**Example PowerShell Download**:
```powershell
Invoke-WebRequest -Uri "https://****/payload/tool.exe" -OutFile "tool.exe"
```

This supports all file types, including:
- `.exe`, `.dll`, `.ps1`, `.bat`, `.sh`, `.cmd`
- `.csv`, `.txt`, `.html`, `.xls`, etc.

---

###  `GET /files`

**Purpose**: List all available files in the C2 server’s payloads directory as clickable HTML links.

**URL**:
```
https://****/files
```

 This is useful for browsing or testing from a web browser. You’ll see:

```html
Available Payloads:
• [tool.exe](https://****/payload/tool.exe)
• [capec.csv](https://****/payload/capec.csv)
...
```
###  `GET /upload`

**Purpose**: Web interface to upload one or more files into the server’s `payloads/` directory.

**URL**:
```
https://****/upload
```

- Allows **multiple file selection and upload** from your local machine.
- After upload, you are redirected to `/files` to view all payloads.
- Fully browser-based and does not require scripting or CLI access.

---

##  Batch Fetch Example (Multiple URLs)

Use this to fetch several files from the internet into the C2 server:

```powershell
$urls = @(
  "https://raw.githubusercontent.com/mitre/capec/master/data/capec.csv",
  "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv",
  "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-relationship-objects.csv"
)

$c2_url = "https://****/fetch"

foreach ($url in $urls) {
    $body = @{ url = $url } | ConvertTo-Json
    Write-Host "`n[+] Fetching: $url"
    Invoke-RestMethod -Uri $c2_url -Method Post -ContentType "application/json" -Body $body
}
```

After execution, all files will be available at:
```
https://****/files
```

---
