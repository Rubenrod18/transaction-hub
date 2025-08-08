from cli import app as typer_app
from tests.common.base_tests.test_base_integration import TestCliBaseIntegration


# pylint: disable=attribute-defined-outside-init
class TestCli(TestCliBaseIntegration):
    def test_is_cli_seeder_ok_execute_all_seeders_process_executed_successfully(self):
        result = self.runner.invoke(typer_app, args=['seed'])

        stdout_str = result.stdout_bytes.decode('utf-8')
        finished_message = 'Database seeding completed successfully'
        is_finished_process = stdout_str.find(finished_message) != -1

        assert result.exit_code == 0, result.exception
        assert is_finished_process
