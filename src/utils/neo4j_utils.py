import os
from logging import info
from typing import LiteralString, cast

from neo4j import GraphDatabase, Driver, Query


class Neo4jUtils:
    """
    Neo4j工具
    """
    driver: Driver
    """数据库驱动器"""

    def __init__(self):
        uri = os.getenv("NEO4J_URI") or "bolt://localhost:7687"
        """Neo4j数据库连接地址"""
        neo4j_user = os.getenv("NEO4J_USER") or "neo4j"
        """Neo4j用户名称"""
        neo4j_pswd = os.getenv("NEO4J_PSWD") or "neo4j12345"
        """Neo4j用户密码"""

        self.driver = GraphDatabase.driver(uri, auth=(neo4j_user, neo4j_pswd))
        self.verify_connection()
        pass

    def verify_connection(self):
        """验证连接"""
        info("验证Neo4j数据库连接...")
        records = self.driver.execute_query("MATCH (n) RETURN COUNT(n) AS count").records
        info(f"数据库中实体数量: {records[0].data()['count']}")
        self.create_node_and_relationship("张三", "Person", "李四", "Person", "KNOWS")
        pass

    def close(self):
        """关闭连接"""
        self.driver.close()
        pass

    def create_node_and_relationship(self, name1: str, label1: LiteralString, name2: str, label2: LiteralString, relationship: LiteralString):
        """
        创建两个节点并建立关系
        :param name1: 节点1的名称
        :param label1: 节点1的标签
        :param name2: 节点2的名称
        :param label2: 节点2的标签
        :param relationship: 关系
        """
        self.driver.execute_query(f"""
            MERGE (n1:{label1} {{name: $name1}})
            MERGE (n2:{label2} {{name: $name2}})
            MERGE (n1)-[r:{relationship}]->(n2)
        """, {"name1": name1, "label1": label1, "name2": name2, "label2": label2})
