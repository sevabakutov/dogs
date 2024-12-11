

mod private
{
  use core::str;
use std::process::Command;

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
    match args
    {
      Args { dist, start_train, end_train, start_test, end_test, grade } =>
      {
        let output = Command::new( "python3" )
        .arg( "/usr/src/ml_project/ml_project/src/scripts/estimate.py" )
        .arg( dist )
        .arg( start_train )
        .arg( end_train )
        .arg( start_test )
        .arg( end_test )
        .arg( grade )
        .output()
        .expect( "Failed to start estimate command" );

        if output.status.success()
        {
          println!( "Success!" )
        }
        else 
        {
          eprintln!( "Error: {:?}", str::from_utf8( &output.stderr ) )    
        }
      }
    }
  }

}

pub use private::
{
  Args,
  command,
};