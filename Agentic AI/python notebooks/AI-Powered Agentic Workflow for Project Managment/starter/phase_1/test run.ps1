$Folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputFile = Join-Path $Folder "phase1Output.txt"
$Divider = "=" * 80

# Clear/create output file
"" | Set-Content $OutputFile

$TestFiles = Get-ChildItem -Path $Folder -Filter "*_test.py" | Sort-Object Name

foreach ($TestFile in $TestFiles) {

    Add-Content $OutputFile $Divider
    Add-Content $OutputFile $TestFile.Name
    Add-Content $OutputFile $Divider
    Add-Content $OutputFile ""

    # Run Python file and capture stdout + stderr
    $Output = & python $TestFile.FullName 2>&1

    $Output | Add-Content $OutputFile

    Add-Content $OutputFile ""
    Add-Content $OutputFile "Exit Code: $LASTEXITCODE"
    Add-Content $OutputFile ""
    Add-Content $OutputFile $Divider
    Add-Content $OutputFile ""
}

Write-Host "Finished running $($TestFiles.Count) test files."
Write-Host "Output written to: $OutputFile"