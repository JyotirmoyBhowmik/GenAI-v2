"""
GenAI Platform - Command Line Interface
Provides CLI commands for platform management, testing, and operations
"""

import sys
import click
from pathlib import Path
from loguru import logger
import subprocess


@click.group()
@click.version_option(version='1.0.0', prog_name='genai-platform')
def cli():
    """GenAI Platform - Enterprise AI Orchestration System
    
    Manage, test, and operate the GenAI platform from the command line.
    """
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
    pass


@cli.command()
@click.option('--config-dir', default='./config', help='Configuration directory path')
def init(config_dir):
    """Initialize the GenAI Platform
    
    Creates directories, databases, and default configurations.
    """
    logger.info("Initializing GenAI Platform...")
    try:
        from scripts.initialize import main as init_main
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        success = init_main()
        if success:
            logger.info("✓ Platform initialized successfully")
            sys.exit(0)
        else:
            logger.error("✗ Platform initialization failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose test output')
@click.option('--coverage', is_flag=True, help='Generate coverage report')
def test(verbose, coverage):
    """Run the test suite
    
    Executes all unit and integration tests.
    """
    logger.info("Running tests...")
    try:
        cmd = ['pytest', 'tests/', '-v' if verbose else '-q']
        if coverage:
            cmd.extend(['--cov=backend', '--cov=gui', '--cov-report=html', '--cov-report=term'])
        
        result = subprocess.run(cmd, cwd=str(Path(__file__).parent.parent))
        if result.returncode == 0:
            logger.info("✓ All tests passed")
            if coverage:
                logger.info("Coverage report generated in htmlcov/")
        else:
            logger.error("✗ Some tests failed")
        sys.exit(result.returncode)
    except Exception as e:
        logger.error(f"Test execution error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--division', default='fmcg', help='Division to generate data for')
@click.option('--count', default=100, type=int, help='Number of records to generate')
def generate(division, count):
    """Generate sample data for testing
    
    Creates mock data for specified division.
    """
    logger.info(f"Generating {count} sample records for {division}...")
    try:
        from scripts.generate_sample_data import SampleDataGenerator
        gen = SampleDataGenerator()
        
        if division.lower() == 'fmcg':
            gen.generate_fmcg_data(count)
        elif division.lower() == 'manufacturing':
            gen.generate_manufacturing_data(count)
        elif division.lower() == 'hotel':
            gen.generate_hotel_data(count)
        elif division.lower() == 'stationery':
            gen.generate_stationery_data(count)
        else:
            logger.error(f"Unknown division: {division}")
            sys.exit(1)
        
        logger.info(f"✓ Generated {count} records for {division}")
    except Exception as e:
        logger.error(f"Data generation error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--host', default='0.0.0.0', help='Server host')
@click.option('--port', default=8000, type=int, help='Server port')
@click.option('--reload', is_flag=True, help='Enable auto-reload on file changes')
def server(host, port, reload):
    """Start the REST API server
    
    Runs the FastAPI server for REST API access.
    """
    logger.info(f"Starting API server on {host}:{port}...")
    try:
        import uvicorn
        uvicorn.run(
            'backend.api.main:app',
            host=host,
            port=port,
            reload=reload,
            log_level='info'
        )
    except ImportError:
        logger.error("uvicorn not installed. Run: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Server startup error: {e}")
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration
    
    Displays loaded configuration from YAML files.
    """
    logger.info("Loading configuration...")
    try:
        from backend.config_manager import get_config
        conf = get_config()
        
        divisions = conf.list_divisions()
        models = conf.list_models()
        personas = conf.list_personas()
        
        click.echo("\n📋 CONFIGURATION SUMMARY")
        click.echo("=" * 50)
        click.echo(f"\n🏢 Divisions: {len(divisions)}")
        for div in divisions:
            click.echo(f"  - {div.get('id').upper()}: {div.get('name', 'N/A')}")
        
        click.echo(f"\n🤖 Models: {len(models)}")
        for model in models[:5]:
            click.echo(f"  - {model.get('id')}: {model.get('name')} ({model.get('provider')})")
        if len(models) > 5:
            click.echo(f"  ... and {len(models) - 5} more")
        
        click.echo(f"\n👤 Personas: {len(personas)}")
        for persona in personas[:5]:
            click.echo(f"  - {persona.get('id')}: {persona.get('name')}")
        if len(personas) > 5:
            click.echo(f"  ... and {len(personas) - 5} more")
        
        click.echo("\n" + "=" * 50)
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--user-id', prompt='User ID', help='User to authenticate')
@click.option('--password', prompt=True, hide_input=True, help='User password')
def auth(user_id, password):
    """Authenticate a user
    
    Tests user authentication against the MDM system.
    """
    logger.info(f"Authenticating user: {user_id}...")
    try:
        from backend.mdm.user_manager import UserManager
        um = UserManager()
        
        user = um.authenticate(user_id, password)
        if user:
            click.echo(f"✓ Authentication successful")
            click.echo(f"  User: {user.full_name} ({user.username})")
            click.echo(f"  Division: {user.division_id}")
            click.echo(f"  Department: {user.department_id}")
            click.echo(f"  Role: {user.role_id}")
        else:
            click.echo(f"✗ Authentication failed for {user_id}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        sys.exit(1)


@cli.command()
def version():
    """Show version information"""
    click.echo("GenAI Platform v1.0.0")
    click.echo("Enterprise AI Orchestration System")
    click.echo("Copyright 2024 - All Rights Reserved")


@cli.command()
def health():
    """Check system health
    
    Verifies that all system components are accessible.
    """
    logger.info("Checking system health...")
    try:
        from backend.config_manager import get_config
        from backend.mdm.user_manager import UserManager
        from backend.models.model_router import ModelRouter
        
        checks = {
            'Configuration': False,
            'User Manager': False,
            'Model Router': False,
        }
        
        # Check configuration
        try:
            conf = get_config()
            checks['Configuration'] = True
        except:
            pass
        
        # Check user manager
        try:
            um = UserManager()
            checks['User Manager'] = True
        except:
            pass
        
        # Check model router
        try:
            mr = ModelRouter()
            checks['Model Router'] = len(mr.get_available_models()) > 0
        except:
            pass
        
        click.echo("\n🏥 SYSTEM HEALTH CHECK")
        click.echo("=" * 50)
        for component, status in checks.items():
            status_icon = "✓" if status else "✗"
            click.echo(f"{status_icon} {component}")
        click.echo("=" * 50)
        
        if all(checks.values()):
            click.echo("✓ All systems operational")
        else:
            failed = [c for c, s in checks.items() if not s]
            click.echo(f"⚠ {len(failed)} system(s) not operational: {', '.join(failed)}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Health check error: {e}")
        sys.exit(1)


def main():
    """Main entry point for CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
