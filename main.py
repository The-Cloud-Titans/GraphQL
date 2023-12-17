import graphene
from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, ObjectType
from ariadne.constants import PLAYGROUND_HTML
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# User model
class User:
    def __init__(self, first_name, last_name, email, major, minor, graduation_date, divisionCode, personType):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.major = major
        self.minor = minor
        self.graduation_date = graduation_date
        self.divisionCode = divisionCode
        self.personType = personType

class UserType(graphene.ObjectType):
    first_name = graphene.String()  # Make sure this matches 'first_name' in the User class
    last_name = graphene.String()   # Matches 'last_name'
    email = graphene.String()
    major = graphene.String()
    minor = graphene.String()
    graduation_date = graphene.String()  # Matches 'graduation_date'
    divisionCode = graphene.String()
    personType = graphene.String()


# Sample data
users = [
    User("John", "Doe", "john.doe@example.com", "Computer Science", "Math", "2023-05-20", "CS", "Student"),
    User("Jane", "Smith", "jane.smith@example.com", "Biology", "Chemistry", "2024-06-15", "BIO", "Student"),
    User("Emily", "Johnson", "emily.johnson@example.com", "English Literature", "History", "2022-12-10", "ENG", "Alumni"),
    User("Michael", "Brown", "michael.brown@example.com", "Mechanical Engineering", "Physics", "2025-05-30", "ENG", "Student"),
    User("Ahmed", "Khan", "ahmed.khan@example.com", "Business Administration", "Economics", "2023-11-20", "BUS", "Student"),
    User("Linda", "Garcia", "linda.garcia@example.com", "Psychology", "Sociology", "2024-08-25", "PSY", "Student"),
    User("Daniel", "Martinez", "daniel.martinez@example.com", "Computer Engineering", "Mathematics", "2022-09-15", "ENG", "Alumni"),
    User("Sarah", "Lee", "sarah.lee@example.com", "Fine Arts", "Art History", "2025-04-10", "ART", "Student"),
    User("Carlos", "Rodriguez", "carlos.rodriguez@example.com", "Political Science", "Public Policy", "2023-02-20", "POL", "Student"),
    User("Lisa", "Wong", "lisa.wong@example.com", "Environmental Science", "Biology", "2026-06-18", "ENV", "Student")
]


# Type definitions
type_defs = """
    type Query {
        users: [User!]!
    }

    type User {
        firstName: String
        lastName: String
        email: String
        major: String
        minor: String
        graduationDate: String
        divisionCode: String
        personType: String
    }
"""

# Resolvers
query = ObjectType("Query")

@query.field("users")
def resolve_users(*_):
    return [
        {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "major": user.major,
            "minor": user.minor,
            "graduationDate": user.graduation_date,
            "divisionCode": user.divisionCode,
            "personType": user.personType,
        }
        for user in users
    ]


# Create executable schema
schema = make_executable_schema(type_defs, query)

# Flask app setup
app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GraphQL Playground</title>
        <link href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" rel="stylesheet" />
        <script src="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>window.addEventListener('load', function (event) {
            GraphQLPlayground.init(document.getElementById('root'), { endpoint: '/graphql' })
        })</script>
    </body>
    </html>
    """

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    try:
        # Process the GraphQL query
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        # Determine HTTP status code based on GraphQL query success
        status_code = 200 if success else 400
        return jsonify(result), status_code
    except Exception as e:
        # Log the exception details
        logging.exception("An error occurred during a GraphQL request.")
        # Return a generic error response
        return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == "__main__":
    app.run(port=8000,debug=True)
