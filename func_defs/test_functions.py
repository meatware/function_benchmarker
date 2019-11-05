""" Place to store function sto be tested."""
import logging 

LOG = logging.getLogger(__name__)

def check_substrings_0(test_string, check_str_list, inc_exc_switch):
    """First naive attempt."""

    if inc_exc_switch == "exclude":
        for substring in check_str_list:
            if substring.lower() in test_string.lower():
                return False
    elif inc_exc_switch == "include":
        for substring in check_str_list:
            if substring.lower() not in test_string.lower():
                return False
    return True

def check_substrings_1(test_string, check_str_list, inc_exc_switch):
    """Second naive attempt."""

    test_string_lower = test_string.lower()
    if inc_exc_switch == "exclude":
        for substring in check_str_list:
            if substring.lower() in test_string_lower:
                return False
    elif inc_exc_switch == "include":
        for substring in check_str_list:
            if substring.lower() not in test_string_lower:
                return False
    return True

def check_substrings_artur_initial(test_string, check_str_list, inc_exc_switch):
    """Artur's initial."""
    test_string_lower = test_string.lower()
    flag = True if inc_exc_switch == "include" else False
    for substring in check_str_list:
        if substring.lower() in test_string_lower:
            return flag
    return not flag
    
def check_substrings_giles(test_string, check_str_list, inc_exc_switch):
    """Giles's Ugly attempt"""
    return True if (len([s for s in check_str_list if s.lower() in test_string.lower()])>=1) == (inc_exc_switch == "include") else False
    
def check_substrings_artur(test_string, check_str_list, inc_exc_switch):
    """Artur's improvement ogn Giles."""
    test_string_lower = test_string.lower()
    return (inc_exc_switch == "include") if (len([ True for substring in check_str_list if substring.lower() in test_string_lower] ) >=1) else (inc_exc_switch != "include")

