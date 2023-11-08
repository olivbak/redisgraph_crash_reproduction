import random
import redis

from redisgraph import Graph
from concurrent.futures import ThreadPoolExecutor

query1 = lambda actor_id, movie_id: f"""
CYPHER actor_id={actor_id} movie_id={movie_id}
""" + """
MERGE (actor:Actor {id: $actor_id})
WITH actor
OPTIONAL MATCH (actor)-[acts:STARS_IN]->(old_movie:Movie)
DELETE acts
MERGE (movie:Movie {id: $movie_id})
MERGE (actor)-[:STARS_IN]->(movie)

RETURN actor
"""

query2 = lambda actor_id, movie_id: f"""
CYPHER actor_id={actor_id}
""" + """
MATCH (actor:Actor {id: $actor_id})
DELETE actor
"""

# Second tuple element determine whether to run
# the query in a `MULTI` - `EXEC` transaction or not.
# CASES:
# 1. IF query1 and query2 are both transactions, THEN: no crash
# 2. IF query1 and query2 are both non-transactions, THEN: no crash
# 3. IF query1 and query2 are different (one transaction, one none), THEN crash!
queries = [
    (query1, True),
    (query2, False)
]

r  = redis.Redis(host='crash-redis', port=6379)

def execute_random_queries(limit):
    for _ in range(1, limit):
        actor_id = 1
        query_transaction = random.choice(queries)
        query, transaction = query_transaction[0], query_transaction[1]
        movie_id = random.choice([1, 2])
        query_with_values = query(actor_id, movie_id)

        if transaction:
            pipe = r.pipeline()
            pipe.multi()
            pipe.execute_command("GRAPH.QUERY", 'key', query_with_values)
            pipe.execute()
        else:
            r.execute_command("GRAPH.QUERY", 'key', query_with_values)

limit = 100000000

with ThreadPoolExecutor() as threads:
    threads.map(execute_random_queries, [limit, limit])
