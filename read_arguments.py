import sys, argparse
from _version import __version__, __name__



def read_arguments(args):
    """

    :param args: List of arguments
    :return: TCP_IP, TCP_PORT, BUFFER_SIZE, test mode
    """
    TCP_IP = '0.0.0.0'
    TCP_PORT = 4533
    BUFFER_SIZE = 100

    parser = argparse.ArgumentParser(prog=__name__, usage='%(prog)s [options]')

    # Adding arguments
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s is version: {Version}'.format(Name=__name__, Version=__version__)
    )

    parser.add_argument(
        '--port',
        type=int,
        default=TCP_PORT,
        help='Port number to use (must be a positive integer between 1 and 65535).'
    )
    parser.add_argument(
        '--host',
        type=str,
        default=TCP_IP,
        help='Hostname (default: 0.0.0.0).'
    )
    parser.add_argument(
        '--buffer',
        type=int,
        default=BUFFER_SIZE,
        help='Buffer size for the socket connection'
    )
    parser.add_argument(
        '--test_mode',
        action='store_true',
        default="store_false",
        help='Test mode will allow to send specific commande to the rotator, '
             'must be tested direcly on the rotator host'
    )

    args = parser.parse_args()
    print('Parser args:', args)
    TCP_IP = args.host
    TCP_PORT = args.port
    BUFFER_SIZE = args.buffer


    return TCP_IP, TCP_PORT, BUFFER_SIZE, args.test_mode