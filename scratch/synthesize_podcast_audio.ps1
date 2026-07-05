Add-Type -AssemblyName System.Speech

$jsonPath = Join-Path $PSScriptRoot "podcast_script_30min.json"
$wavOutputPath = Join-Path $PSScriptRoot "..\podcast_audio_30min.wav"
$fullWavPath = (Get-Item -Path $wavOutputPath -ErrorAction SilentlyContinue).FullName
if (-not $fullWavPath) {
    $parentDir = (Get-Item $PSScriptRoot).Parent.FullName
    $fullWavPath = Join-Path $parentDir "podcast_audio_30min.wav"
}

Write-Host "=== Synthesizing 30-Minute Administrative Law Master Podcast Audio ==="
Write-Host "Target Audio Output: $fullWavPath"

if (-not (Test-Path $jsonPath)) {
    Write-Host "JSON script not found!"
    exit 1
}

$chapters = Get-Content -Path $jsonPath -Encoding UTF8 | ConvertFrom-Json

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Hanhan Desktop")
$synth.Rate = 1
$synth.Volume = 100

$synth.SetOutputToWaveFile($fullWavPath)

$chCount = 0
foreach ($ch in $chapters) {
    $chCount++
    Write-Host "[Synthesizing Chapter $chCount/10] $($ch.title) ($($ch.time))..."
    $synth.Speak($ch.script)
}

$synth.SetOutputToNull()
$synth.Dispose()

Write-Host "[OK] 30-Minute Podcast WAV Audio File Successfully Created: $fullWavPath"
