

def add_zeros(element):
    
    """This changes the format of postcodes to string with the needed zeros
    

    Args:
        element: individual row from apply codes  
    
    Returns:
        parameter postcode value with zeros

    """
    #postinumeroihin etunollat jos on ollut integer
    element=str(element)
    if len(element) == 3:
        element = "00" + element
    if len(element) == 4:
        element = "0" + element
    return(element)


def add_zeros_muncipality(element):
    """This changes the format of municipalities to string with the needed zeros
    

    Args:
        element: individual row from apply codes  
    
    Returns:
        parameter municipality value with zeros

    """
    element=str(element)
    if len(element) == 1:
        element = "00" + element
    if len(element) == 2:
        element = "0" + element
    return(element)