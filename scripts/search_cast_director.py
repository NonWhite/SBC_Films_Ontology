import sys

FILES = [ '../data/actors/helena_bonham_carter.txt' ,	'../data/actors/javier_bardem.txt' , '../data/actors/johnny_depp.txt' , '../data/actors/scarlett_johansson.txt' ]
DIRECTOR_FILES = [ '../raw_data/directors.list' ]
IGNORE_LINES = [ 239 , 241 ]
TO_PRUNE = [ '(TV)' , '(V)' , '{' , '(voice)' , '(archive footage)' , '(uncredited)' , '(VG)' , '(????)' ]
TO_REPLACE = [ "\"" , "'" , ":" , "." , "," , "/" ]

def standard_moviename( moviename ) :
	st = moviename
	for c in TO_REPLACE : st = st.replace( c , '' )
	par_pos = st.find( ')' )
	st = st[ :par_pos+1 ]
	return st.strip()

def standard_directorname( actorname ) :
	st = actorname
	spl = st.split( ',' )
	if len( spl ) == 1 : return spl[ 0 ]
	return "%s %s" % ( spl[ 1 ] , spl[ 0 ] )

def get_directors( lst_movies ) :
	directors = []
	for x in xrange( len( lst_movies ) ) : directors.append( [] )
	is_actor = lambda l : l[ 0 ].isalpha()
	split_info = lambda l : [ s for s in l.split( '\t' ) if len( s ) > 0 ]
	end_of_list = lambda l : l.startswith( 'SUBMITTING' )
	for k in xrange( len( DIRECTOR_FILES ) ) :
		fpath = DIRECTOR_FILES[ k ]
		print "Searching in %s" % fpath
		with open( fpath , 'r' ) as f :
			cont = 0
			for line in f :
				if cont < IGNORE_LINES[ k ] :
					cont += 1
					continue
				if end_of_list( line ) : break
				if is_actor( line ) :
					inf = split_info( line )
					actor = inf[ 0 ]
					movie = standard_moviename( inf[ 1 ] )
				else :
					inf = split_info( line )
					movie = standard_moviename( inf[ 0 ] )
				for d in xrange( len( lst_movies ) ) :
					if lst_movies[ d ] == movie :
						directors[ d ].append( actor )
	return directors

def get_info( fpath ) :
	#search = search.lower()
	to_prune = lambda s : sum( [ s.find( p ) >= 0 for p in TO_PRUNE ] ) > 0
	movies_to_search = []
	with open( fpath , 'r' ) as f :
		for line in f :
			line = line[ :-1 ]
			movie = standard_moviename( line )
			movies_to_search.append( movie )
	directors = get_directors( movies_to_search )
	for k in xrange( len( movies_to_search ) ) :
		movie = movies_to_search[ k ]
		direct = directors[ k ]
		print "MOVIE = %s" % movie
		for d in direct : print "\t%s" % d

if __name__ == '__main__' :
	if len( sys.argv ) > 1 :
		idx = sys.argv[ 1 ]
		get_info( FILES[ int( idx ) ] )
	else :
		print 'usage: %s [index_of_file]' % sys.argv[ 0 ]
