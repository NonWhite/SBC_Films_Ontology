import sys
from copy import deepcopy as copy

CAST_FILES = [ '../data/movies/helenas_cast.txt' , '../data/movies/javier_cast.txt' , '../data/movies/johnny_cast.txt' , '../data/movies/scarlett_cast.txt' , '../data/movies/woody_cast.txt' , '../data/movies/tim_cast.txt' ]
DIRECTOR_FILES = [ '../data/movies/helenas_directors.txt' , '../data/movies/javier_directors.txt' , '../data/movies/scarlett_directors.txt' , '../data/movies/johnny_directors.txt' ]
MOVIES_DIRECTOR = [ ( 'Woody Allen' , '../data/directors/woody_allen.txt' ) , ( 'Tim Burton' , '../data/directors/tim_burton.txt' ) ]
TO_REPLACE = [ "\"" , "'" , ":" , "." , "," , "/" ]

def standard_personname( actorname ) :
	st = actorname
	pos_par = st.find( '(' )
	if pos_par >= 0 : st = st[ :pos_par ]
	spl = st.split( ',' )
	if len( spl ) == 1 : return spl[ 0 ]
	spl = ( "%s %s" % ( spl[ 1 ] , spl[ 0 ] ) ).strip()
	for p in TO_REPLACE : spl = spl.replace( p , '' )
	spl = spl.replace( '  ' , ' ' )
	return spl

def read_directors( info ) :
	divide = lambda l : [ l.split( '(' )[ 0 ].strip() , l.split( '(' )[ 1 ][ :-1 ] ]
	node = { 'director' : [] , 'name' : '' , 'year' : 0 , 'cast' : [] }
	for direct , fpath in MOVIES_DIRECTOR :
		print "Reading directors from %s" % fpath
		with open( fpath , 'r' ) as f :
			for line in f :
				line = line[ :-1 ]
				movie , year = divide( line )
				if movie not in info : info[ movie ] = copy( node )
				info[ movie ][ 'year' ] = int( year )
				info[ movie ][ 'name' ] = movie
				if direct not in info[ movie ][ 'director' ] :
					info[ movie ][ 'director' ].append( direct )
	#for k in info : print info[ k ]

	for fpath in DIRECTOR_FILES :
		print "Reading directors from %s" % fpath
		with open( fpath , 'r' ) as f :
			for line in f :
				line = line[ :-1 ]
				if line.startswith( 'MOVIE' ) :
					movie , year = divide( line[ 8: ] )
					if movie not in info : info[ movie ] = copy( node )
					info[ movie ][ 'year' ] = int( year )
					info[ movie ][ 'name' ] = movie
				else :
					direct = line.strip()
					direct = standard_personname( direct )
					if direct not in info[ movie ][ 'director' ] :
						info[ movie ][ 'director' ].append( direct )
	#for k in info : print info[ k ]

def read_actors( info ) :
	divide = lambda l : [ l.split( '(' )[ 0 ].strip() , l.split( '(' )[ 1 ][ :-1 ] ]
	node = { 'director' : [] , 'name' : '' , 'year' : 0 , 'cast' : [] }
	for fpath in CAST_FILES :
		print "Reading actors from %s" % fpath
		with open( fpath , 'r' ) as f :
			for line in f :
				line = line[ :-1 ]
				if line.startswith( 'MOVIE' ) :
					movie , year = divide( line[ 8: ] )
					if movie not in info : info[ movie ] = copy( node )
					info[ movie ][ 'year' ] = int( year )
					info[ movie ][ 'name' ] = movie
				else :
					actor = line.strip()
					actor = standard_personname( actor )
					if actor not in info[ movie ][ 'cast' ] :
						info[ movie ][ 'cast' ].append( actor )
	#for k in info : print info[ k ]

def export( info ) :
	isempty = lambda v : len( v ) == 0
	cont = 0
	fpath = '../data/movies/all_movies.txt'
	print "Exporting data to %s" % fpath
	with open( fpath , 'w' ) as f :
		for k in info :
			if isempty( info[ k ][ 'director' ] ) : continue
			if isempty( info[ k ][ 'cast' ] ) : continue
			if info[ k ][ 'year' ] == 0 : continue
			f.write( "MOVIE\n" )
			f.write( "\t%s\n" % info[ k ][ 'name' ] )
			f.write( "YEAR\n" )
			f.write( "\t%s\n" % info[ k ][ 'year' ] )
			f.write( "DIRECTOR\n" )
			for d in info[ k ][ 'director' ] : f.write( "\t%s\n" % d )
			f.write( "CAST\n" )
			for c in info[ k ][ 'cast' ] : f.write( "\t%s\n" % c )
			cont += 1
	print "%s movies exported" % cont
	

def merge_info() :
	info = {}
	read_directors( info )
	read_actors( info )
	export( info )

if __name__ == '__main__' :
	merge_info()
