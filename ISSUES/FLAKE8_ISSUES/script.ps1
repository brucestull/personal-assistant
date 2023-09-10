$sourceFile = "C:\Users\FlynntKnapp\Programming\personal-assitant\Powershell\test_file_flake8_issues.txt"
$e501File = "C:\Users\FlynntKnapp\Programming\personal-assitant\Powershell\e501.txt"
$noE501File = "C:\Users\FlynntKnapp\Programming\personal-assitant\Powershell\no_e501.txt"

Get-Content $sourceFile | ForEach-Object {
    if ($_ -match "E501") {
        Add-Content $e501File $_
    } else {
        Add-Content $noE501File $_
    }
}