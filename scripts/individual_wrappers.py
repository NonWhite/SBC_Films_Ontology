TO_REPLACE = [ "\"" , "'" , ":" , "." , "," , "/" , '-' , '!' , '*' , '&' ]

def camelize( st ) :
	for t in TO_REPLACE : st = st.replace( t , '' )
	st = '_'.join( st.split() )
	return st

def person_individual( actor , movies , is_director = False ) :
	individual = ''
	sp = actor.split()
	first_name = sp[ 0 ]
	family_name = ' '.join( sp[ 1: ] )
	individual += '<owl:NamedIndividual rdf:about="&untitled-ontology-4;%s">\n' % camelize( actor )
	individual += '\t<rdf:type rdf:resource="&renata;FOAF-modifiedAgent"/>\n'
	individual += '\t<rdf:type rdf:resource="&renata;FOAF-modifiedPerson"/>\n'
	if is_director :
		individual += '\t<rdf:type rdf:resource="&untitled-ontology-4;Diretor"/>\n'
	else :
		individual += '\t<rdf:type rdf:resource="&untitled-ontology-4;Ator"/>\n'
	individual += '\t<rdf:type rdf:resource="http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing"/>\n'
	individual += '\t<renata:FOAF-modifiedfirstName xml:lang="en">%s</renata:FOAF-modifiedfirstName>\n' % first_name
	individual += '\t<renata:FOAF-modifiedfamilyName xml:lang="en">%s</renata:FOAF-modifiedfamilyName>\n' % family_name
	if is_director :
		for m in movies :
			individual += '\t<renata:FOAF-modifiedmade rdf:resource="&untitled-ontology-4;%s"/>\n' % camelize( m )
	else :
		for m in movies :
			individual += '\t<untitled-ontology-4:e_membro rdf:resource="&untitled-ontology-4;Elenco_%s"/>\n' % camelize( m )
			continue
	individual += '</owl:NamedIndividual>\n'
	#print individual
	return individual

def cast_individual( movie ) :
	individual = ''
	movie_name = camelize( movie[ 'name' ] )
	individual += '<owl:NamedIndividual rdf:about="&untitled-ontology-4;Elenco_%s">\n' % movie_name
	individual += '\t<rdf:type rdf:resource="&renata;FOAF-modifiedAgent"/>\n'
	individual += '\t<rdf:type rdf:resource="&renata;FOAF-modifiedGroup"/>\n'
	individual += '\t<rdf:type rdf:resource="&untitled-ontology-4;Elenco"/>\n'
	individual += '\t<untitled-ontology-4:estrelado rdf:resource="&untitled-ontology-4;%s"/>\n' % movie_name
	for actor in movie[ 'actors' ] :
		individual += '\t<renata:FOAF-modifiedmember rdf:resource="&untitled-ontology-4;%s"/>\n' % camelize( actor )
	individual += '</owl:NamedIndividual>\n'
	#print individual
	return individual

def movie_individual( movie ) :
	individual = ''
	movie_name = camelize( movie[ 'name' ] )
	individual = '<owl:NamedIndividual rdf:about="&untitled-ontology-4;%s">\n' % movie_name
	individual += '\t<rdf:type rdf:resource="&renata;FOAF-modifiedProject"/>\n'
	individual += '\t<rdf:type rdf:resource="&untitled-ontology-4;Filme"/>\n'
	individual += '\t<untitled-ontology-4:ano_lancamento rdf:datatype="&xsd;integer">%d</untitled-ontology-4:ano_lancamento>\n' % movie[ 'year' ]
	individual += '\t<untitled-ontology-4:nome_filme xml:lang="en">%s</untitled-ontology-4:nome_filme>\n' % movie[ 'name' ]
	for d in movie[ 'director' ] :
		individual += '\t<renata:FOAF-modifiedmaker rdf:resource="&untitled-ontology-4;%s"/>\n' % camelize( d )
	individual += '\t<untitled-ontology-4:estrela rdf:resource="&untitled-ontology-4;Elenco_%s"/>\n' % movie_name
	individual += '</owl:NamedIndividual>\n'
	return individual
