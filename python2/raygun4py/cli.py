from optparse import OptionParser
from raygun4py import raygunprovider

def main():
    usage = '\n  raygun [options]\n  raygun install <apikey>\n  raygun test'
    parser = OptionParser(usage=usage)
    
    parser.add_option('-a', '--apikey', dest='apikey', help='Your API key, available on the Application Settings page in the Raygun web app')

    options, args = parser.parse_args()

    if 'install' in args:
        if len(args) > 1:
            print "Installed API key! Now run 'raygun test' to check it's working"
        else:
            print 'Please provide a Raygun API key!'
    elif 'test' in args:
        print 'Sending a test exception...'
    elif options.apikey:
        print 'Updated API key'
    else:
        parser.print_help()
