Get-NetAdapterBinding -ComponentID ms_tcpip6 | Select-Object -Property Name, ComponentID, Enabled
Get-NetAdapterBinding -ComponentID ms_tcpip6 |
Where-Object Enabled -eq $False |
Select-Object name |
ForEach-Object {
    sudo Enable-NetAdapterBinding -Name $_.name -ComponentID ms_tcpip6
}
# Get-NetAdapterBinding -ComponentID ms_tcpip6 | Select-Object -Property Name, Enabled