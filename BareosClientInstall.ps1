[CmdletBinding()]
param (
    [boolean] $force = $false
)
. "\\villejuif.fr\netlogon\powershell\framework.ps1"

Write_Title -text "Script d'installation et d'inscription du client Bareos sur les serveurs"

#################################################################################################################
### Paramètres & constantes
#################################################################################################################
$certificatePolicy = "IDontCarePolicy"
$bareosServer    = "vjstore.villejuif.fr"
$bareosInstaller = "\\villejuif.fr\netlogon\Deploy\BAREOS\winbareos-16.2.4-postvista-64-bit-r14.1"
$bareosConfFile  = "C:\ProgramData\Bareos\bareos-fd.d\director\bareos-dir.conf" # depuis la version 16.x
$bareosUri       = "https://$($bareosServer):10000/bareossetup/index.cgi"
$clientName      = "$($env:COMPUTERNAME)".ToLower()
$urlData         = @{
    add      = 1;
    os       = "windows";
    host     ="$($clientName)";
}

#################################################################################################################
### Fonctions
#################################################################################################################
Function Get-DirectorPassword
{
    param()
    return ((Get-Content $bareosConfFile  | Select-String -Pattern "Password").ToString().split("=")[1].Split('"')[1])
}

Function Set-DirectorName
{
    param()
    ((Get-Content $bareosConfFile) -replace "bareos","vjstore") | Out-File -FilePath $bareosConfFile -Force -Encoding utf8
}

Function Is-BareosInstalled
{
    param()
    return (Test-Path -Path $bareosConfFile) -eq $true
}

Function Install-Bareos
{
    param()
    Write_Info -text "Installation du client Bareos en cours, merci de patienter"
    Start-Process -FilePath $bareosInstaller -ArgumentList "/S /D='C:\Program Files\Bareos' /DIRECTORNAME='vjstore'" -NoNewWindow -Wait
}

Function Registrate-ClientOnServer
{
    param()
    Write_Info -text "Enregistrement du client"
    $request = (Invoke-WebRequest -Method Post -ContentType "application/json" -Body $urlData -Uri $bareosUri)
    If($request.StatusCode -eq 200){
        Write_OK -text "OK"
    }Else{
        Write_Error -text "Erreur lors de l'enregistrement"
    }
}

Function Is-AttentedCertificatePolicy
{
    param()
    [System.Net.ServicePointManager]::CertificatePolicy
    return ([System.Net.ServicePointManager]::CertificatePolicy.ToString() -eq $certificatePolicy)
}

Function Set-AttentedCertificatePolicy
{
    param()
    add-type @"
	using System.Net;
	using System.Security.Cryptography.X509Certificates;

		public class IDontCarePolicy : ICertificatePolicy {
		public IDontCarePolicy() {}
		public bool CheckValidationResult(
			ServicePoint sPoint, X509Certificate cert,
			WebRequest wRequest, int certProb) {
			return true;
		}
	}
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object $($certificatePolicy)
}

#################################################################################################################
### Procédure du script
#################################################################################################################
If(!(Is-BareosInstalled) -or ($force -eq $true)){
    Install-Bareos

    # application d'une politique de certificat libertaire pour le webservice
    If(Is-AttentedCertificatePolicy -ne $true){
        Set-AttentedCertificatePolicy
    }

    Set-DirectorName
    $directorPassword  = Get-DirectorPassword
    $urlData.Add("password", $directorPassword)
    Registrate-ClientOnServer

    Write_Info -text "Redémarrage du service Bareos-FD"
    Stop-Service "Bareos-fd" -Force
    Start-Service "Bareos-fd"
}