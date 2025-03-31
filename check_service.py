import subprocess, configparser, sys, os, requests, time
from discord_webhook import DiscordWebhook

def main():
    config_file = sys.argv[0].replace(".py", ".ini") # config file is program name with .py replaced by .ini
    err_file_path = sys.argv[0].replace(".py", ".err") # err file is program name with .py replaced by .err
    params = get_config(config_file) # get program parameters from config file
    err_list = "" # list of services that are not running

    if params != {}:
        for element in params['service_name']:
            status = get_service_status(element)
            print (f"\033[32m{element} is running.\033[0m " if status else f"\033[31m{element} is not running.\033[0m ")
            if not status:
                err_list += element + " " # err_list is a list of all services in error

        if err_list == "": # all services are running, so
            # delete contents of error file by writing empty string
            _ = write_err(err_file_path, "")
        else:
            # if the new_alarm function says the error list has changed or snooze time has elapsed
            # then call the webhook
            if new_alarm(params['snooze_time'], err_file_path, err_list):
                call_webhook(params['webhook_url'], "services not running: " + err_list)

def write_err(err_file_path, err):
    # reads content of error file and compares the error parameter to the contents of the file
    # if the error and file contents are the same, returns False
    # if the error and file contents differ, writes the new error to the file and returns True
    with open(err_file_path, 'r+') as file:
        old_err = file.read()
        if old_err != err:
            file.seek(0)
            file.write(err) # write new error message
            file.truncate()
            change = True 
        else:
            change = False
        file.close()
    return change

def get_config(config_file):
    # return paramaters from configuration file
    #
    param_dict = {}
    try:
        Config = configparser.ConfigParser()
        Config.read(config_file)
        param_dict["service_name"] = Config.get('required', 'service_name').split()
        param_dict["webhook_url"] = Config.get('required', 'webhook_url')
        param_dict["snooze_time"] = int(Config.get('required', 'snooze_time'))
    except:
        print (f"invalid config file {config_file}")
        return {} # return empty list on exceptions
    return param_dict

def get_service_status(service_name):
   # Gets the status of a Linux service using systemctl
   # returns True if the service is running and active, false if not
   #
   try:
        output = subprocess.check_output(["systemctl","is-active", service_name], stderr=subprocess.STDOUT)
        return output.decode().strip() == "active"
   except subprocess.CalledProcessError:
        return False

def call_webhook(webhook_url, output_message): 
    # checks the webhook_url parameter, and if present, uses it to send webhook to Discord
    #
    if webhook_url != "": # if url provided, notify Discord to add alert 
        program_name, _ = os.path.splitext(os.path.basename(sys.argv[0])) # remove path and extension from current program name
        webhook = DiscordWebhook(url=webhook_url, content=f"{program_name}: {output_message}")
        response = webhook.execute()
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error in trying to use Discord Webhook", err)

def new_alarm (snooze_time, file_path, err_list):
    # checks the file used to track when the last alarm occured, and
    # returns True if it's recent, False if not
    #
    try:
        # if time since last modified is greater than snooze time, return True
        create_alarm = (time.time() - os.path.getmtime(file_path)) > snooze_time
    except FileNotFoundError:
        create_alarm = True # file doesn't exist so need to create an alarm

    if create_alarm:
        # touch file to update modification time and create if it doesn't exist
        with open(file_path, 'a'):
            os.utime(file_path, None)
    
    # return true if create_alarm indicates enough time has elapsed
    # OR if write_err indicates that the error list has changed in the file
    return create_alarm or write_err(file_path, err_list)

if __name__ == "__main__":
    main()
