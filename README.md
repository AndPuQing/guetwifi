# guetwifi

This is a simple script to connect to the GUET-WIFI and keep it alive!!!!!!.

## Usage

### Installation

```bash
pip install guetwifi
```

### help

```bash
guetwifi --help
```

```bash
Usage: guetwifi [OPTIONS] COMMAND [ARGS]...

  GuetWifi is a command line tool for GUET-WIFI login

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  config   Config your GUET-WIFI account and password
  log      Show guetwifi log
  restart  Restart guetwifi
  start    Start guetwifi
  status   Check guetwifi status
  stop     Stop guetwifi
  version  Show guetwifi version
```

### config

```bash
guetwifi config --help
```

```bash
guetwifi config -a <account> -p <password>
```

you can set the isp to `cmcc` or `telecom` and `unicom` using `-i` option.

```bash
guetwifi config -a <account> -p <password> -i <isp>
```

### start

```bash
guetwifi start
```

### stop

```bash
guetwifi stop
```

### status

```bash
guetwifi status
```

### log

```bash
guetwifi log
```
