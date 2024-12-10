


mod private
{
  use crate::commands::
  {
    dogs_predict,
    dogs_estimate
  };
  use clap::Subcommand;

  #[ derive( Debug, Subcommand ) ]
  pub enum Command
  {
    #[ command ( name = "predict" ) ]
    Predict,

    #[ command ( name = "estimate" ) ]
    Estimate
    (
      dogs_estimate::Args
    )
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
      },

      Command::Estimate( args ) =>
      {
        dogs_estimate::command( args );
      }
    }
  }
}

pub use private::
{
  command,
  Command,
};