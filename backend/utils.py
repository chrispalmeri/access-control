from configparser import ConfigParser
from datetime import datetime, timezone

def read_config_file(filename):
    parser = ConfigParser()

    with open(filename, encoding='utf-8') as raw_file:
        # add [data] cause ConfigParser requires ini "sections"
        file_content = '[data]\n' + raw_file.read()
        parser.read_string(file_content)

    return parser['data']

# sqlite CURRENT_TIMESTAMP has space seperator, no millis, no timezone
# datetime.utcnow().isoformat(timespec='milliseconds') + 'Z' is not actually timezone aware
# can use json replacer/reviver in js: new Date().toISOString()/new Date(value)

def iso_timestamp():
    output = datetime.now(tz=timezone.utc).isoformat(timespec='milliseconds')
    # has +00:00 instead of Z, replace just for consistency with js
    output = output.replace('+00:00', 'Z')
    return output

def utc_time_float():
    """Not used anywhere"""
    return datetime.now(tz=timezone.utc).timestamp()
