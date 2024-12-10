


mod private
{
  use std::process::Command;

  pub fn command() 
  {
    let output = Command::new( "python3" )
    .arg( "/usr/src/dogs/ml_project/predict.py" )
    .output()
    .expect( "Failed to run command 'predict' " );

    if output.status.success()
    {
      println!( "Success!" )
    }
    else 
    {
      eprint!( "Error!" )
    }
  }
}

pub use private::command;