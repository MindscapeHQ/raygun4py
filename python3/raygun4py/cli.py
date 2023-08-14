from optparse import OptionParser

from raygun4py import raygunprovider


def main():
    usage = '\n  raygun4py test <apikey>'
    parser = OptionParser(usage=usage)

    _, args = parser.parse_args()

    if len(args) < 2 or not isinstance(args[1], str):
        print('Please provide your API key')
        parser.print_help()
    elif args[0] == 'test':
        send_test_exception(args[1])
    else:
        print(f"Invalid command '{args[0]}'")
        parser.print_help()


def send_test_exception(apikey):
    client = raygunprovider.RaygunSender(apikey)

    try:
        raise Exception("Test exception from Raygun4py (Python3)")
    except Exception:
        response = client.send_exception()

        if response[0] == 202:
            print("Success! Now check your Raygun dashboard at https://app.raygun.com")
        else:
            print(
                "Something went wrong - please check your API key or contact us for help. The response was:")
            print(response)
