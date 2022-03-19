import os
import click
import sys
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Follow, Role, Permission, Post, Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

COV = None
if os.environ.get('FLASK_COVERAGE'):
        import coverage
        COV = coverage.coverage(branch=True,include='app/*')
        # The branch=True option enables branch coverage analysis
        COV.start()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)


@app.cli.command()
# The code coverage support is enabled by passing the --coverage option to the flask test command. 
@click.argument('--coverage/--no-coverage', default=False, 
                help='Run tests under code coverage')
@click.argument('test_names', nargs=-1)
def test(coverage,test_names):
    """ Run the unit tests """
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    if test_names:
        tests =unittest.TestLoader.loadTestsFromNames(test_names)
    else:
        # put path of tests package - app.tests
        tests = unittest.TestLoader().discover('app.tests')
    unittest.TextTestRunner(verbosity=2).run(tests)    
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Report: ')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir,'/tmp/coverage')
        COV.html_report(covdir)
        print(f'HTML report: file://{covdir}/index.html')
        COV.erase()
