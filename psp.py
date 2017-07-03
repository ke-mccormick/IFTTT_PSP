from subprocess import check_output
import datetime
import getopt
import os
import sys
import time
import urllib.request

# Returns file path as string.
def get_file_path(file):
    file_path = os.path.join(sys.path[0], file)
    return file_path

# Returns the current PSP hourly price as string.
def get_psp_price():
    psp_request = urllib.request.Request('https://www.powersmartpricing.org/psp/servlet?type=instantHOURlyfullsite')
    psp_response = urllib.request.urlopen(psp_request)
    psp_price_string = psp_response.read()
    psp_price_elements = psp_price_string.split()
    current_psp_price = psp_price_elements[3].decode()
    return current_psp_price

# IFTTT Execute Event
def IFTTT_execute(event):
    IFTTT_file = open(get_file_path('IFTTT_id.txt'), 'r')
    IFTTT_id = IFTTT_file.read()
    command = 'curl -s -X POST https://maker.ifttt.com/trigger/' + event + '/with/key/' + IFTTT_id
    check_output(command, shell=True).decode()
    return None

# Print Press ENTER to exit message and exit after user hits ENTER.
def press_ENTER_exit_message():
    input('\n' + 'Press ENTER to exit')
    sys.exit()
    return None

# Print file usage statement.
def usage():
    print('Usage: psp.py -n -p price')
    print('-n        Optional: Enables IFTTT notification.')
    print('-p price  Required: Defines the maximum Power Smart Pricing price.')
    return None

# Clears the output window.
def clear_output_window():
    os.system('cls' if os.name=='nt' else 'clear')
    return None

# Returns current system time.
def get_system_time():
    time = datetime.datetime.time(datetime.datetime.now())
    return time

# Returns current system hour as integer.
def get_system_hour():
    hour = get_system_time().strftime('%H')
    return int(hour)

# Returns current system minute as integer.
def get_system_minute():
    minute = get_system_time().strftime('%M')
    return int(minute)

# Main.
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hnp:',['help','notify','price='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        press_ENTER_exit_message()
    # If no parameters.    
    if not opts:
        print('option -p is required')
        usage()
        press_ENTER_exit_message()

    IFTTT_notify = False
    max_price = float(-1)

    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            press_ENTER_exit_message()
        elif opt in ('-n', '--notify'):
            IFTTT_notify = True
        elif opt in ('-p', '--price'):
            try:
               max_price = float(arg)
            except ValueError:
                usage()
                press_ENTER_exit_message()  
        else:
            assert False, "unhandled option"

    # Max Price must be set.
    if(max_price == -1):
        print('option -p is required')
        usage()
        press_ENTER_exit_message()

    # Keep track of last change.
    previous_hour = -1
    current_hour = get_system_hour()
    current_price = float(0)
    PSP_delay = 15
    PSP_High = -1
    
    # Need loop here.
    while(True):
        # Check for time change.
        while(previous_hour == current_hour):
            time.sleep(1) # Delay for 1 seconds.
            current_hour = get_system_hour() # Update current hour.
        # If hour has just changed, wait for PSP website to updated price.
        if(get_system_minute() == 0):
            clear_output_window()
            print('Updating Current PSP Price')
            print('Please Wait ' + str(PSP_delay) + ' Seconds...')
            time.sleep(PSP_delay) # Delay for PSP_delay number of seconds.
            clear_output_window()
        previous_hour = current_hour # Update previous hour to current hour.
        print('Update Triggered at ' + get_system_time().strftime('%H:%M:%S')) # Display Current Time
        print('Max Price is ' + str(max_price)) # Print Max Price
        current_price = float(get_psp_price()) # Update Current Price
        print('Current Price is ' + str(current_price)) # Display Current Price
        # If current price is cheaper than max price, resume program else set away indefinitely.
        if(current_price <= max_price):
            print('Current Price Less Than Or Equal To Max Price')
            IFTTT_execute('PSP_Price_Low')
            # Notify once when price changed.
            if(IFTTT_notify == True and PSP_High != 0):
                IFTTT_execute('PSP_Price_Low_Notify')
            PSP_High = 0
        else:
            print('Current Price Greater Than Max Price')
            IFTTT_execute('PSP_Price_High')
            # Notify once when price changed.
            if(IFTTT_notify == True and PSP_High != 1):
                IFTTT_execute('PSP_Price_High_Notify')
            PSP_High = 1

        print('Please Wait For Next Hourly Update...')

    press_ENTER_exit_message()

if __name__ == "__main__":
    main()
