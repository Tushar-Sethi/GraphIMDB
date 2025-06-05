from graphiti import GraphSchema, NodeType, EdgeType, StringField, FloatField, IntField, TextField

schema = GraphSchema()

Movie = NodeType(
    name="Movie",
    fields={
        "tconst": StringField(unique=True),
        "title": StringField(),
        "year": IntField(),
        "average_rating": FloatField(),
        # Optional: store plot directly
        "plot_summary": TextField(nullable=True),
    },
)
Person = NodeType(
    name="Person",
    fields={
        "nconst": StringField(unique=True),
        "name": StringField(),
        "birth_year": IntField(nullable=True),
    },
)
Genre = NodeType(
    name="Genre",
    fields={"name": StringField(unique=True)},
)
Review = NodeType(
    name="Review",
    fields={"review_id": StringField(unique=True), "text": TextField()},
)

# Edge definitions
ActedIn = EdgeType("ACTED_IN", from_node=Person, to_node=Movie)
Directed = EdgeType("DIRECTED", from_node=Person, to_node=Movie)
HasGenre = EdgeType("HAS_GENRE", from_node=Movie, to_node=Genre)
HasReview = EdgeType("HAS_REVIEW", from_node=Movie, to_node=Review)
MentionsPerson = EdgeType("MENTIONS_PERSON_IN_REVIEW", from_node=Person, to_node=Review)

# Register nodes and edges
for node in [Movie, Person, Genre, Review]:
    schema.add_node_type(node)
for edge in [ActedIn, Directed, HasGenre, HasReview, MentionsPerson]:
    schema.add_edge_type(edge)