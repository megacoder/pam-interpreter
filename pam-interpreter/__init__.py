#!/usr/bin/env python

import  os
import  sys
import  argparse

class	PamInterpreter( object ):

    def	__init__( self ):
        self.topdir = '/etc/pam.d'
        return

    def do_app( self, app ):
        fn = os.path.join(
            self.topdir,
            app
        )
        if not os.path.isfile( fn ):
            print >>sys.stderr, 'Unknown application "{0}"'.format( app )
            return
        rules = dict()
        with open( fn ) as f:
            for line in f:
                tokens = map(
                    str.strip,
                    line.split( '#', 1 )[0].split()
                )
                if len( tokens ) < 3: continue
                kind = tokens[ 0 ]
                args = tokens[ 1: ]
                rules[kind] = rules.get( kind, [] ) + [ args ]
            for kind in sorted( rules ):
                print 'Kind {0}:'.format( kind )
                for a in rules[kind]:
                    print '  --> {0}'.format( a )
        return

    def	main( self ):
	retval = 0
        p = argparse.ArgumentParser(
        )
        p.add_argument(
            '-o',
            '--out',
            dest    = 'ofile',
            metavar = 'FILE',
            default = None,
            help    = 'output here if not stdout',
        )
        Version = 'v0.0.0'
        p.add_argument(
            '-v',
            '--version',
            action  = 'version',
            version = Version,
            help    = 'Proram version {0}'.format( Version ),
        )
        p.add_argument(
            dest = 'apps',
            nargs = '+',
            metavar = 'app',
            help = 'applications do describe',
        )
        opts = p.parse_args()
        #
        if opts.ofile:
            self.out = open( opts.ofile, 'w+' )
        else:
            self.out = sys.stdout
        #
        for app in opts.apps:
            self.do_app( app )
        #
	return retval

    def	report( self ):
	pass

if __name__ == '__main__':
    pi = PamInterpreter()
    exit( pi.main() )
