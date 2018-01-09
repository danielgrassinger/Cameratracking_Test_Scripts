import configparser
import argparse

'''

'''

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser()

    parser.add_argument('--input', action='store', dest='input',
                        help='Select a camera or video as input')
    parser.add_argument('--gui', action='store', dest='gui',
                        help='Select a camera or video as input')

    results = parser.parse_args()
    if results.input != None:
        print(results.input)
        config['Input']['videoinput']= results.input
    if(results.gui=='True'):
        print('gui')
        config['Output']['screenoutput'] = 'True'

    elif results.gui == 'False':
        print('No gui')
        config['Output']['screenoutput'] = 'False'

    for section in config.sections():
        print(section)
        for option in config[section]:
            print(option + ' ' + config[section][option])

if __name__ == "__main__":
    main()