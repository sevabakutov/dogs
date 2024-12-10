


mod private
{
  use core::str;
  use std::process::Command;

  pub fn command() 
  {
    let output = Command::new( "python3" )
    .arg( "/usr/src/ml_project/ml_project/src/scripts/predict.py" )
    .output()
    .expect( "Failed to run command 'predict' " );

    if output.status.success()
    {
      println!( "Success!" )
    }
    else 
    {
      eprint!( "Error!: {:?}", str::from_utf8( &output.stderr ) )
    }
  }
}

pub use private::command;