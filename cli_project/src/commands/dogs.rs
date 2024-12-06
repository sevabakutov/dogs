


mod private
{
  use crate::commands::
  {
    dogs_predict,
  };

  use clap::Subcommand;

  #[ derive( Debug, Subcommand ) ]
  pub enum Command
  {
    #[ command ( name = "predict" ) ]
    Predict,

    // Estimate,
  }

  pub fn command
  (
    command : Command
  )
  {
    match command
    {
      Command::Predict => 
      {
        dogs_predict::command();
      }
    }
  }
}

pub use private::
{
  command,
  Command
};