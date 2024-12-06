use std::error::Error;
use clap::Parser;

use dogs::commands::
{
  self,
  Cli,
  CliCommand
};

fn main() -> Result< (), Box< dyn Error > > 
{
  let cli = Cli::parse();

  match cli.command 
  {
    CliCommand::Dogs( cmd ) =>
    {
      commands::dogs::command( cmd );
    }
  }
  
  Ok( () )
}
