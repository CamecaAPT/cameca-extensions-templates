using System.Runtime.Versioning;

#if NET5_0_OR_GREATER
// Only support Windows 10
[assembly: SupportedOSPlatform("windows10.0")]
#endif