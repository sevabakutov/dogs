

mod private
{
  use clap::Parser;
  use serde::Serialize;

  #[ derive( Debug, Parser, Serialize ) ]
  pub struct Args
  {
    #[ arg( long ) ]
    pub dist : String,

    #[ arg( long ) ]
    pub start_train : String,

    #[ arg( long ) ]
    pub end_train : String,

    #[ arg( long ) ]
    pub start_test : String,

    #[ arg( long ) ]
    pub end_test : String,

    #[ arg( long ) ]
    pub grade : String,
  }

  pub fn command
  (
    args : Args
  )
  {
    println!( "Estimate command!" );
  }

}

pub use private::
{
  Args,
  command,
};