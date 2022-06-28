$DEBUG = 0

function getFilePath {
    $resout = Split-Path -Parent $MyInvocation.MyCommand.Definition
    return  $resout + "\IPv6Addr.txt"
}
function getAddrFromFile {
    $filePath = getFilePath
    if (Test-Path  $filePath) {
        $ipInfoFromFile = (Get-Content $docPath)[-1]
        if ($ipInfoFromFile -ne "") {
            $ipInfoFromFile = $ipInfoFromFile -replace "^*(\[)([\s\S]*)(\])", ""
            if ($DEBUG) {
                Write-Output $IPv6Addr
            }
            return $ipInfoFromFile
        }
    }
    else {
        # New-Item "IPv6Addr.txt"
        return ""
    }
}

function getAddrFromLocal {
    $ipInfoList = [net.dns]::GetHostAddresses('') | Select-Object -ExpandProperty IPAddressToString
    foreach ($ipInfoLine in $ipInfoList) {
        if ($ipInfoLine -match "^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$" -and $ipInfoLine -match "^2") {
            # $ipInfo = $ipInfoLine
            return $ipInfoLine
            # break
        }
    }
}


function getAddrFromNslookup {
    $ipInfoFromNslookup = nslookup.exe -qt=AAAA nrtqn.noip.cn
    foreach ($ipInfoLine in $ipInfoFromNslookup) {
        if ($ipInfoLine -match "^Address") {
            $ipInfoLine = $ipInfoLine.Split(" ")[-1]
            if ($ipInfoLine -match "^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$" -and $ipInfoLine -match "^2") {
                if ($DEBUG) {
                    Write-Output $ipInfoLine
                }
                return $ipInfoLine
            }
        }
    }
}

function updateAddr {
    param (
        $ipInfoFromFile,
        $ipInfoFromLocal,
        $ipInfoFromNslookup
    )
    $output = "`r[", $(Get-Date), "]"
    $docPath = getFilePath
    if ($ipInfoFromFile -eq $ipInfoFromLocal -eq $ipInfoFromNslookup ) {
        $ipInfo = $ipInfoFromLocal
        $ipUrl = "http://ipv6.meibu.com/?name=nrtqn.noip.cn&pwd=XYze91l9vEONar0Z&ipv6=$ipInfo"
        $ipUrl_1 = "http://ipv6.meibu.com/?name=primimya.noip.cn&pwd=XYze91l9vEONar0Z&ipv6=$ipInfo"
        curl -s $ipUrl
        curl -s $ipUrl_1
        $output += "[T]"
    }
    else {
        $output += "[F]"
    }
    $output += $ipInfo -join ("")
    $output | Out-File -NoNewline -Append -FilePath $docPath
    Write-Output $output
}


function main {
    $ip1 = getAddrFromFile
    $ip2 = getAddrFromLocal
    $ip3 = getAddrFromNslookup
    updateAddr($ip1, $ip2, $ip3)
}
main