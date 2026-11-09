# Tests for adopt_from_video.ps1 on throwaway folders under %TEMP% (no real data touched):
#   powershell -ExecutionPolicy Bypass -File pipeline\test_adopt_from_video.ps1   -> PASS lines, "fails: 0", exit 0
$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "adopt_from_video.ps1"
$base = Join-Path $env:TEMP "adopt_from_video_test"
$fails = 0

function Fresh([switch]$WithData) {
    if (Test-Path $base) { Remove-Item -Recurse -Force $base }
    $v = Join-Path $base "12tails-video"; $w = Join-Path $base "12tails-wardrobe"; $d = Join-Path $base "desk"
    foreach ($p in @("$v\.git", "$v\wardrobe\data\cat", "$v\wardrobe_dist", "$v\.superpowers\sdd\2026-11-07-wardrobe-online", "$v\props\tex", "$w\wardrobe", $d)) { New-Item -ItemType Directory -Force $p | Out-Null }
    Set-Content "$v\wardrobe\index.html" "page" ; Set-Content "$w\wardrobe\index.html" "page"
    Set-Content "$v\wardrobe\data\meta.json" "{}"
    Set-Content "$v\wardrobe\data\cat\props_weapons.json" '[{"name":"p","nodes":[{"name":"n","mats":[{"tex":"x.png"}]}]}]'
    Set-Content "$v\props\tex\x.png" "x"
    Set-Content "$v\wardrobe_dist\index.html" "dist"; Set-Content "$v\wardrobe_dist_report.json" "{}"; Set-Content "$v\wardrobe_dist_report.prev.json" "{}"
    Set-Content "$v\.superpowers\sdd\2026-11-07-wardrobe-online\progress.md" "ledger"
    if ($WithData) { New-Item -ItemType Directory -Force "$w\wardrobe\data" | Out-Null; Set-Content "$w\wardrobe\data\meta.json" '{"home":1}' }
    return @{ v = $v; w = $w; d = $d }
}
function Run($t, [string[]]$extra) {
    $out = & powershell -NoProfile -ExecutionPolicy Bypass -File $script -Video $t.v -Wardrobe $t.w -Desktop $t.d @extra 2>&1 | Out-String
    return @{ code = $LASTEXITCODE; out = $out }
}
function Check($name, $cond, $out) {
    if ($cond) { "PASS  $name" } else { "FAIL  $name"; $script:fails++; $out }
}

# (a) normal run
$t = Fresh; $r = Run $t @()
Check "a: exit 0" ($r.code -eq 0) $r.out
Check "a: five moved" ((Test-Path "$($t.w)\wardrobe\data\meta.json") -and (Test-Path "$($t.w)\wardrobe_dist\index.html") -and (Test-Path "$($t.w)\wardrobe_dist_report.json") -and (Test-Path "$($t.w)\wardrobe_dist_report.prev.json") -and (Test-Path "$($t.w)\.superpowers\sdd\2026-11-07-wardrobe-online\progress.md")) $r.out
Check "a: sources gone" (-not (Test-Path "$($t.v)\wardrobe\data") -and -not (Test-Path "$($t.v)\wardrobe_dist")) $r.out
Check "a: prop texture copied" (Test-Path "$($t.w)\wardrobe\data\props\tex\x.png") $r.out
Check "a: shortcut points here" ((New-Object -ComObject WScript.Shell).CreateShortcut("$($t.d)\12 Tails Wardrobe.lnk").TargetPath -eq "$($t.w)\wardrobe.cmd") $r.out
Check "a: tracked page left in video\wardrobe" ((Test-Path "$($t.v)\wardrobe\index.html") -and $r.out -match "left in") $r.out

# (b) re-run changes nothing
$before = (Get-ChildItem -Recurse -Force $base | Measure-Object).Count
$r = Run $t @()
Check "b: exit 0" ($r.code -eq 0) $r.out
Check "b: all already in place" (([regex]::Matches($r.out, "already in place")).Count -eq 5) $r.out
Check "b: no file count change" ((Get-ChildItem -Recurse -Force $base | Measure-Object).Count -eq $before) $r.out

# (f) home run with data already here: stops, overwrites nothing
$t = Fresh -WithData; $r = Run $t @()
Check "f: exit 1" ($r.code -eq 1) $r.out
Check "f: says both folders" ($r.out -match "in both folders") $r.out
Check "f: target data untouched" ((Get-Content "$($t.w)\wardrobe\data\meta.json") -eq '{"home":1}') $r.out
Check "f: source still there" (Test-Path "$($t.v)\wardrobe\data\meta.json") $r.out

# (c) -SetAside with nothing restored: stops, moves nothing
$t = Fresh; $r = Run $t @("-SetAside")
Check "c: exit 1" ($r.code -eq 1) $r.out
Check "c: restore message" ($r.out -match "restore wardrobe_data.tar") $r.out
Check "c: nothing moved" ((Test-Path "$($t.v)\wardrobe\data\meta.json") -and -not (Test-Path "$($t.v)\wardrobe_data_old") -and (Test-Path "$($t.v)\wardrobe_dist")) $r.out

# (d) -SetAside with restored data: the old copy goes aside
$t = Fresh -WithData; $r = Run $t @("-SetAside")
Check "d: exit 0" ($r.code -eq 0) $r.out
Check "d: old copy set aside" ((Test-Path "$($t.v)\wardrobe_data_old\meta.json") -and -not (Test-Path "$($t.v)\wardrobe\data")) $r.out
Check "d: restored data kept" ((Get-Content "$($t.w)\wardrobe\data\meta.json") -eq '{"home":1}') $r.out

# (e) a held file stops the run and says what moved
$t = Fresh; $fs = [IO.File]::Open("$($t.v)\wardrobe_dist\index.html", "Open", "Read", "None")
try { $r = Run $t @() } finally { $fs.Close() }
Check "e: exit 1" ($r.code -eq 1) $r.out
Check "e: data moved, dist not" ((Test-Path "$($t.w)\wardrobe\data\meta.json") -and (Test-Path "$($t.v)\wardrobe_dist\index.html")) $r.out
Check "e: prints moved and not moved" ($r.out -match "moved so far: wardrobe\\data" -and $r.out -match "not moved: wardrobe_dist") $r.out

# (g) the office's video folder never moved up (move_project.ps1 failed or was skipped): stop, move nothing
$t = Fresh -WithData; New-Item -ItemType Directory -Force "$($t.v)\comic-skit\wardrobe\data" | Out-Null
Set-Content "$($t.v)\comic-skit\wardrobe\data\meta.json" "{}"; $r = Run $t @("-SetAside")
Check "g: exit 1" ($r.code -eq 1) $r.out
Check "g: says run move_project.ps1" ($r.out -match "move_project\.ps1") $r.out
Check "g: nothing moved or set aside" ((Test-Path "$($t.v)\comic-skit\wardrobe\data\meta.json") -and -not (Test-Path "$($t.v)\wardrobe_data_old") -and (Test-Path "$($t.v)\wardrobe_dist")) $r.out

# (h) a folder that isn't the video repo's root (no .git): stop, move nothing
$t = Fresh; Remove-Item -Recurse -Force "$($t.v)\.git"; $r = Run $t @()
Check "h: exit 1" ($r.code -eq 1) $r.out
Check "h: nothing moved" ((Test-Path "$($t.v)\wardrobe\data\meta.json") -and -not (Test-Path "$($t.w)\wardrobe\data")) $r.out

# dry run changes nothing
$t = Fresh; $before = (Get-ChildItem -Recurse -Force $base | Measure-Object).Count; $r = Run $t @("-DryRun")
Check "dry: exit 0 and nothing changed" ($r.code -eq 0 -and (Get-ChildItem -Recurse -Force $base | Measure-Object).Count -eq $before -and $r.out -match "would move: wardrobe\\data") $r.out

Remove-Item -Recurse -Force $base
"fails: $fails"
if ($fails) { exit 1 }
