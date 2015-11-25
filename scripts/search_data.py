import sys

FILES = [ '../raw_data/actors.list' , '../raw_data/actresses.list' , '../raw_data/directors.list' ]
TO_PRUNE = [ '(TV)' , '(V)' , '{' , '(voice)' , '(archive footage)' , '(uncredited)' , '(VG)' , '(????)' ]

def parse( fpath , search ) :
	#search = search.lower()
	to_prune = lambda s : sum( [ s.find( p ) >= 0 for p in TO_PRUNE ] ) > 0
	with open( fpath , 'r' ) as f :
		found = False
		for line in f :
			#line = line[ :-1 ].lower()
			line = line[ :-1 ]
			if line.startswith( search ) :
				if not found :
					found = True
				if not to_prune( line ) :
					print line
			elif line.startswith( '\t' ) and found :
				if not to_prune( line ) :
					print line
			elif not line.startswith( search ) and found :
				found = False

if __name__ == '__main__' :
	if len( sys.argv ) > 2 :
		idx , search = sys.argv[ 1: ]
		parse( FILES[ int( idx ) ] , search )
	else :
		print 'usage: %s [index_of_file] [string_to_seach]' % sys.argv[ 0 ]
