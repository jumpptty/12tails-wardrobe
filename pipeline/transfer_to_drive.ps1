<#
Copy what the wardrobe needs on another PC and git does not carry: its data (wardrobe\data, prop textures included)
as one tar, plus a git bundle of this repo for a PC without GitHub, plus README.txt with the restore steps. The office
PC can't build the data (no game rips there), so it always gets the home PC's copy this way.

  powershell -ExecutionPolicy Bypass -File pipeline\transfer_to_drive.ps1 -Drive E
  -> E:\12tails-wardrobe-transfer\wardrobe_data.tar, 12tails-wardrobe.bundle, README.txt
  -Dest <folder> writes there instead (tests).
One tar, not thousands of files: a flash drive writes small files far slower (NOTES.md in 12tails-video, "Moving to
another PC"). FAT32 caps a file at 4 GB; the data is ~300 MB.
#>
param([string]$Drive = "", [string]$Dest = "")
# (no $ErrorActionPreference = "Stop": Windows PowerShell 5.1 turns git's progress lines on stderr into a fatal error;
# native tools are checked by exit code instead)
$root = Split-Path -Parent $PSScriptRoot
if ($Dest) { $dst = $Dest } elseif ($Drive) { $dst = "$($Drive.TrimEnd(':', '\')):\12tails-wardrobe-transfer" }
else { "Give -Drive <letter> (or -Dest <folder>)."; exit 1 }
$data = Join-Path $root "wardrobe\data"
if (-not (Test-Path -LiteralPath (Join-Path $data "meta.json"))) { "No wardrobe data in $data."; exit 1 }
New-Item -ItemType Directory -Force $dst | Out-Null

$t = Get-Date
$tar = Join-Path $dst "wardrobe_data.tar"
& tar.exe -cf $tar -C $root "wardrobe/data"
if ($LASTEXITCODE) { "tar failed ($LASTEXITCODE)"; exit 1 }
$gb = (Get-Item -LiteralPath $tar).Length / 1GB
if ($gb -ge 4) { "wardrobe_data.tar is {0:N2} GB: over FAT32's 4 GB limit" -f $gb; exit 1 }
"wardrobe_data.tar: {0:N2} GB in {1:N0} s" -f $gb, ((Get-Date) - $t).TotalSeconds

$bundle = Join-Path $dst "12tails-wardrobe.bundle"
Remove-Item -LiteralPath "$bundle.lock" -Force -ErrorAction SilentlyContinue
& git -C $root bundle create $bundle --all 2>&1 | Out-Null
if ($LASTEXITCODE) { "git bundle failed"; exit 1 }
"12tails-wardrobe.bundle written"

@"
12 Tails wardrobe transfer ($(Get-Date -Format 'yyyy-MM-dd'))
=============================================================
<drive> below = this flash drive's letter on that PC. Office paths shown; the home PC uses D:\ for C:\work\.
1. Code:  git clone https://github.com/jumpptty/12tails-wardrobe.git C:\work\12tails-wardrobe
          (no GitHub?  git clone <drive>\12tails-wardrobe-transfer\12tails-wardrobe.bundle C:\work\12tails-wardrobe)
          (already cloned?  cd C:\work\12tails-wardrobe ; git pull)
2. Data:  tar -xf <drive>\12tails-wardrobe-transfer\wardrobe_data.tar -C C:\work\12tails-wardrobe
          (a folder C:\work\12tails-wardrobe\wardrobe\data already there? rename it first, e.g. to data_old)
3. Once, the first time on that PC (the video folder C:\work\12tails-video must exist):
          powershell -ExecutionPolicy Bypass -File C:\work\12tails-wardrobe\pipeline\adopt_from_video.ps1 -SetAside
          (renames the video folder's older wardrobe\data to wardrobe_data_old, points the Desktop shortcut here)
4. Run:   the Desktop shortcut "12 Tails Wardrobe" (or C:\work\12tails-wardrobe\wardrobe.cmd; needs Python 3's "py"
          launcher and internet for three.js)
"@ | Out-File (Join-Path $dst "README.txt") -Encoding utf8
"done: $dst"
exit 0
