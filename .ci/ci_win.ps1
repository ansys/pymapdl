<#
.SYNOPSIS 
    Groups many different powershell actions in one file/library.
.DESCRIPTION 
    It offers the following workflows
    - jfrog: Checks if jfrog CLI () is installed or not. If not, it will install it.
.NOTES 
    Additional Notes, eg 
    Author     : German Martinez-Ayuso - german.ayuso@ansys.com 
    Appears in -full  
.PARAMETER switcher 
    String with the 
.PARAMETER bar 
   Example of a parameter definition for a parameter that does not exist. 
   Does not appear at all. 
#>

$switcher = $args[0]  # 

if ($switcher -eq "jfrog")
{
    # Checking if jfrog is installed 
    Write-Output "Checking existence of jFrog CLI"
    $command = "jf"
    if (Get-Command $command -errorAction SilentlyContinue) {
        Write-Output "$command exists"
    } else {
        Write-Output "$command does not exist. Installing it..."
        Start-Process -Wait -Verb RunAs powershell '-NoProfile iwr https://releases.jfrog.io/artifactory/jfrog-cli/v2-jf/[RELEASE]/jfrog-cli-windows-amd64/jf.exe -OutFile $env:SYSTEMROOT\system32\jf.exe'
        Write-Output "$command installed!"
    }

} elseif ($switcher -eq "git")
{
    Write-Output "Checking existence of git CLI"
    $command = "git"
    if (Get-Command $command -errorAction SilentlyContinue) {
        Write-Output "$command exists"
    }
    else {
        Write-Output "$command does not exist. Installing it..."
        winget install --id Git.Git -e --source winget
        Write-Output "$command installed!"
    }
} else {
    Write-Output "no frog!"
}