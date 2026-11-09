<#
Move the wardrobe's untracked files out of the video folder into this repo (the 2026-11-09 split: the wardrobe has
its own repo, 12tails-wardrobe, beside 12tails-video), then copy its prop textures in and point the Desktop shortcut
"12 Tails Wardrobe" here. Run once per PC; a re-run changes nothing.

  powershell -ExecutionPolicy Bypass -File <wardrobe>\pipeline\adopt_from_video.ps1 [-Video <folder>] [-SetAside] [-DryRun] [-NoShortcut]

Home PC (plain run): moves each of these from the video folder, only if it is there and not here yet (same drive, so
each move is one rename; nothing is ever overwritten):
  wardrobe\data, wardrobe_dist, wardrobe_dist_report.json, wardrobe_dist_report.prev.json,
  .superpowers\sdd\2026-11-07-wardrobe-online
Office PC (-SetAside): the home PC's data was restored here first (wardrobe_data.tar from transfer_to_drive.ps1), so
the office's own older <video>\wardrobe\data is renamed to <video>\wardrobe_data_old instead (delete it when happy);
without restored data here it stops and moves nothing.
Then: wardrobe_props_tex.py (the prop textures from <video>\props\tex), the shortcut, and <video>\wardrobe is removed
once it is empty (on the home PC its tracked page files go with the video repo's own commit).
Stops at the first failed move (a server, editor or Explorer window holding the folder) and prints what moved.
-DryRun prints the plan and changes nothing. -Wardrobe and -Desktop exist for the scratch tests.
#>
param(
    [string]$Video = "",
    [string]$Wardrobe = "",
    [string]$Desktop = "",
    [switch]$SetAside,
    [switch]$DryRun,
    [switch]$NoShortcut
)
$ErrorActionPreference = "Stop"
if (-not $Wardrobe) { $Wardrobe = Split-Path -Parent $PSScriptRoot }
if (-not $Video) { $Video = Join-Path (Split-Path -Parent $Wardrobe) "12tails-video" }
if (-not $Desktop) { $Desktop = [Environment]::GetFolderPath("Desktop") }
$Wardrobe = (Resolve-Path -LiteralPath $Wardrobe).Path
if (-not (Test-Path -LiteralPath $Video)) { "The video folder isn't there: $Video (pass -Video <folder>)"; exit 1 }
$Video = (Resolve-Path -LiteralPath $Video).Path
"wardrobe: $Wardrobe"
"video:    $Video"
if ($DryRun) { "(dry run: nothing changes)" }

# the video folder must be the video repo's own root, already moved up from its old comic-skit folder (the office
# PC runs move_project.ps1 first; it failed twice on held folders at home before it worked)
foreach ($old in @("comic-skit", "comic-skit.__moving__")) {
    if (Test-Path -LiteralPath (Join-Path $Video $old)) {
        "STOPPED: $(Join-Path $Video $old) is still there: the video project hasn't moved up yet."
        "  Run its pipeline\move_project.ps1 first (VS Code closed), then this again. Nothing moved."
        exit 1
    }
}
if (-not (Test-Path -LiteralPath (Join-Path $Video ".git"))) {
    "STOPPED: $Video has no .git, so it isn't the 12tails-video repo's root: pass -Video <that folder>, or run"
    "  move_project.ps1 first if the project still sits in a comic-skit folder. Nothing moved."
    exit 1
}

$items = @("wardrobe\data", "wardrobe_dist", "wardrobe_dist_report.json", "wardrobe_dist_report.prev.json",
           ".superpowers\sdd\2026-11-07-wardrobe-online")
$moved = @(); $problem = $null

if ($SetAside) {
    $here = Join-Path $Wardrobe "wardrobe\data"
    if (-not (Test-Path -LiteralPath (Join-Path $here "meta.json"))) {
        "STOPPED: -SetAside needs the home PC's data here first: restore wardrobe_data.tar into $Wardrobe"
        "  (in PowerShell: tar.exe -xf <transfer folder>\wardrobe_data.tar -C $Wardrobe), then run this again. Nothing moved."
        exit 1
    }
    $items = $items | Where-Object { $_ -ne "wardrobe\data" }
    $old = Join-Path $Video "wardrobe\data"
    $aside = Join-Path $Video "wardrobe_data_old"
    if (Test-Path -LiteralPath $old) {
        if (Test-Path -LiteralPath $aside) { "STOPPED: $aside already exists; move it away first. Nothing moved."; exit 1 }
        if ($DryRun) { "would set aside: $old -> $aside" }
        else {
            try { Move-Item -LiteralPath $old -Destination $aside -ErrorAction Stop; $moved += "wardrobe\data (set aside)" ; "set aside: $old -> $aside" }
            catch { "STOPPED: could not set aside $old ($($_.Exception.Message)). Nothing moved."; exit 1 }
        }
    } else { "no old data to set aside in $Video" }
}

foreach ($rel in $items) {
    $src = Join-Path $Video $rel
    $dst = Join-Path $Wardrobe $rel
    $hasSrc = Test-Path -LiteralPath $src
    $hasDst = Test-Path -LiteralPath $dst
    if (-not $hasSrc -and $hasDst) { "already in place: $rel"; continue }
    if (-not $hasSrc) { "not in the video folder (skipped): $rel"; continue }
    if ($hasDst) { $problem = "$rel is in both folders; nothing is overwritten: compare them and remove one, then run again"; break }
    if ($DryRun) { "would move: $rel"; continue }
    try {
        $parent = Split-Path -Parent $dst
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
        Move-Item -LiteralPath $src -Destination $dst -ErrorAction Stop
        $moved += $rel; "moved: $rel"
    } catch { $problem = "could not move $rel ($($_.Exception.Message)); close what holds it (wardrobe.cmd's server, VS Code, Explorer) and run again"; break }
}
if ($problem) {
    "STOPPED: $problem"
    "  moved so far: " + $(if ($moved) { $moved -join ", " } else { "nothing" })
    "  not moved: " + (($items | Where-Object { $moved -notcontains $_ }) -join ", ")
    exit 1
}

# the prop textures the props JSON names (an existing copy is kept)
$texMissing = $false
$data = Join-Path $Wardrobe "wardrobe\data"
if ($DryRun) { "would copy the prop textures: py -3 wardrobe_props_tex.py --data $data --src $(Join-Path $Video 'props\tex')" }
elseif (Test-Path -LiteralPath $data) {
    & py -3 (Join-Path $PSScriptRoot "wardrobe_props_tex.py") --data $data --src (Join-Path $Video "props\tex")
    if ($LASTEXITCODE -ne 0) { $texMissing = $true }
}

if (-not $NoShortcut) {
    $lnk = Join-Path $Desktop "12 Tails Wardrobe.lnk"
    if ($DryRun) { "would point $lnk at $(Join-Path $Wardrobe 'wardrobe.cmd')" }
    else {
        $ws = New-Object -ComObject WScript.Shell
        $s = $ws.CreateShortcut($lnk)
        $s.TargetPath = Join-Path $Wardrobe "wardrobe.cmd"
        $s.WorkingDirectory = $Wardrobe
        $s.IconLocation = (Join-Path $Wardrobe "wardrobe\wardrobe.ico") + ",0"
        $s.WindowStyle = 7
        $s.Description = "12 Tails wardrobe: every class, outfit, face, prop and emote"
        $s.Save(); "shortcut: $lnk -> $($s.TargetPath)"
    }
}

$vw = Join-Path $Video "wardrobe"
if ((Test-Path -LiteralPath $vw) -and -not $DryRun) {
    $left = @(Get-ChildItem -LiteralPath $vw -Recurse -Force -File)
    if ($left.Count -eq 0) { Remove-Item -LiteralPath $vw -Recurse -Force; "removed the empty $vw" }
    else { "left in ${vw}: $($left.Count) files (tracked page files go with the video repo's commit)" }
}

if ($texMissing) { "DONE, but some prop textures are missing (listed above): those props show untextured."; exit 1 }
"DONE: the wardrobe is $Wardrobe"
exit 0
