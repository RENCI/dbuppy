import logging


from renci.dbuppy.dbaccess.DBAccess import DBAccess
from renci.dbuppy.sqlscripts.SQLScript import SQLScript
from renci.dbuppy.sqlscripts.SQLScriptProvider import SQLScriptProvider


class DBUppy:

    def __init__(self, dbaccess: DBAccess, scriptprovider: SQLScriptProvider):
        self.dba = dbaccess
        self.scriptprovider = scriptprovider

    def update(self) -> None:
        """
        Executes applicable update scripts
        :return: None
        """
        logging.info(f'STARTING UPDATING DB')
        self.dba.check_connection_to_DB()

        if not self.dba.is_versioned():
            logging.info(f'DB is not versioned')
            self.dba.add_version_table()
            logging.info(f'Added version table')

        scripts_to_execute = self.get_scripts_for_update()
        logging.info(f'FOUND {len(scripts_to_execute)} SCRIPT(S) TO EXECUTE')

        for i in range(len(scripts_to_execute)):
            s = scripts_to_execute[i]
            logging.info(f'EXECUTING {i}/{len(scripts_to_execute)} {s.name}')
            try:
                self.dba.execute(s)
            except DBAccess.Exception as err:
                logging.error(err)
                self.dba.add_executed_script(s.name, True)
            else:
                self.dba.add_executed_script(s.name, False)

            logging.info(f'EXECUTING {s.name} COMPLETED')

        logging.info(f'FINISHED')

    def create(self):
        """
       Executes applicable update scripts
       :return: None
       """
        logging.info(f'STARTING CREATING DB')
        self.dba.check_connection_to_DB()
        scripts_to_execute = self.scriptprovider.get_create_scripts()
        logging.info(f'FOUND {len(scripts_to_execute)} SCRIPT(S) TO EXECUTE')

        for i in range(len(scripts_to_execute)):
            s = scripts_to_execute[i]
            logging.info(f'EXECUTING {i}/{len(scripts_to_execute)} {s.name}')
            try:
                self.dba.execute(s)
            except DBAccess.Exception as err:
                logging.error(err)

            logging.info(f'EXECUTING {s.name} COMPLETED')

        logging.info(f'FINISHED')

    def get_scripts_for_update(self) -> list[SQLScript]:
        """
        this method looks at current state of the database and selects only those scripts, that had not been executed.
        :return: lists of SQLScripts to execute
        """
        allscripts = self.scriptprovider.get_update_scripts()
        scripts_in_version = self.dba.get_executed_scripts()
        scripts_to_execute = []

        if len(scripts_in_version) == 0:
            scripts_to_execute = allscripts
        else:
            executed_scripts_ix = len(scripts_in_version) - 1
            allscripts_ix = len(allscripts) - 1

            while executed_scripts_ix >= 0 and allscripts_ix >= 0:
                if scripts_in_version[executed_scripts_ix].haderror:
                    logging.getLogger().error(f'Script {scripts_in_version[i].name } execution ended with an error. '
                                              f'Please resolve this issue before running update.')
                    break

                if allscripts[allscripts_ix].name != scripts_in_version[executed_scripts_ix].name:
                    scripts_to_execute.insert(0, allscripts[allscripts_ix])
                else:
                    break

                allscripts_ix -= 1

        return scripts_to_execute

