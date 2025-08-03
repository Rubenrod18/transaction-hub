import collections

from sqlalchemy.orm import Session

from app.cli.base_cli import BaseCli
from tests.common import seeds


class SeederCli(BaseCli):
    def __init__(self, session: Session):
        self.session = session

    def run_command(self, *args, **kwargs):
        try:
            seeders = seeds.get_seeders()

            if not seeders:
                raise LookupError('No seeders found')

            ordered_seeders = collections.OrderedDict(sorted(seeders.items()))
            for seeder in ordered_seeders.values():
                seeder.seed()
            self.session.commit()

            print(' Database seeding completed successfully.')  # noqa
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
