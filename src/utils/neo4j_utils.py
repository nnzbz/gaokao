import os
from logging import info, warning, debug
from typing import LiteralString

from neo4j import GraphDatabase, Driver


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
        # self.create_node_and_relationship("张三", "Person", "李四", "Person", "KNOWS")

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
        ids = self.driver.execute_query(f"""
            MERGE (n1:{label1} {{name: $name1}})
            MERGE (n2:{label2} {{name: $name2}})
            MERGE (n1)-[r:{relationship}]->(n2)
            RETURN elementId(n1) as id1, elementId(n2) as id2 
            """, {"name1": name1, "label1": label1, "name2": name2, "label2": label2}).records[0]
        id1 = ids.data()["id1"]
        id2 = ids.data()["id2"]
        return id1, id2

    def add_property_to_node_by_id(self, node_id: str, property_name: LiteralString, property_value):
        """
        为指定 ID 的节点添加属性
        :param node_id: 节点 ID
        :param property_name: 属性名
        :param property_value: 属性值
        """
        records = self.driver.execute_query(f"""
            MATCH (n)
            WHERE elementId(n) = $node_id
            SET n.{property_name} = $value
            RETURN count(n) as updated_count
            """, node_id=node_id, value=property_value).records

        if len(records) == 1:
            debug(f"已为节点 ID {node_id} 添加了属性 {property_name}")
        else:
            warning(f"未找到节点 ID {node_id}")
