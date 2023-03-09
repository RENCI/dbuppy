# import unittest
#
# from renci.dbuppy.sqlscripts.SQLScript import SQLScript, SQLScriptReader
#
#
# class SQLScriptReaderTests(unittest.TestCase):
#     content = """
#             create table if not exists "Administrator"
#             (
#                 "userId"     varchar,
#                 "adminName"  varchar,
#                 "adminEmail" varchar
#             );
#
#             alter table "Administrator"
#                 owner to postgres;
#
#             insert into "Administrator" (userId, adminName, adminEmail)
#             values (1,"admin", "test@admin.admin");
#             """
#     def test_set_statements(self):
#
#         s = SQLScript("test", None, None, self.content)
#         SQLScriptReader.set_statements(s)
#
#         self.assertEqual(3, len(s.statements))
