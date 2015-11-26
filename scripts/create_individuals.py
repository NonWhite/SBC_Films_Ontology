import sys
from copy import deepcopy as copy
from individual_wrappers import *

DATA_FILE = '../data/movies/all_movies.txt'
RDF_FILE = '../data/individuals.rdf'

onto = 'PREFIX onto: <http://www.semanticweb.org/marcelo/ontologies/2015/10/untitled-ontology-4#>'
foaf = 'PREFIX foaf: <http://www.ime.usp.br/~renata/FOAF-modified>'

def read_content( fpath ) :
	data = {}
	node = { 'name' : '' , 'standard_name' : '' , 'year' : 0 , 'director' : [] , 'actors' : [] }
	with open( fpath , 'r' ) as f :
		for line in f :
			line = line[ :-1 ]
			if line[ 0 ].isalpha() :
				key = line
			else :
				line = line.strip()
				if key == 'MOVIE' :
					movie = line
					data[ movie ] = copy( node )
					data[ movie ][ 'name' ] = line
					#data[ movie ][ 'standard_name' ] = camelize( line )
				elif key == 'YEAR' :
					data[ movie ][ 'year' ] = int( line )
				elif key == 'DIRECTOR' :
					data[ movie ][ 'director' ].append( line )
				elif key == 'CAST' :
					data[ movie ][ 'actors' ].append( line )
	return data

def create_individuals() :
	data = read_content( DATA_FILE )
	individuals = []
	# CREATE ACTORS
	actors_info = {}
	for movie in data :
		for actor in data[ movie ][ 'actors' ] :
			if actor not in actors_info : actors_info[ actor ] = []
			actors_info[ actor ].append( movie )
	for actor in actors_info :
		individuals.append( person_individual( actor , actors_info[ actor ] ) )
	export( individuals , '../data/individuals_actors.rdf' )
	individuals = []
	# CREATE DIRECTORS
	directors_info = {}
	for movie in data :
		for director in data[ movie ][ 'director' ] :
			if director not in directors_info : directors_info[ director ] = []
			directors_info[ director ].append( movie )
	for director in directors_info :
		individuals.append( person_individual( director , directors_info[ director ] , True ) )
	export( individuals , '../data/individuals_directors.rdf' )
	individuals = []
	# CREATE ELENCO
	for movie in data :
		individuals.append( cast_individual( data[ movie ] ) )
	export( individuals , '../data/individuals_cast.rdf' )
	individuals = []
	# CREATE MOVIES
	for movie in data :
		individuals.append( movie_individual( data[ movie ] ) )
	export( individuals , '../data/individuals_movies.rdf' )
	individuals = []

def export( data , fpath = RDF_FILE ) :
	with open( fpath , 'w' ) as f :
		for ind in data :
			f.write( ind )

if __name__ == '__main__' :
	create_individuals()
