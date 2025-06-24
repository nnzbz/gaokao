from src.utils.neo4j_utils import Neo4jUtils


class Dao:
    """数据访问层"""

    neo4j_utils: Neo4jUtils
    """Neo4j工具"""

    def __init__(self, neo4j_utils: Neo4jUtils):
        self.neo4j_utils = neo4j_utils

    def create_college_and_relationship(self, college_name: str, city: str, dept: str, college_level: str, project: str | None):
        """
        创建学校和关系
        :param college_name: 学校名称
        :param city: 城市
        :param dept: 主管部门
        :param college_level: 办学层次(本科、高职(专科))
        :param project: 建设工程(985/211/双一流)
        """
        college_id = self.neo4j_utils.create_node_and_relationship(college_name, "学校", city, "城市", "所在城市")[0]
        self.neo4j_utils.create_node_and_relationship(college_name, "学校", dept, "主管部门", "主管部门")
        self.neo4j_utils.create_node_and_relationship(college_name, "学校", college_level, "办学层次", "办学层次")
        if project is not None:
            self.neo4j_utils.create_node_and_relationship(college_name, "学校", project, "建设工程", "建设工程")
        return college_id

    def save_college_zszc(self, college_name: str, zszc_title: str, zszc_content: str, publish_time: str):
        """
        创建学校招生章程
        :param college_name: 学校名称
        :param zszc_title: 招生章程标题
        :param zszc_content: 招生章程内容
        :param publish_time: 发布时间
        """
        college_id, zszc_id = self.neo4j_utils.create_node_and_relationship(college_name, "学校", f'{college_name}-招生章程-{publish_time}', "招生章程", "招生章程")
        self.neo4j_utils.add_property_to_node_by_id(zszc_id, "标题", zszc_title)
        self.neo4j_utils.add_property_to_node_by_id(zszc_id, "内容", zszc_content)
        self.neo4j_utils.add_property_to_node_by_id(zszc_id, "年份", 2025)
        self.neo4j_utils.add_property_to_node_by_id(zszc_id, "发布时间", publish_time)
