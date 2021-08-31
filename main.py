import socket
import requests
import argparse


def login(ip, args):
    args.ip = ip
    args.device = 0 if args.device == 'pc' else 1
    res = requests.get(
        'http://10.0.1.5:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C{device}%2C{account}%40{operator}&user_password={password}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=10.32.254.33&wlan_ac_name='
        .format_map(vars(args)))
    print(res.text)
    print('Verify Connect....')
    ver = requests.get('http://www.baidu.com')
    if ver.status_code == 200:
        print('You are surfing the Internet')
    else:
        print('error!response is', ver)


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-a', '--account')
    parser.add_argument('-p', '--password')
    parser.add_argument('-o',
                        '--operator',
                        default='',
                        choices=['cmcc', 'telecom', 'unicom'],
                        help='operator,cmcc,telecom,unicom')
    parser.add_argument('-d',
                        '--device',
                        default='pc',
                        choices=['pc','phone'],
                        help='Select the id of the login device')
    return parser.parse_args()


if __name__ == '__main__':
    ip = get_ip()
    args = get_args()
    login(ip, args)
