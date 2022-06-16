from neo4j import GraphDatabase, basic_auth
import socket


class Movie_queries(object):
    def __init__(self, password):
        self.driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", password), encrypted=False)
        self.session = self.driver.session()
        self.transaction = self.session.begin_transaction()

    def q0(self):
        result = self.transaction.run("""
            MATCH (n:Actor) RETURN n.name, n.id ORDER BY n.birthday ASC LIMIT 3
        """)
        return [(r[0], r[1]) for r in result]

    def q1(self):
        result = self.transaction.run("""
            MATCH (a:Actor) -[:ACTS_IN]-> () RETURN a.name, count(*) as cnt ORDER BY cnt DESC, a.name ASC LIMIT 20
        """)
        return [(r[0], r[1]) for r in result]

    def q2(self):
        result = self.transaction.run("""
            MATCH (m:Movie)<-[:RATED]- (u)
            MATCH (n:Actor) -[:ACTS_IN]-> (m)
            WITH m.title AS title, count(DISTINCT n) AS num_act
            RETURN title, num_act
            ORDER BY num_act DESC
            LIMIT 1
        """)
        return [(r[0], r[1]) for r in result]

    def q3(self):
        result = self.transaction.run("""
            MATCH (d:Director)-[:DIRECTED]->(m:Movie) WITH d, count(distinct m.genre) as cnt WHERE cnt >= 2 RETURN d.name as dn, cnt ORDER BY cnt DESC, dn ASC
        """)
        return [(r[0], r[1]) for r in result]

    def q4(self):
        result = self.transaction.run("""
            MATCH (a:Actor {name: 'Kevin Bacon'})-[:ACTS_IN*4]-(a2:Actor) WHERE a <> a2 AND NOT (a)-[:ACTS_IN]->()<-[:ACTS_IN]-(a2) RETURN DISTINCT a2.name ORDER BY a2.name ASC
        """)
        return [(r[0]) for r in result]

if __name__ == "__main__":
    sol = Movie_queries("neo4jpass")
    print("---------- Q0 ----------")
    print(sol.q0())
    print("---------- Q1 ----------")
    print(sol.q1())
    print("---------- Q2 ----------")
    print(sol.q2())
    print("---------- Q3 ----------")
    print(sol.q3())
    print("---------- Q4 ----------")
    print(sol.q4())
    sol.transaction.close()
    sol.session.close()
    sol.driver.close()
