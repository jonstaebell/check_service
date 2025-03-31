# check_service
(c) 2025 Jon Staebell

Program to turn check a list of services to see if they're running or not

## Description

When run, checks each service in the list and prints status.
If a Discword webhook url is provided, will raise an alert if there's an error.
Uses a snooze time parameter in the configuration file to prevent spamming Discord notifications.

### Dependencies

Requires crontab set up to run every 5 minutes during desired times. 
e.g. to set to run between 7 a.m. and 9:55 p.m. use:
*/5 7-21 * * * /path/to/python /path/to/check_service.py

Set the following parameters in grandfather.ini: 
   service_name
   snooze_time
   webhook_url (optional, set to "" to disable Discord webhook calls on errors)
(if program is renamed, need to rename the .ini file. E.g. if renamed "foo.py" it looks for "foo.ini")

### Executing program

* install in same directory as check_service.ini
* python3 check_service.py 

## Authors

Jon Staebell
jonstaebell@gmail.com

## Version History

* V1
    * Initial Release 3/31/2025

## License

check_service Copyright (C) 2025 Jon Staebell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Acknowledgments



