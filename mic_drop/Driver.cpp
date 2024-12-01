#include <ntddk.h>
#include <ks.h>
#include <ksmedia.h>

extern "C" NTSTATUS DriverEntry(
    _In_ PDRIVER_OBJECT DriverObject,
    _In_ PUNICODE_STRING RegistryPath
)
{
    UNREFERENCED_PARAMETER(DriverObject);
    UNREFERENCED_PARAMETER(RegistryPath);

    KdPrint(("Dummy microphone driver loaded!\n"));
    return STATUS_SUCCESS;
}

extern "C" void DriverUnload(
    _In_ PDRIVER_OBJECT DriverObject
)
{
    UNREFERENCED_PARAMETER(DriverObject);
    KdPrint(("Dummy microphone driver unloaded!\n"));
}