if (Get-Process logonui -ea silentlycontinue) {
    # Code to put Windows to sleep
    Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;

    public class SleepUtils {
        [DllImport("powrprof.dll", SetLastError = true)]
        public static extern bool SetSuspendState(bool hibernate, bool forceCritical, bool disableWakeEvent);
    }
"@
    [SleepUtils]::SetSuspendState($false, $true, $false)

}
