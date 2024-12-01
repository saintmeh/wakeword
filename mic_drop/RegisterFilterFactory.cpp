NTSTATUS DriverEntry(
    PDRIVER_OBJECT DriverObject,
    PUNICODE_STRING RegistryPath
)
{
    UNREFERENCED_PARAMETER(RegistryPath);

    DriverObject->DriverUnload = DriverUnload;

    KdPrint(("Initializing Dummy Microphone Driver...\n"));

    
    NTSTATUS status = KsInitializeDriver(DriverObject);
    if (!NT_SUCCESS(status)) {
        KdPrint(("KsInitializeDriver failed: 0x%X\n", status));
        return status;
    }

    status = KsCreateFilterFactory(
        DriverObject,
        &FilterDescriptor,
        NULL 
    );

    if (!NT_SUCCESS(status)) {
        KdPrint(("Failed to create filter factory: 0x%X\n", status));
        return status;
    }

    KdPrint(("Dummy Microphone Driver initialized successfully!\n"));
    return STATUS_SUCCESS;
}