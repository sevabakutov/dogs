///!
///! Commands
///!
///

pub mod dogs;
mod dogs_predict;

mod private
{
  use crate::commands::dogs;
  use clap::
  {
    Parser,
    Subcommand
  };

  #[ derive( Debug, Parser ) ]
  pub struct Cli
  {
    #[ command ( subcommand ) ]
    pub command: CliCommand,
  } 

  #[ derive( Debug, Subcommand ) ]
  pub enum CliCommand
  {
    #[ command( subcommand, name = "dogs" ) ]
    Dogs( dogs::Command )
  }
}

pub use private::
{
  Cli,
  CliCommand
};