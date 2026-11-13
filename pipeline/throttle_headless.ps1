# Keep the headless browsers of the checks (Playwright's chrome-headless-shell: SwiftShader draws on the CPU and takes
# every core it finds) off most of the PC (user 2026-11-13: "reduce PC power consumption to 30%, everything is really
# laggy" during the Whale's build). Every few seconds each such process is put on the last <Percent>% of the logical
# cores (the efficiency cores on this PC's CPU) at Idle priority; browsers started later are caught on the next pass.
# The checks run slower for it. Stops by itself after -Hours.
#   powershell -ExecutionPolicy Bypass -File pipeline\throttle_headless.ps1 [-Percent 30] [-Hours 8] [-Once]
param([int]$Percent = 30, [double]$Hours = 8, [switch]$Once)
$n = [Environment]::ProcessorCount
$use = [math]::Max(1, [math]::Floor($n * $Percent / 100))
[long]$mask = 0
for ($i = $n - $use; $i -lt $n; $i++) { $mask = $mask -bor ([long]1 -shl $i) }
$until = (Get-Date).AddHours($Hours)
"chrome-headless-shell -> $use of $n logical cores (mask 0x$($mask.ToString('X'))), Idle priority"
do {
  foreach ($p in Get-Process -Name "chrome-headless-shell" -ErrorAction SilentlyContinue) {
    try {
      if ($p.ProcessorAffinity.ToInt64() -ne $mask) { $p.ProcessorAffinity = [IntPtr]$mask }
      if ($p.PriorityClass -ne "Idle") { $p.PriorityClass = "Idle" }
    } catch {}   # gone already
  }
  if ($Once) { break }
  Start-Sleep -Seconds 3
} while ((Get-Date) -lt $until)
