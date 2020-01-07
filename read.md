##固件打包

`pyinstaller -F src/local2gps.py`



##使用方法

```bash
$ python ./src/local2gps.py -h

usage: local2gps.py -h -z [+/-]HH:MM [Y-m-d H:M:S]

convert local time to gps time

positional arguments:
  Y-m-d H:M:S           local time to convert. if not exit, the system current
                        time will be taken

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -z [+/-]HH:MM, --zone [+/-]HH:MM
                        local time zone, default value is +08:00
  -p LEAPS              leap senconds since gps epoch, default value is 13s
                        since 2000

When the time zone is negative, you need to add a space before '-' and use
quotes marks, such as ' -8:00'

```



