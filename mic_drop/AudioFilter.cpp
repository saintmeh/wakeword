#include <ks.h>
#include <ksmedia.h>


const KSPIN_DESCRIPTOR_EX PinDescriptors[] = {
    {
        NULL,                        
        NULL,                        
        {
            0,                       
            NULL,                    
            0,                       
            NULL,                    
            SIZEOF_ARRAY(NULL),      
            NULL,                    
            KSPIN_DATAFLOW_OUT,      
            KSPIN_COMMUNICATION_NONE 
        },
        KSPIN_FLAG_FIXED_FORMAT,    
        1,                          
        1,                          
        NULL,                       
        NULL                        
    }
};