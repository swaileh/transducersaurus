#!/usr/bin/python

class hmm2wfst( ):
    """
       Generate the H-level transducer.
       Expects an AT&T text-format hmm.hmm file as input.
       The hmm.hmm file is generated by the sphinx-am2wfst package: 
          http://code.google.com/p/sphinx-am2wfst/
       It takes the following form:
       ----------------------------------------
        c.isym   n/a   state1  state2  state3
          1       1       1       2       3
          2       1       4       5       6
          3       1       7       8       9
       ----------------------------------------
        where the c.isym is either a monophone or context-dependent
        triphone, and the states refer to the HMM state.  It is 
        currently hard-wired to a 3-state hmm configuration.  
        This is essentially a subset of the Sphinx mdef file listing.
        The hmm.hmm approach simplifies the H-level build by assuming
        a standardized AM setup, however I haven't written a separate
        htk-am2wfst project yet so for the time being this is
        restricted to use with TCubed and Sphinx models.  It also 
        has yet to be included in the transducersaurus.py build program.
        Nevertheless I HAVE tested it and confirmed that it works!
    """
    def __init__( self, hmm_file, prefix="test", amtype="sphinx", aux_file=None, eps="<eps>" ):
        self.hmm_file = hmm_file
        self.aux      = self._read_aux( aux_file )
        self.prefix   = prefix
        self.amtype   = amtype
        self.eps      = eps
        self.hmm_file_ofp = open( "PREFIX.h.fst.txt".replace("PREFIX",self.prefix), "w" )

    def _read_aux( self, aux_file ):
        aux = set([])
        if aux_file==None:
            return aux
        aux_file_fp = open( aux_file, "r" )
        for line in aux_file_fp:
            line = line.strip()
            aux.add(line)
        return aux

    def _gen_aux( self, ssym ):
        for asym in self.aux:
            self.hmm_file_ofp.write("%d\t%d\t%s\t%s\n" % (ssym, ssym, asym, asym))
        return

    def hmm2wfst( self ):
        hmm_file_ifp = open( self.hmm_file, "r" )
        ssym = 2
        esym = 1
        self._gen_aux( 0 )
        self._gen_aux( 1 )
        for line in hmm_file_ifp:
            line = line.strip()
            hisym, crud, s1, s2, s3 = line.split("\t")
            self.hmm_file_ofp.write("%d\t%d\t%s\t%s\n" % (0,ssym,s1,hisym))
            self._gen_aux( ssym )
            self.hmm_file_ofp.write("%d\t%d\t%s\t0\n"  % (ssym,ssym+1,s2))
            self.hmm_file_ofp.write("%d\t%d\t%s\t0\n"  % (ssym+1,esym,s3))
            ssym += 2
        self.hmm_file_ofp.write("%d\n" % (esym))
        hmm_file_ifp.close()
        self.hmm_file_ofp.close()
        return


if __name__=="__main__":
    import os, sys, argparse
    example = """./hmm2wfst.py --hmm hmm.hmm --aux aux.list --prefix test"""
    parser = argparse.ArgumentParser(description=example)
    parser.add_argument("--hmm",     "-m", help="hmm.hmm file generated during AM conversion.", required=True )
    parser.add_argument("--aux",     "-a", help="Auxiliary symbols list.", default=None )
    parser.add_argument("--prefix",  "-p", help="Filename prefix.", default="test" )
    parser.add_argument("--amtype",  "-t", help="Acoustic Model type. 'sphinx', or 'htk'.", default="sphinx" )
    parser.add_argument("--eps",     "-e", help="Epsilon symbol.", default="<eps>" )
    parser.add_argument("--verbose", "-v", help="Verbose mode.", default=False, action="store_true" )
    args = parser.parse_args( )

    if args.verbose==True:
        print "Running with the following arguments:"
        for attr, value in args.__dict__.iteritems():
            print attr, "=", value        
    
    h2w = hmm2wfst( 
        args.hmm, 
        aux_file=args.aux, 
        prefix=args.prefix,
        amtype=args.amtype,
        eps=args.eps 
        )
    h2w.hmm2wfst( )